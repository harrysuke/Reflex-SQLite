"""Library workbench: run a selected Python library on a dataset."""
from __future__ import annotations

import reflex as rx

from ..components import charts, ui
from ..components.layout import shell
from ..components.theme import BORDER, FAINT, MUTED, PRIMARY, PRIMARY_SOFT, SURFACE_ALT, TEXT
from ..state import ExploreState


def _library_header():
    return ui.card(
        rx.hstack(
            rx.box(
                rx.text("PY", font_size="13px", font_weight="800", color="white"),
                background=ExploreState.active_library_color,
                border_radius="12px",
                width="46px",
                height="46px",
                min_width="46px",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(ExploreState.active_library_name, font_size="20px", font_weight="750", color=TEXT),
                    ui.pill(ExploreState.library_version, PRIMARY, PRIMARY_SOFT, "#DDD6FE"),
                    gap="10px",
                    align_items="center",
                ),
                rx.text(ExploreState.active_op_description, font_size="11px", color=MUTED),
                gap="4px",
                align_items="start",
            ),
            rx.box(flex="1"),
            rx.cond(
                ExploreState.library_available,
                ui.pill("INSTALLED", "#047857", "#ECFDF5", "#A7F3D0"),
                ui.pill("NOT INSTALLED", "#B45309", "#FFFBEB", "#FDE68A"),
            ),
            gap="14px",
            align_items="center",
            width="100%",
            flex_wrap="wrap",
        ),
        padding="18px 20px",
        width="100%",
    )


def _operation_button(op):
    return rx.button(
        rx.vstack(
            rx.text(op["label"], font_size="12px", font_weight="650", color=TEXT),
            rx.text(op["description"], font_size="10px", color=MUTED, text_align="left", line_height="1.4"),
            gap="3px",
            align_items="start",
            width="100%",
        ),
        on_click=ExploreState.select_operation(op["id"]),
        background=SURFACE_ALT,
        border="1px solid #E5E8F1",
        border_radius="10px",
        padding="11px 13px",
        width="100%",
        cursor="pointer",
        text_align="left",
        _hover={"border": "1px solid #C7D2FE"},
    )


def _dataset_chip(item):
    return rx.button(
        rx.text(item["name"], font_size="11px", font_weight="600", color=TEXT),
        on_click=ExploreState.select_dataset(item["id"]),
        background=SURFACE_ALT,
        border="1px solid #E5E8F1",
        border_radius="8px",
        padding="7px 11px",
        cursor="pointer",
    )


def _config_panel():
    return ui.card(
        ui.section_title("Operations", "Choose what this library should compute"),
        rx.box(
            rx.foreach(ExploreState.operations, _operation_button),
            display="grid",
            grid_template_columns="repeat(auto-fit, minmax(180px, 1fr))",
            gap="8px",
            width="100%",
            margin_top="12px",
        ),
        rx.text("DATASET", font_size="10px", font_weight="700", color=FAINT, letter_spacing="0.8px", margin_top="18px"),
        rx.hstack(
            rx.foreach(ExploreState.datasets, _dataset_chip),
            gap="8px",
            flex_wrap="wrap",
            margin_top="8px",
            width="100%",
        ),
        rx.hstack(
            rx.vstack(
                rx.text("X / category column", font_size="10px", color=MUTED),
                rx.select(
                    ExploreState.x_options,
                    value=ExploreState.x_column,
                    on_change=ExploreState.set_x_column,
                    width="180px",
                    size="1",
                ),
                gap="4px",
                align_items="start",
            ),
            rx.vstack(
                rx.text("Y / target column", font_size="10px", color=MUTED),
                rx.select(
                    ExploreState.y_options,
                    value=ExploreState.y_column,
                    on_change=ExploreState.set_y_column,
                    width="180px",
                    size="1",
                ),
                gap="4px",
                align_items="start",
            ),
            rx.box(flex="1"),
            ui.primary_button(
                "Run analysis",
                on_click=ExploreState.run_analysis,
                disabled=ExploreState.is_running,
                margin_top="14px",
            ),
            gap="12px",
            align_items="end",
            flex_wrap="wrap",
            width="100%",
            margin_top="14px",
        ),
        ui.notice_banner(ExploreState.explore_error),
        padding="20px",
        width="100%",
    )


