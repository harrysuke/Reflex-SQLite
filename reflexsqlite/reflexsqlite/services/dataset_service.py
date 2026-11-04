"""Dataset service: file ingestion, validation, row-level CRUD and chart feeds."""
from __future__ import annotations

import csv
import io
import json
import math
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .. import repositories as repo
from ..config import settings
from ..db import session_scope
from ..errors import NotFoundError, UploadError, ValidationError
from ..models import display_time, utcnow

MAX_STORED_ROWS = 5000
MAX_LIVE_POINTS = 120
SUPPORTED_EXTENSIONS = {".csv", ".tsv", ".txt", ".json", ".xlsx", ".xls"}


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #


def _clean(value: Any) -> Any:
    """Convert numpy/pandas scalars into JSON-safe Python values."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (bool,)):
        return bool(value)
    if isinstance(value, (int,)):
        return int(value)
    if isinstance(value, (float,)):
        return None if not math.isfinite(value) else float(value)
    if isinstance(value, str):
        return value
    if hasattr(value, "item"):
        try:
            return _clean(value.item())
        except (ValueError, AttributeError):
            pass
    if isinstance(value, (datetime,)):
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, (list, dict, tuple)):
        return json.loads(json.dumps(value, default=str))
    return str(value)


def _read_frame(filename: str, content: bytes) -> Any:
    import pandas as pd

    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise UploadError(f"Unsupported file type '{suffix}'. Use CSV, TSV, JSON or Excel.")
    if len(content) == 0:
        raise UploadError("The uploaded file is empty.")
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise UploadError(f"File exceeds the {settings.max_upload_mb} MB limit.")

    buffer = io.BytesIO(content)
    try:
        if suffix in {".csv", ".tsv", ".txt"}:
            # `.txt` has no canonical delimiter, so let pandas sniff it with the
            # python engine.  csv/tsv use the faster C engine; note that
            # `low_memory` is C-engine-only and must NOT be passed when sep=None.
            sep = "\t" if suffix == ".tsv" else ("," if suffix == ".csv" else None)
            options = {} if sep is None else {"low_memory": False}
            # utf-8-sig strips a BOM; latin-1 is a pragmatic fallback.
            try:
                buffer.seek(0)
                frame = pd.read_csv(buffer, sep=sep, encoding="utf-8-sig", **options)
            except UnicodeDecodeError:
                buffer.seek(0)
                frame = pd.read_csv(buffer, sep=sep, encoding="latin-1", **options)
            # Semicolon/tab/pipe-delimited files often arrive with a .csv name.
            if len(frame.columns) == 1:
                head = content[:4096].decode("utf-8-sig", errors="ignore")
                for candidate in (";", "\t", "|"):
                    if candidate in head:
                        buffer.seek(0)
                        frame = pd.read_csv(
                            buffer, sep=candidate, encoding="utf-8-sig", low_memory=False
                        )
                        break
            return frame
        if suffix == ".json":
            return pd.read_json(buffer)
        return pd.read_excel(buffer)
    except UploadError:
        raise
    except Exception as exc:
        raise UploadError(f"Could not parse this file: {type(exc).__name__}: {exc}") from exc


def _frame_to_records(frame: Any) -> tuple[list[str], list[str], list[str], list[dict[str, Any]]]:
    import pandas as pd

    # Guarantee unique, string column names (pandas allows duplicates/non-strings).
    seen: dict[str, int] = {}
    rename: dict[Any, str] = {}
    for original in frame.columns:
        base = str(original).strip() or "column"
        seen[base] = seen.get(base, 0) + 1
        rename[original] = base if seen[base] == 1 else f"{base}_{seen[base]}"
    frame = frame.rename(columns=rename)

    columns = [str(c) for c in frame.columns]
    numeric = [c for c in columns if pd.api.types.is_numeric_dtype(frame[c])]
    categorical = [c for c in columns if c not in numeric]

    frame = frame.head(MAX_STORED_ROWS)
    records = [
        {col: _clean(value) for col, value in row.items()}
        for row in frame.to_dict(orient="records")
    ]
    return columns, numeric, categorical, records


# --------------------------------------------------------------------------- #
# Ingestion / CRUD
# --------------------------------------------------------------------------- #


def ingest_upload(owner_id: int, filename: str, content: bytes, description: str = "") -> int:
    """Parse a file and persist a Dataset plus its rows in one transaction."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise UploadError(f"Unsupported file type '{suffix}'.")

    frame = _read_frame(filename, content)
    if frame.empty or len(frame.columns) == 0:
        raise UploadError("The dataset contains no rows or columns.")
    columns, numeric, categorical, records = _frame_to_records(frame)

    # Keep an archival copy of the original upload.
    stored_path = settings.upload_dir / f"{utcnow():%Y%m%d%H%M%S}_{Path(filename).name}"
    stored_path.write_bytes(content)

    with session_scope() as session:
        dataset = repo.create_dataset(
            session,
            owner_id=owner_id,
            name=Path(filename).stem.replace("_", " ").title(),
            filename=Path(filename).name,
            file_format=suffix.lstrip("."),
            description=description.strip(),
            size_bytes=len(content),
            row_count=len(records),
            column_count=len(columns),
            columns_json=json.dumps(columns, ensure_ascii=False),
            numeric_columns_json=json.dumps(numeric, ensure_ascii=False),
            categorical_columns_json=json.dumps(categorical, ensure_ascii=False),
        )
        dataset_id = int(dataset.id)
        repo.bulk_insert_rows(session, dataset_id, records)
        repo.add_activity(
            session, owner_id, "upload", f"Imported {len(records)} rows from {filename}", dataset_id
        )
        repo.clear_points(session, dataset_id)
        for index in range(12):
            repo.add_metric_point(
                session,
                dataset_id,
                label=f"{(utcnow() - timedelta(minutes=11 - index)):%H:%M:%S}",
                value=round(random.uniform(40, 90), 2),
            )
    return dataset_id


