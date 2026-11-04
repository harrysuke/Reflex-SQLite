"""Interactive data dashboard with live visualizations."""
from __future__ import annotations

import reflex as rx

from ..components import charts, ui
from ..components.layout import shell
from ..components.theme import ACCENT, FAINT, MUTED, PRIMARY, SUCCESS, SURFACE_ALT, TEXT
from ..state import DashboardState


def _dataset_chip(item):
    return rx.button(
        rx.hstack(
            rx.box(
                width="6px",
                height="6px",
                min_width="6px",
                border_radius="999px",
                background=PRIMARY,
            ),
            rx.vstack(
                rx.text(item["name"], font_size="11px", font_weight="650", color=TEXT),
                rx.text(f"{item['rows']} rows · {item['columns']} cols", font_size="9px", color=MUTED),
                gap="1px",
                align_items="start",
            ),
            gap="8px",
            align_items="center",
        ),
        on_click=DashboardState.select_dataset(item["id"]),
        background=SURFACE_ALT,
        border="1px solid #E5E8F1",
        border_radius="9px",
        padding="8px 12px",
        cursor="pointer",
        _hover={"border": "1px solid #C7D2FE"},
    )


def _controls():
    return ui.card(
        rx.vstack(
            rx.hstack(
                rx.text("DATASETS", font_size="10px", font_weight="700", color=FAINT, letter_spacing="0.8px"),
                rx.box(flex="1"),
                rx.link(
                    rx.text("Manage datasets", font_size="11px", font_weight="600", color=PRIMARY),
                    href="/datasets",
                    text_decoration="none",
                ),
                width="100%",
                align_items="center",
            ),
            rx.hstack(
                rx.foreach(DashboardState.datasets, _dataset_chip),
                gap="8px",
                flex_wrap="wrap",
                width="100%",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("Chart type", font_size="10px", color=MUTED),
                    rx.select(
                        ["line", "area", "bar", "histogram"],
                        value=DashboardState.chart_type,
                        on_change=DashboardState.set_chart_type,
                        width="150px",
                        size="1",
                    ),
                    gap="4px",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("X / category", font_size="10px", color=MUTED),
                    rx.select(
                        DashboardState.x_options,
                        value=DashboardState.x_column,
                        on_change=DashboardState.set_x_column,
                        width="150px",
                        size="1",
                    ),
                    gap="4px",
                    align_items="start",
                ),
                rx.vstack(
                    rx.text("Y / metric", font_size="10px", color=MUTED),
                    rx.select(
                        DashboardState.y_options,
                        value=DashboardState.y_column,
                        on_change=DashboardState.set_y_column,
                        width="150px",
                        size="1",
                    ),
                    gap="4px",
                    align_items="start",
                ),
                rx.box(flex="1"),
                rx.vstack(
                    rx.text("Live feed", font_size="10px", color=MUTED),
                    rx.hstack(
                        rx.switch(
                            checked=DashboardState.live_enabled,
                            on_change=DashboardState.toggle_live,
                        ),
                        rx.text(DashboardState.tick, font_size="10px", color=FAINT),
                        gap="6px",
                        align_items="center",
                    ),
                    gap="4px",
                    align_items="start",
                ),
                ui.ghost_button("Refresh", on_click=DashboardState.refresh_dashboard),
                gap="12px",
                align_items="end",
                width="100%",
                flex_wrap="wrap",
                margin_top="8px",
            ),
            gap="10px",
            width="100%",
        ),
        padding="18px",
    )


def _kpis():
    return rx.hstack(
        ui.stat_card("DATASETS", DashboardState.kpi_datasets, "Stored in SQLite", PRIMARY, "DB"),
        ui.stat_card("ROWS", DashboardState.kpi_rows, "Across active dataset", ACCENT, "RW"),
        ui.stat_card("COLUMNS", DashboardState.kpi_columns, "Inferred schema", "#10B981", "CL"),
        ui.stat_card("COMPLETENESS", DashboardState.kpi_completeness,
                     DashboardState.missing_hint, "#F59E0B", "QA"),
        gap="14px",
        width="100%",
        flex_wrap="wrap",
    )


def _main_chart():
    return ui.card(
        ui.section_title(
            "Interactive analysis",
            DashboardState.chart_subtitle,
            ui.pill("RECHARTS", PRIMARY, "#EEF0FF", "#DDD6FE"),
        ),
        rx.box(
            charts.interactive_chart(
                DashboardState.chart_data,
                DashboardState.chart_type,
                color=PRIMARY,
                label=DashboardState.y_column,
                height=300,
            ),
            margin_top="12px",
            width="100%",
        ),
        padding="20px",
        width="calc(66% - 8px)",
        min_width="440px",
    )


def _live_panel():
    return ui.card(
        ui.section_title(
            "Live stream",
            "New samples every few seconds",
            ui.pill("LIVE", SUCCESS, "#ECFDF5", "#A7F3D0"),
        ),
        rx.box(
            charts.live_chart(DashboardState.live_data, height=190),
            margin_top="14px",
            width="100%",
        ),
        rx.hstack(
            rx.text("Samples", font_size="11px", color=MUTED),
            rx.box(flex="1"),
            rx.text(DashboardState.tick, font_size="11px", font_weight="700", color=TEXT),
            width="100%",
            margin_top="10px",
        ),
        rx.text(
            "Toggle the switch above to pause or resume the background stream.",
            font_size="10px",
            color=FAINT,
            margin_top="8px",
        ),
        padding="20px",
        width="calc(34% - 8px)",
        min_width="300px",
    )


def _correlation_panel():
    return ui.card(
        ui.section_title("Correlation matrix", "Pearson coefficients between numeric columns"),
        rx.box(
            charts.correlation_grid(DashboardState.corr_labels, DashboardState.corr_rows),
            margin_top="14px",
            width="100%",
        ),
        padding="20px",
        width="calc(60% - 8px)",
        min_width="420px",
    )


def _activity_panel():
    def line(item):
        return rx.hstack(
            rx.box(
                width="7px",
                height="7px",
                min_width="7px",
                border_radius="999px",
                background=PRIMARY,
                margin_top="5px",
            ),
            rx.vstack(
                rx.text(item["detail"], font_size="11px", font_weight="600", color=TEXT),
                rx.text(f"{item['action']} · {item['time']}", font_size="10px", color=MUTED),
                gap="1px",
                align_items="start",
            ),
            gap="10px",
            align_items="start",
            padding_y="6px",
            border_bottom="1px solid #F1F3F9",
            width="100%",
        )

    return ui.card(
        ui.section_title("Recent activity", "Audit trail from SQLite"),
        rx.box(
            rx.foreach(DashboardState.activity, line),
            margin_top="10px",
            width="100%",
        ),
        padding="20px",
        width="calc(40% - 8px)",
        min_width="300px",
    )


def dashboard():
    return shell(
        "Dashboard",
        "Interactive charts and live data visualizations",
        ui.notice_banner(DashboardState.dashboard_error),
        _controls(),
        _kpis(),
        rx.hstack(
            _main_chart(),
            _live_panel(),
            gap="16px",
            width="100%",
            flex_wrap="wrap",
            align_items="stretch",
        ),
        rx.hstack(
            _correlation_panel(),
            _activity_panel(),
            gap="16px",
            width="100%",
            flex_wrap="wrap",
            align_items="stretch",
        ),
    )
