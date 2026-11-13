"""Inferential regression and time-series modelling with statsmodels.

Both functions return plain dictionaries containing coefficients, p-values and
confidence intervals plus chart-ready series that map 1:1 onto ``rx.recharts``
line / composed charts in the UI.

Note on imports
---------------
``statsmodels.api`` drags in the state-space ``_hamilton_filter`` extension
module, which is blocked by some endpoint application-control policies (the
import fails with a DLL load error). We therefore import the *concrete*
submodules we actually need. They load fine even when the umbrella ``api``
module does not, and they expose the same symbols.
"""
from __future__ import annotations

import warnings
from typing import Any, Sequence

import numpy as np

from ._optional import require
from .preprocessing import clean_frame, float_or_none, json_safe, numeric_columns

MAX_CHART_POINTS = 60
MAX_SERIES_ROWS = 800


def _r(value: Any, digits: int = 4) -> float | None:
    number = float_or_none(value)
    return None if number is None else round(number, digits)


def _statsmodels():
    """Import the concrete statsmodels submodules we use.

    Returns ``(OLS, add_constant, durbin_watson, ARIMA, seasonal_decompose)``.
    ``require`` converts any ImportError into a friendly ``MissingDependency``.
    """
    require("statsmodels.regression.linear_model")
    require("statsmodels.tools")
    require("statsmodels.stats.stattools")
    require("statsmodels.tsa.arima.model")
    require("statsmodels.tsa.seasonal")
    from statsmodels.regression.linear_model import OLS
    from statsmodels.stats.stattools import durbin_watson
    from statsmodels.tools import add_constant
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose

    return OLS, add_constant, durbin_watson, ARIMA, seasonal_decompose


