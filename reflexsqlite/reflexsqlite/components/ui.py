"""Small reusable presentational helpers built on stable Reflex primitives.

Python-level decisions (optional subtitle, optional action, optional hint) are
made in Python; only runtime state is handled with rx.cond / rx.foreach.
"""
from __future__ import annotations

import reflex as rx

from .theme import (
    BORDER,
    DANGER,
    FAINT,
    MUTED,
    PRIMARY,
    PRIMARY_SOFT,
    SURFACE,
    SURFACE_ALT,
    TEXT,
)


def card(*children, padding: str = "20px", **overrides):
    style = {
        "background": SURFACE,
        "border": f"1px solid {BORDER}",
        "border_radius": "14px",
        "box_shadow": "0 1px 2px rgba(16,24,40,.04), 0 8px 24px rgba(16,24,40,.05)",
        "padding": padding,
    }
    style.update(overrides)
    return rx.box(*children, **style)


def pill(text, color: str = MUTED, bg: str = SURFACE_ALT, border: str = BORDER):
    return rx.box(
        rx.text(text, font_size="11px", font_weight="600", color=color),
        background=bg,
        border=f"1px solid {border}",
        border_radius="999px",
        padding="3px 10px",
        white_space="nowrap",
    )


def section_title(title, subtitle="", action=None):
    # Always render the subtitle node: an empty Var/str is visually a no-op and
    # avoids Python truthiness checks on Reflex Vars at render time.
    left_children = [
        rx.text(title, font_size="16px", font_weight="700", color=TEXT),
        rx.text(subtitle, font_size="12px", color=MUTED),
    ]
    children = [rx.vstack(*left_children, gap="3px", align_items="start")]
    if action is not None:
        children.append(action)
    return rx.hstack(*children, justify="between", align_items="center", width="100%")


def primary_button(label, on_click=None, **props):
    style = dict(
        background=PRIMARY,
        color="white",
        border_radius="9px",
        padding="9px 16px",
        font_size="13px",
        font_weight="600",
        cursor="pointer",
        _hover={"background": "#4338CA"},
    )
    style.update(props)
    return rx.button(label, on_click=on_click, **style)


def ghost_button(label, on_click=None, **props):
    style = dict(
        background=SURFACE,
        color=TEXT,
        border=f"1px solid {BORDER}",
        border_radius="9px",
        padding="9px 14px",
        font_size="13px",
        font_weight="500",
        cursor="pointer",
        _hover={"background": SURFACE_ALT},
    )
    style.update(props)
    return rx.button(label, on_click=on_click, **style)


def danger_button(label, on_click=None, **props):
    style = dict(
        background="#FEF2F2",
        color=DANGER,
        border="1px solid #FECACA",
        border_radius="9px",
        padding="8px 13px",
        font_size="12px",
        font_weight="600",
        cursor="pointer",
    )
    style.update(props)
    return rx.button(label, on_click=on_click, **style)


def field(label, input_component, hint=""):
    return rx.vstack(
        rx.text(label, font_size="12px", font_weight="600", color=TEXT),
        input_component,
        rx.text(hint, font_size="11px", color=FAINT),
        gap="6px",
        align_items="start",
        width="100%",
    )


def text_input(value, on_change, placeholder="", password: bool = False):
    return rx.input(
        value=value,
        on_change=on_change,
        placeholder=placeholder,
        type="password" if password else "text",
        width="100%",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="9px",
        padding="10px 12px",
        font_size="13px",
        color=TEXT,
    )


def stat_card(label, value, hint="", color: str = PRIMARY, icon_text=""):
    return card(
        rx.hstack(
            rx.box(
                rx.text(icon_text, font_size="11px", font_weight="800", color="white"),
                background=color,
                border_radius="9px",
                width="32px",
                height="32px",
                min_width="32px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.text(label, font_size="11px", color=MUTED, font_weight="600"),
                rx.text(value, font_size="22px", font_weight="750", color=TEXT, line_height="1.1"),
                gap="2px",
                align_items="start",
            ),
            gap="12px",
            align_items="center",
        ),
        rx.text(hint, font_size="11px", color=FAINT, margin_top="8px"),
        padding="18px",
    )


