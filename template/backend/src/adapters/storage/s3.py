"""AWS S3 storage provider.

This module provides file storage using AWS S3.
Requires the 'aws' optional dependencies to be installed.
"""

from typing import TYPE_CHECKING

from src.adapters.storage.base import StorageError, StorageFile, StorageProvider
from src.config import get_settings
from src.core.logging import logger

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class S3StorageProvider(StorageProvider):
    """AWS S3 storage provider.

    Stores files in an S3 bucket.

    Attributes:
        _client: Boto3 S3 client.
        _bucket: S3 bucket name.
        _region: AWS region.
    """

    def __init__(self) -> None:
        """Initialize S3 storage provider.

        Raises:
            ImportError: If boto3 is not installed.
            ValueError: If S3 configuration is missing.
        """
        try:
            import boto3
        except ImportError as e:
            raise ImportError(
                "boto3 is required for S3 storage. "
                "Install with: uv add boto3"
            ) from e

        settings = get_settings()

        if not settings.aws_s3_bucket:
            raise ValueError("AWS_S3_BUCKET is required")

        self._client: S3Client = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )
        self._bucket = settings.aws_s3_bucket
        self._region = settings.aws_region

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> StorageFile:
        """Upload a file to S3.

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
            self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )

            url = f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{key}"

            return StorageFile(
                key=key,
                url=url,
                size=len(data),
                content_type=content_type,
            )

        except Exception as e:
            logger.exception("S3 upload error", error=str(e))
            raise StorageError(f"Failed to upload file: {e}") from e

    async def download(self, key: str) -> bytes:
        """Download a file from S3.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            File content as bytes.

        Raises:
            FileNotFoundError: If file does not exist.
            StorageError: If download fails.
        """
        try:
            response = self._client.get_object(
                Bucket=self._bucket,
                Key=key,
            )
            return response["Body"].read()

        except self._client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"File not found: {key}")
        except Exception as e:
            logger.exception("S3 download error", error=str(e))
            raise StorageError(f"Failed to download file: {e}") from e

    async def delete(self, key: str) -> bool:
        """Delete a file from S3.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file was deleted, False if file not found.

        Raises:
            StorageError: If deletion fails.
        """
        try:
            # Check if file exists first
            if not await self.exists(key):
                return False

            self._client.delete_object(
                Bucket=self._bucket,
                Key=key,
            )
            return True

        except Exception as e:
            logger.exception("S3 delete error", error=str(e))
            raise StorageError(f"Failed to delete file: {e}") from e

    async def get_url(self, key: str, expires_in: int = 3600) -> str:
        """Get a presigned URL for a file.

        Args:
            key: Unique identifier/path for the file.
            expires_in: URL expiration time in seconds.

        Returns:
            Presigned URL to access the file.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        if not await self.exists(key):
            raise FileNotFoundError(f"File not found: {key}")

        try:
            url = self._client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": key,
                },
                ExpiresIn=expires_in,
            )
            return url

        except Exception as e:
            logger.exception("S3 presigned URL error", error=str(e))
            raise StorageError(f"Failed to generate URL: {e}") from e

    async def exists(self, key: str) -> bool:
        """Check if a file exists in S3.

        Args:
            key: Unique identifier/path for the file.

        Returns:
            True if file exists, False otherwise.
        """
        try:
            self._client.head_object(
                Bucket=self._bucket,
                Key=key,
            )
            return True
        except self._client.exceptions.ClientError:
            return False
