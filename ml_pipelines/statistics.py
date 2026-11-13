"""Automated statistical profiling with scipy.stats.

Produces a fully JSON-serializable report (no numpy scalars, no DataFrames) that
the Reflex state can hand directly to ``rx.recharts`` and a table component:

* descriptive statistics per numeric column,
* Shapiro-Wilk normality tests (p-value + normal/reject verdict),
* Pearson correlation matrix with per-pair p-values,
* independent t-tests / Welch t-tests and one-way ANOVA across category groups,
* one-sample t-tests against zero when no grouping column is available.
"""
from __future__ import annotations

import warnings
from typing import Any, Sequence

import numpy as np

from ._optional import require
from .preprocessing import clean_frame, float_or_none, json_safe, numeric_columns

MAX_NORMALITY_ROWS = 5000  # SciPy documents Shapiro-Wilk for 3 <= n <= 5000
MAX_NUMERIC = 8
MAX_CATEGORICAL = 3
MAX_TESTS = 40


def _finite(values) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    return array[np.isfinite(array)]


def _r(value: Any, digits: int = 4) -> float | None:
    number = float_or_none(value)
    return None if number is None else round(number, digits)


def _descriptives(frame, numeric: Sequence[str], n_rows: int) -> tuple[list[str], list[dict], list[dict]]:
    columns = ["Column", "N", "Missing", "Mean", "Std", "Min", "Q1", "Median", "Q3", "Max", "Skew", "Kurtosis"]
    rows: list[dict] = []
    missing_chart: list[dict] = []
    stats = require("scipy.stats")
    for column in numeric:
        series = frame[column]
        values = _finite(series)
        missing = int(series.isna().sum())
        if values.size:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                skew = float(stats.skew(values, bias=False)) if values.size > 2 else 0.0
                kurt = float(stats.kurtosis(values, bias=False)) if values.size > 3 else 0.0
            q1, median, q3 = np.percentile(values, [25, 50, 75])
            row = [
                column, int(values.size), missing, float(values.mean()),
                float(values.std(ddof=1)) if values.size > 1 else 0.0,
                float(values.min()), float(q1), float(median), float(q3), float(values.max()),
                skew, kurt,
            ]
        else:
            row = [column, 0, missing] + [None] * 9
        rows.append({key: json_safe(value) for key, value in zip(columns, row)})
        missing_chart.append({"name": str(column)[:18], "value": missing})
    return columns, rows, missing_chart


def _normality(frame, numeric: Sequence[str], alpha: float) -> tuple[list[str], list[dict], list[dict]]:
    stats = require("scipy.stats")
    columns = ["Column", "N tested", "Shapiro W", "p-value", "Verdict (α=%.2f)" % alpha]
    rows: list[dict] = []
    chart: list[dict] = []
    rng = np.random.default_rng(42)
    for column in numeric:
        values = _finite(frame[column])
        if values.size > MAX_NORMALITY_ROWS:
            values = rng.choice(values, size=MAX_NORMALITY_ROWS, replace=False)
        w = p = None
        verdict = "insufficient data"
        if 3 <= values.size <= MAX_NORMALITY_ROWS and np.ptp(values) > 0:
            try:
                result = stats.shapiro(values)
                w, p = float(result.statistic), float(result.pvalue)
                verdict = "normal (fail to reject H₀)" if p >= alpha else "not normal (reject H₀)"
            except Exception as exc:  # pragma: no cover - defensive
                verdict = f"test unavailable: {type(exc).__name__}"
        rows.append({
            "Column": column,
            "N tested": int(values.size),
            "Shapiro W": _r(w),
            "p-value": _r(p, 6),
            "Verdict (α=%.2f)" % alpha: verdict,
        })
        chart.append({
            "name": str(column)[:18],
            "value": round(float(p), 4) if p is not None else 0.0,
            "alpha": alpha,
        })
    return columns, rows, chart


