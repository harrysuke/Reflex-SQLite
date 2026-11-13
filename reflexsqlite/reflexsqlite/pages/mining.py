"""Data-mining page: DuckDB OLAP, Polars large files, clustering and association rules."""
from __future__ import annotations

import reflex as rx

from ..components import charts, ui
from ..components.layout import shell
from ..components.theme import ACCENT, MUTED, PRIMARY, SUCCESS, TEXT, WARNING
from ..state import MiningState


def _dataset_chip(item):
    return rx.button(
        rx.text(item["name"], font_size="11px", font_weight="600"),
        on_click=MiningState.select_dataset(item["id"]),
        background=rx.cond(MiningState.dataset_id == item["id"], PRIMARY, "#FFFFFF"),
        color=rx.cond(MiningState.dataset_id == item["id"], "white", TEXT),
        border="1px solid #E5E8F1",
        border_radius="999px",
        padding="6px 12px",
        cursor="pointer",
    )


def _metrics(metrics):
    return rx.hstack(
        rx.foreach(metrics, lambda m: ui.stat_card(m["label"], m["value"], m["hint"])),
        gap="12px",
        flex_wrap="wrap",
        width="100%",
    )


def _table_card(title, subtitle, columns, rows):
    return ui.card(
        ui.section_title(title, subtitle),
        rx.box(ui.data_table(columns, rows), margin_top="12px", width="100%"),
        width="100%",
        padding="20px",
    )


def _dataset_card():
    return ui.card(
        ui.section_title(
            "Choose a dataset",
            "Mining runs directly over the SQLite rows via DuckDB / pandas / scikit-learn",
        ),
        rx.hstack(
            rx.foreach(MiningState.datasets, _dataset_chip),
            gap="8px",
            flex_wrap="wrap",
            margin_top="12px",
        ),
        ui.notice_banner(MiningState.notice, "success"),
        ui.notice_banner(MiningState.error),
        width="100%",
        padding="20px",
    )


def _feature_toggle(feature):
    return rx.hstack(
        rx.checkbox(
            checked=MiningState.cluster_features.contains(feature),
            on_change=lambda _value: MiningState.toggle_feature(feature),
            size="1",
        ),
        rx.text(feature, font_size="11px", color=TEXT),
        gap="6px",
        align_items="center",
        background="#FAFBFE",
        border="1px solid #E5E8F1",
        border_radius="8px",
        padding="5px 9px",
    )


