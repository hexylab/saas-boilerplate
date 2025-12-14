"""Local filesystem storage provider.

This module provides file storage using the local filesystem.
Useful for local development without external dependencies.
"""

import os
from pathlib import Path

from src.adapters.storage.base import StorageError, StorageFile, StorageProvider


class LocalStorageProvider(StorageProvider):
    """Local filesystem storage provider.

    Stores files in a local directory.

    Attributes:
        _base_path: Base directory for file storage.
        _base_url: Base URL for accessing files.
    """

    def __init__(
        self,
        base_path: str = "storage",
        base_url: str = "http://localhost:8000/files",
    ) -> None:
        """Initialize local storage provider.

        Args:
            base_path: Base directory for file storage.
            base_url: Base URL for accessing files.
        """
        self._base_path = Path(base_path)
        self._base_url = base_url.rstrip("/")

        # Ensure base directory exists
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, key: str) -> Path:
        """Get the full file path for a key.

        Args:
            key: File key/path.

        Returns:
            Full path to the file.
        """
        # Sanitize key to prevent directory traversal
        safe_key = key.lstrip("/").replace("..", "")
        return self._base_path / safe_key

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageFile:
        """Upload a file to local storage.

        Args:
            key: Unique identifier/path for the file.
            data: File content as bytes.
            content_type: MIME type of the file.

        Returns:
            StorageFile with file information.

        Raises:
            StorageError: If upload fails.
        """
        try:
            file_path = self._get_file_path(key)

            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_bytes(data)

            return StorageFile(
                key=key,
                url=f"{self._base_url}/{key}",
                size=len(data),
                content_type=content_type,
            )

        except Exception as e:
            raise StorageError(f"Failed to upload file: {e}") from e

    async def download(self, key: str) -> bytes:
        """Download a file from local storage.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            File content as bytes.

        Raises:
            FileNotFoundError: If file does not exist.
            StorageError: If download fails.
        """
        file_path = self._get_file_path(key)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {key}")

        try:
            return file_path.read_bytes()
        except Exception as e:
            raise StorageError(f"Failed to download file: {e}") from e

    async def delete(self, key: str) -> bool:
        """Delete a file from local storage.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file was deleted, False if file not found.

        Raises:
            StorageError: If deletion fails.
        """
        file_path = self._get_file_path(key)

        if not file_path.exists():
            return False

        try:
            os.remove(file_path)
            return True
        except Exception as e:
            raise StorageError(f"Failed to delete file: {e}") from e

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        """Get URL for a file.

        Note: Local storage does not support signed URLs,
        so expires_in is ignored.

        Args:
            key: Unique identifier/path for the file.
            expires_in: Ignored for local storage.

        Returns:
            URL to access the file.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        file_path = self._get_file_path(key)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {key}")

        return f"{self._base_url}/{key}"

    async def exists(self, key: str) -> bool:
        """Check if a file exists.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file exists, False otherwise.
        """
        return self._get_file_path(key).exists()
