"""Authentication adapters."""

from src.adapters.auth.base import AuthProvider, AuthUser
from src.adapters.auth.factory import get_auth_provider

__all__ = ["AuthProvider", "AuthUser", "get_auth_provider"]
