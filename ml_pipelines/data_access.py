"""Bridge between the raw-SQL SQLite store and DataFrames.

Rows are stored as JSON text in ``dataset_rows.payload``. Instead of dragging an
ORM into the analytics layer, this module builds a parameterized *raw SQL*
projection with SQLite's ``json_extract`` and hands it straight to
``pandas.read_sql_query`` (default) or ``polars.read_database``. No intermediate
Python list of dictionaries is built, so large queries stay cheap.

Example
-------
>>> frame = load_dataset(1, backend="pandas")           # doctest: +SKIP
>>> frame = load_dataset(1, backend="polars")           # doctest: +SKIP
>>> rows = read_sql("SELECT count(*) AS n FROM dataset_rows", backend="pandas")
"""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

from ._optional import require
from .paths import database_path

PREDICTION_KEY = "__ml_prediction__"
RESERVED_PREFIX = "__"

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def connect(*, db_path: str | Path | None = None, read_only: bool = True) -> sqlite3.Connection:
    """Open a SQLite connection with a generous lock timeout (WAL friendly)."""
    path = Path(db_path) if db_path is not None else database_path()
    if read_only and path.exists():
        conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, timeout=30)
    else:
        conn = sqlite3.connect(str(path), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def quote_ident(name: str) -> str:
    """Quote a SQL identifier, rejecting embedded NUL bytes."""
    if "\x00" in name:
        raise ValueError("Invalid column name.")
    return '"' + str(name).replace('"', '""') + '"'


def json_path(name: str) -> str:
    """Build a SQLite JSON path that tolerates spaces / quotes in column names."""
    escaped = str(name).replace("\\", "\\\\").replace('"', '\\"')
    return '$."' + escaped + '"'


def dataset_meta(dataset_id: int, *, db_path: str | Path | None = None) -> dict[str, Any]:
    """Read a dataset's schema with a single raw SQL statement."""
    with connect(db_path=db_path) as conn:
        row = conn.execute(
            "SELECT id, owner_id, name, columns_json, numeric_columns_json, "
            "categorical_columns_json, row_count FROM datasets WHERE id = ?",
            (int(dataset_id),),
        ).fetchone()
    if row is None:
        raise LookupError(f"Dataset #{dataset_id} was not found.")
    return {
        "id": int(row["id"]),
        "owner_id": int(row["owner_id"]),
        "name": str(row["name"]),
        "columns": _decode(row["columns_json"]),
        "numeric": _decode(row["numeric_columns_json"]),
        "categorical": _decode(row["categorical_columns_json"]),
        "row_count": int(row["row_count"]),
    }


def _decode(raw: str | None) -> list[str]:
    try:
        value = json.loads(raw or "[]")
        return [str(v) for v in value] if isinstance(value, list) else []
    except (ValueError, TypeError):
        return []


def visible_columns(meta: dict[str, Any], columns: Sequence[str] | None = None) -> list[str]:
    """Resolve requested columns, never exposing internal reserved keys."""
    available = [c for c in meta["columns"] if not c.startswith(RESERVED_PREFIX)]
    if not columns:
        return available
    allowed = set(available)
    return [c for c in columns if c in allowed]


def build_dataset_query(
    dataset_id: int,
    columns: Sequence[str],
    *,
    limit: int | None = None,
) -> tuple[str, list[Any]]:
    """Return (sql, params) projecting JSON payloads into real typed columns."""
    if not columns:
        raise ValueError("At least one column is required.")
    projections = ", ".join(
        f"json_extract(payload, ?) AS {quote_ident(column)}" for column in columns
    )
    sql = (
        f"SELECT {quote_ident('dataset_id')} AS dataset_id, "
        f"row_index, {projections} "
        "FROM dataset_rows WHERE dataset_id = ? ORDER BY row_index"
    )
    params: list[Any] = [json_path(column) for column in columns]
    params.append(int(dataset_id))
    if limit is not None and limit > 0:
        sql += " LIMIT ?"
        params.append(int(limit))
    return sql, params


def read_sql(
    sql: str,
    params: Sequence[Any] | Iterable[Any] = (),
    *,
    backend: str = "pandas",
    db_path: str | Path | None = None,
    connection: Any | None = None,
):
    """Execute raw SQL and return a pandas or polars DataFrame.

    ``params`` is always bound (never string-formatted) to prevent SQL injection
    in the dynamic JSON paths built above.
    """
    bound = list(params)
    own_connection = connection is None
    conn = connection if connection is not None else connect(db_path=db_path)
    try:
        if backend == "pandas":
            pd = require("pandas")
            return pd.read_sql_query(sql, conn, params=bound)
        if backend == "polars":
            pl = require("polars")
            try:
                return pl.read_database(
                    query=sql,
                    connection=conn,
                    execute_options={"parameters": tuple(bound)},
                )
            except Exception:
                # Some polars builds need connectorx/ADBC for DBAPI cursors.
                # Falling back through pandas keeps the public API identical.
                pd = require("pandas")
                return pl.from_pandas(pd.read_sql_query(sql, conn, params=bound))
        raise ValueError(f"Unknown DataFrame backend: {backend!r}")
    finally:
        if own_connection:
            conn.close()


def load_dataset(
    dataset_id: int,
    *,
    columns: Sequence[str] | None = None,
    limit: int | None = None,
    backend: str = "pandas",
    db_path: str | Path | None = None,
    connection: Any | None = None,
):
    """Load one dataset as a real DataFrame using the raw-SQL JSON projection."""
    meta = dataset_meta(dataset_id, db_path=db_path)
    chosen = visible_columns(meta, columns)
    sql, params = build_dataset_query(dataset_id, chosen, limit=limit)
    frame = read_sql(
        sql, params, backend=backend, db_path=db_path, connection=connection
    )
    # dataset_id / row_index are query bookkeeping, never analytical features.
    internal = [c for c in ("dataset_id", "row_index") if c in frame.columns]
    if backend == "pandas":
        frame = frame.drop(columns=internal)
    else:
        frame = frame.drop(internal)
    targets = [c for c in chosen if c in set(meta["numeric"])]
    if backend == "pandas":
        pd = require("pandas")
        for column in targets:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        return frame
    return coerce_polars(frame, targets)


def coerce_polars(frame, numeric: Sequence[str]):
    """Return a polars frame with numeric columns cast to Float64."""
    pl = require("polars")
    selected = [c for c in numeric if c in frame.columns]
    if not selected:
        return frame
    return frame.with_columns(
        [pl.col(c).cast(pl.Float64, strict=False).alias(c) for c in selected]
    )


def table_names(*, db_path: str | Path | None = None) -> list[str]:
    with connect(db_path=db_path) as conn:
        return [
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            )
        ]


def iter_dataset_batches(
    dataset_id: int,
    *,
    batch_size: int = 2000,
    columns: Sequence[str] | None = None,
    db_path: str | Path | None = None,
):
    """Yield pandas DataFrame batches so training never loads a huge table at once."""
    meta = dataset_meta(dataset_id, db_path=db_path)
    chosen = visible_columns(meta, columns)
    offset = 0
    while True:
        sql, params = build_dataset_query(dataset_id, chosen, limit=None)
        sql += " LIMIT ? OFFSET ?"
        params.extend([int(batch_size), int(offset)])
        frame = read_sql(sql, params, backend="pandas", db_path=db_path)
        if frame.empty:
            break
        yield frame.drop(columns=["dataset_id", "row_index"], errors="ignore")
        if len(frame) < batch_size:
            break
        offset += batch_size
