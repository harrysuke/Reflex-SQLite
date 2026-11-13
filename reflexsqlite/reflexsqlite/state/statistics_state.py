"""Statistical profiling state: scipy hypothesis tests + statsmodels OLS/ARIMA.

Every heavy computation runs inside a ``@rx.event(background=True)`` handler and
is offloaded with ``asyncio.to_thread`` so the websocket loop stays responsive.
"""
from __future__ import annotations

import asyncio

import reflex as rx

from ml_pipelines import _optional as deps

from ..errors import friendly
from ..services import dataset_service, ml_service
from .base import AuthState
from .dashboard_state import CorrRow

ALPHA_OPTIONS = ["0.01", "0.05", "0.10"]
STEP_OPTIONS = ["6", "12", "24"]
PERIOD_OPTIONS = ["0", "4", "7", "12"]


def _indexed(rows: list[dict]) -> list[dict]:
    return [{**row, "_index": position + 1} for position, row in enumerate(rows)]


class StatisticsState(AuthState):
    datasets: list[dict] = []
    dataset_id: int = 0
    dataset_name: str = ""
    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []

    alpha: str = "0.05"
    target: str = ""
    value_column: str = ""
    date_column: str = ""
    steps: str = "12"
    period: str = "0"

    profile: dict = {}
    profile_metrics: list[dict] = []
    profile_summary_columns: list[str] = []
    profile_summary_rows: list[dict] = []
    profile_normality_columns: list[str] = []
    profile_normality_rows: list[dict] = []
    profile_hypothesis_columns: list[str] = []
    profile_hypothesis_rows: list[dict] = []
    profile_corr_test_columns: list[str] = []
    profile_corr_test_rows: list[dict] = []
    corr_labels: list[str] = []
    corr_rows: list[CorrRow] = []
    normality_chart: list[dict] = []
    significance_chart: list[dict] = []

    regression: dict = {}
    reg_columns: list[str] = []
    reg_rows: list[dict] = []
    reg_metrics: list[dict] = []
    reg_chart: list[dict] = []
    reg_importance: list[dict] = []

    timeseries: dict = {}
    ts_columns: list[str] = []
    ts_rows: list[dict] = []
    ts_metrics: list[dict] = []
    ts_chart: list[dict] = []
    ts_trend: list[dict] = []

    profile_busy: bool = False
    regression_busy: bool = False
    timeseries_busy: bool = False
    error: str = ""
    notice: str = ""

    @rx.var
    def has_datasets(self) -> bool:
        return len(self.datasets) > 0

    @rx.var
    def env_warning(self) -> str:
        """Preflight: name the missing libraries before the user clicks Run."""
        return deps.warning(("pandas", "scipy", "statsmodels"))

    @rx.var
    def has_profile(self) -> bool:
        return bool(self.profile)

    @rx.var
    def has_regression(self) -> bool:
        return bool(self.regression)

    @rx.var
    def has_timeseries(self) -> bool:
        return bool(self.timeseries)

    @rx.var
    def target_options(self) -> list[str]:
        return self.numeric or self.columns

    @rx.var
    def date_options(self) -> list[str]:
        return ["(row order)"] + self.columns

    @rx.var
    def date_value(self) -> str:
        return self.date_column or "(row order)"

    def _refresh_datasets(self) -> None:
        self.datasets = dataset_service.list_user_datasets(self.user_id)
        if not any(d["id"] == self.dataset_id for d in self.datasets):
            self.dataset_id = int(self.datasets[0]["id"]) if self.datasets else 0

    def _refresh_columns(self) -> None:
        detail = dataset_service.get_dataset_detail(self.user_id, self.dataset_id) or {}
        self.dataset_name = str(detail.get("name", ""))
        self.columns = list(detail.get("columns", []))
        self.numeric = list(detail.get("numeric", []))
        self.categorical = list(detail.get("categorical", []))
        if self.target not in self.numeric:
            self.target = (self.numeric or self.columns or [""])[0]
        if self.value_column not in self.numeric:
            self.value_column = (self.numeric or [""])[0]
        if self.date_column not in self.columns:
            self.date_column = ""

    @rx.event
    def load_page(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            self._refresh_datasets()
            self._refresh_columns()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.dataset_id = int(dataset_id)
        self.profile, self.regression, self.timeseries = {}, {}, {}
        self.profile_metrics, self.reg_metrics, self.ts_metrics = [], [], []
        self.error, self.notice = "", ""
        try:
            self._refresh_columns()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def set_alpha(self, value: str):
        self.alpha = value

    @rx.event
    def set_target(self, value: str):
        self.target = value

    @rx.event
    def set_value_column(self, value: str):
        self.value_column = value

    @rx.event
    def set_date_column(self, value: str):
        self.date_column = "" if value == "(row order)" else value

    @rx.event
    def set_steps(self, value: str):
        self.steps = value

    @rx.event
    def set_period(self, value: str):
        self.period = value

    # Background jobs -------------------------------------------------------
    @rx.event(background=True)
    async def run_profile(self):
        async with self:
            if self.profile_busy or not self.dataset_id:
                return
            self.profile_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id = self.user_id, self.dataset_id
            alpha = float(self.alpha)
        try:
            report = await asyncio.to_thread(ml_service.run_profile, user_id, dataset_id, alpha)
            async with self:
                self.profile = report
                self.profile_metrics = [
                    {"label": "Rows", "value": report.get("row_count", 0), "hint": "Rows profiled"},
                    {"label": "Numeric cols", "value": report.get("numeric_count", 0), "hint": "Tested with scipy"},
                    {"label": "Missing", "value": report.get("missing_cells", 0), "hint": "Empty cells"},
                    {"label": "Completeness", "value": f"{report.get('completeness', 0)}%", "hint": "Non-missing share"},
                ]
                self.profile_summary_columns = list(report.get("summary_columns", []))
                self.profile_summary_rows = _indexed(report.get("summary_rows", []))
                self.profile_normality_columns = list(report.get("normality_columns", []))
                self.profile_normality_rows = _indexed(report.get("normality_rows", []))
                self.profile_hypothesis_columns = list(report.get("hypothesis_columns", []))
                self.profile_hypothesis_rows = _indexed(report.get("hypothesis_rows", []))
                self.profile_corr_test_columns = list(report.get("correlation_test_columns", []))
                self.profile_corr_test_rows = _indexed(report.get("correlation_test_rows", []))
                self.corr_labels = list(report.get("correlation_labels", []))
                self.corr_rows = list(report.get("correlation_rows", []))
                charts = report.get("charts", {})
                self.normality_chart = list(charts.get("normality", []))
                self.significance_chart = list(charts.get("significance", []))
                self.notice = f"Profiled {report.get('row_count', 0)} rows across {report.get('numeric_count', 0)} numeric columns."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.profile_busy = False

    @rx.event(background=True)
    async def run_regression(self):
        async with self:
            if self.regression_busy or not self.dataset_id or not self.target:
                return
            self.regression_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id, target = self.user_id, self.dataset_id, self.target
            alpha = float(self.alpha)
        try:
            result = await asyncio.to_thread(
                ml_service.run_regression, user_id, dataset_id, target, None, alpha
            )
            async with self:
                self.regression = result
                self.reg_metrics = list(result.get("metrics", []))
                self.reg_columns = list(result.get("coefficient_columns", []))
                self.reg_rows = _indexed(result.get("coefficient_rows", []))
                self.reg_chart = list(result.get("chart", []))
                self.reg_importance = list(result.get("importance", []))
                self.notice = f"OLS fitted: {result.get('equation', target)}"
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.regression_busy = False

    @rx.event(background=True)
    async def run_timeseries(self):
        async with self:
            if self.timeseries_busy or not self.dataset_id or not self.value_column:
                return
            self.timeseries_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id = self.user_id, self.dataset_id
            value_column, date_column = self.value_column, self.date_column
            steps, period = int(self.steps), int(self.period)
        try:
            result = await asyncio.to_thread(
                ml_service.run_time_series,
                user_id,
                dataset_id,
                value_column,
                date_column,
                (1, 1, 1),
                steps,
                period,
            )
            async with self:
                self.timeseries = result
                self.ts_metrics = list(result.get("metrics", []))
                self.ts_columns = list(result.get("parameter_columns", []))
                self.ts_rows = _indexed(result.get("parameter_rows", []))
                self.ts_chart = list(result.get("chart", []))
                self.ts_trend = list(result.get("trend_chart", []))
                self.notice = f"{result.get('model_label', 'ARIMA')} forecast ready."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.timeseries_busy = False