def rename_dataset(owner_id: int, dataset_id: int, name: str, description: str) -> None:
    if not name.strip():
        raise ValidationError("Dataset name cannot be empty.")
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, owner_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        dataset.name = name.strip()[:120]
        dataset.description = description.strip()[:500]
        repo.save_dataset(session, dataset)
        repo.add_activity(session, owner_id, "update", f"Updated metadata for {dataset.name}", dataset_id)


def remove_dataset(owner_id: int, dataset_id: int) -> None:
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, owner_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        repo.delete_dataset(session, dataset)
        repo.add_activity(session, owner_id, "delete", f"Deleted {dataset.name}")


def add_record(owner_id: int, dataset_id: int, payload: dict[str, Any]) -> None:
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, owner_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        clean = _coerce_payload(payload, dataset.columns, dataset.numeric_columns)
        repo.add_row(session, dataset_id, clean)
        dataset.row_count += 1
        repo.save_dataset(session, dataset)
        repo.add_activity(session, owner_id, "create", "Added a row", dataset_id)


def edit_record(owner_id: int, dataset_id: int, row_id: int, payload: dict[str, Any]) -> None:
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, owner_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        row = repo.get_row(session, row_id, dataset_id)
        if row is None:
            raise NotFoundError("Row not found.")
        clean = _coerce_payload(payload, dataset.columns, dataset.numeric_columns)
        repo.save_row(session, row, clean)
        repo.add_activity(session, owner_id, "update", f"Edited row #{row.row_index + 1}", dataset_id)


def delete_record(owner_id: int, dataset_id: int, row_id: int) -> None:
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, owner_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        row = repo.get_row(session, row_id, dataset_id)
        if row is None:
            raise NotFoundError("Row not found.")
        repo.delete_row(session, row)
        dataset.row_count = max(0, dataset.row_count - 1)
        repo.save_dataset(session, dataset)
        repo.add_activity(session, owner_id, "delete", f"Deleted row #{row.row_index + 1}", dataset_id)


