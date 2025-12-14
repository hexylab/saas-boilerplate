"""Mock authentication provider for local development.

This module provides a mock authentication provider that stores
users in memory. Useful for local development without external
dependencies.
"""

from src.adapters.auth.base import (
    AuthenticationError,
    AuthProvider,
    AuthUser,
    UserExistsError,
)
from src.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


class MockAuthProvider(AuthProvider):
    """Mock authentication provider for development.

    Stores users in memory with password hashing.
    Pre-populated with a test user for convenience.

    Attributes:
        _users: Dictionary of users keyed by email.
    """

    def __init__(self) -> None:
        """Initialize mock provider with a test user."""
        # Pre-populate with a test user
        self._users: dict[str, dict[str, str]] = {
            "test@example.com": {
                "email": "test@example.com",
                "name": "Test User",
                "hashed_password": get_password_hash("password"),
            }
        }

    async def authenticate(self, email: str, password: str) -> AuthUser | None:
        """Authenticate a user with email and password.

        Args:
            email: User's email address.
            password: User's password.

        Returns:
            AuthUser if authentication successful, None otherwise.

        Raises:
            AuthenticationError: If credentials are invalid.
        """
        user = self._users.get(email)
        if not user:
            raise AuthenticationError("Invalid email or password")

        if not verify_password(password, user["hashed_password"]):
            raise AuthenticationError("Invalid email or password")

        return AuthUser(
            id=email,
            email=email,
            name=user["name"],
        )

    async def verify_token(self, token: str) -> AuthUser | None:
        """Verify a JWT token.

        Args:
            token: JWT token to verify.

        Returns:
            AuthUser if token is valid, None otherwise.
        """
        payload = decode_access_token(token)
        if not payload:
            return None

        email = payload.get("sub")
        if not email:
            return None

        user = self._users.get(email)
        if not user:
            return None

        return AuthUser(
            id=email,
            email=email,
            name=user["name"],
        )

    async def create_user(
        self,
        email: str,
        password: str,
        name: str,
    ) -> AuthUser:
        """Create a new user.

        Args:
            email: User's email address.
            password: User's password.
            name: User's display name.

        Returns:
            The created AuthUser.

        Raises:
            UserExistsError: If a user with this email already exists.
        """
        if email in self._users:
            raise UserExistsError(f"User with email {email} already exists")

        self._users[email] = {
            "email": email,
            "name": name,
            "hashed_password": get_password_hash(password),
        }

        return AuthUser(
            id=email,
            email=email,
            name=name,
        )

    async def delete_user(self, email: str) -> bool:
        """Delete a user.

        Args:
            email: User's email address.

        Returns:
            True if user was deleted, False if user not found.
        """
        if email in self._users:
            del self._users[email]
            return True
        return False

    def create_token(self, email: str) -> str:
        """Create a JWT token for a user.

        Args:
            email: User's email address.

        Returns:
            JWT token string.
        """
        return create_access_token({"sub": email})
