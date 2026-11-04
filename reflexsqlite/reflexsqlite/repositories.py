"""Repository layer: the only module allowed to issue database queries.

Services call these functions; event handlers never touch a Session directly.
"""
from __future__ import annotations

import json
from datetime import timedelta
from typing import Any

from sqlalchemy import func, or_
from sqlmodel import Session, select

from .models import (
    ActivityLog,
    AuthSession,
    Dataset,
    DatasetRow,
    MetricPoint,
    User,
    UserSetting,
    now_iso,
    utcnow,
)

# --------------------------------------------------------------------------- #
# Users
# --------------------------------------------------------------------------- #


def create_user(session: Session, **fields: Any) -> User:
    user = User(**fields)
    session.add(user)
    session.flush()
    return user


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def find_user_by_login(session: Session, login: str) -> User | None:
    needle = login.strip().lower()
    return session.exec(
        select(User).where(or_(func.lower(User.username) == needle, func.lower(User.email) == needle))
    ).first()


def user_exists(session: Session, username: str, email: str) -> bool:
    return (
        session.exec(
            select(User.id).where(
                or_(
                    func.lower(User.username) == username.strip().lower(),
                    func.lower(User.email) == email.strip().lower(),
                )
            )
        ).first()
        is not None
    )


def list_users(session: Session) -> list[User]:
    return list(session.exec(select(User).order_by(User.created_at)))


def save_user(session: Session, user: User) -> User:
    session.add(user)
    session.flush()
    return user


# --------------------------------------------------------------------------- #
# Auth sessions
# --------------------------------------------------------------------------- #


def create_auth_session(session: Session, user_id: int, token: str, ttl_hours: int) -> AuthSession:
    record = AuthSession(
        user_id=user_id,
        token=token,
        expires_at=(utcnow() + timedelta(hours=ttl_hours)).isoformat(timespec="seconds"),
    )
    session.add(record)
    session.flush()
    return record


def get_valid_session(session: Session, token: str) -> AuthSession | None:
    record = session.exec(select(AuthSession).where(AuthSession.token == token)).first()
    if record is None or record.expires_at < now_iso():
        return None
    return record


def delete_auth_session(session: Session, token: str) -> None:
    for record in session.exec(select(AuthSession).where(AuthSession.token == token)):
        session.delete(record)
    session.flush()


# --------------------------------------------------------------------------- #
# User settings
# --------------------------------------------------------------------------- #


def get_or_create_settings(session: Session, user_id: int) -> UserSetting:
    record = session.exec(select(UserSetting).where(UserSetting.user_id == user_id)).first()
    if record is None:
        record = UserSetting(user_id=user_id)
        session.add(record)
        session.flush()
    return record


def save_settings(session: Session, record: UserSetting) -> UserSetting:
    record.updated_at = now_iso()
    session.add(record)
    session.flush()
    return record


# --------------------------------------------------------------------------- #
# Datasets
# --------------------------------------------------------------------------- #


def create_dataset(session: Session, **fields: Any) -> Dataset:
    dataset = Dataset(**fields)
    session.add(dataset)
    session.flush()
    return dataset


def get_dataset(session: Session, dataset_id: int, owner_id: int | None = None) -> Dataset | None:
    dataset = session.get(Dataset, dataset_id)
    if dataset is None:
        return None
    if owner_id is not None and dataset.owner_id != owner_id:
        return None
    return dataset


def list_datasets(session: Session, owner_id: int, search: str = "") -> list[Dataset]:
    query = select(Dataset).where(Dataset.owner_id == owner_id)
    if search.strip():
        like = f"%{search.strip()}%"
        query = query.where(or_(Dataset.name.ilike(like), Dataset.filename.ilike(like)))
    return list(session.exec(query.order_by(Dataset.updated_at.desc())))


def count_datasets(session: Session, owner_id: int) -> int:
    return session.exec(
        select(func.count()).select_from(Dataset).where(Dataset.owner_id == owner_id)
    ).one()


def save_dataset(session: Session, dataset: Dataset) -> Dataset:
    dataset.updated_at = now_iso()
    session.add(dataset)
    session.flush()
    return dataset


def delete_dataset(session: Session, dataset: Dataset) -> None:
    for table in (DatasetRow, ActivityLog, MetricPoint):
        for record in session.exec(select(table).where(table.dataset_id == dataset.id)):
            session.delete(record)
    session.delete(dataset)
    session.flush()


