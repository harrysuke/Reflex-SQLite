"""Data-mining state: DuckDB OLAP, Polars large files, clustering and association rules.

Each job runs in a ``@rx.event(background=True)`` handler with ``asyncio.to_thread``
so a long aggregation never blocks the websocket.
"""
from __future__ import annotations

import asyncio

import reflex as rx

from ..errors import friendly
from ..services import dataset_service, ml_service
from .base import AuthState

CLUSTER_ALGORITHMS = ["kmeans", "hdbscan"]
ASSOC_ALGORITHMS = ["fpgrowth", "apriori"]
AGGREGATIONS = ["mean", "sum", "count", "median", "max", "min"]


def _indexed(rows: list[dict]) -> list[dict]:
    return [{**row, "_index": position + 1} for position, row in enumerate(rows)]


class MiningState(AuthState):
    datasets: list[dict] = []
    dataset_id: int = 0
    dataset_name: str = ""
    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []

    # Clustering
    cluster_features: list[str] = []
    cluster_k: str = "3"
    cluster_algorithm: str = "kmeans"
    cluster: dict = {}
    cluster_columns: list[str] = []
    cluster_rows: list[dict] = []
    cluster_metrics: list[dict] = []
    cluster_chart: list[dict] = []
    cluster_busy: bool = False

    # Association rules
    transaction_col: str = ""
    item_col: str = ""
    assoc_algorithm: str = "fpgrowth"
    min_support: str = "0.05"
    assoc: dict = {}
    assoc_columns: list[str] = []
    assoc_rows: list[dict] = []
    assoc_metrics: list[dict] = []
    assoc_chart: list[dict] = []
    assoc_busy: bool = False

    # OLAP console
    olap_sql: str = ""
    olap: dict = {}
    olap_rows: list[dict] = []
    olap_columns: list[str] = []
    olap_chart: list[dict] = []
    olap_busy: bool = False

    # Large files
    uploads: list[dict] = []
    upload_file: str = ""
    group_by: str = ""
    value_column: str = ""
    aggregation: str = "mean"
    large: dict = {}
    large_columns: list[str] = []
    large_rows: list[dict] = []
    large_chart: list[dict] = []
    large_metrics: list[dict] = []
    large_busy: bool = False

    error: str = ""
    notice: str = ""

    @rx.var
    def has_datasets(self) -> bool:
        return len(self.datasets) > 0

    @rx.var
    def has_uploads(self) -> bool:
        return len(self.uploads) > 0

    @rx.var
    def has_olap(self) -> bool:
        return bool(self.olap)

    @rx.var
    def has_cluster(self) -> bool:
        return bool(self.cluster)

    @rx.var
    def has_assoc(self) -> bool:
        return bool(self.assoc)

    @rx.var
    def has_large(self) -> bool:
        return bool(self.large)

    @rx.var
    def upload_options(self) -> list[str]:
        return [item["name"] for item in self.uploads]

    def _default_sql(self) -> str:
        group = (self.categorical or self.columns or [""])[0]
        value = (self.numeric or [""])[0]
        if group and value:
            return (
                f"SELECT {group}, round(avg({value}), 2) AS avg_{value}, count(*) AS n\n"
                "FROM rows_flat\n"
                f"GROUP BY {group}\n"
                f"ORDER BY avg_{value} DESC"
            )
        if group:
            return f"SELECT {group}, count(*) AS n\nFROM rows_flat\nGROUP BY {group}\nORDER BY n DESC"
        return "SELECT count(*) AS n FROM rows_flat"

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
        self.cluster_features = self.numeric[:6]
        self.transaction_col = (self.categorical or self.columns or [""])[0]
        self.item_col = next((c for c in self.categorical[1:] or self.columns if c != self.transaction_col), "")
        self.olap_sql = self._default_sql()

    @rx.event
    def load_page(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            self._refresh_datasets()
            self._refresh_columns()
            self.uploads = ml_service.list_uploads()
            if self.upload_file not in [u["name"] for u in self.uploads]:
                self.upload_file = self.uploads[0]["name"] if self.uploads else ""
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.dataset_id = int(dataset_id)
        self.cluster, self.assoc, self.olap = {}, {}, {}
        self.error, self.notice = "", ""
        try:
            self._refresh_columns()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def toggle_feature(self, feature: str):
        selected = list(self.cluster_features)
        if feature in selected:
            selected.remove(feature)
        else:
            selected.append(feature)
        self.cluster_features = selected

    @rx.event
    def set_cluster_k(self, value: str):
        self.cluster_k = value

    @rx.event
    def set_cluster_algorithm(self, value: str):
        self.cluster_algorithm = value

    @rx.event
    def set_transaction_col(self, value: str):
        self.transaction_col = value

    @rx.event
    def set_item_col(self, value: str):
        self.item_col = value

    @rx.event
    def set_assoc_algorithm(self, value: str):
        self.assoc_algorithm = value

    @rx.event
    def set_min_support(self, value: str):
        self.min_support = value

    @rx.event
    def set_olap_sql(self, value: str):
        self.olap_sql = value

    @rx.event
    def reset_olap_sql(self):
        self.olap_sql = self._default_sql()

    @rx.event
    def set_upload_file(self, value: str):
        self.upload_file = value

    @rx.event
    def set_group_by(self, value: str):
        self.group_by = value

    @rx.event
    def set_value_column(self, value: str):
        self.value_column = value

    @rx.event
    def set_aggregation(self, value: str):
        self.aggregation = value

    @rx.event
    def refresh_uploads(self):
        try:
            self.uploads = ml_service.list_uploads()
            if self.upload_file not in [u["name"] for u in self.uploads]:
                self.upload_file = self.uploads[0]["name"] if self.uploads else ""
            self.notice = f"{len(self.uploads)} uploaded file(s) found."
        except Exception as exc:
            self.error = friendly(exc)

    # Background jobs -------------------------------------------------------
    @rx.event(background=True)
    async def run_cluster(self):
        async with self:
            if self.cluster_busy or not self.dataset_id or not self.cluster_features:
                return
            self.cluster_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id = self.user_id, self.dataset_id
            features = list(self.cluster_features)
            k = max(2, int(self.cluster_k or 3))
            algorithm = self.cluster_algorithm
        try:
            result = await asyncio.to_thread(
                ml_service.run_clustering, user_id, dataset_id, features, k, algorithm
            )
            async with self:
                self.cluster = result
                self.cluster_columns = list(result.get("columns", []))
                self.cluster_rows = _indexed(result.get("rows", []))
                self.cluster_metrics = list(result.get("metrics", []))
                self.cluster_chart = [
                    {"name": str(row.get("Cluster", "")), "value": row.get("Rows", 0)}
                    for row in result.get("rows", [])
                ]
                self.notice = f"{result.get('algorithm', 'KMEANS')} segmented the data into {len(result.get('rows', []))} groups."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.cluster_busy = False

    @rx.event(background=True)
    async def run_assoc(self):
        async with self:
            if self.assoc_busy or not self.dataset_id or not self.transaction_col or not self.item_col:
                return
            self.assoc_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id = self.user_id, self.dataset_id
            transaction_col, item_col = self.transaction_col, self.item_col
            algorithm = self.assoc_algorithm
            support = float(self.min_support or 0.05)
        try:
            result = await asyncio.to_thread(
                ml_service.run_association,
                user_id,
                dataset_id,
                transaction_col,
                item_col,
                algorithm=algorithm,
                min_support=support,
            )
            async with self:
                self.assoc = result
                self.assoc_columns = list(result.get("rule_columns", []))
                self.assoc_rows = _indexed(result.get("rule_rows", []))
                self.assoc_metrics = list(result.get("metrics", []))
                self.assoc_chart = list(result.get("chart", []))
                self.notice = f"{len(result.get('rule_rows', []))} association rules discovered."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.assoc_busy = False

    @rx.event(background=True)
    async def run_olap(self):
        async with self:
            if self.olap_busy or not self.dataset_id or not self.olap_sql.strip():
                return
            self.olap_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id = self.user_id, self.dataset_id
            sql = self.olap_sql
        try:
            result = await asyncio.to_thread(ml_service.run_olap, user_id, dataset_id, sql)
            async with self:
                self.olap = result
                self.olap_columns = list(result.get("columns", []))
                self.olap_rows = _indexed(result.get("rows", []))
                self.olap_chart = list(result.get("chart", []))
                self.notice = f"{result.get('row_count', 0)} rows in {result.get('elapsed_ms', 0)} ms."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.olap_busy = False

    @rx.event(background=True)
    async def run_large(self):
        async with self:
            if self.large_busy or not self.upload_file:
                return
            self.large_busy = True
            self.error, self.notice = "", ""
            filename = self.upload_file
            group_by, value_column = self.group_by, self.value_column
            aggregation = self.aggregation
        try:
            result = await asyncio.to_thread(
                ml_service.profile_large_file,
                filename,
                group_by=group_by,
                value_column=value_column,
                aggregation=aggregation,
            )
            async with self:
                self.large = result
                self.large_columns = list(result.get("group_columns", []))
                self.large_rows = _indexed(result.get("group_rows", []))
                self.large_chart = list(result.get("chart", []))
                self.large_metrics = [
                    {"label": "Rows", "value": result.get("row_count", 0), "hint": "Scanned lazily"},
                    {"label": "Columns", "value": result.get("column_count", 0), "hint": "From the file schema"},
                    {"label": "Missing", "value": result.get("missing_cells", 0), "hint": "Empty cells"},
                    {"label": "Elapsed", "value": f"{result.get('elapsed_ms', 0)} ms", "hint": "Polars streaming"},
                ]
                self.notice = f"Profiled {result.get('row_count', 0)} rows out-of-core."
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.large_busy = False
