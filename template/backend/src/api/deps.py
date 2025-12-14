"""API dependencies.

This module provides common dependencies for API endpoints.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.auth import AuthProvider, get_auth_provider
{%- if include_advanced_auth %}
from src.adapters.auth.base import AuthUser
{%- else %}
from src.adapters.auth.mock import AuthUser
{%- endif %}
from src.db.session import get_db
from src.models.user import User

# Security scheme
security = HTTPBearer()


async def get_current_auth_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth: Annotated[AuthProvider, Depends(get_auth_provider)],
) -> AuthUser:
    """Get the current authenticated user from token.

    Args:
        credentials: HTTP Bearer credentials.
        auth: Authentication provider.

    Returns:
        Authenticated user information.

    Raises:
        HTTPException: If authentication fails.
    """
    auth_user = await auth.verify_token(credentials.credentials)

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_user


async def get_current_user(
    auth_user: Annotated[AuthUser, Depends(get_current_auth_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get the current user from database.

    Args:
        auth_user: Authenticated user from token.
        db: Database session.

    Returns:
        User model from database.

    Raises:
        HTTPException: If user not found in database.
    """
    # Try to find user by external_id first, then by email
    stmt = select(User).where(
        (User.external_id == auth_user.external_id) | (User.email == auth_user.email)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user


async def get_current_active_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get the current active superuser.

    Args:
        current_user: Current authenticated user.

    Returns:
        User if they are a superuser.

    Raises:
        HTTPException: If user is not a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return current_user


# Type aliases for cleaner dependency injection
CurrentAuthUser = Annotated[AuthUser, Depends(get_current_auth_user)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentSuperuser = Annotated[User, Depends(get_current_active_superuser)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
Auth = Annotated[AuthProvider, Depends(get_auth_provider)]
