"""Storage adapters."""

from src.adapters.storage.base import StorageProvider
from src.adapters.storage.factory import get_storage_provider

__all__ = ["StorageProvider", "get_storage_provider"]
