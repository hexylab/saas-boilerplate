"""Authentication endpoints.

This module provides authentication-related API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.adapters.auth.base import AuthenticationError, UserExistsError
from src.adapters.auth.mock import MockAuthProvider
from src.api.deps import Auth, DBSession
from src.core.logging import logger
from src.core.security import get_password_hash
from src.models.user import User
from src.schemas.user import LoginRequest, Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    auth: Auth,
    db: DBSession,
) -> Token:
    """Authenticate user and return access token.

    Args:
        request: Login credentials.
        auth: Authentication provider.
        db: Database session.

    Returns:
        JWT access token.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        auth_user = await auth.authenticate(request.email, request.password)
    except AuthenticationError as e:
        logger.warning("Login failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ensure user exists in database
    stmt = select(User).where(User.email == auth_user.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Create user in database if not exists
        async with db.begin():
            user = User(
                email=auth_user.email,
                name=auth_user.name,
                external_id=auth_user.external_id,
                is_active=True,
            )
            db.add(user)
            await db.flush()
        logger.info("Created new user from auth", user_id=user.id, email=user.email)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    # Generate token
    if isinstance(auth, MockAuthProvider):
        token = auth.create_token(auth_user.email)
    else:
        from src.core.security import create_access_token
        token = create_access_token({"sub": auth_user.email})

    logger.info("User logged in", user_id=user.id, email=user.email)

    return Token(access_token=token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserCreate,
    auth: Auth,
    db: DBSession,
) -> User:
    """Register a new user.

    Args:
        request: User registration data.
        auth: Authentication provider.
        db: Database session.

    Returns:
        Created user.

    Raises:
        HTTPException: If registration fails.
    """
    # Check if user already exists in database
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    try:
        # Create user in auth provider
        auth_user = await auth.create_user(
            email=request.email,
            password=request.password,
            name=request.name,
        )

        # Create user in database
        async with db.begin():
            user = User(
                email=auth_user.email,
                name=auth_user.name,
                hashed_password=get_password_hash(request.password),
                external_id=auth_user.external_id,
                is_active=True,
            )
            db.add(user)
            await db.flush()

        logger.info("User registered", user_id=user.id, email=user.email)

        return user

    except UserExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    except Exception as e:
        logger.exception("Registration failed", email=request.email, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/logout")
async def logout() -> dict[str, str]:
    """Logout user.

    Note: For stateless JWT auth, the client should discard the token.

    Returns:
        Success message.
    """
    return {"message": "Successfully logged out"}
