"""Out-of-core processing of large uploads with ``polars.scan_csv``.

LazyFrames never materialize the whole file: row counts, null audits, filters,
group-bys and aggregations are pushed into Polars' streaming engine. A
``sink_ndjson`` -> batched SQLite ``INSERT`` path is provided for genuinely
larger-than-RAM files that must land in the database.
"""
from __future__ import annotations

import json
import sqlite3
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from ._optional import require
from .paths import database_path, uploads_dir
from .preprocessing import json_safe

LAZY_EXTENSIONS = {".csv", ".tsv", ".txt"}
EXCEL_EXTENSIONS = {".xlsx", ".xls"}
MAX_PREVIEW_ROWS = 16


def list_uploads(folder: str | Path | None = None) -> list[dict[str, Any]]:
    """List files dropped directly into uploads/ (oldest first)."""
    path = Path(folder) if folder is not None else uploads_dir()
    if not path.exists():
        return []
    files = []
    for item in sorted(path.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not item.is_file():
            continue
        stat = item.stat()
        files.append({
            "name": item.name,
            "path": str(item),
            "suffix": item.suffix.lower(),
            "size_kb": round(stat.st_size / 1024, 1),
            "modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M"),
            "lazy": item.suffix.lower() in LAZY_EXTENSIONS,
        })
    return files


def detect_separator(path: str | Path) -> str:
    """Sniff the delimiter from the first non-empty line."""
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as handle:
        head = handle.readline()
    counts = {candidate: head.count(candidate) for candidate in (",", "\t", ";", "|")}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def scan_upload(path: str | Path, *, separator: str | None = None, has_header: bool = True):
    """Return a lazy Polars frame pointing at the file (no data loaded yet)."""
    pl = require("polars")
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Upload not found: {source.name}")
    if source.suffix.lower() == ".tsv":
        separator = "\t"
    return pl.scan_csv(
        source,
        separator=separator or detect_separator(source),
        has_header=has_header,
        infer_schema_length=200,
        ignore_errors=True,
        truncate_ragged_lines=True,
    )


def _schema(lazy) -> dict[str, str]:
    try:
        return {str(k): str(v) for k, v in lazy.collect_schema().items()}
    except AttributeError:  # polars < 1.x
        return {str(k): str(v) for k, v in lazy.schema.items()}


def profile_lazy(
    path: str | Path,
    *,
    separator: str | None = None,
    group_by: str = "",
    value_column: str = "",
    aggregation: str = "mean",
    filter_expression: str = "",
    limit: int = 12,
) -> dict[str, Any]:
    """Stream a large file and compute counts / null audit / grouped aggregation."""
    pl = require("polars")
    started = time.perf_counter()
    lazy = scan_upload(path, separator=separator)
    schema = _schema(lazy)
    columns = list(schema.keys())
    if not columns:
        raise ValueError("The file has no readable columns.")

    if filter_expression.strip():
        try:
            lazy = lazy.filter(pl.sql_expr(filter_expression.strip()))
        except Exception as exc:
            raise ValueError(f"Invalid filter expression: {exc}") from exc

    numeric = [
        c for c in columns
        if any(token in schema[c].lower() for token in ("int", "float", "decimal"))
    ]
    numeric = numeric[:8] or columns[:8]

    count = int(lazy.select(pl.len()).collect(engine="streaming").item())
    null_counts = lazy.select([pl.col(c).null_count().alias(c) for c in columns]).collect(
        engine="streaming"
    )
    missing = {c: int(null_counts[c][0]) for c in columns}

    summary_columns = ["Column", "Dtype", "Missing", "Mean", "Std", "Min", "Max"]
    expressions: list[Any] = []
    for column in numeric:
        cast = pl.col(column).cast(pl.Float64, strict=False)
        expressions.extend([
            cast.mean().alias(f"{column}__mean"),
            cast.std().alias(f"{column}__std"),
            cast.min().alias(f"{column}__min"),
            cast.max().alias(f"{column}__max"),
        ])
    stats_frame = lazy.select(expressions).collect(engine="streaming") if expressions else None
    summary_rows = []
    for column in numeric:
        def value(suffix: str) -> float | None:
            if stats_frame is None or f"{column}__{suffix}" not in stats_frame.columns:
                return None
            return json_safe(stats_frame[f"{column}__{suffix}"][0])
        summary_rows.append({
            "Column": column,
            "Dtype": schema[column],
            "Missing": missing.get(column, 0),
            "Mean": value("mean"),
            "Std": value("std"),
            "Min": value("min"),
            "Max": value("max"),
        })

    chart: list[dict[str, Any]] = [
        {"name": c[:18], "value": missing.get(c, 0)} for c in columns[:12]
    ]
    group_rows: list[dict[str, Any]] = []
    group_columns: list[str] = []
    group_key = group_by if group_by in columns else ""
    value_key = value_column if value_column in numeric else (numeric[0] if numeric else "")
    if group_key and value_key:
        operations = {
            "mean": lambda expr: expr.mean(),
            "sum": lambda expr: expr.sum(),
            "count": lambda expr: expr.count(),
            "max": lambda expr: expr.max(),
            "min": lambda expr: expr.min(),
        }
        aggregator = operations.get(aggregation, operations["mean"])
        grouped = (
            lazy.group_by(group_key)
            .agg(aggregator(pl.col(value_key).cast(pl.Float64, strict=False)).alias(aggregation))
            .sort(aggregation, descending=True)
            .limit(limit)
            .collect(engine="streaming")
        )
        group_columns = [str(c) for c in grouped.columns]
        group_rows = [
            {str(c): json_safe(row[c]) for c in grouped.columns}
            for row in grouped.head(limit).to_dicts()
        ]
        chart = [
            {"name": str(row[group_key])[:22], "value": float(row[aggregation] or 0)}
            for row in group_rows
        ]

    preview = lazy.head(MAX_PREVIEW_ROWS).collect(engine="streaming")
    elapsed = int((time.perf_counter() - started) * 1000)
    return {
        "filename": Path(path).name,
        "row_count": count,
        "column_count": len(columns),
        "columns": columns,
        "schema": schema,
        "numeric": numeric,
        "missing_cells": sum(missing.values()),
        "preview_columns": columns,
        "preview_rows": [
            {str(c): json_safe(row[c]) for c in preview.columns}
            for row in preview.head(MAX_PREVIEW_ROWS).to_dicts()
        ],
        "summary_columns": summary_columns,
        "summary_rows": summary_rows,
        "group_columns": group_columns,
        "group_rows": group_rows,
        "chart": chart,
        "chart_label": aggregation if group_rows else "Missing cells",
        "elapsed_ms": elapsed,
        "engine": "polars.scan_csv · streaming engine",
        "notes": [
            "polars.scan_csv builds a LazyFrame; no full-file materialization is performed.",
            "All aggregations are collected with engine='streaming' so they work on files larger than RAM.",
            f"{count:,} rows scanned in {elapsed} ms.",
        ],
    }


