"""Public landing page."""
from __future__ import annotations

import reflex as rx

from ..analytics import registry
from ..components.theme import (
    ACCENT,
    BG,
    BORDER,
    FONT,
    MUTED,
    PRIMARY,
    PRIMARY_SOFT,
    SUCCESS,
    SURFACE,
    TEXT,
)
from ..components.ui import card, pill

LIBS = registry.catalog()

FEATURES = [
    ("01", "Upload & persist", "CSV, TSV, JSON and Excel files land in SQLite with row-level create, read, update and delete."),
    ("02", "Pick your engine", "NumPy, Pandas, Matplotlib, Seaborn, scikit-learn, PyTorch and TensorFlow are one click away in the sidebar."),
    ("03", "Live dashboards", "Interactive Recharts visuals, streaming samples and correlation matrices refresh as your data changes."),
    ("04", "Your workspace", "Accounts, sessions, preferences and activity history are stored locally - no external service needed."),
]


def _gradient_orb(size: str, color: str, top: str, right: str, blur: str = "60px"):
    return rx.box(
        width=size,
        height=size,
        min_width=size,
        border_radius="999px",
        background=color,
        filter=f"blur({blur})",
        opacity="0.5",
        position="absolute",
        top=top,
        right=right,
        z_index="0",
    )


def _feature(item):
    number, title, body = item
    return card(
        rx.vstack(
            rx.text(number, font_size="11px", font_weight="800", color=PRIMARY, font_family="monospace"),
            rx.text(title, font_size="15px", font_weight="700", color=TEXT),
            rx.text(body, font_size="12px", color=MUTED, line_height="1.65"),
            gap="8px",
            align_items="start",
        ),
        padding="22px",
    )


def _library_chip(item):
    return rx.hstack(
        rx.box(
            rx.text(item["badge"], font_size="9px", font_weight="800", color="white"),
            background=item["color"] if item["available"] else "#CBD5E1",
            border_radius="6px",
            width="26px",
            height="26px",
            min_width="26px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.vstack(
            rx.text(item["name"], font_size="12px", font_weight="650", color=TEXT),
            rx.text(item["category"], font_size="10px", color=MUTED),
            gap="1px",
            align_items="start",
        ),
        rx.box(flex="1"),
        rx.box(
            width="7px",
            height="7px",
            min_width="7px",
            border_radius="999px",
            background=SUCCESS if item["available"] else "#CBD5E1",
        ),
        gap="10px",
        align_items="center",
        border=f"1px solid {BORDER}",
        border_radius="10px",
        padding="10px 12px",
        background=SURFACE,
        width="220px",
    )


