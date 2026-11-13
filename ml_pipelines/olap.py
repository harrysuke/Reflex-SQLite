"""Vectorized OLAP over SQLite via DuckDB's native SQLite scanner.

Nothing is copied or migrated: DuckDB ``ATTACH``-es the existing
``data/app.db`` file as a catalog and reads ``dataset_rows`` directly. A lazy
``rows_flat`` view exposes the JSON payload as typed columns so analysts can
write ordinary SQL aggregations instead of parsing JSON in Python.

If the DuckDB ``sqlite`` extension cannot be installed (offline machine), the
caller can fall back to :func:`pandas_aggregate`, which reproduces the default
aggregation using ``pandas.read_sql_query``.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Sequence

from ._optional import MissingDependency, require
from .data_access import dataset_meta, json_path, quote_ident
from .paths import database_path
from .preprocessing import clean_frame, frame_to_records, json_safe

ATTACH_ALIAS = "appdb"
FLAT_VIEW = "rows_flat"
_READ_ONLY_PREFIXES = ("select", "with", "show", "describe", "explain", "pragma")


def _escape_literal(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def attach_sqlite(*, db_path: str | Path | None = None, dataset_id: int | None = None):
    """Return (duckdb connection, attached_alias, view_name).

    Raises :class:`MissingDependency` with an actionable hint if the extension
    is unavailable, so the caller can degrade gracefully.
    """
    duckdb = require("duckdb")
    path = Path(db_path) if db_path is not None else database_path()
    con = duckdb.connect(config={"threads": 4})
    try:
        try:
            con.execute("LOAD sqlite;")
        except Exception:
            try:
                con.execute("INSTALL sqlite;")
                con.execute("LOAD sqlite;")
            except Exception as exc:
                raise MissingDependency(
                    "DuckDB sqlite extension (offline install unavailable)",
                    "pip install duckdb  # then run once online: INSTALL sqlite; LOAD sqlite;",
                ) from exc
        con.execute(
            f"ATTACH '{_escape_literal(path)}' AS {ATTACH_ALIAS} (TYPE sqlite, READ_ONLY);"
        )
        if dataset_id is not None:
            create_flat_view(con, dataset_id)
        return con
    except Exception:
        con.close()
        raise


def create_flat_view(con, dataset_id: int) -> str:
    """Create a lazy typed view over the attached SQLite ``dataset_rows`` table."""
    meta = dataset_meta(dataset_id)
    columns = [c for c in meta["columns"] if not c.startswith("__")]
    numeric = set(meta["numeric"])
    if not columns:
        raise ValueError("This dataset has no columns to expose.")
    expressions = []
    for column in columns:
        path = json_path(column).replace("'", "''")
        extract = f"json_extract_string(payload, '{path}')"
        if column in numeric:
            expressions.append(
                f"TRY_CAST({extract} AS DOUBLE) AS {quote_ident(column)}"
            )
        else:
            expressions.append(f"{extract} AS {quote_ident(column)}")
    sql = (
        f"CREATE OR REPLACE TEMP VIEW {FLAT_VIEW} AS "
        f"SELECT id, dataset_id, row_index, {', '.join(expressions)} "
        f"FROM {ATTACH_ALIAS}.dataset_rows WHERE dataset_id = {int(dataset_id)}"
    )
    con.execute(sql)
    return FLAT_VIEW


def validate_read_only(sql: str) -> str:
    """Reject mutations and multi-statement batches before they reach DuckDB."""
    stripped = sql.strip().rstrip(";").strip()
    if not stripped:
        raise ValueError("Enter a SQL query first.")
    if ";" in stripped:
        raise ValueError("Only a single read-only statement is allowed.")
    if not stripped.lstrip("(").lower().startswith(_READ_ONLY_PREFIXES):
        raise ValueError("Only SELECT / WITH / SHOW / DESCRIBE / EXPLAIN queries are allowed.")
    forbidden = ("attach ", "detach ", "copy ", "install ", "load ", "create ", "drop ", "delete ", "update ", "insert ")
    lowered = " " + stripped.lower() + " "
    if any(f" {token.strip()} " in lowered for token in forbidden):
        raise ValueError("Mutating statements are not allowed in the OLAP console.")
    return stripped


def run_query(
    sql: str,
    *,
    db_path: str | Path | None = None,
    dataset_id: int | None = None,
    chart_x_column: str = "",
    chart_y_column: str = "",
) -> dict[str, Any]:
    """Execute a read-only OLAP query and return UI-ready columns/rows/chart."""
    query = validate_read_only(sql)
    started = time.perf_counter()
    con = attach_sqlite(db_path=db_path, dataset_id=dataset_id)
    try:
        cursor = con.execute(query)
        raw_columns = [str(c[0]) for c in cursor.description]
        rows = [dict(zip(raw_columns, row)) for row in cursor.fetchall()]
    finally:
        con.close()
    elapsed = int((time.perf_counter() - started) * 1000)

    safe_rows = [{k: json_safe(v) for k, v in row.items()} for row in rows[:200]]
    x = chart_x_column if chart_x_column in raw_columns else (raw_columns[0] if raw_columns else "")
    y = chart_y_column if chart_y_column in raw_columns else ""
    if not y:
        y = next((c for c in raw_columns if c != x and isinstance(safe_rows[0].get(c), (int, float))), "") if safe_rows else ""
    chart = []
    if x and y:
        for row in safe_rows[:24]:
            value = row.get(y)
            if isinstance(value, (int, float)):
                chart.append({"name": str(row.get(x))[:22], "value": value})
    return {
        "columns": raw_columns,
        "rows": safe_rows,
        "row_count": len(rows),
        "chart": chart,
        "chart_label": y,
        "elapsed_ms": elapsed,
        "engine": "DuckDB · SQLite scanner (ATTACH)",
        "notes": [
            "DuckDB ATTACH reads data/app.db in place — no copy, no migration.",
            f"rows_flat is a lazy view over json_extract_string(payload, ...).",
            f"Completed in {elapsed} ms.",
        ],
    }


def pandas_aggregate(frame, group_by: str, value: str, agg: str = "mean", limit: int = 12) -> dict[str, Any]:
    """Pandas fallback used when the DuckDB sqlite extension is unavailable."""
    pd = require("pandas")
    started = time.perf_counter()
    working = clean_frame(frame)
    if group_by not in working.columns or value not in working.columns:
        raise ValueError("Group and value columns must exist in the dataset.")
    working[value] = pd.to_numeric(working[value], errors="coerce")
    allowed = {"mean", "sum", "count", "max", "min", "median"}
    operation = agg if agg in allowed else "mean"
    grouped = (
        working.groupby(group_by, dropna=False)[value]
        .agg(operation)
        .reset_index()
        .sort_values(value, ascending=False)
        .head(limit)
    )
    grouped.columns = [group_by, operation]
    rows = frame_to_records(grouped, list(grouped.columns), limit)
    chart = [
        {"name": str(r[group_by])[:22], "value": float(r[operation] or 0)}
        for r in rows
    ]
    elapsed = int((time.perf_counter() - started) * 1000)
    return {
        "columns": list(grouped.columns),
        "rows": rows,
        "row_count": len(rows),
        "chart": chart,
        "chart_label": operation,
        "elapsed_ms": elapsed,
        "engine": "pandas fallback (DuckDB sqlite extension unavailable)",
        "notes": [
            "DuckDB's sqlite extension was unavailable; the same aggregation ran through pandas.read_sql_query data.",
            "Install duckdb and run `INSTALL sqlite; LOAD sqlite;` once to enable columnar vectorized OLAP.",
        ],
    }
