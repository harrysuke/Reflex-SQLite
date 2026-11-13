"""Predictive analytics state: training, the model registry, live inference and drift.

Training runs as a background event (offloaded with ``asyncio.to_thread``).
Inference itself is cheap — the ``.joblib`` bundle is cached once at backend
startup — so the predict handler runs inline and logs each call to ``model_logs``.
"""
from __future__ import annotations

import asyncio

import reflex as rx

from ml_pipelines import _optional as deps

from ..errors import friendly
from ..services import dataset_service, ml_service
from .base import AuthState

ALGORITHMS = ["random_forest", "gradient_boosting", "linear", "xgboost", "lightgbm"]
TASKS = ["auto", "regression", "classification"]


def _indexed(rows: list[dict]) -> list[dict]:
    return [{**row, "_index": position + 1} for position, row in enumerate(rows)]


class ModelsState(AuthState):
    datasets: list[dict] = []
    dataset_id: int = 0
    dataset_name: str = ""
    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []

    target: str = ""
    algorithm: str = "random_forest"
    task: str = "auto"
    model_name: str = ""
    train_busy: bool = False

    models: list[dict] = []
    active: dict = {}
    last_training: dict = {}

    predict_form: dict[str, str] = {}
    last_prediction: dict = {}

    logs: list[dict] = []
    drift: dict = {}
    drift_chart: list[dict] = []
    drift_metrics: list[dict] = []

    resolve_options: list[str] = []
    resolve_id: str = ""
    actual_value: str = ""

    error: str = ""
    notice: str = ""

    @rx.var
    def has_datasets(self) -> bool:
        return len(self.datasets) > 0

    @rx.var
    def env_warning(self) -> str:
        """Preflight: name the missing libraries before the user clicks Train."""
        return deps.warning(("pandas", "sklearn", "joblib"))

    @rx.var
    def has_models(self) -> bool:
        return len(self.models) > 0

    @rx.var
    def has_active(self) -> bool:
        return bool(self.active.get("loaded"))

    @rx.var
    def active_label(self) -> str:
        if not self.active.get("loaded"):
            return "No active model"
        return f"{self.active.get('name', '')} · {self.active.get('algorithm', '')} · {self.active.get('target', '')}"

    @rx.var
    def feature_columns(self) -> list[str]:
        return list(self.active.get("features", []))

    @rx.var
    def target_options(self) -> list[str]:
        return self.columns or self.numeric

    @rx.var
    def prediction_label(self) -> str:
        return str(self.last_prediction.get("label", ""))

    @rx.var
    def active_metrics(self) -> list[dict]:
        metrics = self.active.get("metrics", {}) or {}
        return [
            {"label": str(key).replace("_", " ").title(), "value": value, "hint": ""}
            for key, value in metrics.items()
        ]

    @rx.var
    def log_columns(self) -> list[str]:
        return ["id", "model", "target", "predicted", "actual", "created"]

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
        if self.target not in self.columns:
            self.target = (self.numeric or self.columns or [""])[0]

    def _load_registry(self) -> None:
        self.models = _indexed(ml_service.list_models())
        self.active = ml_service.active_model()
        features = list(self.active.get("features", []))
        self.predict_form = {feature: self.predict_form.get(feature, "") for feature in features}

    def _load_logs(self) -> None:
        self.logs = _indexed(ml_service.model_logs(limit=40))
        self.resolve_options = [f"#{row['id']}" for row in self.logs if not row["resolved"]]
        if self.resolve_id not in self.resolve_options:
            self.resolve_id = self.resolve_options[0] if self.resolve_options else ""

    def _load_drift(self) -> None:
        summary = ml_service.drift(window=10)
        self.drift = summary
        self.drift_chart = list(summary.get("chart", []))
        self.drift_metrics = [
            {**metric, "value": "—" if metric.get("value") is None else metric["value"]}
            for metric in summary.get("metrics", [])
        ]

    @rx.event
    def load_page(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            self._refresh_datasets()
            self._refresh_columns()
            self._load_registry()
            self._load_logs()
            self._load_drift()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.dataset_id = int(dataset_id)
        self.last_prediction = {}
        self.error, self.notice = "", ""
        try:
            self._refresh_columns()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def set_target(self, value: str):
        self.target = value

    @rx.event
    def set_algorithm(self, value: str):
        self.algorithm = value

    @rx.event
    def set_task(self, value: str):
        self.task = value

    @rx.event
    def set_model_name(self, value: str):
        self.model_name = value

    @rx.event
    def set_predict_field(self, key: str, value: str):
        updated = dict(self.predict_form)
        updated[key] = value
        self.predict_form = updated

    @rx.event
    def set_resolve_id(self, value: str):
        self.resolve_id = value

    @rx.event
    def set_actual_value(self, value: str):
        self.actual_value = value

    @rx.event(background=True)
    async def train(self):
        async with self:
            if self.train_busy or not self.dataset_id or not self.target:
                return
            self.train_busy = True
            self.error, self.notice = "", ""
            user_id, dataset_id, target = self.user_id, self.dataset_id, self.target
            algorithm, task, name = self.algorithm, self.task, self.model_name
        try:
            meta = await asyncio.to_thread(
                ml_service.run_training,
                user_id,
                dataset_id,
                target,
                algorithm=algorithm,
                task="" if task == "auto" else task,
                name=name,
            )
            async with self:
                self.last_training = meta
                self.notice = (
                    f"Trained {meta['algorithm']} for '{meta['target']}' ({meta['task']})."
                )
                self._load_registry()
        except Exception as exc:
            async with self:
                self.error = friendly(exc)
        finally:
            async with self:
                self.train_busy = False

    @rx.event
    def activate(self, name: str):
        try:
            self.active = ml_service.activate_model(name)
            self._load_registry()
            self.notice = f"Activated {name}."
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def refresh_registry(self):
        try:
            self._load_registry()
            self._load_logs()
            self._load_drift()
            self.notice = "Registry refreshed."
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def predict_now(self):
        if not self.active.get("loaded"):
            self.error = "Train and activate a model first."
            return
        try:
            payload = {key: value for key, value in self.predict_form.items()}
            result = ml_service.predict_and_log(self.user_id, self.dataset_id, payload)
            if result is None:
                self.error = "The active model belongs to a different dataset. Train one for this dataset."
                return
            self.last_prediction = result
            self.notice = f"Prediction: {result.get('label', '')}"
            self._load_logs()
            self._load_drift()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def resolve_outcome(self):
        raw = (self.resolve_id or "").lstrip("#").strip()
        if not raw.isdigit():
            self.error = "Choose a prediction log first."
            return
        if not self.actual_value.strip():
            self.error = "Enter the observed actual value."
            return
        try:
            ml_service.resolve_log(int(raw), self.actual_value.strip())
            self.actual_value = ""
            self.notice = "Outcome recorded; drift metrics updated."
            self._load_logs()
            self._load_drift()
        except Exception as exc:
            self.error = friendly(exc)
