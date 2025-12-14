"""SQLAlchemy base model.

This module provides the base class for all SQLAlchemy models.
"""

from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Provides common columns and functionality for all models.
    """

    pass


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns.

    Attributes:
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """Base model with ID and timestamp columns.

    All domain models should inherit from this class.

    Attributes:
        id: Primary key.
        created_at: Timestamp when the record was created.
        updated_at: Timestamp when the record was last updated.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
