"""Application shell: sidebar with library picker, top navbar and page wrapper."""
from __future__ import annotations

import reflex as rx

from ..analytics import registry
from ..state import AuthState, ExploreState
from .theme import (
    ACCENT,
    BG,
    BORDER,
    FAINT,
    FONT,
    MUTED,
    PRIMARY,
    PRIMARY_SOFT,
    SIDEBAR_WIDTH,
    SUCCESS,
    SURFACE,
    SURFACE_ALT,
    TEXT,
)
from .ui import ghost_button

LIBRARY_CARDS = registry.catalog()
CATEGORIES = list(registry.CATEGORIES)

NAV_ITEMS = [
    ("/dashboard", "Dashboard", "DB"),
    ("/datasets", "Datasets", "DS"),
    ("/explore", "Library Workbench", "LB"),
    ("/settings", "Settings", "ST"),
]


def _brand():
    return rx.hstack(
        rx.box(
            rx.text("DF", font_size="13px", font_weight="800", color="white", letter_spacing="0.5px"),
            background=PRIMARY,
            border_radius="10px",
            width="36px",
            height="36px",
            min_width="36px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.vstack(
            rx.text("DataForge", font_size="15px", font_weight="750", color=TEXT, line_height="1.1"),
            rx.text("Reflex · SQLite Workspace", font_size="10px", color=MUTED),
            gap="2px",
            align_items="start",
        ),
        gap="10px",
        align_items="center",
        padding="20px 18px 18px 18px",
        width="100%",
    )


def _nav_item(href, label, badge):
    return rx.link(
        rx.hstack(
            rx.box(
                rx.text(badge, font_size="9px", font_weight="800", color=PRIMARY),
                background=PRIMARY_SOFT,
                border_radius="6px",
                width="26px",
                height="26px",
                min_width="26px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.text(label, font_size="13px", font_weight="550", color=TEXT),
            gap="10px",
            align_items="center",
            padding="8px 10px",
            border_radius="9px",
            _hover={"background": SURFACE_ALT},
            width="100%",
        ),
        href=href,
        text_decoration="none",
        width="100%",
    )


def _library_card(item):
    """A sidebar entry that selects a Python library and opens the workbench."""
    available = bool(item["available"])
    return rx.button(
        rx.hstack(
            rx.box(
                rx.text(item["badge"], font_size="9px", font_weight="800", color="white"),
                background=item["color"] if available else "#CBD5E1",
                border_radius="7px",
                width="28px",
                height="28px",
                min_width="28px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(item["name"], font_size="12px", font_weight="650", color=TEXT, line_height="1.2"),
                rx.text(
                    f"v{item['version']}" if available else "not installed",
                    font_size="9px",
                    color=MUTED if available else FAINT,
                ),
                gap="1px",
                align_items="start",
                overflow="hidden",
            ),
            rx.box(
                width="7px",
                height="7px",
                min_width="7px",
                border_radius="999px",
                background=SUCCESS if available else "#CBD5E1",
            ),
            gap="8px",
            align_items="center",
            width="100%",
        ),
        on_click=ExploreState.choose_library(item["id"]),
        background=SURFACE_ALT if available else SURFACE,
        border="1px solid transparent",
        border_radius="9px",
        padding="7px 9px",
        cursor="pointer",
        width="100%",
        text_align="left",
        _hover={"border": f"1px solid {BORDER}", "background": SURFACE},
    )


def _library_sections():
    sections = []
    for category in CATEGORIES:
        items = [item for item in LIBRARY_CARDS if item["category"] == category]
        sections.append(
            rx.vstack(
                rx.text(category.upper(), font_size="9px", font_weight="700", color=FAINT, letter_spacing="0.8px"),
                *[_library_card(item) for item in items],
                gap="5px",
                align_items="start",
                width="100%",
                margin_top="10px",
            )
        )
    return rx.vstack(*sections, gap="4px", width="100%")


def sidebar():
    return rx.box(
        rx.vstack(
            _brand(),
            rx.vstack(
                *[_nav_item(*item) for item in NAV_ITEMS],
                gap="2px",
                width="100%",
                padding="0 12px",
            ),
            rx.box(
                rx.hstack(
                    rx.text("PYTHON LIBRARIES", font_size="9px", font_weight="700", color=FAINT, letter_spacing="0.8px"),
                    rx.box(flex="1"),
                    rx.text(f"{sum(1 for i in LIBRARY_CARDS if i['available'])}/{len(LIBRARY_CARDS)}", font_size="9px", color=MUTED),
                    width="100%",
                ),
                padding="18px 18px 4px 18px",
                width="100%",
                border_top=f"1px solid {BORDER}",
                margin_top="14px",
            ),
            rx.box(
                _library_sections(),
                padding="0 12px 20px 12px",
                width="100%",
            ),
            gap="0",
            align_items="start",
            width="100%",
        ),
        width=SIDEBAR_WIDTH,
        min_width=SIDEBAR_WIDTH,
        height="100vh",
        position="sticky",
        top="0",
        background=SURFACE,
        border_right=f"1px solid {BORDER}",
        overflow_y="auto",
        font_family=FONT,
    )


def navbar(title, subtitle=""):
    left = [rx.text(title, font_size="18px", font_weight="750", color=TEXT, line_height="1.2")]
    if subtitle:
        left.append(rx.text(subtitle, font_size="11px", color=MUTED))
    return rx.hstack(
        rx.vstack(
            *left,
            gap="2px",
            align_items="start",
        ),
        rx.box(flex="1"),
        rx.hstack(
            rx.box(
                rx.text(AuthState.initials, font_size="11px", font_weight="750", color="white"),
                background=AuthState.avatar_color,
                border_radius="999px",
                width="32px",
                height="32px",
                min_width="32px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(AuthState.display_name, font_size="12px", font_weight="650", color=TEXT, line_height="1.1"),
                rx.text(AuthState.role, font_size="10px", color=MUTED),
                gap="1px",
                align_items="start",
            ),
            ghost_button("Sign out", on_click=AuthState.sign_out),
            gap="10px",
            align_items="center",
        ),
        padding="16px 28px",
        background=SURFACE,
        border_bottom=f"1px solid {BORDER}",
        width="100%",
        min_height="72px",
        align_items="center",
        position="sticky",
        top="0",
        z_index="10",
    )


def shell(title, subtitle, *children):
    return rx.hstack(
        sidebar(),
        rx.vstack(
            navbar(title, subtitle),
            rx.box(
                rx.vstack(*children, gap="18px", width="100%", align_items="start"),
                padding="26px 28px 48px 28px",
                width="100%",
                overflow_y="auto",
            ),
            gap="0",
            align_items="start",
            width="100%",
            min_width="0",
        ),
        gap="0",
        align_items="start",
        min_height="100vh",
        width="100%",
        background=BG,
        font_family=FONT,
        color=TEXT,
    )