def _clustering_card():
    return ui.card(
        ui.section_title(
            "Clustering",
            "K-Means / HDBSCAN on standardized numeric features to segment rows into behavioural groups",
        ),
        rx.hstack(
            rx.foreach(MiningState.numeric, _feature_toggle),
            gap="6px",
            flex_wrap="wrap",
            margin_top="12px",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Segments (k)",
                    rx.select(
                        ["2", "3", "4", "5", "6"],
                        value=MiningState.cluster_k,
                        on_change=MiningState.set_cluster_k,
                        width="120px",
                        size="1",
                    ),
                ),
                width="140px",
            ),
            rx.box(
                ui.field(
                    "Algorithm",
                    rx.select(
                        ["kmeans", "hdbscan"],
                        value=MiningState.cluster_algorithm,
                        on_change=MiningState.set_cluster_algorithm,
                        width="150px",
                        size="1",
                    ),
                ),
                width="170px",
            ),
            ui.primary_button(
                rx.cond(MiningState.cluster_busy, "Clustering…", "Run clustering"),
                on_click=MiningState.run_cluster,
                disabled=MiningState.cluster_busy,
            ),
            gap="12px",
            align_items="end",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.cond(
            MiningState.has_cluster,
            rx.vstack(
                _metrics(MiningState.cluster_metrics),
                rx.hstack(
                    rx.box(
                        ui.card(
                            ui.section_title("Segment sizes", "Rows per cluster"),
                            rx.box(
                                charts.bar_chart_simple(MiningState.cluster_chart, "Rows", PRIMARY),
                                margin_top="12px",
                            ),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _table_card(
                            "Cluster profiles",
                            "Mean feature values per segment",
                            MiningState.cluster_columns,
                            MiningState.cluster_rows,
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                gap="14px",
                width="100%",
                margin_top="12px",
            ),
            rx.text("Select features and run clustering.", font_size="12px", color=MUTED, margin_top="10px"),
        ),
        width="100%",
        padding="20px",
    )


def _association_card():
    return ui.card(
        ui.section_title(
            "Association rules",
            "mlxtend FP-Growth / Apriori over transactional columns: 'frequently occurring together'",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Transaction column",
                    rx.select(
                        MiningState.columns,
                        value=MiningState.transaction_col,
                        on_change=MiningState.set_transaction_col,
                        width="180px",
                        size="1",
                    ),
                ),
                width="200px",
            ),
            rx.box(
                ui.field(
                    "Item column",
                    rx.select(
                        MiningState.columns,
                        value=MiningState.item_col,
                        on_change=MiningState.set_item_col,
                        width="180px",
                        size="1",
                    ),
                ),
                width="200px",
            ),
            rx.box(
                ui.field(
                    "Algorithm",
                    rx.select(
                        ["fpgrowth", "apriori"],
                        value=MiningState.assoc_algorithm,
                        on_change=MiningState.set_assoc_algorithm,
                        width="150px",
                        size="1",
                    ),
                ),
                width="170px",
            ),
            rx.box(
                ui.field(
                    "Min support",
                    ui.text_input(MiningState.min_support, MiningState.set_min_support, "0.05"),
                ),
                width="120px",
            ),
            ui.primary_button(
                rx.cond(MiningState.assoc_busy, "Mining…", "Find rules"),
                on_click=MiningState.run_assoc,
                disabled=MiningState.assoc_busy,
            ),
            gap="12px",
            align_items="end",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.cond(
            MiningState.has_assoc,
            rx.vstack(
                _metrics(MiningState.assoc_metrics),
                rx.hstack(
                    rx.box(
                        ui.card(
                            ui.section_title("Rule lift", "Top rules by lift"),
                            rx.box(
                                charts.bar_chart_simple(MiningState.assoc_chart, "Lift", ACCENT),
                                margin_top="12px",
                            ),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _table_card(
                            "Association rules",
                            "Antecedent → consequent with support, confidence and lift",
                            MiningState.assoc_columns,
                            MiningState.assoc_rows,
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                gap="14px",
                width="100%",
                margin_top="12px",
            ),
            rx.text(
                "Pick a transaction column and an item column, then mine rules.",
                font_size="12px",
                color=MUTED,
                margin_top="10px",
            ),
        ),
        width="100%",
        padding="20px",
    )


def _olap_card():
    return ui.card(
        ui.section_title(
            "DuckDB OLAP console",
            "ATTACH the live SQLite file and query the rows_flat view with vectorized SQL",
        ),
        rx.box(
            rx.text_area(
                value=MiningState.olap_sql,
                on_change=MiningState.set_olap_sql,
                min_height="120px",
                width="100%",
                font_family="'JetBrains Mono', Consolas, monospace",
                font_size="12px",
                border="1px solid #E5E8F1",
                border_radius="10px",
                padding="12px",
                margin_top="12px",
            ),
            width="100%",
        ),
        rx.hstack(
            ui.primary_button(
                rx.cond(MiningState.olap_busy, "Running…", "Run query"),
                on_click=MiningState.run_olap,
                disabled=MiningState.olap_busy,
            ),
            ui.ghost_button("Reset template", on_click=MiningState.reset_olap_sql),
            rx.cond(
                MiningState.has_olap,
                rx.text(MiningState.olap["engine"], font_size="11px", color=MUTED),
            ),
            gap="10px",
            align_items="center",
            margin_top="10px",
            flex_wrap="wrap",
        ),
        rx.cond(
            MiningState.has_olap,
            rx.vstack(
                rx.box(
                    charts.bar_chart_simple(MiningState.olap_chart, "Result", PRIMARY),
                    margin_top="12px",
                    width="100%",
                ),
                rx.box(
                    ui.data_table(MiningState.olap_columns, MiningState.olap_rows),
                    margin_top="12px",
                    width="100%",
                ),
                gap="6px",
                width="100%",
            ),
        ),
        width="100%",
        padding="20px",
    )


def _large_card():
    return ui.card(
        ui.section_title(
            "Large files (Polars)",
            "Scan uploaded CSVs lazily with streaming aggregation — larger than RAM",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Uploaded file",
                    rx.select(
                        MiningState.upload_options,
                        value=MiningState.upload_file,
                        on_change=MiningState.set_upload_file,
                        width="240px",
                        size="1",
                    ),
                ),
                width="260px",
            ),
            rx.box(
                ui.field(
                    "Group by",
                    ui.text_input(MiningState.group_by, MiningState.set_group_by, "e.g. region"),
                ),
                width="180px",
            ),
            rx.box(
                ui.field(
                    "Value column",
                    ui.text_input(MiningState.value_column, MiningState.set_value_column, "e.g. revenue"),
                ),
                width="180px",
            ),
            rx.box(
                ui.field(
                    "Aggregation",
                    rx.select(
                        ["mean", "sum", "count", "median", "max", "min"],
                        value=MiningState.aggregation,
                        on_change=MiningState.set_aggregation,
                        width="140px",
                        size="1",
                    ),
                ),
                width="160px",
            ),
            ui.primary_button(
                rx.cond(MiningState.large_busy, "Scanning…", "Scan file"),
                on_click=MiningState.run_large,
                disabled=MiningState.large_busy,
            ),
            ui.ghost_button("Refresh list", on_click=MiningState.refresh_uploads),
            gap="12px",
            align_items="end",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.cond(
            MiningState.has_uploads,
            rx.text("", font_size="1px"),
            rx.text(
                "No files in uploads/ yet — import a CSV on the Datasets page first.",
                font_size="12px",
                color=MUTED,
                margin_top="10px",
            ),
        ),
        rx.cond(
            MiningState.has_large,
            rx.vstack(
                _metrics(MiningState.large_metrics),
                rx.hstack(
                    rx.box(
                        ui.card(
                            ui.section_title("Grouped aggregate", "Streaming group-by"),
                            rx.box(
                                charts.bar_chart_simple(MiningState.large_chart, "Value", SUCCESS),
                                margin_top="12px",
                            ),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _table_card(
                            "Aggregation result",
                            "Computed out-of-core by Polars",
                            MiningState.large_columns,
                            MiningState.large_rows,
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                gap="14px",
                width="100%",
                margin_top="12px",
            ),
        ),
        width="100%",
        padding="20px",
    )


def mining():
    return shell(
        "Data Mining",
        "DuckDB OLAP, Polars out-of-core scans, K-Means/HDBSCAN segmentation and association rules",
        ui.notice_banner(MiningState.env_warning, "warning"),
        _dataset_card(),
        _clustering_card(),
        _association_card(),
        _olap_card(),
        _large_card(),
    )
