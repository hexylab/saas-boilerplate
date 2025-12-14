"""User endpoint tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user(
    client: AsyncClient,
    test_user,
    auth_headers: dict[str, str],
):
    """Test getting current user info."""
    response = await client.get(
        "/api/v1/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    """Test getting current user without auth."""
    response = await client.get("/api/v1/users/me")

    assert response.status_code == 403  # No Authorization header


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """Test getting current user with invalid token."""
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_current_user(
    client: AsyncClient,
    test_user,
    auth_headers: dict[str, str],
):
    """Test updating current user info."""
    response = await client.patch(
        "/api/v1/users/me",
        headers=auth_headers,
        json={"name": "Updated Name"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_list_users_as_superuser(
    client: AsyncClient,
    test_user,
    superuser,
    superuser_headers: dict[str, str],
):
    """Test listing users as superuser."""
    response = await client.get(
        "/api/v1/users/",
        headers=superuser_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least test_user and superuser


@pytest.mark.asyncio
async def test_list_users_as_regular_user(
    client: AsyncClient,
    test_user,
    auth_headers: dict[str, str],
):
    """Test listing users as regular user (should fail)."""
    response = await client.get(
        "/api/v1/users/",
        headers=auth_headers,
    )

    assert response.status_code == 403
    assert "Not enough privileges" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_user_by_id(
    client: AsyncClient,
    test_user,
    superuser,
    superuser_headers: dict[str, str],
):
    """Test getting user by ID as superuser."""
    response = await client.get(
        f"/api/v1/users/{test_user.id}",
        headers=superuser_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(
    client: AsyncClient,
    superuser,
    superuser_headers: dict[str, str],
):
    """Test getting non-existent user."""
    response = await client.get(
        "/api/v1/users/99999",
        headers=superuser_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(
    client: AsyncClient,
    test_user,
    superuser,
    superuser_headers: dict[str, str],
):
    """Test deleting a user as superuser."""
    response = await client.delete(
        f"/api/v1/users/{test_user.id}",
        headers=superuser_headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_self(
    client: AsyncClient,
    superuser,
    superuser_headers: dict[str, str],
):
    """Test that superuser cannot delete themselves."""
    response = await client.delete(
        f"/api/v1/users/{superuser.id}",
        headers=superuser_headers,
    )

    assert response.status_code == 400
    assert "Cannot delete yourself" in response.json()["detail"]
