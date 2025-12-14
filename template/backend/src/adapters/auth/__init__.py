"""Authentication adapters."""
{%- if include_advanced_auth %}
from src.adapters.auth.base import AuthProvider
from src.adapters.auth.factory import get_auth_provider

__all__ = ["AuthProvider", "get_auth_provider"]
{%- else %}
from src.adapters.auth.mock import MockAuthProvider

# Simple type alias for base version
AuthProvider = MockAuthProvider


def get_auth_provider() -> MockAuthProvider:
    """Get the mock auth provider (base version)."""
    return MockAuthProvider()


__all__ = ["AuthProvider", "get_auth_provider"]
{%- endif %}
