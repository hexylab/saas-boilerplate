"""User schemas.

This module defines Pydantic schemas for user-related operations.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields.

    Attributes:
        email: User's email address.
        name: User's display name.
    """

    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a new user.

    Attributes:
        email: User's email address.
        name: User's display name.
        password: Plain text password (will be hashed).
    """

    password: str


class UserUpdate(BaseModel):
    """Schema for updating an existing user.

    All fields are optional.

    Attributes:
        email: User's email address.
        name: User's display name.
        password: Plain text password (will be hashed).
        is_active: Whether the user account is active.
    """

    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for user response.

    Attributes:
        id: User's ID.
        email: User's email address.
        name: User's display name.
        is_active: Whether the user account is active.
        is_superuser: Whether the user has superuser privileges.
        created_at: Timestamp when the user was created.
        updated_at: Timestamp when the user was last updated.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserInDB(UserResponse):
    """Schema for user with hashed password.

    Used internally, not exposed via API.

    Attributes:
        hashed_password: Bcrypt hashed password.
    """

    hashed_password: str | None = None


class Token(BaseModel):
    """JWT token response schema.

    Attributes:
        access_token: The JWT access token.
        token_type: The token type (always "bearer").
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload schema.

    Attributes:
        sub: Subject (user ID or email).
        exp: Expiration timestamp.
    """

    sub: str
    exp: datetime | None = None


class LoginRequest(BaseModel):
    """Login request schema.

    Attributes:
        email: User's email address.
        password: User's password.
    """

    email: EmailStr
    password: str