def _bindable(value: Any) -> Any:
    """SQLite can only bind scalars; serialize containers to JSON text."""
    safe = json_safe(value)
    if isinstance(safe, (dict, list)):
        return json.dumps(safe, ensure_ascii=False, default=str)
    return safe


def stream_into_sqlite(
    path: str | Path,
    *,
    table_name: str = "bulk_upload",
    db_path: str | Path | None = None,
    batch_size: int = 2000,
    separator: str | None = None,
) -> dict[str, Any]:
    """Sink a huge CSV into a flat SQLite table in bounded-memory batches.

    Uses ``LazyFrame.sink_ndjson`` (streaming) then reads the NDJSON line by line
    and issues batched ``executemany`` inserts. Peak memory is one batch.
    """
    lazy = scan_upload(path, separator=separator)
    schema = _schema(lazy)
    columns = [str(c) for c in schema.keys()]
    safe_table = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in table_name)
    if not safe_table or safe_table[0].isdigit():
        safe_table = "bulk_" + safe_table
    if not columns:
        raise ValueError("The file has no readable columns.")

    target = Path(db_path) if db_path is not None else database_path()
    started = time.perf_counter()
    conn = sqlite3.connect(str(target), timeout=30)
    inserted = 0
    with tempfile.NamedTemporaryFile(suffix=".ndjson", delete=False) as handle:
        temp_path = Path(handle.name)
    try:
        lazy.sink_ndjson(temp_path)
        quoted = ", ".join(f'"{c.replace(chr(34), chr(34) * 2)}"' for c in columns)
        placeholders = ", ".join("?" for _ in columns)
        conn.execute(f'DROP TABLE IF EXISTS "{safe_table}"')
        conn.execute(f'CREATE TABLE "{safe_table}" ({quoted})')
        batch: list[tuple[Any, ...]] = []
        with open(temp_path, "r", encoding="utf-8") as source:
            for line in source:
                if not line.strip():
                    continue
                record = json.loads(line)
                batch.append(tuple(_bindable(record.get(c)) for c in columns))
                if len(batch) >= batch_size:
                    conn.executemany(
                        f'INSERT INTO "{safe_table}" ({quoted}) VALUES ({placeholders})', batch
                    )
                    inserted += len(batch)
                    batch.clear()
            if batch:
                conn.executemany(
                    f'INSERT INTO "{safe_table}" ({quoted}) VALUES ({placeholders})', batch
                )
                inserted += len(batch)
        conn.commit()
    finally:
        conn.close()
        temp_path.unlink(missing_ok=True)
    return {
        "table": safe_table,
        "rows": inserted,
        "columns": columns,
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
    }


def load_excel_lazy(path: str | Path, *, limit: int = MAX_PREVIEW_ROWS) -> dict[str, Any]:
    """Excel has no lazy scanner; read a bounded preview and say so explicitly."""
    pd = require("pandas")
    frame = pd.read_excel(path)
    columns = [str(c) for c in frame.columns]
    return {
        "filename": Path(path).name,
        "row_count": int(len(frame)),
        "column_count": len(columns),
        "columns": columns,
        "preview_columns": columns,
        "preview_rows": [
            {str(c): json_safe(row.get(c)) for c in columns}
            for row in frame.head(limit).to_dict(orient="records")
        ],
        "engine": "pandas.read_excel (bounded preview — Excel has no lazy scanner)",
        "notes": ["Convert .xlsx to .csv to enable polars.scan_csv out-of-core processing."],
    }
