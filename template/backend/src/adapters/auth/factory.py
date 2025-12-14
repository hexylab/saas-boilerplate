"""Authentication provider factory.

This module provides a factory function to get the appropriate
authentication provider based on configuration.
"""

from functools import lru_cache

from src.adapters.auth.base import AuthProvider
from src.config import get_settings


@lru_cache
def get_auth_provider() -> AuthProvider:
    """Get the configured authentication provider.

    Returns the appropriate AuthProvider implementation based on
    the AUTH_PROVIDER environment variable.

    Returns:
        AuthProvider instance.

    Raises:
        ValueError: If an unknown provider is configured.

    Example:
        ```python
        from fastapi import Depends
        from src.adapters.auth import get_auth_provider, AuthProvider

        @router.post("/login")
        async def login(
            auth: AuthProvider = Depends(get_auth_provider),
        ):
            user = await auth.authenticate(email, password)
        ```
    """
    settings = get_settings()

    if settings.auth_provider == "mock":
        from src.adapters.auth.mock import MockAuthProvider

        return MockAuthProvider()
{%- if _enable_aws_auth %}

    elif settings.auth_provider == "cognito":
        from src.adapters.auth.cognito import CognitoAuthProvider

        return CognitoAuthProvider()
{%- endif %}

    else:
        raise ValueError(f"Unknown auth provider: {settings.auth_provider}")