def _coerce_payload(payload: dict[str, Any], columns: list[str], numeric: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for column in columns:
        raw = payload.get(column, "")
        if column in numeric:
            if raw is None or str(raw).strip() == "":
                result[column] = None
            else:
                try:
                    result[column] = float(raw)
                except (TypeError, ValueError) as exc:
                    raise ValidationError(f"'{column}' must be numeric.") from exc
        else:
            result[column] = "" if raw is None else str(raw)[:500]
    return result


# --------------------------------------------------------------------------- #
# Queries / summaries
# --------------------------------------------------------------------------- #


def list_user_datasets(user_id: int, search: str = "") -> list[dict[str, Any]]:
    with session_scope() as session:
        return [
            {
                "id": d.id,
                "name": d.name,
                "filename": d.filename,
                "format": d.file_format.upper(),
                "rows": d.row_count,
                "columns": d.column_count,
                "size_kb": round(d.size_bytes / 1024, 1),
                "description": d.description,
                "updated": display_time(d.updated_at),
            }
            for d in repo.list_datasets(session, user_id, search)
        ]


def get_dataset_detail(user_id: int, dataset_id: int) -> dict[str, Any] | None:
    with session_scope() as session:
        d = repo.get_dataset(session, dataset_id, user_id)
        if d is None:
            return None
        return {
            "id": d.id,
            "name": d.name,
            "columns": d.columns,
            "numeric": d.numeric_columns,
            "categorical": d.categorical_columns,
            "row_count": d.row_count,
            "column_count": d.column_count,
            "filename": d.filename,
            "description": d.description,
            "updated": display_time(d.updated_at),
        }


def get_table_page(
    user_id: int, dataset_id: int, page: int = 1, page_size: int = 10, search: str = ""
) -> dict[str, Any]:
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, user_id)
        if dataset is None:
            raise NotFoundError("Dataset not found.")
        offset = max(0, (page - 1) * page_size)
        rows, matched = repo.list_rows(session, dataset_id, offset, page_size, search)
        return {
            "columns": dataset.columns,
            "numeric": dataset.numeric_columns,
            "rows": [
                {"_id": r.id, "_index": r.row_index + 1, **r.as_dict()} for r in rows
            ],
            "total": matched,
            "page": page,
            "page_size": page_size,
        }