def _correlations(frame, numeric: Sequence[str]) -> dict[str, Any]:
    stats = require("scipy.stats")
    labels = list(numeric[:MAX_NUMERIC])
    if len(labels) < 2:
        return {"labels": labels, "rows": [], "test_columns": [], "test_rows": [], "chart": []}
    matrix: list[dict] = []
    test_columns = ["Pair", "Pearson r", "p-value", "N", "Significant (α=0.05)"]
    test_rows: list[dict] = []
    for a in labels:
        cells = []
        for b in labels:
            va = np.asarray(frame[a], dtype=float)
            vb = np.asarray(frame[b], dtype=float)
            mask = np.isfinite(va) & np.isfinite(vb)
            coef = 1.0 if a == b else 0.0
            p_value = 0.0
            count = int(mask.sum())
            if a != b and count > 2 and np.ptp(va[mask]) > 0 and np.ptp(vb[mask]) > 0:
                try:
                    r, p = stats.pearsonr(va[mask], vb[mask])
                    coef = float(r) if np.isfinite(r) else 0.0
                    p_value = float(p) if np.isfinite(p) else 1.0
                except Exception:
                    coef, p_value = 0.0, 1.0
            value = round(coef, 3)
            intensity = min(1.0, abs(value))
            color = (
                f"rgba(79, 70, 229, {0.08 + 0.72 * intensity:.2f})"
                if value >= 0
                else f"rgba(14, 165, 233, {0.08 + 0.72 * intensity:.2f})"
            )
            cells.append({"v": value, "color": color, "tip": f"{a} × {b}: {value:+.3f} (p={p_value:.4g})"})
            if a != b and b in labels[labels.index(a) + 1 :]:
                test_rows.append({
                    "Pair": f"{a} × {b}",
                    "Pearson r": round(coef, 4),
                    "p-value": _r(p_value, 6),
                    "N": count,
                    "Significant (α=0.05)": "Yes" if p_value < 0.05 else "No",
                })
        matrix.append({"label": a, "cells": cells})
    chart = [
        {"name": labels[i][:18], "value": matrix[i]["cells"][0]["v"]}
        for i in range(len(labels))
    ]
    return {
        "labels": labels,
        "rows": matrix,
        "test_columns": test_columns,
        "test_rows": test_rows[:24],
        "chart": chart,
    }


def _group_tests(frame, numeric: Sequence[str], categorical: Sequence[str], alpha: float):
    stats = require("scipy.stats")
    pd = require("pandas")
    columns = ["Test", "Group / column", "Target", "Statistic", "p-value", "Effect size", "Verdict"]
    rows: list[dict] = []
    chart: list[dict] = []

    def add(test: str, group: str, target: str, statistic: Any, p: Any, effect: Any, label: str = "") -> None:
        p_num = float_or_none(p)
        significant = p_num is not None and p_num < alpha
        rows.append({
            "Test": test,
            "Group / column": str(group)[:24],
            "Target": str(target)[:24],
            "Statistic": _r(statistic),
            "p-value": _r(p_num, 6),
            "Effect size": _r(effect),
            "Verdict": "Significant" if significant else "Not significant",
        })
        chart.append({
            "name": f"{str(group)[:10]}/{str(target)[:8]}",
            "value": round(min(8.0, -np.log10(max(p_num, 1e-12))), 3) if p_num else 0.0,
        })

    for group in list(categorical)[:MAX_CATEGORICAL]:
        if group not in frame.columns:
            continue
        levels = frame[group].astype(str)
        usable = [lv for lv, count in levels.value_counts().items() if count >= 3][:8]
        if len(usable) < 2:
            continue
        for target in list(numeric)[:5]:
            groups = []
            for level in usable:
                values = _finite(pd.to_numeric(frame.loc[levels == level, target], errors="coerce"))
                if values.size >= 3:
                    groups.append(values)
            if len(groups) < 2:
                continue
            try:
                if len(groups) == 2:
                    levene_p = float(stats.levene(*groups).pvalue)
                    equal_var = levene_p >= alpha
                    result = stats.ttest_ind(*groups, equal_var=equal_var)
                    pooled = np.sqrt((groups[0].var(ddof=1) + groups[1].var(ddof=1)) / 2) or 1.0
                    effect = (groups[0].mean() - groups[1].mean()) / pooled
                    add(
                        "Welch t-test" if not equal_var else "Student t-test",
                        f"{group} ({usable[0]} vs {usable[1]})",
                        target,
                        result.statistic,
                        result.pvalue,
                        effect,
                    )
                else:
                    result = stats.f_oneway(*groups)
                    grand = np.concatenate(groups).mean()
                    ss_between = sum(g.size * (g.mean() - grand) ** 2 for g in groups)
                    ss_total = sum(((g - grand) ** 2).sum() for g in groups) or 1.0
                    add("One-way ANOVA", f"{group} ({len(usable)} groups)", target,
                        result.statistic, result.pvalue, ss_between / ss_total)
            except Exception:
                continue
            if len(rows) >= MAX_TESTS:
                break
        if len(rows) >= MAX_TESTS:
            break

    if not rows:
        # Always surface a valid inferential result even for purely numeric data.
        for target in list(numeric)[:6]:
            values = _finite(frame[target])
            if values.size < 3 or np.ptp(values) == 0:
                continue
            try:
                result = stats.ttest_1samp(values, popmean=0.0)
                effect = values.mean() / (values.std(ddof=1) or 1.0)
                add("One-sample t-test (μ=0)", "all rows", target,
                    result.statistic, result.pvalue, effect)
            except Exception:
                continue
    return columns, rows[:MAX_TESTS], chart[:MAX_TESTS]


