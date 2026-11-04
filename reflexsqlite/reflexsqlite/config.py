"""Centralized, typed application configuration.

All environment variables are read here and validated once at import time so the
app fails fast on a bad configuration instead of failing deep inside a handler.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _int(name: str, default: int, *, minimum: int = 1) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {raw!r}") from exc
    if value < minimum:
        raise RuntimeError(f"{name} must be >= {minimum}, got {value}")
    return value


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    environment: str
    data_dir: Path
    upload_dir: Path
    database_url: str
    secret_key: str
    session_ttl_hours: int
    max_upload_mb: int
    max_preview_rows: int
    live_refresh_ms: int
    max_training_rows: int
    seed_demo_data: bool

    @property
    def database_path(self) -> Path:
        return self.data_dir / "app.db"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


def _load() -> Settings:
    # Runtime state lives *beside* the app package, never inside it: `reflex run`
    # watches every file under the app root, and SQLite's WAL sidecars
    # (app.db-wal / app.db-shm) change on every write. Keeping them inside the
    # watched tree puts the dev server in an endless worker-reload loop.
    runtime_root = PROJECT_ROOT.parent
    data_dir = Path(os.getenv("APP_DATA_DIR", runtime_root / "data")).resolve()
    upload_dir = Path(os.getenv("APP_UPLOAD_DIR", runtime_root / "uploads")).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    upload_dir.mkdir(parents=True, exist_ok=True)

    environment = os.getenv("APP_ENV", "development").strip().lower()
    secret_key = os.getenv("APP_SECRET_KEY", "")
    if not secret_key:
        if environment == "production":
            raise RuntimeError("APP_SECRET_KEY is required when APP_ENV=production")
        # Stable per-install dev key; override via .env for anything shared.
        secret_key = "dev-only-change-me-4f9b2c7a1e8d"
    if len(secret_key) < 16:
        raise RuntimeError("APP_SECRET_KEY must be at least 16 characters")

    return Settings(
        app_name=os.getenv("APP_NAME", "DataForge"),
        environment=environment,
        data_dir=data_dir,
        upload_dir=upload_dir,
        database_url=os.getenv("APP_DATABASE_URL", f"sqlite:///{data_dir / 'app.db'}"),
        secret_key=secret_key,
        session_ttl_hours=_int("SESSION_TTL_HOURS", 24 * 7),
        max_upload_mb=_int("MAX_UPLOAD_MB", 25),
        max_preview_rows=_int("MAX_PREVIEW_ROWS", 12),
        live_refresh_ms=_int("LIVE_REFRESH_MS", 3000),
        max_training_rows=_int("MAX_TRAINING_ROWS", 400),
        seed_demo_data=_bool("SEED_DEMO_DATA", True),
    )


settings = _load()
