"""SQLite table definitions (SQLModel / SQLAlchemy).

Timestamps are stored as UTC ISO-8601 strings: they sort lexicographically in
SQLite and avoid the timezone-aware/naive datetime incompatibility introduced
in recent SQLModel releases.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return utcnow().isoformat(timespec="seconds")


def display_time(value: str) -> str:
    """'2026-11-04T06:12:00+00:00' -> '2026-11-04 06:12'."""
    return (value or "")[:16].replace("T", " ")


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(default="", max_length=64)
    email: str = Field(default="", max_length=255)
    full_name: str = Field(default="")
    password_hash: str = Field(default="")
    role: str = Field(default="analyst")
    is_active: bool = Field(default=True)
    avatar_color: str = Field(default="#4F46E5")
    created_at: str = Field(default_factory=now_iso)


class UserSetting(SQLModel, table=True):
    __tablename__ = "user_settings"
    __table_args__ = (UniqueConstraint("user_id", name="uq_settings_user"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    theme: str = Field(default="light")
    default_library: str = Field(default="pandas")
    chart_type: str = Field(default="line")
    rows_per_page: int = Field(default=10)
    live_refresh_seconds: int = Field(default=3)
    live_enabled: bool = Field(default=True)
    show_advanced: bool = Field(default=False)
    updated_at: str = Field(default_factory=now_iso)


class AuthSession(SQLModel, table=True):
    __tablename__ = "auth_sessions"

    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(index=True)
    user_id: int = Field(index=True)
    created_at: str = Field(default_factory=now_iso)
    expires_at: str = Field(default="")


class Dataset(SQLModel, table=True):
    __tablename__ = "datasets"

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(index=True)
    name: str = Field(default="Untitled dataset")
    filename: str = Field(default="")
    file_format: str = Field(default="csv")
    description: str = Field(default="")
    size_bytes: int = Field(default=0)
    row_count: int = Field(default=0)
    column_count: int = Field(default=0)
    # JSON-encoded list of column names, split by inferred type.
    columns_json: str = Field(default="[]")
    numeric_columns_json: str = Field(default="[]")
    categorical_columns_json: str = Field(default="[]")
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)

    @staticmethod
    def decode(raw: str) -> list[str]:
        try:
            value = json.loads(raw or "[]")
            return [str(v) for v in value] if isinstance(value, list) else []
        except (ValueError, TypeError):
            return []

    @property
    def columns(self) -> list[str]:
        return self.decode(self.columns_json)

    @property
    def numeric_columns(self) -> list[str]:
        return self.decode(self.numeric_columns_json)

    @property
    def categorical_columns(self) -> list[str]:
        return self.decode(self.categorical_columns_json)


class DatasetRow(SQLModel, table=True):
    """One source row, stored as JSON text so arbitrary schemas are supported."""
    __tablename__ = "dataset_rows"
    __table_args__ = (UniqueConstraint("dataset_id", "row_index", name="uq_row_position"),)

    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(index=True)
    row_index: int = Field(default=0)
    payload: str = Field(default="{}")
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)

    def as_dict(self) -> dict[str, Any]:
        try:
            value = json.loads(self.payload or "{}")
            return value if isinstance(value, dict) else {}
        except (ValueError, TypeError):
            return {}


class ActivityLog(SQLModel, table=True):
    __tablename__ = "activity_logs"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    dataset_id: int | None = Field(default=None, index=True)
    action: str = Field(default="")
    detail: str = Field(default="")
    created_at: str = Field(default_factory=now_iso)


class MetricPoint(SQLModel, table=True):
    """Time-series samples backing the live dashboard chart."""
    __tablename__ = "metric_points"

    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(index=True)
    series: str = Field(default="value", max_length=64)
    value: float = Field(default=0.0)
    label: str = Field(default="", max_length=32)
    created_at: str = Field(default_factory=now_iso)
