"""Storage provider factory.

This module provides a factory function to get the appropriate
storage provider based on configuration.
"""

from functools import lru_cache

from src.adapters.storage.base import StorageProvider
from src.config import get_settings


@lru_cache
def get_storage_provider() -> StorageProvider:
    """Get the configured storage provider.

    Returns the appropriate StorageProvider implementation based on
    the STORAGE_PROVIDER environment variable.

    Returns:
        StorageProvider instance.

    Raises:
        ValueError: If an unknown provider is configured.

    Example:
        ```python
        from fastapi import Depends, UploadFile
        from src.adapters.storage import get_storage_provider, StorageProvider

        @router.post("/upload")
        async def upload_file(
            file: UploadFile,
            storage: StorageProvider = Depends(get_storage_provider),
        ):
            data = await file.read()
            result = await storage.upload(file.filename, data)
            return {"url": result.url}
        ```
    """
    settings = get_settings()

    if settings.storage_provider == "local":
        from src.adapters.storage.local import LocalStorageProvider

        return LocalStorageProvider()

    elif settings.storage_provider == "s3":
        from src.adapters.storage.s3 import S3StorageProvider

        return S3StorageProvider()

    else:
        raise ValueError(f"Unknown storage provider: {settings.storage_provider}")
