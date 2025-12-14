"""Application configuration.

This module provides configuration management using Pydantic Settings.
Configuration values are loaded from environment variables.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        project_name: The name of the project.
        version: The version of the application.
        debug: Whether debug mode is enabled.
        database_url: The database connection URL.
        secret_key: Secret key for JWT signing.
        auth_provider: The authentication provider to use.
        storage_provider: The storage provider to use.
        log_handler: The log handler to use.
        log_level: The log level.
        cors_origins: Comma-separated list of allowed CORS origins.
        aws_region: AWS region for AWS services.
        aws_cognito_user_pool_id: Cognito User Pool ID.
        aws_cognito_client_id: Cognito Client ID.
        aws_s3_bucket: S3 bucket name for storage.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    project_name: str = "{{ project_name }}"
    version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str

    # Security
    secret_key: str

    # Providers
    auth_provider: Literal["mock", "cognito"] = "mock"
    storage_provider: Literal["local", "s3"] = "local"

    # Logging
    log_handler: Literal["console", "cloudwatch", "datadog"] = "console"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # AWS (optional, required for cognito/s3 providers)
    aws_region: str = "{{ aws_region }}"
    aws_cognito_user_pool_id: str | None = None
    aws_cognito_client_id: str | None = None
    aws_s3_bucket: str | None = None

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string.

        Returns:
            List of allowed CORS origins.
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        The application settings.
    """
    return Settings()
