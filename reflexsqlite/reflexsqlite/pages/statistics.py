"""Statistical profiling page: scipy hypothesis tests + statsmodels OLS / ARIMA."""
from __future__ import annotations

import reflex as rx

from ..components import charts, ui
from ..components.layout import shell
from ..components.theme import ACCENT, MUTED, PRIMARY, SUCCESS, TEXT, WARNING
from ..state import StatisticsState


def _dataset_chip(item):
    return rx.button(
        rx.text(item["name"], font_size="11px", font_weight="600"),
        on_click=StatisticsState.select_dataset(item["id"]),
        background=rx.cond(
            StatisticsState.dataset_id == item["id"], PRIMARY, "#FFFFFF"
        ),
        color=rx.cond(StatisticsState.dataset_id == item["id"], "white", TEXT),
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


def _chart_card(title, subtitle, chart):
    return ui.card(
        ui.section_title(title, subtitle),
        rx.box(chart, margin_top="12px", width="100%"),
        width="100%",
    )


def _table_card(title, subtitle, columns, rows):
    return ui.card(
        ui.section_title(title, subtitle),
        rx.box(ui.data_table(columns, rows), margin_top="12px", width="100%"),
        width="100%",
    )


def _controls():
    return ui.card(
        ui.section_title(
            "Automated profiling",
            "Pick a dataset, choose a significance level and run the full scipy suite",
        ),
        rx.hstack(
            rx.foreach(StatisticsState.datasets, _dataset_chip),
            gap="8px",
            flex_wrap="wrap",
            margin_top="12px",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Significance α",
                    rx.select(
                        ["0.01", "0.05", "0.10"],
                        value=StatisticsState.alpha,
                        on_change=StatisticsState.set_alpha,
                        width="120px",
                        size="1",
                    ),
                ),
                width="140px",
            ),
            ui.primary_button(
                rx.cond(StatisticsState.profile_busy, "Profiling…", "Run profile"),
                on_click=StatisticsState.run_profile,
                disabled=StatisticsState.profile_busy,
            ),
            gap="14px",
            align_items="end",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        ui.notice_banner(StatisticsState.notice, "success"),
        ui.notice_banner(StatisticsState.error),
        padding="20px",
        width="100%",
    )


