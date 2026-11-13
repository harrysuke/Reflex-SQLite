"""Single-load model registry for real-time inference inside Reflex state.

The backend calls :func:`warm_start` once at startup. Artifacts are loaded from
``models/*.joblib`` with ``joblib.load`` and cached; the cache is invalidated
only when a file's mtime changes (i.e. after a retrain), so a CRUD request never
pays the deserialization cost.

This module has no Reflex imports: it also works from a plain Python script.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ._optional import require
from .paths import database_path, models_dir
from .preprocessing import float_or_none, json_safe

PREDICTION_KEY = "__ml_prediction__"


@dataclass
class LoadedModel:
    name: str
    metadata: dict[str, Any]
    pipeline: Any
    mtime: float

    def predict(self, features: dict[str, Any]) -> dict[str, Any]:
        """Align a form dictionary to the training schema and call model.predict()."""
        pd = require("pandas")
        meta = self.metadata
        columns = [str(c) for c in meta.get("features", [])]
        if not columns:
            raise ValueError("The model artifact has no feature metadata.")
        row: dict[str, Any] = {}
        numeric = set(meta.get("numeric_features", []))
        for column in columns:
            value = features.get(column, None)
            if column in numeric:
                row[column] = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
            else:
                row[column] = "" if value is None else str(value)
        frame = pd.DataFrame([row], columns=columns)
        prediction = self.pipeline.predict(frame)[0]

        probability: float | None = None
        if hasattr(self.pipeline, "predict_proba"):
            try:
                probability = round(float(max(self.pipeline.predict_proba(frame)[0])), 4)
            except Exception:
                probability = None

        task = str(meta.get("task", "regression"))
        predicted_numeric = float_or_none(prediction) if task == "regression" else None
        display = json_safe(prediction)
        if isinstance(display, float):
            display = round(display, 4)
        return {
            "model_name": self.name,
            "task": task,
            "target": str(meta.get("target", "")),
            "dataset_id": int(meta.get("dataset_id", 0) or 0),
            "algorithm": str(meta.get("algorithm", "")),
            "version": str(meta.get("version", "1")),
            "prediction": display,
            "prediction_value": str(display),
            "prediction_numeric": predicted_numeric,
            "probability": probability,
            "input_features": {c: json_safe(row.get(c)) for c in columns},
            "label": f"{display}" + (f" ({probability:.0%} confidence)" if probability else ""),
        }


class ModelRegistry:
    """Thread-safe, lazy, mtime-aware cache of serialized model artifacts."""

    def __init__(self, directory: str | Path | None = None):
        self.directory = Path(directory) if directory is not None else models_dir()
        self._cache: dict[str, LoadedModel] = {}
        self._lock = threading.RLock()  # reload() re-enters via describe()
        self._active_name: str | None = None

    def artifacts(self) -> list[Path]:
        if not self.directory.exists():
            return []
        return sorted(
            self.directory.glob("*.joblib"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    def _active_from_db(self) -> str | None:
        path = database_path()
        if not path.exists():
            return None
        try:
            conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True, timeout=10)
            try:
                row = conn.execute(
                    "SELECT name FROM ml_models WHERE is_active = 1 ORDER BY id DESC LIMIT 1"
                ).fetchone()
                return str(row[0]) if row else None
            finally:
                conn.close()
        except sqlite3.Error:
            return None  # table not created yet

    def resolve_name(self, *, refresh: bool = False) -> str | None:
        if self._active_name and not refresh:
            return self._active_name
        name = self._active_from_db()
        if not name:
            marker = self.directory / "active.json"
            if marker.exists():
                try:
                    name = str(json.loads(marker.read_text(encoding="utf-8")).get("name") or "")
                except (ValueError, OSError):
                    name = ""
        if not name:
            files = self.artifacts()
            name = files[0].stem if files else None
        self._active_name = name or None
        return self._active_name

    def active(self, *, refresh: bool = False) -> LoadedModel | None:
        """Load the .joblib artifact once; reload only when the file changes."""
        name = self.resolve_name(refresh=refresh)
        if not name:
            return None
        artifact = self.directory / f"{name}.joblib"
        if not artifact.exists():
            files = self.artifacts()
            if not files:
                return None
            artifact = files[0]
            name = artifact.stem
        with self._lock:
            mtime = artifact.stat().st_mtime
            cached = self._cache.get(name)
            if cached is not None and cached.mtime == mtime:
                return cached
            joblib = require("joblib")
            bundle = joblib.load(artifact)
            if not isinstance(bundle, dict) or "pipeline" not in bundle:
                raise ValueError(f"{artifact.name} is not a DataForge model bundle.")
            loaded = LoadedModel(
                name=name,
                metadata=dict(bundle.get("metadata", {})),
                pipeline=bundle["pipeline"],
                mtime=mtime,
            )
            self._cache = {name: loaded}  # keep memory bounded to the active model
            self._active_name = name
            return loaded

    def predict(self, features: dict[str, Any]) -> dict[str, Any] | None:
        model = self.active()
        if model is None:
            return None
        return model.predict(features)

    def reload(self) -> dict[str, Any]:
        with self._lock:
            self._cache.clear()
            self._active_name = None
        return self.describe()

    def describe(self) -> dict[str, Any]:
        model = self.active()
        files = self.artifacts()
        return {
            "loaded": model is not None,
            "name": model.name if model else "",
            "task": str(model.metadata.get("task", "")) if model else "",
            "algorithm": str(model.metadata.get("algorithm", "")) if model else "",
            "target": str(model.metadata.get("target", "")) if model else "",
            "features": list(model.metadata.get("features", [])) if model else [],
            "metrics": dict(model.metadata.get("metrics", {})) if model else {},
            "trained_at": str(model.metadata.get("trained_at", "")) if model else "",
            "artifact_count": len(files),
            "models_dir": str(self.directory),
            "hint": "" if model else "No trained model yet. Run the training pipeline on the Predictive Analytics page.",
        }


_REGISTRY = ModelRegistry()


def registry() -> ModelRegistry:
    return _REGISTRY


def warm_start() -> dict[str, Any]:
    """Called once from the Reflex backend bootstrap."""
    return _REGISTRY.describe()


def predict(features: dict[str, Any]) -> dict[str, Any] | None:
    return _REGISTRY.predict(features)
