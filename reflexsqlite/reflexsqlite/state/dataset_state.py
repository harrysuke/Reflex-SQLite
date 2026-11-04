"""Dataset manager state: upload, list, paginate, create/edit/delete rows."""
from __future__ import annotations

import math

import reflex as rx

from ..errors import friendly
from ..services import dataset_service
from .base import AuthState


class DatasetState(AuthState):
    datasets: list[dict] = []
    active_dataset_id: int = 0
    detail: dict = {}

    columns: list[str] = []
    numeric: list[str] = []
    categorical: list[str] = []
    table_rows: list[dict] = []
    total_rows: int = 0
    page: int = 1
    page_size: int = 10
    row_search: str = ""
    dataset_search: str = ""

    upload_description: str = ""
    upload_message: str = ""
    upload_error: str = ""
    is_uploading: bool = False

    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_meta_dialog: bool = False
    editing_row_id: int = 0
    form_values: dict[str, str] = {}
    meta_name: str = ""
    meta_description: str = ""
    notice: str = ""
    error: str = ""

    @rx.var
    def has_datasets(self) -> bool:
        return len(self.datasets) > 0

    @rx.var
    def page_count(self) -> int:
        return max(1, math.ceil(self.total_rows / max(1, self.page_size)))

    @rx.var
    def active_name(self) -> str:
        return str(self.detail.get("name", "No dataset selected"))

    def _refresh_datasets(self) -> None:
        self.datasets = dataset_service.list_user_datasets(self.user_id, self.dataset_search)
        if not any(d["id"] == self.active_dataset_id for d in self.datasets):
            self.active_dataset_id = int(self.datasets[0]["id"]) if self.datasets else 0

    def _refresh_detail(self) -> None:
        self.detail = dataset_service.get_dataset_detail(self.user_id, self.active_dataset_id) or {}
        self.columns = list(self.detail.get("columns", []))
        self.numeric = list(self.detail.get("numeric", []))
        self.categorical = list(self.detail.get("categorical", []))
        self.meta_name = str(self.detail.get("name", ""))
        self.meta_description = str(self.detail.get("description", ""))

    def _refresh_table(self) -> None:
        if not self.active_dataset_id:
            self.table_rows = []
            self.total_rows = 0
            return
        payload = dataset_service.get_table_page(
            self.user_id, self.active_dataset_id, self.page, self.page_size, self.row_search
        )
        self.table_rows = payload["rows"]
        self.total_rows = int(payload["total"])
        self.columns = payload["columns"]

    def _blank_form(self) -> None:
        self.form_values = {c: "" for c in self.columns}

    @rx.event
    def load_page(self):
        if not self._restore():
            return rx.redirect("/login")
        try:
            self._refresh_datasets()
            if self.active_dataset_id:
                self._refresh_detail()
                self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not self._restore():
            return rx.redirect("/login")
        if not files:
            return
        self.is_uploading = True
        self.upload_message, self.upload_error = "", ""
        for file in files:
            try:
                data = await file.read()
                new_id = dataset_service.ingest_upload(
                    self.user_id, file.name or "dataset.csv", data, self.upload_description
                )
                self.active_dataset_id = new_id
                self.upload_message = f"Imported {file.name} successfully."
                self.page = 1
                self.row_search = ""
            except Exception as exc:
                self.upload_error = friendly(exc)
        self.is_uploading = False
        try:
            self._refresh_datasets()
            self._refresh_detail()
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def select_dataset(self, dataset_id: int):
        self.active_dataset_id = int(dataset_id)
        self.page = 1
        self.row_search = ""
        self.notice, self.error = "", ""
        try:
            self._refresh_detail()
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def set_row_search(self, value: str):
        self.row_search = value
        self.page = 1
        try:
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def set_dataset_search(self, value: str):
        self.dataset_search = value
        try:
            self._refresh_datasets()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def set_page_size(self, value: str):
        try:
            self.page_size = max(1, int(value))
        except ValueError:
            self.page_size = 10
        self.page = 1
        self._refresh_table()

    @rx.event
    def next_page(self):
        if self.page < self.page_count:
            self.page += 1
            self._refresh_table()

    @rx.event
    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self._refresh_table()

    # Row CRUD --------------------------------------------------------------
    @rx.event
    def open_add(self):
        if not self.active_dataset_id:
            self.error = "Upload or select a dataset first."
            return
        self._blank_form()
        self.editing_row_id = 0
        self.show_add_dialog = True
        self.error = ""

    @rx.event
    def open_edit(self, row_id: int):
        try:
            record = dataset_service.get_record(self.user_id, self.active_dataset_id, int(row_id))
        except Exception as exc:
            self.error = friendly(exc)
            return
        if record is None:
            self.error = "That row no longer exists."
            return
        self.form_values = {c: "" if record.get(c) is None else str(record.get(c)) for c in self.columns}
        self.editing_row_id = int(row_id)
        self.show_edit_dialog = True
        self.error = ""

    @rx.event
    def close_dialogs(self):
        self.show_add_dialog = False
        self.show_edit_dialog = False
        self.show_meta_dialog = False

    @rx.event
    def set_form_field(self, key: str, value: str):
        updated = dict(self.form_values)
        updated[key] = value
        self.form_values = updated

    @rx.event
    def save_new_row(self):
        try:
            dataset_service.add_record(self.user_id, self.active_dataset_id, self.form_values)
            self.show_add_dialog = False
            self.notice = "Row added."
            self._refresh_datasets()
            self._refresh_detail()
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def save_edited_row(self):
        try:
            dataset_service.edit_record(
                self.user_id, self.active_dataset_id, self.editing_row_id, self.form_values
            )
            self.show_edit_dialog = False
            self.notice = "Row updated."
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def delete_row(self, row_id: int):
        try:
            dataset_service.delete_record(self.user_id, self.active_dataset_id, int(row_id))
            self.notice = "Row deleted."
            self._refresh_datasets()
            self._refresh_detail()
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    # Dataset CRUD ----------------------------------------------------------
    @rx.event
    def open_meta(self):
        if not self.active_dataset_id:
            return
        self.show_meta_dialog = True

    @rx.event
    def save_metadata(self):
        try:
            dataset_service.rename_dataset(
                self.user_id, self.active_dataset_id, self.meta_name, self.meta_description
            )
            self.show_meta_dialog = False
            self.notice = "Dataset details saved."
            self._refresh_datasets()
            self._refresh_detail()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def delete_dataset(self):
        if not self.active_dataset_id:
            return
        try:
            dataset_service.remove_dataset(self.user_id, self.active_dataset_id)
            self.active_dataset_id = 0
            self.notice = "Dataset deleted."
            self._refresh_datasets()
            self._refresh_detail()
            self._refresh_table()
        except Exception as exc:
            self.error = friendly(exc)

    @rx.event
    def download_csv(self):
        if not self.active_dataset_id:
            return
        try:
            filename, data = dataset_service.export_csv(self.user_id, self.active_dataset_id)
            return rx.download(data=data, filename=filename)
        except Exception as exc:
            self.error = friendly(exc)

    # Field setters ---------------------------------------------------------
    @rx.event
    def set_upload_description(self, value: str):
        self.upload_description = value

    @rx.event
    def set_meta_name(self, value: str):
        self.meta_name = value

    @rx.event
    def set_meta_description(self, value: str):
        self.meta_description = value

    @rx.event
    def clear_notices(self):
        self.notice = ""
        self.error = ""