def get_all_records(user_id: int, dataset_id: int, limit: int | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    with session_scope() as session:
        d = repo.get_dataset(session, dataset_id, user_id)
        if d is None:
            raise NotFoundError("Dataset not found.")
        meta = {
            "columns": d.columns,
            "numeric": d.numeric_columns,
            "categorical": d.categorical_columns,
            "name": d.name,
        }
        return meta, repo.all_rows(session, dataset_id, limit)


def compute_stats(user_id: int, dataset_id: int) -> dict[str, Any]:
    with session_scope() as session:
        d = repo.get_dataset(session, dataset_id, user_id)
        if d is None:
            raise NotFoundError("Dataset not found.")
        rows = repo.all_rows(session, dataset_id)
        columns = d.columns
        total_cells = max(1, len(rows) * len(columns))
        missing = sum(1 for row in rows for col in columns if row.get(col) in (None, ""))
        return {
            "datasets": repo.count_datasets(session, user_id),
            "rows": len(rows),
            "columns": len(columns),
            "numeric": len(d.numeric_columns),
            "missing": missing,
            "completeness": round(100 * (1 - missing / total_cells), 1),
            "activity": [
                {
                    "action": a.action,
                    "detail": a.detail,
                    "time": display_time(a.created_at),
                }
                for a in repo.recent_activity(session, user_id, 6)
            ],
        }


def get_record(user_id: int, dataset_id: int, row_id: int) -> dict[str, Any] | None:
    """Fetch a single row as a plain dict for the edit form."""
    with session_scope() as session:
        dataset = repo.get_dataset(session, dataset_id, user_id)
        if dataset is None:
            return None
        row = repo.get_row(session, row_id, dataset_id)
        if row is None:
            return None
        return {c: row.as_dict().get(c, "") for c in dataset.columns}



def chart_series(
    user_id: int,
    dataset_id: int,
    chart_type: str = "line",
    x_column: str = "",
    y_column: str = "",
) -> list[dict[str, Any]]:
    """Build the data array consumed by the interactive dashboard charts."""
    import numpy as np

    meta, rows = get_all_records(user_id, dataset_id, settings.max_training_rows * 3)
    columns, numeric, categorical = meta["columns"], meta["numeric"], meta["categorical"]
    if not rows or not columns:
        return []
    y = y_column if y_column in numeric else (numeric[0] if numeric else "")
    x = x_column if x_column in columns else ""
    if not y:
        # No numeric column -> count categories instead.
        target = x if x in categorical else (categorical[0] if categorical else columns[0])
        counts: dict[str, int] = {}
        for row in rows:
            key = str(row.get(target, "—"))
            counts[key] = counts.get(key, 0) + 1
        return [
            {"name": str(k)[:22], "value": v}
            for k, v in sorted(counts.items(), key=lambda kv: -kv[1])[:12]
        ]

    values = [float(row[y]) for row in rows if isinstance(row.get(y), (int, float))]

    if chart_type == "histogram":
        if not values:
            return []
        hist, edges = np.histogram(values, bins=min(12, max(4, int(np.sqrt(len(values))))))
        return [
            {"name": f"{edges[i]:.1f}–{edges[i + 1]:.1f}", "value": int(hist[i])}
            for i in range(len(hist))
        ]

    if chart_type == "scatter":
        other = next((c for c in numeric if c != y), y)
        return [
            {"name": str(i + 1), "x": float(r.get(other) or 0), "y": float(r.get(y) or 0)}
            for i, r in enumerate(rows[:120])
            if isinstance(r.get(y), (int, float))
        ]

    if chart_type == "bar" and categorical:
        group = x if x in categorical else categorical[0]
        buckets: dict[str, list[float]] = {}
        for row in rows:
            value = row.get(y)
            if isinstance(value, (int, float)):
                buckets.setdefault(str(row.get(group, "—"))[:22], []).append(float(value))
        return [
            {"name": key, "value": round(sum(vals) / len(vals), 2)}
            for key, vals in sorted(buckets.items(), key=lambda kv: -sum(kv[1]))[:12]
        ]

    # Trend: bucket the primary numeric column over source order.
    buckets_count = min(16, max(6, len(rows) // 12))
    chunks = np.array_split(np.array(values, dtype=float), max(1, buckets_count)) if values else []
    return [
        {"name": f"T{i + 1}", "value": round(float(chunk.mean()), 2), "min": round(float(chunk.min()), 2), "max": round(float(chunk.max()), 2)}
        for i, chunk in enumerate(chunks)
        if chunk.size
    ]


def correlation_matrix(user_id: int, dataset_id: int) -> dict[str, Any]:
    meta, rows = get_all_records(user_id, dataset_id, settings.max_training_rows)
    numeric = meta["numeric"][:8]
    if len(numeric) < 2:
        return {"labels": numeric, "rows": []}
    import numpy as np

    values = {
        c: np.array([float(r.get(c)) if isinstance(r.get(c), (int, float)) else np.nan for r in rows])
        for c in numeric
    }
    result_rows = []
    for a in numeric:
        cells = []
        for b in numeric:
            va, vb = values[a], values[b]
            mask = ~(np.isnan(va) | np.isnan(vb))
            coef = float(np.corrcoef(va[mask], vb[mask])[0, 1]) if mask.sum() > 2 else 0.0
            value = round(coef if np.isfinite(coef) else 0.0, 2)
            intensity = min(1.0, abs(value))
            color = (
                f"rgba(79, 70, 229, {0.08 + 0.72 * intensity:.2f})"
                if value >= 0
                else f"rgba(14, 165, 233, {0.08 + 0.72 * intensity:.2f})"
            )
            cells.append({"v": value, "color": color, "tip": f"{a} × {b}: {value:+.2f}"})
        result_rows.append({"label": a, "cells": cells})
    return {"labels": numeric, "rows": result_rows}


def live_points(user_id: int, dataset_id: int, limit: int = 24) -> list[dict[str, Any]]:
    with session_scope() as session:
        d = repo.get_dataset(session, dataset_id, user_id)
        if d is None:
            return []
        return [
            {"name": p.label, "value": p.value, "series": p.series}
            for p in repo.recent_points(session, dataset_id, limit)
        ]


def append_live_point(user_id: int, dataset_id: int) -> list[dict[str, Any]]:
    """Append one synthetic streaming sample derived from real dataset values."""
    meta, rows = get_all_records(user_id, dataset_id, 250)
    numeric = meta["numeric"]
    base = 50.0
    if numeric and rows:
        sample = [float(r.get(numeric[0])) for r in rows if isinstance(r.get(numeric[0]), (int, float))]
        if sample:
            base = sum(sample) / len(sample)
    value = round(base * random.uniform(0.82, 1.18) + random.uniform(-2, 2), 2)
    with session_scope() as session:
        repo.add_metric_point(session, dataset_id, utcnow().strftime("%H:%M:%S"), value)
        # A dashboard left open for hours must not grow the table without bound.
        repo.trim_points(session, dataset_id, keep=MAX_LIVE_POINTS)
    return live_points(user_id, dataset_id)


def export_csv(user_id: int, dataset_id: int) -> tuple[str, str]:
    meta, rows = get_all_records(user_id, dataset_id)
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=meta["columns"], extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow({c: row.get(c, "") for c in meta["columns"]})
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in meta["name"])
    return f"{safe_name or 'dataset'}.csv", out.getvalue()


# --------------------------------------------------------------------------- #
# First-run demo content
# --------------------------------------------------------------------------- #


def seed_demo(force: bool = False) -> None:
    """Create a demo account and two sample datasets on an empty database."""
    import numpy as np

    from .auth_service import hash_password

    with session_scope() as session:
        existing = repo.find_user_by_login(session, "demo")
        if existing is not None and not force:
            return
        if existing is not None:
            demo = existing
        else:
            demo = repo.create_user(
                session,
                username="demo",
                email="demo@dataforge.local",
                full_name="Demo Analyst",
                password_hash=hash_password("demo1234"),
                role="admin",
                avatar_color="#4F46E5",
            )
        repo.get_or_create_settings(session, demo.id)

        rng = np.random.default_rng(42)
        start = utcnow() - timedelta(days=120)
        regions = ["North", "South", "East", "West"]
        products = ["Starter", "Pro", "Enterprise", "Add-on"]
        sales_rows = []
        for i in range(360):
            units = int(rng.integers(2, 60))
            price = float(round(rng.uniform(19, 240), 2))
            discount = float(round(rng.uniform(0, 0.35), 2))
            sales_rows.append(
                {
                    "date": (start + timedelta(days=i % 120)).strftime("%Y-%m-%d"),
                    "region": regions[int(rng.integers(0, len(regions)))],
                    "product": products[int(rng.integers(0, len(products)))],
                    "segment": "B2B" if i % 3 else "B2C",
                    "units": units,
                    "unit_price": price,
                    "discount": discount,
                    "revenue": round(units * price * (1 - discount), 2),
                    "satisfaction": float(round(rng.uniform(3.0, 5.0), 2)),
                }
            )

        sensor_rows = []
        for i in range(240):
            temp = float(round(rng.normal(22, 4), 2))
            sensor_rows.append(
                {
                    "sample_id": i + 1,
                    "temperature": temp,
                    "humidity": float(round(rng.normal(55, 12), 2)),
                    "pressure": float(round(rng.normal(1013, 8), 2)),
                    "vibration": float(round(abs(rng.normal(0.5, 0.25)), 3)),
                    "power_kw": float(round(2 + 0.05 * temp + rng.normal(0, 0.3), 3)),
                    "status": "nominal" if abs(temp - 22) < 6 else "alert",
                }
            )

        specs = [
            ("Global Sales 2026", "sales.csv", sales_rows, "Synthetic sales transactions across four regions"),
            ("Sensor Telemetry", "sensors.csv", sensor_rows, "Equipment telemetry for regression and clustering"),
        ]
        for name, filename, records, description in specs:
            columns = list(records[0].keys())
            numeric = [c for c in columns if all(isinstance(r[c], (int, float)) for r in records[:20])]
            categorical = [c for c in columns if c not in numeric]
            d = repo.create_dataset(
                session,
                owner_id=demo.id,
                name=name,
                filename=filename,
                file_format="csv",
                description=description,
                size_bytes=len(records) * 120,
                row_count=len(records),
                column_count=len(columns),
                columns_json=json.dumps(columns),
                numeric_columns_json=json.dumps(numeric),
                categorical_columns_json=json.dumps(categorical),
            )
            repo.bulk_insert_rows(session, int(d.id), records)
            for k in range(12):
                repo.add_metric_point(
                    session,
                    int(d.id),
                    (utcnow() - timedelta(minutes=11 - k)).strftime("%H:%M:%S"),
                    round(float(rng.uniform(45, 95)), 2),
                )
        repo.add_activity(session, demo.id, "account", "Demo workspace initialized")
