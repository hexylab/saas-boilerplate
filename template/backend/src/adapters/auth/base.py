"""Base authentication provider interface.

This module defines the abstract base class for authentication providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthUser:
    """Authenticated user information.

    Attributes:
        id: User identifier (email or external ID).
        email: User's email address.
        name: User's display name.
        external_id: External ID from auth provider (e.g., Cognito sub).
    """

    id: str
    email: str
    name: str
    external_id: str | None = None


class AuthProvider(ABC):
    """Abstract base class for authentication providers.

    All authentication providers must implement this interface.
    This allows for easy switching between providers (mock, Cognito, etc.)
    via configuration.

    Example:
        ```python
        class MockAuthProvider(AuthProvider):
            async def authenticate(self, email: str, password: str) -> AuthUser:
                # Mock authentication logic
                return AuthUser(id=email, email=email, name="Test User")
        ```
    """

    @abstractmethod
    async def authenticate(self, email: str, password: str) -> AuthUser | None:
        """Authenticate a user with email and password.

        Args:
            email: User's email address.
            password: User's password.

        Returns:
            AuthUser if authentication successful, None otherwise.

        Raises:
            AuthenticationError: If authentication fails due to invalid credentials.
        """
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> AuthUser | None:
        """Verify an authentication token.

        Args:
            token: JWT or other authentication token.

        Returns:
            AuthUser if token is valid, None otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def delete_user(self, email: str) -> bool:
        """Delete a user.

        Args:
            email: User's email address.

        Returns:
            True if user was deleted, False if user not found.
        """
        pass


class AuthenticationError(Exception):
    """Raised when authentication fails."""

    pass


class UserExistsError(Exception):
    """Raised when trying to create a user that already exists."""

    pass
