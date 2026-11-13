"""Model drift / accuracy monitoring over the ``model_logs`` table.

Every CRUD prediction is logged with its input features and predicted value.
When an actual outcome arrives (user feedback or a later measurement) the log is
completed with correctness / absolute error. :func:`drift_summary` turns those
logs into rolling-window accuracy and error series for the UI.
"""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from .preprocessing import float_or_none


def outcome_fields(predicted: Any, actual: Any, task: str) -> dict[str, Any]:
    """Derive correctness / error columns when an actual outcome is recorded."""
    predicted_number = float_or_none(predicted)
    actual_number = float_or_none(actual)
    predicted_text = "" if predicted is None else str(predicted)
    actual_text = "" if actual is None else str(actual)
    is_correct: bool | None = None
    if task == "classification":
        is_correct = predicted_text.strip().lower() == actual_text.strip().lower()
    absolute_error = (
        abs(predicted_number - actual_number)
        if predicted_number is not None and actual_number is not None
        else None
    )
    return {
        "actual_value": actual_text,
        "actual_numeric": actual_number,
        "predicted_numeric": predicted_number if task == "regression" else None,
        "is_correct": is_correct,
        "absolute_error": round(absolute_error, 6) if absolute_error is not None else None,
    }


def drift_summary(logs: Sequence[dict[str, Any]], *, window: int = 10) -> dict[str, Any]:
    """Compute overall + rolling accuracy/MAE from prediction logs.

    ``logs`` must be chronologically ordered (oldest first). Only rows carrying
    an actual outcome contribute to accuracy metrics.
    """
    resolved = [
        log for log in logs
        if str(log.get("actual_value", "")) != ""
    ]
    predicted_total = len(logs)
    resolved_total = len(resolved)
    tasks = {str(log.get("task", "")) for log in resolved}
    classification = "classification" in tasks and "regression" not in tasks

    correct_flags = [
        bool(log["is_correct"])
        for log in resolved
        if log.get("is_correct") is not None
    ]
    errors = [
        float(log["absolute_error"])
        for log in resolved
        if log.get("absolute_error") is not None and np.isfinite(float(log["absolute_error"]))
    ]

    overall_accuracy = round(sum(correct_flags) / len(correct_flags), 4) if correct_flags else None
    overall_mae = round(float(np.mean(errors)), 4) if errors else None

    window = max(2, min(int(window), 50))
    chart: list[dict[str, Any]] = []
    for end in range(window, resolved_total + 1, window):
        chunk = resolved[end - window : end]
        flags = [bool(log["is_correct"]) for log in chunk if log.get("is_correct") is not None]
        chunk_errors = [
            float(log["absolute_error"])
            for log in chunk
            if log.get("absolute_error") is not None
        ]
        point: dict[str, Any] = {"name": f"W{len(chart) + 1}"}
        if flags:
            point["accuracy"] = round(sum(flags) / len(flags), 4)
        if chunk_errors:
            point["mae"] = round(float(np.mean(chunk_errors)), 4)
        if len(point) > 1:
            chart.append(point)
    if resolved_total % window and resolved_total > 0:
        tail = resolved[resolved_total - (resolved_total % window) :]
        flags = [bool(log["is_correct"]) for log in tail if log.get("is_correct") is not None]
        chunk_errors = [float(log["absolute_error"]) for log in tail if log.get("absolute_error") is not None]
        point = {"name": f"W{len(chart) + 1}"}
        if flags:
            point["accuracy"] = round(sum(flags) / len(flags), 4)
        if chunk_errors:
            point["mae"] = round(float(np.mean(chunk_errors)), 4)
        if len(point) > 1:
            chart.append(point)

    coverage = round(100 * resolved_total / predicted_total, 1) if predicted_total else 0.0
    metrics = [
        {"label": "Predictions", "value": predicted_total, "hint": "Total inference calls logged"},
        {"label": "With outcome", "value": resolved_total, "hint": f"{coverage}% feedback coverage"},
        {"label": "Accuracy", "value": overall_accuracy, "hint": "Classification correctness"},
        {"label": "MAE", "value": overall_mae, "hint": "Mean absolute error"},
    ]
    if classification and chart:
        first = chart[0].get("accuracy")
        last = chart[-1].get("accuracy")
        drift = None if first is None or last is None else round(last - first, 4)
    elif chart:
        first = chart[0].get("mae")
        last = chart[-1].get("mae")
        drift = None if first is None or last is None else round(last - first, 4)
    else:
        drift = None
    return {
        "metrics": metrics,
        "chart": chart,
        "chart_label": "accuracy" if classification else "mae",
        "window": window,
        "coverage": coverage,
        "drift": drift,
        "notes": [
            "Every CRUD create/update writes a model_logs row with a timestamp, input features and prediction.",
            "Record an actual outcome to compute rolling accuracy / error and detect drift.",
            f"Rolling windows contain up to {window} resolved predictions.",
        ],
    }
