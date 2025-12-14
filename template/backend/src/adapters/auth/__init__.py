"""Authentication adapters."""
{%- if include_advanced_auth %}
from src.adapters.auth.base import AuthProvider
from src.adapters.auth.factory import get_auth_provider

__all__ = ["AuthProvider", "get_auth_provider"]
{%- else %}
from src.adapters.auth.mock import MockAuthProvider

# Simple type alias for base version
AuthProvider = MockAuthProvider

# Singleton instance for mock provider
_mock_provider_instance: MockAuthProvider | None = None


def get_auth_provider() -> MockAuthProvider:
    """Get the mock auth provider (singleton).

    Returns the same instance across all calls to ensure
    user data persists throughout the application lifecycle.
    """
    global _mock_provider_instance
    if _mock_provider_instance is None:
        _mock_provider_instance = MockAuthProvider()
    return _mock_provider_instance


__all__ = ["AuthProvider", "get_auth_provider"]
{%- endif %}
