"""User endpoints.

This module provides user-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.api.deps import CurrentUser, CurrentSuperuser, DBSession
from src.core.logging import logger
from src.core.security import get_password_hash
from src.models.user import User
from src.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentUser,
) -> User:
    """Get current user information.

    Args:
        current_user: Current authenticated user.

    Returns:
        Current user information.
    """
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user: CurrentUser,
    db: DBSession,
) -> User:
    """Update current user information.

    Args:
        update_data: Fields to update.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        Updated user information.
    """
    # Check if email is already taken (before transaction)
    if update_data.email is not None:
        stmt = select(User).where(
            User.email == update_data.email,
            User.id != current_user.id,
        )
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )

    # Update allowed fields within transaction
    async with db.begin():
        if update_data.name is not None:
            current_user.name = update_data.name

        if update_data.email is not None:
            current_user.email = update_data.email

        if update_data.password is not None:
            current_user.hashed_password = get_password_hash(update_data.password)

        await db.flush()

    logger.info("User updated", user_id=current_user.id)

    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: CurrentSuperuser,
    db: DBSession,
) -> User:
    """Get user by ID (superuser only).

    Args:
        user_id: User ID to retrieve.
        current_user: Current authenticated superuser.
        db: Database session.

    Returns:
        User information.

    Raises:
        HTTPException: If user not found.
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get("/", response_model=list[UserResponse])
async def list_users(
    current_user: CurrentSuperuser,
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    """List all users (superuser only).

    Args:
        current_user: Current authenticated superuser.
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List of users.
    """
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: CurrentSuperuser,
    db: DBSession,
) -> None:
    """Delete user by ID (superuser only).

    Args:
        user_id: User ID to delete.
        current_user: Current authenticated superuser.
        db: Database session.

    Raises:
        HTTPException: If user not found or trying to delete self.
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    async with db.begin():
        await db.delete(user)

    logger.info("User deleted", user_id=user_id, deleted_by=current_user.id)
