"""User settings page state."""
from __future__ import annotations

import asyncio

import reflex as rx

from ml_pipelines._optional import diagnostics

from ..errors import friendly
from ..services import settings_service
from .base import AuthState

THEMES = ["light", "dark", "system"]
CHART_TYPES = ["line", "area", "bar", "histogram"]
LIBRARY_IDS = ["numpy", "pandas", "matplotlib", "seaborn", "sklearn", "torch", "tensorflow"]
PAGE_SIZES = ["5", "10", "20", "50"]
REFRESH_INTERVALS = ["1", "3", "5", "10"]
AVATAR_COLORS = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]


class SettingsState(AuthState):
    profile_name: str = ""
    profile_email: str = ""
    profile_username: str = ""
    profile_role: str = ""
    avatar_color: str = "#4F46E5"

    theme: str = "light"
    default_library: str = "pandas"
    chart_type: str = "line"
    rows_per_page: str = "10"
    live_refresh_seconds: str = "3"
    live_enabled: bool = True
    show_advanced: bool = False

    current_password: str = ""
    new_password: str = ""
    confirm_password: str = ""

    settings_ok: str = ""
    settings_error: str = ""

    # Live environment audit (see ml_pipelines._optional.diagnostics) --------
    # Flattened to a single list because Reflex cannot foreach over an untyped
    # nested key; each item is either a group header or one library row.
    env_rows: list[dict] = []
    env_python: str = ""
    env_version: str = ""
    env_prefix: str = ""
    env_ready: bool = False
    env_fix: str = ""
    env_issue_count: int = 0
    env_busy: bool = False
    env_checked: bool = False

    @rx.event
    def load_settings(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            data = settings_service.get_settings(self.user_id)
        except Exception as exc:
            self.settings_error = friendly(exc)
            return
        self.profile_name = data["full_name"]
        self.profile_email = data["email"]
        self.profile_username = data["username"]
        self.profile_role = data["role"]
        self.avatar_color = data["avatar_color"]
        self.theme = data["theme"]
        self.default_library = data["default_library"]
        self.chart_type = data["chart_type"]
        self.rows_per_page = str(data["rows_per_page"])
        self.live_refresh_seconds = str(data["live_refresh_seconds"])
        self.live_enabled = bool(data["live_enabled"])
        self.show_advanced = bool(data["show_advanced"])
        return SettingsState.check_environment

    @rx.event(background=True)
    async def check_environment(self):
        """Import every dependency for real and record the outcome.

        Metadata-only checks lie: a package can be registered in site-packages
        and still fail to import. This runs in a background event because the
        first import of scipy / sklearn takes a second or two.
        """
        async with self:
            if self.env_busy:
                return
            self.env_busy = True
        try:
            report = await asyncio.to_thread(diagnostics)
        except Exception as exc:  # noqa: BLE001 - never break the page
            async with self:
                self.env_busy = False
                self.settings_error = friendly(exc)
            return
        python = report.get("python", {})
        rows: list[dict] = []
        for group in report.get("groups", []):
            rows.append(
                {
                    "kind": "group",
                    "tier": group.get("tier", ""),
                    "required": bool(group.get("required", False)),
                    "ok": bool(group.get("ok", False)),
                    "label": "",
                    "version": "",
                    "status": "",
                    "error": "",
                    "fix": "",
                }
            )
            for row in group.get("rows", []):
                rows.append(
                    {
                        "kind": "row",
                        "tier": "",
                        "required": False,
                        "ok": False,
                        "label": row.get("label", ""),
                        "version": row.get("version", ""),
                        "status": row.get("status", ""),
                        "error": row.get("error", ""),
                        "fix": row.get("fix", ""),
                    }
                )
        async with self:
            self.env_rows = rows
            self.env_python = str(python.get("executable", ""))
            self.env_version = str(python.get("version", ""))
            self.env_prefix = str(python.get("prefix", ""))
            self.env_ready = bool(report.get("ready", False))
            self.env_fix = str(report.get("fix", ""))
            self.env_issue_count = len(report.get("missing", [])) + len(report.get("broken", []))
            self.env_busy = False
            self.env_checked = True

    @rx.event
    def save_profile(self):
        self.settings_ok, self.settings_error = "", ""
        try:
            data = settings_service.save_profile(
                self.user_id, self.profile_name, self.profile_email, self.avatar_color
            )
            self.full_name = data["full_name"]
            self.email = data["email"]
            self.avatar_color = data["avatar_color"]
            self.settings_ok = "Profile saved."
        except Exception as exc:
            self.settings_error = friendly(exc)

    @rx.event
    def save_preferences(self):
        self.settings_ok, self.settings_error = "", ""
        try:
            settings_service.save_preferences(
                self.user_id,
                theme=self.theme,
                default_library=self.default_library,
                chart_type=self.chart_type,
                rows_per_page=int(self.rows_per_page),
                live_refresh_seconds=int(self.live_refresh_seconds),
                live_enabled=self.live_enabled,
                show_advanced=self.show_advanced,
            )
            self.settings_ok = "Preferences saved. They apply to your next dashboard visit."
        except Exception as exc:
            self.settings_error = friendly(exc)

    @rx.event
    def update_password(self):
        self.settings_ok, self.settings_error = "", ""
        try:
            settings_service.change_password(
                self.user_id, self.current_password, self.new_password, self.confirm_password
            )
            self.current_password = ""
            self.new_password = ""
            self.confirm_password = ""
            self.settings_ok = "Password updated."
        except Exception as exc:
            self.settings_error = friendly(exc)

    # Field setters ---------------------------------------------------------
    @rx.event
    def set_profile_name(self, value: str):
        self.profile_name = value

    @rx.event
    def set_profile_email(self, value: str):
        self.profile_email = value

    @rx.event
    def set_avatar_color(self, value: str):
        self.avatar_color = value

    @rx.event
    def set_theme(self, value: str):
        self.theme = value

    @rx.event
    def set_default_library(self, value: str):
        self.default_library = value

    @rx.event
    def set_chart_type(self, value: str):
        self.chart_type = value

    @rx.event
    def set_rows_per_page(self, value: str):
        self.rows_per_page = value

    @rx.event
    def set_live_refresh_seconds(self, value: str):
        self.live_refresh_seconds = value

    @rx.event
    def set_live_enabled(self, value: bool):
        self.live_enabled = value

    @rx.event
    def set_show_advanced(self, value: bool):
        self.show_advanced = value

    @rx.event
    def set_current_password(self, value: str):
        self.current_password = value

    @rx.event
    def set_new_password(self, value: str):
        self.new_password = value

    @rx.event
    def set_confirm_password(self, value: str):
        self.confirm_password = value