def ols_regression(
    frame,
    target: str,
    predictors: Sequence[str] | None = None,
    *,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Fit an OLS model and report coefficients, p-values and confidence intervals."""
    pd = require("pandas")
    OLS, add_constant, durbin_watson, _, _ = _statsmodels()

    working = clean_frame(frame)
    if target not in working.columns:
        raise ValueError(f"Target column '{target}' is not in the dataset.")
    if predictors:
        features = [c for c in predictors if c in working.columns and c != target]
    else:
        features = [c for c in numeric_columns(working) if c != target]
    features = features[:8]
    if not features:
        raise ValueError("OLS needs at least one numeric predictor column.")

    model_frame = (
        working[[target, *features]]
        .apply(pd.to_numeric, errors="coerce")
        .dropna()
        .reset_index(drop=True)
    )
    if len(model_frame) < max(4, len(features) + 2):
        raise ValueError("Not enough complete numeric rows to fit an OLS model.")

    y = model_frame[target].astype(float)
    x = add_constant(model_frame[features].astype(float), has_constant="add")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fitted = OLS(y, x).fit()

    conf = fitted.conf_int(alpha=alpha)
    lower_col, upper_col = conf.columns[0], conf.columns[1]
    columns = ["Term", "Coefficient", "Std error", "t", "p-value", "CI lower", "CI upper", "Significant"]
    rows: list[dict[str, Any]] = []
    for term in fitted.params.index:
        p_value = float_or_none(fitted.pvalues.get(term))
        rows.append({
            "Term": str(term),
            "Coefficient": _r(fitted.params[term], 6),
            "Std error": _r(fitted.bse[term], 6),
            "t": _r(fitted.tvalues[term]),
            "p-value": _r(p_value, 6),
            "CI lower": _r(conf.loc[term, lower_col], 6),
            "CI upper": _r(conf.loc[term, upper_col], 6),
            "Significant": "Yes" if p_value is not None and p_value < alpha else "No",
        })

    prediction = fitted.get_prediction(x).summary_frame(alpha=alpha)
    mean_ci_lower = next((c for c in prediction.columns if c.startswith("mean_ci_lower")), None)
    mean_ci_upper = next((c for c in prediction.columns if c.startswith("mean_ci_upper")), None)
    step = max(1, len(model_frame) // MAX_CHART_POINTS)
    chart = []
    for index in range(0, len(model_frame), step):
        position = int(model_frame.index[index])
        if position >= len(y):
            continue
        chart.append({
            "name": str(position + 1),
            "actual": _r(float(y.iloc[position]), 3),
            "fitted": _r(float(fitted.fittedvalues.iloc[position]), 3),
            "lower": _r(float(prediction[mean_ci_lower].iloc[position]), 3) if mean_ci_lower else None,
            "upper": _r(float(prediction[mean_ci_upper].iloc[position]), 3) if mean_ci_upper else None,
        })

    metrics = [
        {"label": "R²", "value": _r(fitted.rsquared), "hint": "Coefficient of determination"},
        {"label": "Adj. R²", "value": _r(fitted.rsquared_adj), "hint": "Penalized for predictor count"},
        {"label": "F statistic", "value": _r(fitted.fvalue, 2), "hint": "Overall model significance"},
        {"label": "Prob (F)", "value": _r(fitted.f_pvalue, 6), "hint": "p-value of the F test"},
        {"label": "AIC", "value": _r(fitted.aic, 2), "hint": "Akaike information criterion"},
        {"label": "Durbin–Watson", "value": _r(durbin_watson(fitted.resid), 3), "hint": "Residual autocorrelation (≈2 is ideal)"},
        {"label": "N", "value": len(model_frame), "hint": "Complete cases"},
    ]
    feature_importance = [
        {"name": str(term)[:18], "value": round(abs(float(value)), 4)}
        for term, value in fitted.params.items()
        if str(term) != "const"
    ]
    return {
        "target": target,
        "predictors": features,
        "equation": f"{target} ~ " + " + ".join(features),
        "coefficient_columns": columns,
        "coefficient_rows": rows,
        "metrics": metrics,
        "chart": chart[:MAX_CHART_POINTS],
        "importance": feature_importance[:10],
        "alpha": alpha,
        "notes": [
            f"statsmodels OLS with {int((1 - alpha) * 100)}% confidence intervals from t-distribution.",
            "Rows with missing values in the model columns are dropped listwise.",
            "The chart shows actual values, fitted trendline and the mean-response confidence band.",
        ],
    }


def _build_series(frame, value_column: str, date_column: str | None):
    pd = require("pandas")
    working = clean_frame(frame)
    if value_column not in working.columns:
        raise ValueError(f"Value column '{value_column}' is not in the dataset.")
    values = pd.to_numeric(working[value_column], errors="coerce")
    labels: list[str] = []
    if date_column and date_column in working.columns:
        dates = pd.to_datetime(working[date_column], errors="coerce")
        order = dates.sort_values().index
        series = values.loc[order].reset_index(drop=True)
        labels = [
            d.strftime("%Y-%m-%d") if pd.notna(d) else f"t{i + 1}"
            for i, d in enumerate(dates.loc[order])
        ]
    else:
        series = values.reset_index(drop=True)
        labels = [f"t{i + 1}" for i in range(len(series))]
    series = series.interpolate(limit_direction="both").dropna()
    labels = labels[: len(series)]
    if len(series) < 8:
        raise ValueError("Time-series analysis needs at least 8 numeric observations.")
    return series.astype(float).head(MAX_SERIES_ROWS), labels


def time_series_analysis(
    frame,
    *,
    value_column: str,
    date_column: str | None = None,
    order: Sequence[int] = (1, 1, 1),
    seasonal_order: Sequence[int] = (0, 0, 0, 0),
    steps: int = 12,
    period: int = 0,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """Fit ARIMA / SARIMAX, forecast with confidence intervals, decompose trend/seasonality."""
    _, _, _, ARIMA, seasonal_decompose = _statsmodels()
    series, labels = _build_series(frame, value_column, date_column)
    steps = max(1, min(int(steps), 48))
    order = tuple(int(v) for v in order)
    seasonal_order = tuple(int(v) for v in seasonal_order)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = ARIMA(
            series,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False,
        )
        fitted = model.fit()
        forecast = fitted.get_forecast(steps=steps)
        forecast_frame = forecast.summary_frame(alpha=alpha)

    mean_col = forecast_frame.columns[0]
    lower_col = next((c for c in forecast_frame.columns if "ci_lower" in c), forecast_frame.columns[1])
    upper_col = next((c for c in forecast_frame.columns if "ci_upper" in c), forecast_frame.columns[2])

    # Trend / seasonality decomposition (only when a full period is observable).
    trend_chart: list[dict[str, Any]] = []
    seasonality_strength: float | None = None
    slope: float | None = None
    period = int(period or (seasonal_order[3] if len(seasonal_order) > 3 else 0))
    if period >= 2 and len(series) >= 2 * period:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                decomposition = seasonal_decompose(
                    series, model="additive", period=period, extrapolate_trend="period"
                )
            residual = np.asarray(decomposition.resid, dtype=float)
            seasonal = np.asarray(decomposition.seasonal, dtype=float)
            seasonal = seasonal[np.isfinite(seasonal)]
            residual = residual[np.isfinite(residual)]
            if seasonal.size and residual.size:
                seasonality_strength = float(
                    max(0.0, 1.0 - np.var(residual) / (np.var(seasonal + residual) or 1.0))
                )
            step = max(1, len(series) // MAX_CHART_POINTS)
            for index in range(0, len(series), step):
                trend_chart.append({
                    "name": labels[index],
                    "actual": _r(float(series.iloc[index]), 3),
                    "trend": _r(float(np.asarray(decomposition.trend)[index]), 3),
                    "seasonal": _r(float(np.asarray(decomposition.seasonal)[index]), 3),
                })
        except Exception:
            trend_chart = []

    x_time = np.arange(len(series), dtype=float)
    if len(series) > 2 and np.ptp(x_time) > 0:
        slope = float(np.polyfit(x_time, np.asarray(series, dtype=float), 1)[0])

    conf = fitted.conf_int(alpha=alpha)
    columns = ["Parameter", "Estimate", "Std error", "p-value", "CI lower", "CI upper"]
    param_rows: list[dict[str, Any]] = []
    for name in fitted.params.index:
        lower, upper = conf.columns[0], conf.columns[1]
        param_rows.append({
            "Parameter": str(name),
            "Estimate": _r(fitted.params[name], 6),
            "Std error": _r(fitted.bse[name], 6),
            "p-value": _r(fitted.pvalues[name], 6),
            "CI lower": _r(conf.loc[name, lower], 6),
            "CI upper": _r(conf.loc[name, upper], 6),
        })

    history_count = min(MAX_CHART_POINTS - steps, len(series))
    history_count = max(history_count, 12) if len(series) >= 12 else len(series)
    start = len(series) - history_count
    in_sample = np.asarray(fitted.fittedvalues, dtype=float)
    chart: list[dict[str, Any]] = []
    for index in range(start, len(series)):
        chart.append({
            "name": labels[index],
            "actual": _r(float(series.iloc[index]), 3),
            "fitted": _r(float(in_sample[index]), 3) if index < len(in_sample) else None,
            "forecast": None,
            "lower": None,
            "upper": None,
        })
    last = chart[-1] if chart else None
    if last is not None:
        last["forecast"] = last["actual"]
    for offset in range(steps):
        chart.append({
            "name": f"+{offset + 1}",
            "actual": None,
            "fitted": None,
            "forecast": _r(float(forecast_frame[mean_col].iloc[offset]), 3),
            "lower": _r(float(forecast_frame[lower_col].iloc[offset]), 3),
            "upper": _r(float(forecast_frame[upper_col].iloc[offset]), 3),
        })

    metrics = [
        {"label": "AIC", "value": _r(fitted.aic, 2), "hint": "Akaike information criterion"},
        {"label": "BIC", "value": _r(fitted.bic, 2), "hint": "Bayesian information criterion"},
        {"label": "Trend slope", "value": _r(slope, 4), "hint": "OLS slope per observation"},
        {"label": "Seasonality", "value": _r(seasonality_strength, 3), "hint": "Variance share of seasonal component"},
        {"label": "Observations", "value": len(series), "hint": "Points used for fitting"},
        {"label": "Forecast steps", "value": steps, "hint": "Out-of-sample horizon"},
    ]
    return {
        "value_column": value_column,
        "date_column": date_column or "",
        "model_label": f"ARIMA{order}×{seasonal_order}" if any(seasonal_order) else f"ARIMA{order}",
        "parameter_columns": columns,
        "parameter_rows": param_rows,
        "metrics": metrics,
        "chart": chart,
        "trend_chart": trend_chart,
        "alpha": alpha,
        "notes": [
            "statsmodels ARIMA/SARIMAX with enforce_stationarity=False for robust convergence.",
            f"Forecast band is the {int((1 - alpha) * 100)}% confidence interval from get_forecast().",
            "Trend / seasonality come from an additive seasonal_decompose (requires a full period).",
        ],
    }
