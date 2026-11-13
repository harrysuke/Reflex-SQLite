"""Runtime path resolution shared by the CLI and the web backend.

Kept free of application imports so ``python -m ml_pipelines train ...`` works
from a bare checkout. The environment variables are the same ones read by
``reflexsqlite.reflexsqlite.config`` (``APP_DATA_DIR``, ``APP_UPLOAD_DIR``,
``APP_DATABASE_URL``, ``APP_MODELS_DIR``).
"""
from __future__ import annotations

import os
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def workspace_root() -> Path:
    return WORKSPACE_ROOT


def _path(env_name: str, default: Path) -> Path:
    raw = os.getenv(env_name, "").strip()
    return Path(raw).expanduser().resolve() if raw else default.resolve()


def data_dir() -> Path:
    return _path("APP_DATA_DIR", WORKSPACE_ROOT / "data")


def database_path() -> Path:
    url = os.getenv("APP_DATABASE_URL", "").strip()
    if url.startswith("sqlite:///"):
        return Path(url[len("sqlite:///") :]).expanduser().resolve()
    return data_dir() / "app.db"


def uploads_dir() -> Path:
    return _path("APP_UPLOAD_DIR", WORKSPACE_ROOT / "uploads")


def models_dir() -> Path:
    return _path("APP_MODELS_DIR", WORKSPACE_ROOT / "models")


def ensure_model_dir() -> Path:
    path = models_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_runtime_dirs() -> None:
    for path in (data_dir(), uploads_dir(), models_dir()):
        path.mkdir(parents=True, exist_ok=True)
