"""Predictive analytics page: training, registry, live inference and drift."""
from __future__ import annotations

import reflex as rx

from ..components import charts, ui
from ..components.layout import shell
from ..components.theme import ACCENT, MUTED, PRIMARY, SUCCESS, TEXT, WARNING
from ..state import ModelsState


def _dataset_chip(item):
    return rx.button(
        rx.text(item["name"], font_size="11px", font_weight="600"),
        on_click=ModelsState.select_dataset(item["id"]),
        background=rx.cond(ModelsState.dataset_id == item["id"], PRIMARY, "#FFFFFF"),
        color=rx.cond(ModelsState.dataset_id == item["id"], "white", TEXT),
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


def _training_card():
    return ui.card(
        ui.section_title(
            "Train a model",
            "Queries SQLite, fits a scikit-learn pipeline and saves models/<name>.joblib",
        ),
        rx.hstack(
            rx.foreach(ModelsState.datasets, _dataset_chip),
            gap="8px",
            flex_wrap="wrap",
            margin_top="12px",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Target column",
                    rx.select(
                        ModelsState.target_options,
                        value=ModelsState.target,
                        on_change=ModelsState.set_target,
                        width="200px",
                        size="1",
                    ),
                ),
                width="220px",
            ),
            rx.box(
                ui.field(
                    "Algorithm",
                    rx.select(
                        ["random_forest", "gradient_boosting", "linear", "xgboost", "lightgbm"],
                        value=ModelsState.algorithm,
                        on_change=ModelsState.set_algorithm,
                        width="180px",
                        size="1",
                    ),
                ),
                width="200px",
            ),
            rx.box(
                ui.field(
                    "Task",
                    rx.select(
                        ["auto", "regression", "classification"],
                        value=ModelsState.task,
                        on_change=ModelsState.set_task,
                        width="160px",
                        size="1",
                    ),
                ),
                width="180px",
            ),
            rx.box(
                ui.field(
                    "Model name (optional)",
                    ui.text_input(ModelsState.model_name, ModelsState.set_model_name, "auto-generated"),
                ),
                width="240px",
            ),
            ui.primary_button(
                rx.cond(ModelsState.train_busy, "Training…", "Train model"),
                on_click=ModelsState.train,
                disabled=ModelsState.train_busy,
            ),
            gap="12px",
            align_items="end",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        ui.notice_banner(ModelsState.notice, "success"),
        ui.notice_banner(ModelsState.error),
        width="100%",
        padding="20px",
    )


def _active_card():
    return ui.card(
        rx.hstack(
            rx.vstack(
                rx.text("Active model", font_size="16px", font_weight="700", color=TEXT),
                rx.text(ModelsState.active_label, font_size="12px", color=MUTED),
                gap="2px",
                align_items="start",
            ),
            rx.box(flex="1"),
            ui.ghost_button("Refresh", on_click=ModelsState.refresh_registry),
            align_items="center",
            width="100%",
        ),
        rx.cond(
            ModelsState.has_active,
            rx.vstack(
                _metrics(ModelsState.active_metrics),
                rx.text(
                    "Artifacts loaded once at backend startup; the registry reloads only when a .joblib changes.",
                    font_size="11px",
                    color=MUTED,
                ),
                gap="12px",
                width="100%",
                margin_top="12px",
            ),
            rx.text(
                "No model is active yet. Train one below, or run `python -m ml_pipelines train --dataset-id 1 --target revenue`.",
                font_size="12px",
                color=MUTED,
                margin_top="10px",
            ),
        ),
        width="100%",
        padding="20px",
    )


def _activate_action(item):
    return rx.cond(
        item["active"],
        ui.pill("Active", SUCCESS, "#ECFDF5", "#A7F3D0"),
        ui.ghost_button(
            "Activate",
            on_click=ModelsState.activate(item["name"]),
            padding="5px 9px",
        ),
    )


def _registry_card():
    return ui.card(
        ui.section_title(
            "Model registry",
            "Every trained artifact with its holdout metrics; activate one to serve predictions",
        ),
        rx.box(
            ui.data_table(
                ["name", "task", "algorithm", "target", "training_rows", "updated"],
                ModelsState.models,
                _activate_action,
            ),
            margin_top="12px",
            width="100%",
        ),
        width="100%",
        padding="20px",
    )


def _feature_field(feature):
    return ui.field(
        feature,
        rx.input(
            value=ModelsState.predict_form[feature],
            on_change=lambda value: ModelsState.set_predict_field(feature, value),
            placeholder=f"Value for {feature}",
            width="100%",
            border="1px solid #E5E8F1",
            border_radius="9px",
            padding="9px 11px",
            font_size="12px",
        ),
    )


def _prediction_card():
    return ui.card(
        ui.section_title(
            "Real-time inference",
            "The cached model runs inside the state handler; every call is logged to model_logs",
        ),
        rx.cond(
            ModelsState.has_active,
            rx.vstack(
                rx.hstack(
                    rx.foreach(ModelsState.feature_columns, _feature_field),
                    gap="10px",
                    flex_wrap="wrap",
                    width="100%",
                    margin_top="12px",
                ),
                rx.hstack(
                    ui.primary_button("Predict & log", on_click=ModelsState.predict_now),
                    rx.cond(
                        ModelsState.prediction_label != "",
                        rx.box(
                            rx.text("Prediction", font_size="10px", color=MUTED),
                            rx.text(ModelsState.prediction_label, font_size="18px", font_weight="750", color=PRIMARY),
                            background="#EEF0FF",
                            border_radius="10px",
                            padding="8px 14px",
                        ),
                    ),
                    gap="14px",
                    align_items="center",
                    margin_top="12px",
                    flex_wrap="wrap",
                ),
                gap="6px",
                width="100%",
            ),
            rx.text("Activate a model first to enable inference.", font_size="12px", color=MUTED, margin_top="10px"),
        ),
        width="100%",
        padding="20px",
    )


def _resolve_form():
    return rx.hstack(
        rx.box(
            ui.field(
                "Prediction log",
                rx.select(
                    ModelsState.resolve_options,
                    value=ModelsState.resolve_id,
                    on_change=ModelsState.set_resolve_id,
                    width="160px",
                    size="1",
                ),
            ),
            width="180px",
        ),
        rx.box(
            ui.field(
                "Observed actual",
                ui.text_input(ModelsState.actual_value, ModelsState.set_actual_value, "e.g. 612.5"),
            ),
            width="200px",
        ),
        ui.ghost_button("Record outcome", on_click=ModelsState.resolve_outcome),
        gap="12px",
        align_items="end",
        margin_top="12px",
        flex_wrap="wrap",
    )


def _drift_card():
    return ui.card(
        ui.section_title(
            "Model drift monitoring",
            "Rolling accuracy / MAE over resolved predictions from the model_logs table",
        ),
        _metrics(ModelsState.drift_metrics),
        rx.box(
            charts.multi_line_chart(
                ModelsState.drift_chart,
                [
                    {"key": "accuracy", "label": "Accuracy", "color": SUCCESS},
                    {"key": "mae", "label": "MAE", "color": WARNING},
                ],
            ),
            margin_top="12px",
            width="100%",
        ),
        _resolve_form(),
        rx.box(
            ui.data_table(ModelsState.log_columns, ModelsState.logs),
            margin_top="14px",
            width="100%",
        ),
        width="100%",
        padding="20px",
    )


def models():
    return shell(
        "Predictive Models",
        "Offline training, a joblib model registry, live inference and drift monitoring",
        _training_card(),
        _active_card(),
        _registry_card(),
        _prediction_card(),
        _drift_card(),
    )
