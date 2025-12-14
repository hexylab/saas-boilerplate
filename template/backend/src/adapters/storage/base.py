"""Base storage provider interface.

This module defines the abstract base class for storage providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StorageFile:
    """Stored file information.

    Attributes:
        key: Unique identifier/path for the file.
        url: URL to access the file.
        size: File size in bytes.
        content_type: MIME type of the file.
    """

    key: str
    url: str
    size: int
    content_type: str


class StorageProvider(ABC):
    """Abstract base class for storage providers.

    All storage providers must implement this interface.
    This allows for easy switching between providers (local, S3, etc.)
    via configuration.

    Example:
        ```python
        class LocalStorageProvider(StorageProvider):
            async def upload(self, key: str, data: bytes, ...) -> StorageFile:
                # Save to local filesystem
                ...
        ```
    """

    @abstractmethod
    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageFile:
        """Upload a file.

        Args:
            key: Unique identifier/path for the file.
            data: File content as bytes.
            content_type: MIME type of the file.

        Returns:
            StorageFile with file information.

        Raises:
            StorageError: If upload fails.
        """
        pass

    @abstractmethod
    async def download(self, key: str) -> bytes:
        """Download a file.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            File content as bytes.

        Raises:
            FileNotFoundError: If file does not exist.
            StorageError: If download fails.
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete a file.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file was deleted, False if file not found.

        Raises:
            StorageError: If deletion fails.
        """
        pass

    @abstractmethod
    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        """Get a URL to access a file.

        Args:
            key: Unique identifier/path for the file.
            expires_in: URL expiration time in seconds (for signed URLs).

        Returns:
            URL to access the file.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a file exists.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file exists, False otherwise.
        """
        pass


class StorageError(Exception):
    """Raised when a storage operation fails."""

    pass
