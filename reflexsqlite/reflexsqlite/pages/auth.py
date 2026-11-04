"""Login and registration screens."""
from __future__ import annotations

import reflex as rx

from ..components.theme import (
    BORDER,
    FONT,
    MUTED,
    PRIMARY,
    PRIMARY_SOFT,
    SURFACE,
    TEXT,
)
from ..components.ui import field, notice_banner, primary_button, text_input
from ..state import AuthState

BULLETS = [
    ("SQLite CRUD", "Every uploaded row is editable, searchable and deletable."),
    ("7 Python libraries", "Switch engines without leaving the dashboard."),
    ("Live charts", "Streaming metrics and interactive visualizations."),
]


def _auth_frame(title, subtitle, *form_children, footer):
    return rx.hstack(
        # Left brand panel
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("DF", font_size="13px", font_weight="800", color="white"),
                        background=PRIMARY,
                        border_radius="10px",
                        width="36px",
                        height="36px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text("DataForge", font_size="18px", font_weight="750", color=TEXT),
                    gap="10px",
                    align_items="center",
                ),
                rx.text(
                    "Your data, your libraries,\nyour workspace.",
                    font_size="30px",
                    font_weight="800",
                    color=TEXT,
                    line_height="1.25",
                    white_space="pre-line",
                    margin_top="42px",
                ),
                rx.text(
                    "A local-first analytics studio built with Reflex and SQLite.",
                    font_size="13px",
                    color=MUTED,
                    line_height="1.7",
                    max_width="330px",
                ),
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.box(
                                width="7px",
                                height="7px",
                                min_width="7px",
                                border_radius="999px",
                                background=PRIMARY,
                                margin_top="6px",
                            ),
                            rx.vstack(
                                rx.text(t, font_size="12px", font_weight="700", color=TEXT),
                                rx.text(d, font_size="11px", color=MUTED, line_height="1.5"),
                                gap="2px",
                                align_items="start",
                            ),
                            gap="10px",
                            align_items="start",
                        )
                        for t, d in BULLETS
                    ],
                    gap="16px",
                    margin_top="34px",
                    align_items="start",
                ),
                rx.box(flex="1"),
                rx.text("Reflex 0.10  ·  SQLite  ·  Python 3.13", font_size="10px", color=MUTED),
                gap="0",
                align_items="start",
                height="100%",
                width="100%",
                padding="38px",
            ),
            width="42%",
            min_width="340px",
            height="100vh",
            background=PRIMARY_SOFT,
            border_right=f"1px solid {BORDER}",
            position="relative",
            overflow="hidden",
        ),
        # Right form panel
        rx.vstack(
            rx.box(flex="1"),
            rx.box(
                rx.vstack(
                    rx.text(title, font_size="24px", font_weight="800", color=TEXT),
                    rx.text(subtitle, font_size="12px", color=MUTED, margin_bottom="8px"),
                    *form_children,
                    gap="14px",
                    width="100%",
                    align_items="start",
                ),
                width="100%",
                max_width="400px",
                padding="34px",
                background=SURFACE,
                border=f"1px solid {BORDER}",
                border_radius="18px",
                box_shadow="0 18px 48px rgba(15,23,42,.08)",
            ),
            footer,
            rx.box(flex="1"),
            gap="20px",
            align_items="center",
            width="100%",
            padding="30px",
        ),
        gap="0",
        align_items="start",
        min_height="100vh",
        width="100%",
        background=SURFACE,
        font_family=FONT,
        color=TEXT,
    )


def login_page():
    footer = rx.hstack(
        rx.text("New here?", font_size="12px", color=MUTED),
        rx.link(rx.text("Create an account", font_size="12px", font_weight="650", color=PRIMARY),
                href="/register", text_decoration="none"),
        rx.box(flex="1"),
        rx.link(rx.text("Back to home", font_size="11px", color=MUTED), href="/", text_decoration="none"),
        gap="6px",
        width="100%",
        max_width="400px",
        align_items="center",
    )
    return _auth_frame(
        "Welcome back",
        "Sign in to continue to your workspace.",
        notice_banner(AuthState.auth_error),
        field(
            "Username or email",
            text_input(AuthState.login_name, AuthState.set_login_name, "demo"),
        ),
        field(
            "Password",
            text_input(AuthState.login_password, AuthState.set_login_password, "••••••••", password=True),
        ),
        primary_button(
            "Sign in",
            on_click=AuthState.sign_in,
            width="100%",
            margin_top="4px",
            disabled=AuthState.auth_busy,
        ),
        rx.box(
            rx.text("Demo credentials: demo / demo1234", font_size="11px", color=MUTED, font_family="monospace"),
            background=PRIMARY_SOFT,
            border_radius="8px",
            padding="9px 12px",
            width="100%",
        ),
        footer=footer,
    )


def register_page():
    footer = rx.hstack(
        rx.text("Already have an account?", font_size="12px", color=MUTED),
        rx.link(rx.text("Sign in", font_size="12px", font_weight="650", color=PRIMARY),
                href="/login", text_decoration="none"),
        rx.box(flex="1"),
        rx.link(rx.text("Back to home", font_size="11px", color=MUTED), href="/", text_decoration="none"),
        gap="6px",
        width="100%",
        max_width="400px",
        align_items="center",
    )
    return _auth_frame(
        "Create your workspace",
        "A local account keeps your datasets and preferences together.",
        notice_banner(AuthState.auth_error),
        field("Username", text_input(AuthState.reg_username, AuthState.set_reg_username, "analyst_01")),
        field("Full name", text_input(AuthState.reg_full_name, AuthState.set_reg_full_name, "Optional")),
        field("Email", text_input(AuthState.reg_email, AuthState.set_reg_email, "you@example.com")),
        field("Password", text_input(AuthState.reg_password, AuthState.set_reg_password, "At least 8 characters", password=True)),
        field("Confirm password", text_input(AuthState.reg_confirm, AuthState.set_reg_confirm, "Repeat password", password=True)),
        primary_button("Create account", on_click=AuthState.sign_up, width="100%", margin_top="4px", disabled=AuthState.auth_busy),
        footer=footer,
    )
