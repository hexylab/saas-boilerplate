"""User model.

This module defines the User SQLAlchemy model.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import BaseModel


class User(BaseModel):
    """User model.

    Represents a user in the system.

    Attributes:
        id: Primary key.
        email: User's email address (unique).
        hashed_password: Bcrypt hashed password.
        name: User's display name.
        is_active: Whether the user account is active.
        is_superuser: Whether the user has superuser privileges.
        external_id: External ID from auth provider (e.g., Cognito sub).
        created_at: Timestamp when the user was created.
        updated_at: Timestamp when the user was last updated.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,  # Null for external auth providers
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    external_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=True,  # For external auth providers like Cognito
    )

    def __repr__(self) -> str:
        """Return string representation of the user.

        Returns:
            String representation.
        """
        return f"<User(id={self.id}, email={self.email})>"
