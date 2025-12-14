"""Pytest configuration and fixtures.

This module provides common fixtures for testing.
"""

import asyncio
from collections.abc import AsyncGenerator
from typing import Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.adapters.auth.mock import MockAuthProvider
from src.config import Settings, get_settings
from src.db.base import Base
from src.db.session import get_db
from src.main import app
from src.models.user import User


# Test database URL (SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings."""
    return Settings(
        database_url=TEST_DATABASE_URL,
        secret_key="test-secret-key",
        auth_provider="mock",
        storage_provider="local",
        debug=True,
    )


@pytest.fixture(scope="session")
async def test_engine(test_settings: Settings):
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session with proper isolation.

    Uses nested transactions (savepoints) to ensure each test
    runs in isolation and changes are rolled back after each test.
    """
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        # Start a transaction for the test
        async with session.begin():
            # Create a nested transaction (savepoint)
            nested = await session.begin_nested()

            yield session

            # Rollback the nested transaction to clean up test data
            if nested.is_active:
                await nested.rollback()


@pytest.fixture
def mock_auth() -> MockAuthProvider:
    """Create mock auth provider."""
    return MockAuthProvider()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def superuser(db_session: AsyncSession) -> User:
    """Create a superuser in the database."""
    user = User(
        email="admin@example.com",
        name="Admin User",
        hashed_password="hashed",
        is_active=True,
        is_superuser=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(mock_auth: MockAuthProvider) -> dict[str, str]:
    """Create authorization headers with a valid token."""
    token = mock_auth.create_token("test@example.com")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def superuser_headers(mock_auth: MockAuthProvider) -> dict[str, str]:
    """Create authorization headers for superuser."""
    token = mock_auth.create_token("admin@example.com")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def client(
    db_session: AsyncSession,
    test_settings: Settings,
) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client."""
    # Override dependencies
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_settings] = lambda: test_settings

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