def profile_frame(
    frame,
    *,
    numeric: Sequence[str] | None = None,
    categorical: Sequence[str] | None = None,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Run the complete automated hypothesis-testing suite on a DataFrame."""
    cleaned = clean_frame(frame)
    if cleaned.empty:
        raise ValueError("The dataset has no rows to profile.")
    detected_numeric = numeric_columns(cleaned) if numeric is None else list(numeric)
    numeric = [c for c in detected_numeric[:MAX_NUMERIC] if c in cleaned.columns]
    if categorical is None:
        categorical = [c for c in cleaned.columns if c not in set(numeric)]
    categorical = list(categorical)[:MAX_CATEGORICAL]
    if not numeric:
        raise ValueError("Shapiro-Wilk / correlation / ANOVA need at least one numeric column.")

    pd = require("pandas")
    for column in numeric:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    n_rows = int(len(cleaned))
    total_cells = max(1, n_rows * len(cleaned.columns))
    missing = int(cleaned.isna().sum().sum())
    summary_columns, summary_rows, missing_chart = _descriptives(cleaned, numeric, n_rows)
    normality_columns, normality_rows, normality_chart = _normality(cleaned, numeric, alpha)
    correlation = _correlations(cleaned, numeric)
    test_columns, test_rows, test_chart = _group_tests(cleaned, numeric, categorical, alpha)

    notes = [
        f"SciPy Shapiro-Wilk uses a deterministic sample of at most {MAX_NORMALITY_ROWS:,} rows per column.",
        "Welch t-test is chosen when Levene's test rejects equal variances; one-way ANOVA is used for 3+ groups.",
        f"Significance threshold α = {alpha}. Correlation p-values come from scipy.stats.pearsonr.",
        "Rows are read from SQLite with a parameterized json_extract SQL projection (pandas.read_sql_query).",
    ]
    return {
        "row_count": n_rows,
        "column_count": int(len(cleaned.columns)),
        "numeric_count": len(numeric),
        "missing_cells": missing,
        "completeness": round(100 * (1 - missing / total_cells), 2),
        "alpha": alpha,
        "summary_columns": summary_columns,
        "summary_rows": summary_rows,
        "normality_columns": normality_columns,
        "normality_rows": normality_rows,
        "correlation_labels": correlation["labels"],
        "correlation_rows": correlation["rows"],
        "correlation_test_columns": correlation["test_columns"],
        "correlation_test_rows": correlation["test_rows"],
        "hypothesis_columns": test_columns,
        "hypothesis_rows": test_rows,
        "charts": {
            "missing": missing_chart,
            "normality": normality_chart,
            "correlation": correlation["chart"],
            "significance": test_chart,
        },
        "notes": notes,
    }