def _metrics():
    def metric(item):
        return ui.card(
            rx.vstack(
                rx.text(item["label"], font_size="10px", color=MUTED, font_weight="600"),
                rx.text(item["value"], font_size="18px", font_weight="750", color=TEXT),
                rx.text(item["hint"], font_size="9px", color=FAINT),
                gap="3px",
                align_items="start",
            ),
            padding="14px",
            min_width="130px",
        )

    return rx.hstack(
        rx.foreach(ExploreState.result_metrics, metric),
        gap="10px",
        flex_wrap="wrap",
        width="100%",
    )


def _result_table():
    def header_cell(col):
        return rx.box(
            rx.text(col, font_size="10px", font_weight="700", color=MUTED, white_space="nowrap"),
            min_width="110px",
            flex="1",
            padding="9px 8px",
        )

    def body_row(row):
        return rx.hstack(
            rx.foreach(
                ExploreState.result_table_columns,
                lambda col: rx.box(
                    rx.text(row[col], font_size="11px", color=TEXT, white_space="nowrap"),
                    min_width="110px",
                    flex="1",
                    padding="8px",
                    overflow="hidden",
                ),
            ),
            border_bottom=f"1px solid {BORDER}",
            gap="0",
            _hover={"background": SURFACE_ALT},
        )

    return rx.box(
        rx.hstack(
            rx.foreach(ExploreState.result_table_columns, header_cell),
            background=SURFACE_ALT,
            border_bottom=f"1px solid {BORDER}",
            gap="0",
        ),
        rx.foreach(ExploreState.result_table_rows, body_row),
        border=f"1px solid {BORDER}",
        border_radius="10px",
        overflow="auto",
        max_height="320px",
        width="100%",
    )


def _results():
    return ui.card(
        ui.section_title(
            "Results",
            ExploreState.result_summary,
            ui.pill(ExploreState.result_library, PRIMARY, PRIMARY_SOFT, "#DDD6FE"),
        ),
        rx.text(ExploreState.result_title, font_size="14px", font_weight="700", color=TEXT, margin_top="10px"),
        _metrics(),
        rx.cond(
            ExploreState.result_image != "",
            rx.box(
                rx.image(src=ExploreState.result_image, width="100%", border_radius="10px", alt="Library figure"),
                border=f"1px solid {BORDER}",
                border_radius="10px",
                padding="8px",
                margin_top="14px",
                width="100%",
            ),
        ),
        rx.cond(
            ExploreState.has_result_chart,
            rx.box(
                charts.result_chart(
                    ExploreState.result_chart,
                    color=ExploreState.result_color,
                    label=ExploreState.result_chart_label,
                    secondary=ExploreState.result_secondary,
                    secondary_label=ExploreState.result_secondary_label,
                ),
                margin_top="14px",
                width="100%",
            ),
        ),
        rx.box(_result_table(), margin_top="14px", width="100%"),
        rx.vstack(
            rx.foreach(
                ExploreState.result_notes,
                lambda note: rx.text(note, font_size="10px", color=MUTED),
            ),
            gap="3px",
            align_items="start",
            margin_top="12px",
        ),
        rx.text(
            ExploreState.result_elapsed_label,
            font_size="9px",
            color=FAINT,
            margin_top="8px",
        ),
        padding="20px",
        width="100%",
    )


def _empty_results():
    return ui.empty_state(
        "Ready when you are",
        "Select an operation above and press Run analysis. The chosen library executes server-side on rows read from SQLite.",
    )


def explore():
    return shell(
        "Library Workbench",
        "Pick a Python engine from the sidebar and run it against your data",
        _library_header(),
        _config_panel(),
        rx.cond(ExploreState.has_result, _results(), _empty_results()),
    )
