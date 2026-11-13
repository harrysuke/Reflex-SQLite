"""ML service layer: the single bridge between Reflex state and ``ml_pipelines``.

The pipelines package never imports Reflex, and the UI never imports pandas /
scikit-learn directly. Everything heavy runs here (or in a background event that
calls here), and every function returns plain JSON-serializable dictionaries so
Reflex state can hold the result without custom serializers.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .. import repositories as repo
from ..config import settings
from ..db import session_scope
from ..errors import LibraryUnavailableError, NotFoundError, ValidationError
from ..models import display_time
from . import dataset_service


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


def _db_path() -> Path:
    return settings.database_path


def _missing(exc: Exception) -> LibraryUnavailableError:
    return LibraryUnavailableError(str(exc))


def _assert_dataset(user_id: int, dataset_id: int) -> dict[str, Any]:
    detail = dataset_service.get_dataset_detail(user_id, dataset_id)
    if detail is None:
        raise NotFoundError("Dataset not found.")
    return detail


def _load_frame(dataset_id: int):
    from ml_pipelines.data_access import load_dataset

    return load_dataset(dataset_id, db_path=_db_path())


# --------------------------------------------------------------------------- #
# Statistical profiling (scipy) + regression / time-series (statsmodels)
# --------------------------------------------------------------------------- #


def run_profile(user_id: int, dataset_id: int, alpha: float = 0.05) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.statistics import profile_frame

    _assert_dataset(user_id, dataset_id)
    try:
        frame = _load_frame(dataset_id)
        return profile_frame(frame, alpha=alpha)
    except MissingDependency as exc:
        raise _missing(exc) from exc


def run_regression(
    user_id: int,
    dataset_id: int,
    target: str,
    predictors: list[str] | None = None,
    alpha: float = 0.05,
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.regression import ols_regression

    detail = _assert_dataset(user_id, dataset_id)
    if target not in detail["columns"]:
        raise ValidationError(f"'{target}' is not a column in this dataset.")
    try:
        frame = _load_frame(dataset_id)
        return ols_regression(frame, target, predictors or None, alpha=alpha)
    except MissingDependency as exc:
        raise _missing(exc) from exc


def run_time_series(
    user_id: int,
    dataset_id: int,
    value_column: str,
    date_column: str = "",
    order: tuple[int, int, int] = (1, 1, 1),
    steps: int = 12,
    period: int = 0,
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.regression import time_series_analysis

    detail = _assert_dataset(user_id, dataset_id)
    if value_column not in detail["columns"]:
        raise ValidationError(f"'{value_column}' is not a column in this dataset.")
    try:
        frame = _load_frame(dataset_id)
        return time_series_analysis(
            frame,
            value_column=value_column,
            date_column=date_column or None,
            order=order,
            steps=steps,
            period=period,
        )
    except MissingDependency as exc:
        raise _missing(exc) from exc


# --------------------------------------------------------------------------- #
# Offline training + registry
# --------------------------------------------------------------------------- #


def run_training(
    user_id: int,
    dataset_id: int,
    target: str,
    *,
    algorithm: str = "random_forest",
    task: str = "",
    name: str = "",
    max_rows: int = 20000,
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.train import train_model

    detail = _assert_dataset(user_id, dataset_id)
    if target not in detail["columns"]:
        raise ValidationError(f"'{target}' is not a column in this dataset.")
    try:
        meta = train_model(
            dataset_id,
            target,
            algorithm=algorithm or "random_forest",
            task=task or None,
            name=name or None,
            max_rows=max_rows,
            db_path=_db_path(),
        )
    except MissingDependency as exc:
        raise _missing(exc) from exc

    with session_scope() as session:
        repo.upsert_ml_model(
            session,
            name=meta["name"],
            task=meta["task"],
            algorithm=meta["algorithm"],
            target=meta["target"],
            features_json=json.dumps(meta.get("features", [])),
            artifact_path=meta.get("artifact_path", ""),
            metrics_json=json.dumps(meta.get("metrics", {})),
            training_rows=int(meta.get("training_rows", 0)),
        )
        repo.add_activity(
            session,
            user_id,
            "train",
            f"Trained {meta['algorithm']} for '{target}' ({meta['task']})",
            dataset_id,
        )

    from ml_pipelines.inference import registry

    registry().reload()
    return meta


def list_models() -> list[dict[str, Any]]:
    with session_scope() as session:
        return [
            {
                "id": row.id,
                "name": row.name,
                "task": row.task,
                "algorithm": row.algorithm,
                "target": row.target,
                "features": row.decode_list(row.features_json),
                "metrics": row.decode_dict(row.metrics_json),
                "training_rows": row.training_rows,
                "active": bool(row.is_active),
                "artifact": row.artifact_path,
                "updated": display_time(row.updated_at),
            }
            for row in repo.list_ml_models(session)
        ]


def activate_model(name: str) -> dict[str, Any]:
    with session_scope() as session:
        row = repo.activate_ml_model(session, name)
        if row is None:
            raise NotFoundError("Model not found.")
    from ml_pipelines.inference import registry
    from ml_pipelines.paths import ensure_model_dir

    ensure_model_dir()
    (ensure_model_dir() / "active.json").write_text(
        json.dumps({"name": name}, ensure_ascii=False), encoding="utf-8"
    )
    return registry().reload()


def active_model() -> dict[str, Any]:
    from ml_pipelines.inference import registry

    return registry().describe()


def warm_start() -> dict[str, Any]:
    from ml_pipelines.inference import warm_start as _warm

    return _warm()


# --------------------------------------------------------------------------- #
# Real-time inference + drift monitoring
# --------------------------------------------------------------------------- #


def predict_and_log(
    user_id: int, dataset_id: int, payload: dict[str, Any]
) -> dict[str, Any] | None:
    """Run the cached model on a form payload and persist the call to model_logs."""
    from ml_pipelines.inference import predict

    try:
        result = predict(payload)
    except Exception:
        # A prediction failure must never block the CRUD write it accompanies.
        return None
    if result is None:
        return None
    model_dataset = int(result.get("dataset_id", 0) or 0)
    if model_dataset and model_dataset != int(dataset_id):
        return None

    with session_scope() as session:
        repo.add_model_log(
            session,
            dataset_id=dataset_id,
            model_name=str(result.get("model_name", "")),
            task=str(result.get("task", "regression")),
            target=str(result.get("target", "")),
            input_json=json.dumps(result.get("input_features", {}), ensure_ascii=False, default=str),
            prediction_json=json.dumps(result, ensure_ascii=False, default=str),
            predicted_value=result.get("prediction_numeric"),
            predicted_label=str(result.get("label", "")),
        )
    return result


def model_logs(limit: int = 60, dataset_id: int | None = None) -> list[dict[str, Any]]:
    with session_scope() as session:
        rows = repo.list_model_logs(session, dataset_id, limit)
        return [
            {
                "id": row.id,
                "dataset_id": row.dataset_id,
                "model": row.model_name,
                "task": row.task,
                "target": row.target,
                "predicted": row.predicted_label,
                "actual": row.actual_label,
                "resolved": bool(row.actual_label),
                "created": display_time(row.created_at),
                "inputs": _safe_json(row.input_json, {}),
            }
            for row in rows
        ]


def _safe_json(raw: str, fallback: Any) -> Any:
    try:
        return json.loads(raw or "")
    except (ValueError, TypeError):
        return fallback


def drift(dataset_id: int | None = None, window: int = 10) -> dict[str, Any]:
    from ml_pipelines.drift import drift_summary

    with session_scope() as session:
        rows = list(reversed(repo.list_model_logs(session, dataset_id, 200)))
        prepared = []
        for row in rows:
            absolute_error = None
            if row.predicted_value is not None and row.actual_value is not None:
                absolute_error = round(abs(float(row.predicted_value) - float(row.actual_value)), 6)
            prepared.append(
                {
                    "task": row.task,
                    "actual_value": row.actual_label,
                    "is_correct": row.correct,
                    "absolute_error": absolute_error,
                    "created_at": row.created_at,
                }
            )
    return drift_summary(prepared, window=window)


def resolve_log(log_id: int, actual: str) -> dict[str, Any]:
    from ml_pipelines.drift import outcome_fields

    with session_scope() as session:
        rows = [r for r in repo.list_model_logs(session, None, 500) if r.id == log_id]
        if not rows:
            raise NotFoundError("Prediction log not found.")
        row = rows[0]
        outcome = outcome_fields(row.predicted_label, actual, row.task)
        updated = repo.resolve_model_log(
            session,
            log_id,
            actual_value=outcome["actual_numeric"],
            actual_label=str(actual),
            correct=outcome["is_correct"],
        )
        if updated is None:
            raise NotFoundError("Prediction log not found.")
        return {"id": log_id, "actual": str(actual), "correct": outcome["is_correct"]}


# --------------------------------------------------------------------------- #
# OLAP (DuckDB over SQLite)
# --------------------------------------------------------------------------- #


def run_olap(
    user_id: int,
    dataset_id: int,
    sql: str,
    chart_x: str = "",
    chart_y: str = "",
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.olap import run_query

    _assert_dataset(user_id, dataset_id)
    try:
        return run_query(
            sql,
            db_path=_db_path(),
            dataset_id=dataset_id,
            chart_x_column=chart_x,
            chart_y_column=chart_y,
        )
    except MissingDependency as exc:
        raise _missing(exc) from exc


# --------------------------------------------------------------------------- #
# Out-of-core large-file processing (Polars)
# --------------------------------------------------------------------------- #


def list_uploads() -> list[dict[str, Any]]:
    from ml_pipelines.large_files import list_uploads as _list

    try:
        items = _list(settings.upload_dir)
    except Exception:
        return []
    out = []
    for item in items:
        if isinstance(item, dict):
            out.append(
                {
                    "name": item.get("name") or item.get("filename") or "",
                    "size_kb": item.get("size_kb", round(float(item.get("size_bytes", 0)) / 1024, 1)),
                }
            )
        else:
            path = Path(str(item))
            out.append({"name": path.name, "size_kb": round(path.stat().st_size / 1024, 1) if path.exists() else 0})
    return out


def profile_large_file(
    filename: str,
    *,
    group_by: str = "",
    value_column: str = "",
    aggregation: str = "mean",
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.large_files import profile_lazy

    path = (settings.upload_dir / Path(filename).name).resolve()
    if not path.exists():
        raise NotFoundError("Uploaded file not found.")
    try:
        return profile_lazy(
            path,
            group_by=group_by,
            value_column=value_column,
            aggregation=aggregation,
        )
    except MissingDependency as exc:
        raise _missing(exc) from exc


# --------------------------------------------------------------------------- #
# Unsupervised mining
# --------------------------------------------------------------------------- #


def run_clustering(
    user_id: int,
    dataset_id: int,
    features: list[str] | None = None,
    k: int = 3,
    algorithm: str = "kmeans",
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.mining import cluster_frame

    _assert_dataset(user_id, dataset_id)
    try:
        frame = _load_frame(dataset_id)
        return cluster_frame(frame, features=features or None, k=k, algorithm=algorithm)
    except MissingDependency as exc:
        raise _missing(exc) from exc


def run_association(
    user_id: int,
    dataset_id: int,
    transaction_col: str,
    item_col: str,
    *,
    algorithm: str = "fpgrowth",
    min_support: float = 0.05,
) -> dict[str, Any]:
    from ml_pipelines._optional import MissingDependency
    from ml_pipelines.mining import association_rules

    detail = _assert_dataset(user_id, dataset_id)
    for column in (transaction_col, item_col):
        if column not in detail["columns"]:
            raise ValidationError(f"'{column}' is not a column in this dataset.")
    try:
        frame = _load_frame(dataset_id)
        return association_rules(
            frame,
            transaction_col=transaction_col,
            item_col=item_col,
            algorithm=algorithm,
            min_support=min_support,
        )
    except MissingDependency as exc:
        raise _missing(exc) from exc
