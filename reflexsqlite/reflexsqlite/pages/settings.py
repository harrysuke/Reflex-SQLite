"""User settings page."""
from __future__ import annotations

import reflex as rx

from ..analytics import registry
from ..components import ui
from ..components.layout import shell
from ..components.theme import BORDER, FAINT, MUTED, PRIMARY, SURFACE, TEXT
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
        rx.text("Installed libraries", font_size="11px", color=MUTED, margin_top="16px"),
        rx.hstack(
            *[
                ui.pill(
                    spec.name,
                    "#047857" if registry.is_available(spec.id) else "#B45309",
                    "#ECFDF5" if registry.is_available(spec.id) else "#FFFBEB",
                    "#A7F3D0" if registry.is_available(spec.id) else "#FDE68A",
                )
                for spec in registry.LIBRARIES
            ],
            gap="6px",
            flex_wrap="wrap",
            margin_top="8px",
        ),
        padding="20px",
        width="calc(40% - 8px)",
        min_width="300px",
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
    )
