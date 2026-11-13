"""User settings page."""
from __future__ import annotations

import reflex as rx

from ..analytics import registry
from ..components import ui
from ..components.layout import shell
from ..components.theme import BORDER, FAINT, MUTED, PRIMARY, SURFACE, SURFACE_ALT, TEXT
from ..config import settings as app_settings
from ..state import AuthState, SettingsState

LIBRARY_IDS = [spec.id for spec in registry.LIBRARIES]
LIBRARY_NAMES = [spec.name for spec in registry.LIBRARIES]
AVATAR_COLORS = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]


def _profile_card():
    swatches = rx.hstack(
        *[
            rx.button(
                width="26px",
                height="26px",
                min_width="26px",
                border_radius="999px",
                background=color,
                border="2px solid #FFFFFF",
                box_shadow="0 0 0 1px #E5E8F1",
                cursor="pointer",
                on_click=SettingsState.set_avatar_color(color),
            )
            for color in AVATAR_COLORS
        ],
        gap="8px",
        align_items="center",
    )
    return ui.card(
        ui.section_title("Profile", "How you appear across the workspace"),
        rx.hstack(
            rx.box(
                rx.text(AuthState.initials, font_size="16px", font_weight="800", color="white"),
                background=SettingsState.avatar_color,
                border_radius="14px",
                width="52px",
                height="52px",
                min_width="52px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(SettingsState.profile_username, font_size="13px", font_weight="700", color=TEXT),
                rx.text(SettingsState.profile_role, font_size="11px", color=MUTED),
                gap="2px",
                align_items="start",
            ),
            gap="12px",
            align_items="center",
            margin_top="14px",
            width="100%",
        ),
        rx.hstack(
            ui.field("Full name", ui.text_input(SettingsState.profile_name, SettingsState.set_profile_name, "Your name")),
            ui.field("Email", ui.text_input(SettingsState.profile_email, SettingsState.set_profile_email, "you@example.com")),
            gap="14px",
            width="100%",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        rx.text("Avatar color", font_size="11px", color=MUTED, margin_top="14px"),
        rx.box(swatches, margin_top="6px"),
        rx.box(ui.primary_button("Save profile", on_click=SettingsState.save_profile), margin_top="18px"),
        padding="20px",
        width="calc(50% - 8px)",
        min_width="340px",
    )


def _preferences_card():
    return ui.card(
        ui.section_title("Dashboard preferences", "Applied when you open the dashboard"),
        rx.hstack(
            ui.field(
                "Theme",
                rx.select(["light", "dark", "system"], value=SettingsState.theme,
                          on_change=SettingsState.set_theme, width="100%", size="1"),
            ),
            ui.field(
                "Default library",
                rx.select(LIBRARY_IDS, value=SettingsState.default_library,
                          on_change=SettingsState.set_default_library, width="100%", size="1"),
            ),
            gap="14px",
            width="100%",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        rx.hstack(
            ui.field(
                "Default chart",
                rx.select(["line", "area", "bar", "histogram"], value=SettingsState.chart_type,
                          on_change=SettingsState.set_chart_type, width="100%", size="1"),
            ),
            ui.field(
                "Rows per page",
                rx.select(["5", "10", "20", "50"], value=SettingsState.rows_per_page,
                          on_change=SettingsState.set_rows_per_page, width="100%", size="1"),
            ),
            gap="14px",
            width="100%",
            margin_top="4px",
            flex_wrap="wrap",
        ),
        ui.field(
            "Live refresh interval (seconds)",
            rx.select(["1", "3", "5", "10"], value=SettingsState.live_refresh_seconds,
                      on_change=SettingsState.set_live_refresh_seconds, width="160px", size="1"),
        ),
        rx.hstack(
            rx.text("Enable live feed", font_size="12px", color=TEXT),
            rx.switch(checked=SettingsState.live_enabled, on_change=SettingsState.set_live_enabled),
            rx.box(width="24px"),
            rx.text("Show advanced options", font_size="12px", color=TEXT),
            rx.switch(checked=SettingsState.show_advanced, on_change=SettingsState.set_show_advanced),
            gap="10px",
            align_items="center",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.box(ui.primary_button("Save preferences", on_click=SettingsState.save_preferences), margin_top="18px"),
        padding="20px",
        width="calc(50% - 8px)",
        min_width="340px",
    )


def _security_card():
    return ui.card(
        ui.section_title("Security", "Passwords are hashed with PBKDF2-HMAC-SHA256"),
        rx.hstack(
            ui.field("Current password", ui.text_input(SettingsState.current_password,
                     SettingsState.set_current_password, "••••••••", password=True)),
            ui.field("New password", ui.text_input(SettingsState.new_password,
                     SettingsState.set_new_password, "At least 8 characters", password=True)),
            ui.field("Confirm new password", ui.text_input(SettingsState.confirm_password,
                     SettingsState.set_confirm_password, "Repeat new password", password=True)),
            gap="14px",
            width="100%",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        rx.box(ui.primary_button("Update password", on_click=SettingsState.update_password), margin_top="18px"),
        padding="20px",
        width="calc(60% - 8px)",
        min_width="340px",
    )


def _environment_card():
    entries = [
        ("Database", str(app_settings.database_path)),
        ("Uploads", str(app_settings.upload_dir)),
        ("Environment", app_settings.environment),
        ("Max upload", f"{app_settings.max_upload_mb} MB"),
        ("Training cap", f"{app_settings.max_training_rows} rows"),
    ]
    return ui.card(
        ui.section_title("Environment", "Local-first: everything stays on this machine"),
        rx.vstack(
            *[
                rx.hstack(
                    rx.text(key, font_size="11px", color=MUTED, width="120px", min_width="120px"),
                    rx.text(value, font_size="11px", color=TEXT, font_family="monospace", overflow="hidden"),
                    width="100%",
                    padding_y="5px",
                    border_bottom=f"1px solid {BORDER}",
                )
                for key, value in entries
            ],
            gap="0",
            width="100%",
            margin_top="10px",
        ),
        rx.text("Dependency status", font_size="11px", color=MUTED, margin_top="16px"),
        rx.hstack(
            rx.cond(
                SettingsState.env_ready,
                ui.pill("all required libraries ready", "#047857", "#ECFDF5", "#A7F3D0"),
                ui.pill(
                    SettingsState.env_issue_count.to_string() + " issue(s) - see the audit below",
                    "#B45309",
                    "#FFFBEB",
                    "#FDE68A",
                ),
            ),
            gap="6px",
            flex_wrap="wrap",
            margin_top="8px",
        ),
        padding="20px",
        width="calc(40% - 8px)",
        min_width="300px",
    )


def _dep_row(row):
    """One library: real import status, the error, and the exact fix."""
    return rx.vstack(
        rx.hstack(
            rx.box(
                width="8px",
                height="8px",
                min_width="8px",
                border_radius="999px",
                background=rx.cond(
                    row["status"] == "ok",
                    "#10B981",
                    rx.cond(row["status"] == "broken", "#F59E0B", "#EF4444"),
                ),
            ),
            rx.text(
                row["label"],
                font_size="12px",
                font_weight="600",
                color=TEXT,
                width="140px",
                min_width="140px",
            ),
            rx.text(
                row["version"],
                font_size="11px",
                color=MUTED,
                font_family="monospace",
                width="90px",
                min_width="90px",
            ),
            rx.text(row["status"], font_size="11px", color=MUTED),
            gap="10px",
            align_items="center",
            width="100%",
        ),
        rx.cond(
            row["error"] != "",
            rx.text(
                row["error"],
                font_size="11px",
                color="#B91C1C",
                margin_left="18px",
                font_family="monospace",
            ),
        ),
        rx.cond(
            row["fix"] != "",
            rx.hstack(
                rx.text("Fix", font_size="10px", font_weight="700", color=MUTED),
                rx.text(row["fix"], font_size="11px", color=PRIMARY, font_family="monospace"),
                gap="6px",
                align_items="center",
                margin_left="18px",
                flex_wrap="wrap",
            ),
        ),
        gap="3px",
        align_items="start",
        width="100%",
        padding_y="6px",
        border_bottom=f"1px solid {BORDER}",
    )


def _dep_header(item):
    return rx.hstack(
        rx.text(item["tier"], font_size="11px", font_weight="700", color=TEXT),
        rx.cond(
            item["required"],
            ui.pill("required", "#4F46E5", "#EEF2FF", "#C7D2FE"),
            ui.pill("optional", MUTED, SURFACE_ALT, BORDER),
        ),
        gap="8px",
        align_items="center",
        width="100%",
        margin_top="16px",
    )


def _dep_line(item):
    """One rendered line: a tier header or a single library row."""
    return rx.cond(item["kind"] == "group", _dep_header(item), _dep_row(item))


def _dependency_card():
    return ui.card(
        ui.section_title(
            "Dependency audit",
            "Every library is imported for real in the interpreter running the backend",
            action=ui.ghost_button(
                rx.cond(SettingsState.env_busy, "Checking…", "Re-check"),
                on_click=SettingsState.check_environment,
            ),
        ),
        rx.hstack(
            rx.text("Interpreter", font_size="11px", color=MUTED, width="96px", min_width="96px"),
            rx.text(
                SettingsState.env_python,
                font_size="11px",
                color=TEXT,
                font_family="monospace",
            ),
            rx.text(SettingsState.env_version, font_size="11px", color=MUTED),
            gap="8px",
            align_items="center",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.box(
            rx.cond(
                SettingsState.env_ready,
                rx.text(
                    "All required libraries import correctly.",
                    font_size="12px",
                    font_weight="600",
                    color="#047857",
                ),
                rx.text(
                    SettingsState.env_issue_count,
                    " required libraries cannot be imported by this interpreter.",
                    font_size="12px",
                    font_weight="600",
                    color="#B91C1C",
                ),
            ),
            margin_top="10px",
        ),
        rx.foreach(SettingsState.env_rows, _dep_line),
        rx.cond(
            SettingsState.env_fix != "",
            rx.box(
                rx.text(
                    "Install every requirement for this interpreter, then restart the app:",
                    font_size="11px",
                    color=MUTED,
                ),
                rx.text(
                    SettingsState.env_fix,
                    font_size="11px",
                    color=TEXT,
                    font_family="monospace",
                    margin_top="4px",
                ),
                background=SURFACE_ALT,
                border=f"1px solid {BORDER}",
                border_radius="9px",
                padding="10px 12px",
                margin_top="14px",
                width="100%",
            ),
        ),
        rx.cond(
            SettingsState.env_checked,
            rx.fragment(),
            rx.text("Importing libraries…", font_size="11px", color=FAINT, margin_top="12px"),
        ),
        padding="20px",
        width="100%",
    )


def settings_page():
    return shell(
        "Settings",
        "Profile, dashboard preferences and account security",
        ui.notice_banner(SettingsState.settings_ok, "success"),
        ui.notice_banner(SettingsState.settings_error),
        rx.hstack(
            _profile_card(),
            _preferences_card(),
            gap="16px",
            width="100%",
            flex_wrap="wrap",
            align_items="stretch",
        ),
        rx.hstack(
            _security_card(),
            _environment_card(),
            gap="16px",
            width="100%",
            flex_wrap="wrap",
            align_items="stretch",
        ),
        _dependency_card(),
    )