def _profile_section():
    return rx.fragment(
        rx.cond(
            StatisticsState.has_profile,
            rx.vstack(
                _metrics(StatisticsState.profile_metrics),
                rx.hstack(
                    rx.box(
                        _table_card(
                            "Descriptive statistics",
                            "Mean, spread, quartiles, skewness and kurtosis per numeric column",
                            StatisticsState.profile_summary_columns,
                            StatisticsState.profile_summary_rows,
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _chart_card(
                            "Shapiro-Wilk p-values",
                            "Bars below α indicate non-normal distributions",
                            charts.bar_chart_simple(StatisticsState.normality_chart, "p-value", ACCENT),
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                _table_card(
                    "Normality tests",
                    "scipy.stats.shapiro on a deterministic sample of up to 5,000 rows",
                    StatisticsState.profile_normality_columns,
                    StatisticsState.profile_normality_rows,
                ),
                rx.hstack(
                    rx.box(
                        ui.card(
                            ui.section_title(
                                "Correlation matrix",
                                "Pearson r with per-pair p-values (hover a cell)",
                            ),
                            rx.box(
                                charts.correlation_grid(
                                    StatisticsState.corr_labels, StatisticsState.corr_rows
                                ),
                                margin_top="12px",
                            ),
                            width="100%",
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _table_card(
                            "Correlation significance",
                            "Pairwise Pearson tests",
                            StatisticsState.profile_corr_test_columns,
                            StatisticsState.profile_corr_test_rows,
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                rx.hstack(
                    rx.box(
                        _table_card(
                            "Hypothesis tests",
                            "t-tests / ANOVA across categorical groups, one-sample t-test fallback",
                            StatisticsState.profile_hypothesis_columns,
                            StatisticsState.profile_hypothesis_rows,
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _chart_card(
                            "Test significance",
                            "−log₁₀(p) per test; taller bars are stronger evidence",
                            charts.bar_chart_simple(StatisticsState.significance_chart, "−log₁₀ p", WARNING),
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
            ),
            ui.empty_state(
                "No profile yet",
                "Choose a dataset above and run the profiler to see normality, correlation and hypothesis tests.",
            ),
        ),
        width="100%",
    )


def _regression_section():
    return ui.card(
        ui.section_title(
            "OLS regression",
            "statsmodels OLS with coefficients, standard errors, p-values and confidence intervals",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Target column",
                    rx.select(
                        StatisticsState.target_options,
                        value=StatisticsState.target,
                        on_change=StatisticsState.set_target,
                        width="220px",
                        size="1",
                    ),
                ),
                width="240px",
            ),
            ui.primary_button(
                rx.cond(StatisticsState.regression_busy, "Fitting…", "Fit OLS"),
                on_click=StatisticsState.run_regression,
                disabled=StatisticsState.regression_busy,
            ),
            gap="14px",
            align_items="end",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.cond(
            StatisticsState.has_regression,
            rx.vstack(
                _metrics(StatisticsState.reg_metrics),
                rx.hstack(
                    rx.box(
                        _table_card(
                            "Coefficients",
                            "Estimate, std. error, t-statistic, p-value and CI",
                            StatisticsState.reg_columns,
                            StatisticsState.reg_rows,
                        ),
                        width="100%",
                    ),
                    rx.box(
                        _chart_card(
                            "|Coefficient| importance",
                            "Absolute effect size per predictor",
                            charts.bar_chart_simple(StatisticsState.reg_importance, "|coef|", PRIMARY),
                        ),
                        width="100%",
                    ),
                    gap="14px",
                    width="100%",
                    align_items="start",
                    flex_wrap="wrap",
                ),
                _chart_card(
                    "Actual vs fitted",
                    "Fitted trendline with the mean-response confidence band",
                    charts.multi_line_chart(
                        StatisticsState.reg_chart,
                        [
                            {"key": "actual", "label": "Actual", "color": PRIMARY},
                            {"key": "fitted", "label": "Fitted", "color": ACCENT},
                            {"key": "lower", "label": "CI lower", "color": "#94A3B8", "dash": "4 4", "width": 1},
                            {"key": "upper", "label": "CI upper", "color": "#94A3B8", "dash": "4 4", "width": 1},
                        ],
                    ),
                ),
                gap="14px",
                width="100%",
            ),
            rx.text("Choose a numeric target and fit a model.", font_size="12px", color=MUTED),
        ),
        width="100%",
        padding="20px",
    )


def _timeseries_section():
    return ui.card(
        ui.section_title(
            "Time-series forecast",
            "ARIMA / SARIMAX forecast with confidence bands plus additive trend/seasonality",
        ),
        rx.hstack(
            rx.box(
                ui.field(
                    "Value column",
                    rx.select(
                        StatisticsState.target_options,
                        value=StatisticsState.value_column,
                        on_change=StatisticsState.set_value_column,
                        width="200px",
                        size="1",
                    ),
                ),
                width="220px",
            ),
            rx.box(
                ui.field(
                    "Date column",
                    rx.select(
                        StatisticsState.date_options,
                        value=StatisticsState.date_value,
                        on_change=StatisticsState.set_date_column,
                        width="200px",
                        size="1",
                    ),
                ),
                width="220px",
            ),
            rx.box(
                ui.field(
                    "Forecast steps",
                    rx.select(
                        ["6", "12", "24"],
                        value=StatisticsState.steps,
                        on_change=StatisticsState.set_steps,
                        width="120px",
                        size="1",
                    ),
                ),
                width="140px",
            ),
            rx.box(
                ui.field(
                    "Season period",
                    rx.select(
                        ["0", "4", "7", "12"],
                        value=StatisticsState.period,
                        on_change=StatisticsState.set_period,
                        width="120px",
                        size="1",
                    ),
                ),
                width="140px",
            ),
            ui.primary_button(
                rx.cond(StatisticsState.timeseries_busy, "Forecasting…", "Run forecast"),
                on_click=StatisticsState.run_timeseries,
                disabled=StatisticsState.timeseries_busy,
            ),
            gap="12px",
            align_items="end",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        rx.cond(
            StatisticsState.has_timeseries,
            rx.vstack(
                _metrics(StatisticsState.ts_metrics),
                _chart_card(
                    "Forecast",
                    "History, in-sample fit and the out-of-sample forecast band",
                    charts.multi_line_chart(
                        StatisticsState.ts_chart,
                        [
                            {"key": "actual", "label": "Actual", "color": PRIMARY},
                            {"key": "fitted", "label": "Fitted", "color": ACCENT},
                            {"key": "forecast", "label": "Forecast", "color": SUCCESS, "width": 3},
                            {"key": "lower", "label": "CI lower", "color": "#94A3B8", "dash": "4 4", "width": 1},
                            {"key": "upper", "label": "CI upper", "color": "#94A3B8", "dash": "4 4", "width": 1},
                        ],
                    ),
                ),
                _chart_card(
                    "Trend & seasonality",
                    "Additive decomposition (requires a full seasonal period)",
                    charts.multi_line_chart(
                        StatisticsState.ts_trend,
                        [
                            {"key": "actual", "label": "Actual", "color": PRIMARY},
                            {"key": "trend", "label": "Trend", "color": ACCENT},
                            {"key": "seasonal", "label": "Seasonal", "color": WARNING, "dash": "5 4"},
                        ],
                    ),
                ),
                _table_card(
                    "Model parameters",
                    "Estimate, standard error, p-value and confidence interval",
                    StatisticsState.ts_columns,
                    StatisticsState.ts_rows,
                ),
                gap="14px",
                width="100%",
            ),
            rx.text(
                "Pick a numeric value column (and a date column for a real time axis) and run the forecast.",
                font_size="12px",
                color=MUTED,
            ),
        ),
        width="100%",
        padding="20px",
    )


def statistics():
    return shell(
        "Statistical Profiling",
        "Automated scipy hypothesis tests, statsmodels OLS regression and ARIMA forecasting",
        ui.notice_banner(StatisticsState.env_warning, "warning"),
        _controls(),
        _profile_section(),
        _regression_section(),
        _timeseries_section(),
    )
