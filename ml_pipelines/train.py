"""Offline model training: SQLite (raw SQL) -> scikit-learn Pipeline -> .joblib.

Run from the workspace root::

    python -m ml_pipelines train --dataset-id 1 --target revenue
    python -m ml_pipelines train --dataset-id 1 --target status --algorithm xgboost --task classification

The serialized bundle contains the fitted pipeline *and* the exact feature /
dtype metadata inference needs, so serving cannot drift from training.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ._optional import require
from .data_access import load_dataset
from .paths import database_path, ensure_model_dir
from .preprocessing import build_estimator, float_or_none, json_safe, split_features

ALGORITHMS = ("random_forest", "gradient_boosting", "linear", "xgboost", "lightgbm")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def train_model(
    dataset_id: int,
    target: str,
    *,
    algorithm: str = "random_forest",
    task: str | None = None,
    name: str | None = None,
    max_rows: int = 20000,
    test_size: float = 0.25,
    db_path: str | Path | None = None,
    models_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Query SQLite, fit a model and serialize it to ``models/<name>.joblib``."""
    started = time.perf_counter()
    frame = load_dataset(dataset_id, limit=max_rows, db_path=db_path)
    if frame.empty:
        raise ValueError(f"Dataset #{dataset_id} has no rows.")
    if target not in frame.columns:
        raise ValueError(f"Target '{target}' is not a column. Available: {', '.join(map(str, frame.columns))}")
    x, y, numeric, categorical, resolved_task = split_features(frame, target, task)
    if len(x) < 12:
        raise ValueError("At least 12 complete rows are needed to train a model.")
    if len(x.columns) == 0:
        raise ValueError("The dataset has no feature columns besides the target.")

    pipeline, algorithm = build_estimator(resolved_task, algorithm, numeric, categorical)
    from sklearn.model_selection import train_test_split

    stratify = None
    if resolved_task == "classification":
        counts = y.astype(str).value_counts()
        if len(counts) > 1 and counts.min() >= 2:
            stratify = y.astype(str)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=42, stratify=stratify
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    metrics: dict[str, Any] = {"training_rows": int(len(x_train)), "holdout_rows": int(len(x_test))}
    if resolved_task == "classification":
        from sklearn.metrics import accuracy_score, f1_score

        truth = y_test.astype(str)
        predicted = [str(v) for v in predictions]
        metrics["accuracy"] = round(float(accuracy_score(truth, predicted)), 4)
        metrics["f1_weighted"] = round(
            float(f1_score(truth, predicted, average="weighted", zero_division=0)), 4
        )
    else:
        from sklearn.metrics import mean_absolute_error, r2_score

        metrics["r2"] = round(float(r2_score(y_test, predictions)), 4)
        metrics["mae"] = round(float(mean_absolute_error(y_test, predictions)), 4)

    model_name = name or f"model_{dataset_id}_{target}".replace(" ", "_").lower()
    model_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in model_name)
    output_dir = ensure_model_dir() if models_dir is None else Path(models_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact = output_dir / f"{model_name}.joblib"

    metadata = {
        "name": model_name,
        "algorithm": algorithm,
        "task": resolved_task,
        "target": target,
        "dataset_id": int(dataset_id),
        "features": [str(c) for c in x.columns],
        "numeric_features": [str(c) for c in numeric],
        "categorical_features": [str(c) for c in categorical],
        "classes": [json_safe(v) for v in getattr(pipeline.named_steps["model"], "classes_", [])],
        "metrics": metrics,
        "training_rows": int(len(x_train)),
        "artifact_path": str(artifact),
        "trained_at": _now(),
        "elapsed_ms": 0,
        "version": "1",
    }
    bundle = {
        "pipeline": pipeline,
        "metadata": metadata,
        "library_versions": {
            "sklearn": _version("scikit-learn"),
            "numpy": _version("numpy"),
            "pandas": _version("pandas"),
        },
    }
    joblib = require("joblib")
    joblib.dump(bundle, artifact, compress=3)
    metadata["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
    metadata["size_kb"] = round(artifact.stat().st_size / 1024, 1)
    metadata["db_path"] = str(Path(db_path) if db_path else database_path())

    # Point the inference registry at the freshly trained artifact.
    (output_dir / "active.json").write_text(
        json.dumps({"name": model_name}, ensure_ascii=False), encoding="utf-8"
    )
    return metadata


def _version(distribution: str) -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version(distribution)
    except PackageNotFoundError:
        return ""


def register_model_cli(metadata: dict[str, Any], *, db_path: str | Path | None = None) -> None:
    """CLI-only: register the artifact in ``ml_models`` using plain SQL.

    The web app registers through its repository layer instead; keeping this
    here means ``ml_pipelines`` never imports the Reflex application package.
    """
    import sqlite3

    path = Path(db_path) if db_path is not None else database_path()
    conn = sqlite3.connect(str(path), timeout=30)
    try:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS ml_models (
                id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                task VARCHAR NOT NULL,
                algorithm VARCHAR NOT NULL,
                target VARCHAR NOT NULL,
                features_json VARCHAR NOT NULL,
                artifact_path VARCHAR NOT NULL,
                metrics_json VARCHAR NOT NULL,
                training_rows INTEGER NOT NULL,
                is_active BOOLEAN NOT NULL DEFAULT 0,
                created_at VARCHAR NOT NULL,
                updated_at VARCHAR NOT NULL
            )"""
        )
        conn.execute("UPDATE ml_models SET is_active = 0")
        conn.execute(
            """INSERT INTO ml_models
               (name, task, algorithm, target, features_json, artifact_path,
                metrics_json, training_rows, is_active, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
               ON CONFLICT(name) DO UPDATE SET
                 task=excluded.task, algorithm=excluded.algorithm,
                 target=excluded.target, features_json=excluded.features_json,
                 artifact_path=excluded.artifact_path, metrics_json=excluded.metrics_json,
                 training_rows=excluded.training_rows, is_active=1,
                 updated_at=excluded.updated_at""",
            (
                metadata["name"], metadata["task"], metadata["algorithm"],
                metadata["target"], json.dumps(metadata["features"]),
                metadata["artifact_path"], json.dumps(metadata["metrics"]),
                int(metadata["training_rows"]), metadata["trained_at"], metadata["trained_at"],
            ),
        )
        conn.commit()
    finally:
        conn.close()
