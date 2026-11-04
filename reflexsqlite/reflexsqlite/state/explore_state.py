"""Library workbench state: pick a Python library and run it on a dataset."""
from __future__ import annotations

import reflex as rx

from ..analytics import engines, registry
from ..db import session_scope
from ..errors import friendly
from ..repositories import add_activity
from ..services import dataset_service, settings_service
from .base import AuthState

CATEGORIES = list(registry.CATEGORIES)


class ExploreState(AuthState):
    active_library: str = "pandas"
    active_operation: str = "describe"
    active_library_name: str = "Pandas"
    active_library_color: str = "#7069D1"
    active_op_description: str = ""
    operations: list[dict] = []
    needs_x: bool = False
    needs_y: bool = False

    datasets: list[dict] = []
    active_dataset_id: int = 0
    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []
    x_column: str = ""
    y_column: str = ""

    x_options: list[str] = []
    y_options: list[str] = []
    is_running: bool = False
    has_result: bool = False
    explore_error: str = ""

    result_title: str = ""
    result_summary: str = ""
    result_library: str = ""
    result_color: str = "#4F46E5"
    result_elapsed: int = 0
    result_metrics: list[dict] = []
    result_table_columns: list[str] = []
    result_table_rows: list[dict] = []
    result_chart: list[dict] = []
    result_chart_label: str = "Value"
    result_secondary: bool = False
    result_secondary_label: str = ""
    result_image: str = ""
    result_notes: list[str] = []

    @rx.var
    def has_result_chart(self) -> bool:
        return len(self.result_chart) > 0

    @rx.var
    def library_available(self) -> bool:
        return registry.is_available(self.active_library)

    @rx.var
    def library_version(self) -> str:
        return registry.installed_version(self.active_library)

    @rx.var
    def result_elapsed_label(self) -> str:
        return f"Executed in {self.result_elapsed} ms" if self.has_result else ""

    def _select_library(self, library_id: str) -> None:
        spec = registry.get(library_id)
        self.active_library = spec.id
        self.active_library_name = spec.name
        self.active_library_color = spec.color
        self.operations = registry.operations_for(spec.id)
        first = self.operations[0] if self.operations else {}
        self.active_operation = str(first.get("id", ""))
        self.active_op_description = str(first.get("description", ""))
        self.needs_x = bool(first.get("needs_x", False))
        self.needs_y = bool(first.get("needs_y", False))
        self.has_result = False
        self.explore_error = ""

    def _refresh_datasets(self) -> None:
        self.datasets = dataset_service.list_user_datasets(self.user_id)
        if not any(d["id"] == self.active_dataset_id for d in self.datasets):
            self.active_dataset_id = int(self.datasets[0]["id"]) if self.datasets else 0
        if self.active_dataset_id:
            detail = dataset_service.get_dataset_detail(self.user_id, self.active_dataset_id) or {}
            self.columns = list(detail.get("columns", []))
            self.numeric = list(detail.get("numeric", []))
            self.categorical = list(detail.get("categorical", []))
            self.x_options = self.columns
            self.y_options = self.numeric or self.columns
            if self.x_column not in self.columns:
                self.x_column = (self.categorical or self.columns or [""])[0]
            if self.y_column not in (self.numeric or self.columns):
                self.y_column = (self.numeric or self.columns or [""])[0]
        else:
            self.columns, self.numeric, self.categorical = [], [], []
            self.x_options, self.y_options = [], []

    @rx.event
    def load_page(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            prefs = settings_service.get_settings(self.user_id)
            preferred = prefs["default_library"]
            valid_ids = [spec.id for spec in registry.LIBRARIES]
            self._select_library(preferred if preferred in valid_ids else "pandas")
            self._refresh_datasets()
        except Exception as exc:
            self.explore_error = friendly(exc)

    @rx.event
    def choose_library(self, library_id: str):
        """Called from the global sidebar; then navigate to the workbench."""
        if not self._restore():
            return rx.redirect("/login")
        try:
            self._select_library(library_id)
            self._refresh_datasets()
        except Exception as exc:
            self.explore_error = friendly(exc)
        return rx.redirect("/explore")

    @rx.event
    def select_library(self, library_id: str):
        self._select_library(library_id)

    @rx.event
    def select_operation(self, operation_id: str):
        self.active_operation = operation_id
        for op in self.operations:
            if op.get("id") == operation_id:
                self.active_op_description = str(op.get("description", ""))
                self.needs_x = bool(op.get("needs_x", False))
                self.needs_y = bool(op.get("needs_y", False))
                break
        self.has_result = False

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.active_dataset_id = int(dataset_id)
        self.x_column, self.y_column = "", ""
        try:
            self._refresh_datasets()
        except Exception as exc:
            self.explore_error = friendly(exc)

    @rx.event
    def run_analysis(self):
        self.explore_error = ""
        self.is_running = True
        try:
            if not self.active_dataset_id:
                raise ValueError("Upload or select a dataset first.")
            meta, rows = dataset_service.get_all_records(self.user_id, self.active_dataset_id)
            result = engines.run(
                self.active_library,
                self.active_operation,
                {
                    "name": meta["name"],
                    "columns": meta["columns"],
                    "numeric": meta["numeric"],
                    "categorical": meta["categorical"],
                },
                rows,
                {"x_column": self.x_column, "y_column": self.y_column},
            )
            self.result_title = result["title"]
            self.result_summary = result["summary"]
            self.result_library = result["library_name"]
            self.result_color = result["library_color"]
            self.result_elapsed = result["elapsed_ms"]
            self.result_metrics = result["metrics"]
            self.result_table_columns = result["table"]["columns"]
            self.result_table_rows = result["table"]["rows"]
            self.result_chart = result["chart"]
            self.result_chart_label = result["chart_label"]
            self.result_secondary = bool(result["secondary"])
            self.result_secondary_label = result["secondary_label"]
            self.result_image = result["image"]
            self.result_notes = result["notes"]
            self.has_result = True
            with session_scope() as session:
                add_activity(
                    session,
                    self.user_id,
                    "analysis",
                    f"{result['library_name']} · {result['title']}",
                    self.active_dataset_id,
                )
        except Exception as exc:
            self.explore_error = friendly(exc)
            self.has_result = False
        finally:
            self.is_running = False

    # Field setters ---------------------------------------------------------
    @rx.event
    def set_x_column(self, value: str):
        self.x_column = value

    @rx.event
    def set_y_column(self, value: str):
        self.y_column = value

    @rx.event
    def clear_error(self):
        self.explore_error = ""
