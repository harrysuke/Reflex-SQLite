"""Dashboard state: interactive charts, KPI cards, correlation grid and live feed."""
from __future__ import annotations

import asyncio
from typing import TypedDict

import reflex as rx

from ..errors import friendly
from ..services import dataset_service, settings_service
from .base import AuthState

CHART_TYPES = ["line", "area", "bar", "histogram"]


class CorrCell(TypedDict):
    """One correlation-matrix cell; typed so nested rx.foreach can introspect it."""

    v: float
    color: str
    tip: str


class CorrRow(TypedDict):
    label: str
    cells: list[CorrCell]


class DashboardState(AuthState):
    datasets: list[dict] = []
    active_dataset_id: int = 0
    active_name: str = ""

    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []
    x_column: str = ""
    y_column: str = ""
    chart_type: str = "line"

    chart_data: list[dict] = []
    live_data: list[dict] = []
    corr_labels: list[str] = []
    corr_rows: list[CorrRow] = []
    activity: list[dict] = []
    stats: dict = {}

    live_enabled: bool = True
    live_running: bool = False
    tick: int = 0
    refresh_seconds: int = 3
    dashboard_error: str = ""

    @rx.var
    def corr_grid_columns(self) -> str:
        return f"repeat({max(1, len(self.corr_labels) + 1)}, minmax(0, 1fr))"

    @rx.var
    def has_datasets(self) -> bool:
        return len(self.datasets) > 0

    @rx.var
    def kpi_datasets(self) -> str:
        return str(self.stats.get("datasets", 0))

    @rx.var
    def kpi_rows(self) -> str:
        return f"{int(self.stats.get('rows', 0)):,}"

    @rx.var
    def kpi_columns(self) -> str:
        return str(self.stats.get("columns", 0))

    @rx.var
    def kpi_completeness(self) -> str:
        return f"{self.stats.get('completeness', 0)}%"

    @rx.var
    def kpi_missing(self) -> str:
        return f"{int(self.stats.get('missing', 0)):,}"

    @rx.var
    def chart_subtitle(self) -> str:
        return f"Primary metric for {self.active_name}"

    @rx.var
    def missing_hint(self) -> str:
        return f"{int(self.stats.get('missing', 0)):,} missing cells"

    @rx.var
    def y_options(self) -> list[str]:
        return self.numeric if self.numeric else self.columns

    @rx.var
    def x_options(self) -> list[str]:
        return self.columns

    def _refresh(self) -> None:
        self.datasets = dataset_service.list_user_datasets(self.user_id)
        if not any(d["id"] == self.active_dataset_id for d in self.datasets):
            self.active_dataset_id = int(self.datasets[0]["id"]) if self.datasets else 0
        if not self.active_dataset_id:
            self.chart_data, self.live_data = [], []
            self.corr_labels, self.corr_rows = [], []
            self.stats, self.activity, self.columns, self.numeric, self.categorical = {}, [], [], [], []
            self.active_name = "No dataset yet"
            return
        detail = dataset_service.get_dataset_detail(self.user_id, self.active_dataset_id) or {}
        self.active_name = str(detail.get("name", "Dataset"))
        self.columns = list(detail.get("columns", []))
        self.numeric = list(detail.get("numeric", []))
        self.categorical = list(detail.get("categorical", []))
        if self.x_column not in self.columns:
            self.x_column = (self.categorical or self.columns or [""])[0]
        if self.y_column not in self.numeric:
            self.y_column = (self.numeric or [""])[0]
        self.chart_data = dataset_service.chart_series(
            self.user_id, self.active_dataset_id, self.chart_type, self.x_column, self.y_column
        )
        self.live_data = dataset_service.live_points(self.user_id, self.active_dataset_id)
        self.stats = dataset_service.compute_stats(self.user_id, self.active_dataset_id)
        self.activity = list(self.stats.get("activity", []))
        corr = dataset_service.correlation_matrix(self.user_id, self.active_dataset_id)
        self.corr_labels = corr["labels"]
        self.corr_rows = corr["rows"]

    @rx.event
    def load_dashboard(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            prefs = settings_service.get_settings(self.user_id)
            self.chart_type = prefs["chart_type"] if prefs["chart_type"] in CHART_TYPES else "line"
            self.live_enabled = bool(prefs["live_enabled"])
            self.refresh_seconds = max(1, int(prefs["live_refresh_seconds"]))
            self._refresh()
        except Exception as exc:
            self.dashboard_error = friendly(exc)

    @rx.event
    def refresh_dashboard(self):
        try:
            self._refresh()
        except Exception as exc:
            self.dashboard_error = friendly(exc)

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.active_dataset_id = int(dataset_id)
        self.x_column, self.y_column = "", ""
        try:
            self._refresh()
        except Exception as exc:
            self.dashboard_error = friendly(exc)

    @rx.event
    def set_chart_type(self, value: str):
        self.chart_type = value
        try:
            self.chart_data = dataset_service.chart_series(
                self.user_id, self.active_dataset_id, self.chart_type, self.x_column, self.y_column
            )
        except Exception as exc:
            self.dashboard_error = friendly(exc)

    @rx.event
    def set_x_column(self, value: str):
        self.x_column = value
        self.refresh_dashboard()

    @rx.event
    def set_y_column(self, value: str):
        self.y_column = value
        self.refresh_dashboard()

    @rx.event
    def toggle_live(self, value: bool):
        self.live_enabled = bool(value)

    @rx.event(background=True)
    async def live_loop(self):
        """Push a fresh sample into the live chart on an interval."""
        async with self:
            if self.live_running:
                return
            self.live_running = True
            interval = max(1, self.refresh_seconds)
        try:
            while True:
                await asyncio.sleep(interval)
                async with self:
                    # Stop instead of idling forever: a closed session or an
                    # empty workspace must not leave a polling task running.
                    if self.tick >= 1200:
                        break
                    if not self.is_authenticated or not self.active_dataset_id:
                        break
                    if not self.live_enabled:
                        continue
                    try:
                        self.live_data = dataset_service.append_live_point(
                            self.user_id, self.active_dataset_id
                        )
                        self.tick += 1
                    except Exception:
                        pass
        finally:
            async with self:
                self.live_running = False