def bulk_insert_rows(session: Session, dataset_id: int, rows: list[dict[str, Any]]) -> int:
    for index, row in enumerate(rows):
        session.add(
            DatasetRow(
                dataset_id=dataset_id,
                row_index=index,
                payload=json.dumps(row, ensure_ascii=False, default=str),
            )
        )
    session.flush()
    return len(rows)


def list_rows(
    session: Session,
    dataset_id: int,
    offset: int = 0,
    limit: int = 10,
    search: str = "",
) -> tuple[list[DatasetRow], int]:
    base = select(DatasetRow).where(DatasetRow.dataset_id == dataset_id)
    total = session.exec(
        select(func.count()).select_from(DatasetRow).where(DatasetRow.dataset_id == dataset_id)
    ).one()
    if search.strip():
        base = base.where(DatasetRow.payload.ilike(f"%{search.strip()}%"))
    matched = (
        total
        if not search.strip()
        else session.exec(
            select(func.count())
            .select_from(DatasetRow)
            .where(DatasetRow.dataset_id == dataset_id, DatasetRow.payload.ilike(f"%{search.strip()}%"))
        ).one()
    )
    rows = list(
        session.exec(
            base.order_by(DatasetRow.row_index).offset(offset).limit(limit)
        )
    )
    return rows, int(matched)


def all_rows(session: Session, dataset_id: int, limit: int | None = None) -> list[dict[str, Any]]:
    query = select(DatasetRow).where(DatasetRow.dataset_id == dataset_id).order_by(DatasetRow.row_index)
    if limit is not None:
        query = query.limit(limit)
    return [row.as_dict() for row in session.exec(query)]


def get_row(session: Session, row_id: int, dataset_id: int) -> DatasetRow | None:
    row = session.get(DatasetRow, row_id)
    if row is None or row.dataset_id != dataset_id:
        return None
    return row


def add_row(session: Session, dataset_id: int, payload: dict[str, Any]) -> DatasetRow:
    max_index = session.exec(
        select(func.coalesce(func.max(DatasetRow.row_index), -1)).where(
            DatasetRow.dataset_id == dataset_id
        )
    ).one()
    row = DatasetRow(
        dataset_id=dataset_id,
        row_index=int(max_index) + 1,
        payload=json.dumps(payload, ensure_ascii=False, default=str),
    )
    session.add(row)
    session.flush()
    return row


def save_row(session: Session, row: DatasetRow, payload: dict[str, Any]) -> DatasetRow:
    row.payload = json.dumps(payload, ensure_ascii=False, default=str)
    row.updated_at = now_iso()
    session.add(row)
    session.flush()
    return row


def delete_row(session: Session, row: DatasetRow) -> None:
    session.delete(row)
    session.flush()


# --------------------------------------------------------------------------- #
# Activity + live metrics
# --------------------------------------------------------------------------- #


def add_activity(
    session: Session, user_id: int, action: str, detail: str, dataset_id: int | None = None
) -> None:
    session.add(ActivityLog(user_id=user_id, dataset_id=dataset_id, action=action, detail=detail))
    session.flush()


def recent_activity(session: Session, user_id: int, limit: int = 8) -> list[ActivityLog]:
    return list(
        session.exec(
            select(ActivityLog)
            .where(ActivityLog.user_id == user_id)
            .order_by(ActivityLog.id.desc())
            .limit(limit)
        )
    )


def add_metric_point(session: Session, dataset_id: int, label: str, value: float, series: str = "value") -> None:
    session.add(MetricPoint(dataset_id=dataset_id, label=label, value=value, series=series))
    session.flush()


def recent_points(session: Session, dataset_id: int, limit: int = 24) -> list[MetricPoint]:
    rows = list(
        session.exec(
            select(MetricPoint)
            .where(MetricPoint.dataset_id == dataset_id)
            .order_by(MetricPoint.id.desc())
            .limit(limit)
        )
    )
    return list(reversed(rows))


def clear_points(session: Session, dataset_id: int) -> None:
    for record in session.exec(select(MetricPoint).where(MetricPoint.dataset_id == dataset_id)):
        session.delete(record)
    session.flush()


def trim_points(session: Session, dataset_id: int, keep: int = 120) -> None:
    """Keep only the newest `keep` samples so a long live stream stays bounded."""
    stale = list(
        session.exec(
            select(MetricPoint)
            .where(MetricPoint.dataset_id == dataset_id)
            .order_by(MetricPoint.id.desc())
            .offset(keep)
        )
    )
    for record in stale:
        session.delete(record)
    if stale:
        session.flush()