def landing():
    return rx.box(
        # Top navigation ---------------------------------------------------
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.text("DF", font_size="12px", font_weight="800", color="white"),
                    background=PRIMARY,
                    border_radius="9px",
                    width="32px",
                    height="32px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.text("DataForge", font_size="16px", font_weight="750", color=TEXT),
                gap="10px",
                align_items="center",
            ),
            rx.box(flex="1"),
            rx.link(
                rx.text("Sign in", font_size="13px", font_weight="600", color=MUTED),
                href="/login",
                text_decoration="none",
                padding="8px 12px",
            ),
            rx.link(
                rx.box(
                    rx.text("Get started", font_size="13px", font_weight="650", color="white"),
                    background=PRIMARY,
                    border_radius="9px",
                    padding="9px 16px",
                ),
                href="/register",
                text_decoration="none",
            ),
            gap="10px",
            align_items="center",
            padding="18px 5vw",
            width="100%",
            border_bottom=f"1px solid {BORDER}",
            background=SURFACE,
        ),
        # Hero --------------------------------------------------------------
        rx.box(
            _gradient_orb("320px", "#C7D2FE", "40px", "8%"),
            _gradient_orb("240px", "#BAE6FD", "180px", "24%", "50px"),
            rx.vstack(
                pill("REFLEX  ·  SQLITE  ·  PYTHON DATA STACK", PRIMARY, PRIMARY_SOFT, "#DDD6FE"),
                rx.heading(
                    "One workspace for every",
                    size="8",
                    color=TEXT,
                    font_weight="800",
                    line_height="1.08",
                    text_align="center",
                ),
                rx.heading(
                    "dataset and every library",
                    size="8",
                    color=PRIMARY,
                    font_weight="800",
                    line_height="1.08",
                    text_align="center",
                ),
                rx.text(
                    "Upload a dataset, store it in SQLite, then run NumPy, Pandas, Matplotlib, Seaborn, "
                    "scikit-learn, PyTorch or TensorFlow on it - all from an interactive dashboard.",
                    font_size="15px",
                    color=MUTED,
                    text_align="center",
                    max_width="640px",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.link(
                        rx.box(
                            rx.text("Create free account", font_size="13px", font_weight="650", color="white"),
                            background=PRIMARY,
                            border_radius="10px",
                            padding="12px 22px",
                            box_shadow="0 12px 28px rgba(79,70,229,.25)",
                        ),
                        href="/register",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.box(
                            rx.text("Open dashboard", font_size="13px", font_weight="650", color=TEXT),
                            background=SURFACE,
                            border=f"1px solid {BORDER}",
                            border_radius="10px",
                            padding="12px 22px",
                        ),
                        href="/dashboard",
                        text_decoration="none",
                    ),
                    gap="12px",
                    justify="center",
                    margin_top="10px",
                ),
                rx.text(
                    "Demo account: demo / demo1234",
                    font_size="11px",
                    color=MUTED,
                    font_family="monospace",
                    margin_top="6px",
                ),
                gap="18px",
                align_items="center",
                padding="90px 5vw 80px 5vw",
                position="relative",
                z_index="1",
                width="100%",
            ),
            position="relative",
            overflow="hidden",
            width="100%",
            background=BG,
        ),
        # Feature grid ------------------------------------------------------
        rx.vstack(
            rx.text("BUILT FOR THE WHOLE DATA LIFECYCLE", font_size="10px", font_weight="700", color=PRIMARY, letter_spacing="1px"),
            rx.text("From raw file to trained model", font_size="26px", font_weight="750", color=TEXT),
            rx.box(
                rx.hstack(
                    *[_feature(item) for item in FEATURES],
                    gap="16px",
                    width="100%",
                    align_items="stretch",
                    flex_wrap="wrap",
                    justify="center",
                ),
                width="100%",
                max_width="1180px",
            ),
            gap="12px",
            align_items="center",
            padding="70px 5vw",
            width="100%",
            background=SURFACE,
            border_top=f"1px solid {BORDER}",
            border_bottom=f"1px solid {BORDER}",
        ),
        # Libraries ---------------------------------------------------------
        rx.vstack(
            rx.text("EVERY LIBRARY, ONE SIDEBAR", font_size="10px", font_weight="700", color=ACCENT, letter_spacing="1px"),
            rx.text("Choose the engine that fits the question", font_size="24px", font_weight="750", color=TEXT),
            rx.text(
                "Select any library in the sidebar to switch the workbench. Optional deep-learning "
                "runtimes are detected at startup and show an install hint when absent.",
                font_size="12px",
                color=MUTED,
                text_align="center",
                max_width="600px",
            ),
            rx.hstack(
                *[_library_chip(item) for item in LIBS],
                gap="12px",
                flex_wrap="wrap",
                justify="center",
                width="100%",
                max_width="1120px",
                margin_top="16px",
            ),
            gap="10px",
            align_items="center",
            padding="70px 5vw 90px 5vw",
            width="100%",
        ),
        rx.hstack(
            rx.text("DataForge · Reflex + SQLite", font_size="11px", color=MUTED),
            rx.box(flex="1"),
            rx.link(rx.text("Sign in", font_size="11px", color=MUTED), href="/login", text_decoration="none"),
            rx.link(rx.text("Register", font_size="11px", color=MUTED), href="/register", text_decoration="none"),
            gap="16px",
            width="100%",
            padding="22px 5vw",
            border_top=f"1px solid {BORDER}",
            background=SURFACE,
        ),
        background=BG,
        min_height="100vh",
        width="100%",
        font_family=FONT,
        color=TEXT,
    )
