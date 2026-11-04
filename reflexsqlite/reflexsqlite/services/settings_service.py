"""User settings service: persisted preferences, profile and password changes."""
from __future__ import annotations

from typing import Any

from .. import repositories as repo
from ..db import session_scope
from ..errors import NotFoundError
from . import auth_service


def get_settings(user_id: int) -> dict[str, Any]:
    with session_scope() as session:
        user = repo.get_user(session, user_id)
        if user is None:
            raise NotFoundError("User not found.")
        record = repo.get_or_create_settings(session, user_id)
        return {
            "full_name": user.full_name,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "avatar_color": user.avatar_color,
            "theme": record.theme,
            "default_library": record.default_library,
            "chart_type": record.chart_type,
            "rows_per_page": record.rows_per_page,
            "live_refresh_seconds": record.live_refresh_seconds,
            "live_enabled": record.live_enabled,
            "show_advanced": record.show_advanced,
        }


def save_profile(user_id: int, full_name: str, email: str, avatar_color: str) -> dict[str, Any]:
    with session_scope() as session:
        user = repo.get_user(session, user_id)
        if user is None:
            raise NotFoundError("User not found.")
        auth_service.update_profile(
            session, user, full_name=full_name, email=email, avatar_color=avatar_color
        )
        repo.add_activity(session, user_id, "settings", "Updated profile details")
    return {"full_name": full_name, "email": email, "avatar_color": avatar_color}


def save_preferences(user_id: int, **fields: Any) -> None:
    allowed = {
        "theme", "default_library", "chart_type", "rows_per_page",
        "live_refresh_seconds", "live_enabled", "show_advanced",
    }
    with session_scope() as session:
        record = repo.get_or_create_settings(session, user_id)
        for key, value in fields.items():
            if key in allowed:
                setattr(record, key, value)
        repo.save_settings(session, record)
        repo.add_activity(session, user_id, "settings", "Saved dashboard preferences")


def change_password(user_id: int, current: str, new: str, confirm: str) -> None:
    with session_scope() as session:
        user = repo.get_user(session, user_id)
        if user is None:
            raise NotFoundError("User not found.")
        auth_service.change_password(session, user, current, new, confirm)
        repo.add_activity(session, user_id, "security", "Password changed")
