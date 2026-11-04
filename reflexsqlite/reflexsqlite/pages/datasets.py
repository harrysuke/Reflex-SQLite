"""Dataset manager: upload, browse, edit and delete records in SQLite."""
from __future__ import annotations

import reflex as rx

from ..components import ui
from ..components.layout import shell
from ..components.theme import ACCENT, FAINT, MUTED, PRIMARY, PRIMARY_SOFT, SURFACE_ALT, TEXT
from ..state import DatasetState


def _upload_card():
    return ui.card(
        ui.section_title("Upload a dataset", "CSV, TSV, JSON, XLSX or XLS - stored row by row in SQLite"),
        rx.hstack(
            rx.box(
                rx.upload(
                    rx.vstack(
                        rx.box(
                            rx.text("UP", font_size="13px", font_weight="800", color="white"),
                            background=PRIMARY,
                            border_radius="10px",
                            width="38px",
                            height="38px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        rx.text("Drop a file here or click to browse", font_size="12px", font_weight="600", color=TEXT),
                        rx.text("Maximum 25 MB · headers are read automatically", font_size="10px", color=MUTED),
                        gap="8px",
                        align_items="center",
                        padding="18px",
                    ),
                    id="dataset_upload",
                    border="2px dashed #C7D2FE",
                    border_radius="12px",
                    background=PRIMARY_SOFT,
                    width="100%",
                    padding="6px",
                ),
                width="100%",
            ),
            rx.vstack(
                ui.field(
                    "Description (optional)",
                    ui.text_input(DatasetState.upload_description, DatasetState.set_upload_description, "What is this dataset about?"),
                ),
                ui.primary_button(
                    "Import dataset",
                    on_click=DatasetState.handle_upload(rx.upload_files("dataset_upload")),
                    width="100%",
                    disabled=DatasetState.is_uploading,
                ),
                rx.text("Accepted: .csv .tsv .txt .json .xlsx .xls", font_size="10px", color=FAINT),
                gap="10px",
                width="290px",
                min_width="240px",
                align_items="start",
            ),
            gap="16px",
            width="100%",
            align_items="start",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        ui.notice_banner(DatasetState.upload_message, "success"),
        ui.notice_banner(DatasetState.upload_error),
        padding="20px",
    )


def _dataset_tile(item):
    return rx.button(
        rx.vstack(
            rx.hstack(
                ui.pill(item["format"], PRIMARY, PRIMARY_SOFT, "#DDD6FE"),
                rx.box(flex="1"),
                rx.text(item["updated"], font_size="9px", color=FAINT),
                width="100%",
                align_items="center",
            ),
            rx.text(item["name"], font_size="13px", font_weight="700", color=TEXT, text_align="left", width="100%"),
            rx.text(item["description"], font_size="10px", color=MUTED, text_align="left", width="100%"),
            rx.hstack(
                rx.text(f"{item['rows']} rows", font_size="10px", color=MUTED),
                rx.text(f"{item['columns']} cols", font_size="10px", color=MUTED),
                rx.text(f"{item['size_kb']} KB", font_size="10px", color=MUTED),
                gap="12px",
                width="100%",
            ),
            gap="6px",
            align_items="start",
            width="100%",
        ),
        on_click=DatasetState.select_dataset(item["id"]),
        background=SURFACE_ALT,
        border="1px solid #E5E8F1",
        border_radius="12px",
        padding="14px",
        cursor="pointer",
        width="230px",
        text_align="left",
        _hover={"border": "1px solid #C7D2FE"},
    )


def _dataset_list():
    return ui.card(
        ui.section_title("Your datasets", "Select one to inspect and edit its rows"),
        rx.box(
            ui.text_input(DatasetState.dataset_search, DatasetState.set_dataset_search, "Search datasets by name or filename"),
            width="260px",
            margin_top="12px",
        ),
        rx.hstack(
            rx.foreach(DatasetState.datasets, _dataset_tile),
            gap="12px",
            flex_wrap="wrap",
            margin_top="14px",
            width="100%",
        ),
        padding="20px",
        width="100%",
    )


def _row_actions(item):
    return rx.hstack(
        ui.ghost_button("Edit", on_click=DatasetState.open_edit(item["_id"]), padding="5px 9px"),
        ui.danger_button("Delete", on_click=DatasetState.delete_row(item["_id"]), padding="5px 9px"),
        gap="6px",
    )


def _table_card():
    return ui.card(
        rx.hstack(
            rx.vstack(
                rx.text("Dataset rows", font_size="16px", font_weight="700", color=TEXT),
                rx.text(DatasetState.active_name, font_size="11px", color=MUTED),
                gap="2px",
                align_items="start",
            ),
            rx.box(flex="1"),
            ui.ghost_button("Edit details", on_click=DatasetState.open_meta),
            ui.ghost_button("Export CSV", on_click=DatasetState.download_csv),
            ui.danger_button("Delete dataset", on_click=DatasetState.delete_dataset),
            ui.primary_button("Add row", on_click=DatasetState.open_add),
            gap="8px",
            align_items="center",
            flex_wrap="wrap",
            width="100%",
        ),
        rx.hstack(
            rx.box(
                ui.text_input(DatasetState.row_search, DatasetState.set_row_search, "Search rows..."),
                width="260px",
            ),
            rx.box(flex="1"),
            rx.text("Rows per page", font_size="11px", color=MUTED),
            rx.select(
                ["5", "10", "20", "50"],
                value="10",
                on_change=DatasetState.set_page_size,
                width="90px",
                size="1",
            ),
            gap="10px",
            align_items="center",
            width="100%",
            margin_top="14px",
            flex_wrap="wrap",
        ),
        rx.cond(
            DatasetState.has_datasets,
            rx.box(
                ui.data_table(DatasetState.columns, DatasetState.table_rows, _row_actions),
                margin_top="12px",
                width="100%",
            ),
            ui.empty_state("No datasets yet", "Upload a CSV, JSON or Excel file to start creating records."),
        ),
        rx.hstack(
            rx.text(DatasetState.total_rows, font_size="11px", color=MUTED),
            rx.text("matching rows", font_size="11px", color=MUTED),
            rx.box(flex="1"),
            ui.ghost_button("Previous", on_click=DatasetState.prev_page),
            rx.text("Page", font_size="11px", color=MUTED),
            rx.text(DatasetState.page, font_size="11px", font_weight="700", color=TEXT),
            rx.text("of", font_size="11px", color=MUTED),
            rx.text(DatasetState.page_count, font_size="11px", font_weight="700", color=TEXT),
            ui.ghost_button("Next", on_click=DatasetState.next_page),
            gap="8px",
            align_items="center",
            width="100%",
            margin_top="12px",
        ),
        ui.notice_banner(DatasetState.notice, "success"),
        ui.notice_banner(DatasetState.error),
        padding="20px",
        width="100%",
    )


def _row_form():
    def row_field(column):
        return ui.field(
            column,
            rx.input(
                value=DatasetState.form_values[column],
                on_change=lambda value: DatasetState.set_form_field(column, value),
                placeholder=f"Value for {column}",
                width="100%",
                border="1px solid #E5E8F1",
                border_radius="9px",
                padding="9px 11px",
                font_size="12px",
            ),
        )

    return rx.vstack(
        rx.foreach(DatasetState.columns, row_field),
        gap="10px",
        width="100%",
        align_items="start",
    )


def _modals():
    return rx.fragment(
        rx.cond(
            DatasetState.show_add_dialog,
            ui.modal(
                "Add a new row",
                _row_form(),
                rx.hstack(
                    ui.primary_button("Create row", on_click=DatasetState.save_new_row),
                    ui.ghost_button("Cancel", on_click=DatasetState.close_dialogs),
                    gap="10px",
                ),
            ),
        ),
        rx.cond(
            DatasetState.show_edit_dialog,
            ui.modal(
                "Edit row",
                _row_form(),
                rx.hstack(
                    ui.primary_button("Save changes", on_click=DatasetState.save_edited_row),
                    ui.ghost_button("Cancel", on_click=DatasetState.close_dialogs),
                    gap="10px",
                ),
            ),
        ),
        rx.cond(
            DatasetState.show_meta_dialog,
            ui.modal(
                "Dataset details",
                ui.field("Name", ui.text_input(DatasetState.meta_name, DatasetState.set_meta_name, "Dataset name")),
                ui.field(
                    "Description",
                    rx.text_area(
                        value=DatasetState.meta_description,
                        on_change=DatasetState.set_meta_description,
                        placeholder="Describe this dataset",
                        width="100%",
                        min_height="90px",
                        border="1px solid #E5E8F1",
                        border_radius="9px",
                        padding="10px 12px",
                        font_size="12px",
                    ),
                ),
                rx.hstack(
                    ui.primary_button("Save", on_click=DatasetState.save_metadata),
                    ui.ghost_button("Cancel", on_click=DatasetState.close_dialogs),
                    gap="10px",
                ),
            ),
        ),
    )


def datasets():
    return shell(
        "Datasets",
        "Upload, search, create, update and delete records",
        _upload_card(),
        _dataset_list(),
        _table_card(),
        _modals(),
    )
