"""Database engine, session factory and schema bootstrap."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

from . import models  # noqa: F401 - registers tables on SQLModel.metadata
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False, "timeout": 30},
    echo=False,
    pool_pre_ping=True,
)


@event.listens_for(Engine, "connect")
def _sqlite_pragmas(dbapi_connection, connection_record):  # pragma: no cover
    if settings.database_url.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """Transactional session: commits on success, rolls back on any exception.

    ``expire_on_commit=False`` is essential: services return ORM objects and the
    Reflex event handlers read their attributes *after* the ``with`` block has
    committed and closed the session. With the default ``expire_on_commit=True``
    those reads raise ``DetachedInstanceError``.
    """
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Create all tables. Safe to call repeatedly."""
    SQLModel.metadata.create_all(engine)
