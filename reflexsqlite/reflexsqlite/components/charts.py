"""Interactive Recharts wrappers for dashboards and analysis results."""
from __future__ import annotations

import reflex as rx

from .theme import ACCENT, BORDER, MUTED, PRIMARY

# The tooltip component was renamed in newer Reflex releases; support both.
_TOOLTIP = getattr(rx.recharts, "graphing_tooltip", None) or getattr(rx.recharts, "tooltip", None)
_LEGEND = getattr(rx.recharts, "legend", None)


def _common():
    children = [
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#EEF1F7", vertical=False),
        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False, height=28),
        rx.recharts.y_axis(axis_line=False, tick_line=False, width=52),
    ]
    if _TOOLTIP is not None:
        children.append(
            _TOOLTIP(
                content_style={
                    "backgroundColor": "#FFFFFF",
                    "border": "1px solid #E5E8F1",
                    "borderRadius": "10px",
                    "fontSize": "12px",
                    "boxShadow": "0 8px 20px rgba(15,23,42,.08)",
                }
            )
        )
    if _LEGEND is not None:
        children.append(_LEGEND(icon_type="circle", wrapper_style={"fontSize": "11px"}))
    return children


def _base(data, height: int):
    return {
        "data": data,
        "height": height,
        "width": "100%",
        "margin": {"top": 10, "right": 16, "left": 4, "bottom": 6},
    }


def interactive_chart(
    data,
    chart_type,
    color: str = PRIMARY,
    label: str = "Value",
    secondary=False,
    secondary_label: str = "",
    height: int = 300,
):
    """Switch between line / area / bar with hover tooltips and live state data."""
    common = _common()

    line_chart = rx.recharts.line_chart(
        *common,
        rx.recharts.line(
            data_key="value", name=label, stroke=color, stroke_width=3,
            dot=False, type_="monotone", is_animation_active=False,
        ),
        rx.cond(
            secondary,
            rx.recharts.line(
                data_key="extra", name=secondary_label, stroke=ACCENT, stroke_width=2,
                dot=False, type_="monotone", stroke_dasharray="5 4", is_animation_active=False,
            ),
        ),
        **_base(data, height),
    )
    area_chart = rx.recharts.area_chart(
        *common,
        rx.recharts.area(
            data_key="value", name=label, stroke=color, fill=color,
            fill_opacity=0.16, stroke_width=2, type_="monotone", is_animation_active=False,
        ),
        **_base(data, height),
    )
    bar_chart = rx.recharts.bar_chart(
        *common,
        rx.recharts.bar(data_key="value", name=label, fill=color, radius=[5, 5, 0, 0], is_animation_active=False),
        **_base(data, height),
    )
    return rx.cond(
        chart_type == "area",
        area_chart,
        rx.cond(
            chart_type == "bar",
            bar_chart,
            rx.cond(chart_type == "histogram", bar_chart, line_chart),
        ),
    )


def live_chart(data, height: int = 190, color: str = ACCENT):
    """Streaming sparkline fed by the background live_loop task."""
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#EEF1F7", vertical=False),
        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False, height=22),
        rx.recharts.y_axis(axis_line=False, tick_line=False, width=44, domain=["auto", "auto"]),
        *([_TOOLTIP(content_style={"fontSize": "11px", "borderRadius": "8px"})] if _TOOLTIP else []),
        rx.recharts.area(
            data_key="value", name="Live", stroke=color, fill=color,
            fill_opacity=0.18, stroke_width=2.4, type_="monotone", is_animation_active=False,
        ),
        **_base(data, height),
    )


def result_chart(data, color: str = PRIMARY, label: str = "Value", secondary=False, secondary_label: str = "", height: int = 260):
    """Chart shown in the library workbench result panel."""
    common = [
        rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="#EEF1F7", vertical=False),
        rx.recharts.x_axis(data_key="name", axis_line=False, tick_line=False, height=28),
        rx.recharts.y_axis(axis_line=False, tick_line=False, width=52),
    ]
    if _TOOLTIP is not None:
        common.append(_TOOLTIP(content_style={"fontSize": "11px", "borderRadius": "8px"}))
    # A ComposedChart accepts both Bar and Line children; BarChart rejects Line.
    return rx.recharts.composed_chart(
        *common,
        rx.recharts.bar(data_key="value", name=label, fill=color, radius=[4, 4, 0, 0], is_animation_active=False),
        rx.cond(
            secondary,
            rx.recharts.line(
                data_key="extra", name=secondary_label, stroke=ACCENT,
                stroke_width=2, dot=False, is_animation_active=False,
            ),
        ),
        **_base(data, height),
    )


def correlation_grid(labels, rows):
    """Compact correlation matrix; each cell has a hover title."""
    def cell(item):
        return rx.box(
            rx.text(item["v"], font_size="10px", font_weight="600", color="#1E293B"),
            title=item["tip"],
            background=item["color"],
            border="1px solid #FFFFFF",
            border_radius="5px",
            width="64px",
            min_width="64px",
            height="28px",
            display="flex",
            align_items="center",
            justify_content="center",
            cursor="help",
        )

    def header_cell(label):
        return rx.box(
            rx.text(label, font_size="9px", color=MUTED, white_space="nowrap"),
            width="64px",
            min_width="64px",
            height="24px",
            display="flex",
            align_items="center",
            justify_content="center",
            overflow="hidden",
        )

    def matrix_row(row):
        return rx.hstack(
            rx.box(
                rx.text(row["label"], font_size="9px", color=MUTED, font_weight="600"),
                width="88px",
                min_width="88px",
                height="28px",
                display="flex",
                align_items="center",
            ),
            rx.foreach(row["cells"], cell),
            gap="2px",
            align_items="center",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(width="88px", min_width="88px"),
                rx.foreach(labels, header_cell),
                gap="2px",
            ),
            rx.foreach(rows, matrix_row),
            gap="2px",
            align_items="start",
        ),
        width="100%",
        overflow_x="auto",
        border=f"1px solid {BORDER}",
        border_radius="10px",
        padding="10px",
        background="#FFFFFF",
    )