def notice_banner(message, kind: str = "error"):
    is_error = kind == "error"
    return rx.cond(
        message != "",
        rx.box(
            rx.text(message, font_size="12px", font_weight="500"),
            background="#FEF2F2" if is_error else "#ECFDF5",
            color=DANGER if is_error else "#047857",
            border=f"1px solid {'#FECACA' if is_error else '#A7F3D0'}",
            border_radius="10px",
            padding="10px 14px",
            width="100%",
        ),
    )


def empty_state(title, subtitle, action=None):
    children = [
        rx.box(
            rx.text("∅", font_size="26px", color=PRIMARY),
            background=PRIMARY_SOFT,
            border_radius="14px",
            width="54px",
            height="54px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.text(title, font_size="16px", font_weight="700", color=TEXT),
        rx.text(subtitle, font_size="12px", color=MUTED, text_align="center", max_width="380px"),
    ]
    if action is not None:
        children.append(action)
    return card(
        rx.vstack(*children, gap="10px", align_items="center", padding_y="12px"),
        padding="32px",
    )


def modal(title, *children, width: str = "520px"):
    """Conditional full-screen overlay; no dependency on a dialog primitive."""
    return rx.box(
        rx.box(
            rx.vstack(
                rx.text(title, font_size="16px", font_weight="700", color=TEXT),
                rx.vstack(*children, gap="12px", width="100%", margin_top="8px"),
                gap="4px",
                width="100%",
            ),
            background=SURFACE,
            border=f"1px solid {BORDER}",
            border_radius="16px",
            box_shadow="0 24px 64px rgba(15,23,42,.22)",
            padding="24px",
            width=width,
            max_width="94vw",
            max_height="88vh",
            overflow_y="auto",
        ),
        position="fixed",
        top="0",
        left="0",
        right="0",
        bottom="0",
        background="rgba(15,23,42,.42)",
        display="flex",
        align_items="center",
        justify_content="center",
        z_index="50",
    )


def data_table(columns, rows, render_actions=None, max_height: str = "420px"):
    """A scrollable table built from box/text primitives only."""
    # `columns` is a Reflex state Var, so both the header and the cells must be
    # produced with rx.foreach (a Python `for` over a Var raises VarTypeError).
    def header_cell(col):
        return rx.box(
            rx.text(col, font_size="11px", font_weight="700", color=MUTED, white_space="nowrap"),
            min_width="128px",
            flex="1",
            padding="10px 8px",
        )

    header_cells = [
        rx.box(
            rx.text("#", font_size="11px", font_weight="700", color=MUTED),
            width="48px",
            min_width="48px",
            padding="10px 8px",
        ),
        rx.foreach(columns, header_cell),
    ]
    if render_actions is not None:
        header_cells.append(rx.box(width="118px", min_width="118px"))

    def row_cells(item):
        def value_cell(col):
            return rx.box(
                rx.text(item[col], font_size="12px", color=TEXT, white_space="nowrap"),
                min_width="128px",
                flex="1",
                padding="10px 8px",
                overflow="hidden",
            )

        cells = [
            rx.box(
                rx.text(item["_index"], font_size="11px", color=FAINT),
                width="48px",
                min_width="48px",
                padding="10px 8px",
            ),
            rx.foreach(columns, value_cell),
        ]
        if render_actions is not None:
            cells.append(
                rx.box(
                    render_actions(item),
                    width="118px",
                    min_width="118px",
                    padding="8px",
                )
            )
        return rx.hstack(
            *cells,
            border_bottom=f"1px solid {BORDER}",
            gap="0",
            _hover={"background": SURFACE_ALT},
            align_items="center",
        )

    return rx.box(
        rx.hstack(
            *header_cells,
            background=SURFACE_ALT,
            border_bottom=f"1px solid {BORDER}",
            gap="0",
            position="sticky",
            top="0",
            z_index="1",
        ),
        rx.foreach(rows, row_cells),
        border=f"1px solid {BORDER}",
        border_radius="10px",
        overflow="auto",
        max_height=max_height,
        width="100%",
        background=SURFACE,
    )
