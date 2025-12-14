"""AWS Cognito authentication provider.

This module provides authentication via AWS Cognito User Pools.
Requires the 'aws' optional dependencies to be installed.
"""

from typing import TYPE_CHECKING

from src.adapters.auth.base import (
    AuthenticationError,
    AuthProvider,
    AuthUser,
    UserExistsError,
)
from src.config import get_settings
from src.core.logging import logger

if TYPE_CHECKING:
    from mypy_boto3_cognito_idp import CognitoIdentityProviderClient


class CognitoAuthProvider(AuthProvider):
    """AWS Cognito authentication provider.

    Uses AWS Cognito User Pools for authentication.
    Requires AWS credentials to be configured.

    Attributes:
        _client: Boto3 Cognito IDP client.
        _user_pool_id: Cognito User Pool ID.
        _client_id: Cognito App Client ID.
    """

    def __init__(self) -> None:
        """Initialize Cognito provider.

        Raises:
            ImportError: If boto3 is not installed.
            ValueError: If Cognito configuration is missing.
        """
        try:
            import boto3
        except ImportError as e:
            raise ImportError(
                "boto3 is required for Cognito auth. "
                "Install with: uv add boto3"
            ) from e

        settings = get_settings()

        if not settings.aws_cognito_user_pool_id:
            raise ValueError("AWS_COGNITO_USER_POOL_ID is required")
        if not settings.aws_cognito_client_id:
            raise ValueError("AWS_COGNITO_CLIENT_ID is required")

        self._client: CognitoIdentityProviderClient = boto3.client(
            "cognito-idp",
            region_name=settings.aws_region,
        )
        self._user_pool_id = settings.aws_cognito_user_pool_id
        self._client_id = settings.aws_cognito_client_id

    async def authenticate(self, email: str, password: str) -> AuthUser | None:
        """Authenticate a user with Cognito.

        Args:
            email: User's email address.
            password: User's password.

        Returns:
            AuthUser if authentication successful.

        Raises:
            AuthenticationError: If credentials are invalid.
        """
        try:
            response = self._client.initiate_auth(
                ClientId=self._client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                },
            )

            # Get user attributes
            access_token = response["AuthenticationResult"]["AccessToken"]
            user_response = self._client.get_user(AccessToken=access_token)

            attributes = {
                attr["Name"]: attr["Value"] for attr in user_response["UserAttributes"]
            }

            return AuthUser(
                id=attributes.get("sub", email),
                email=attributes.get("email", email),
                name=attributes.get("name", email),
                external_id=attributes.get("sub"),
            )

        except self._client.exceptions.NotAuthorizedException:
            raise AuthenticationError("Invalid email or password")
        except self._client.exceptions.UserNotFoundException:
            raise AuthenticationError("Invalid email or password")
        except Exception as e:
            logger.exception("Cognito authentication error", error=str(e))
            raise AuthenticationError("Authentication failed")

    async def verify_token(self, token: str) -> AuthUser | None:
        """Verify a Cognito access token.

        Args:
            token: Cognito access token.

        Returns:
            AuthUser if token is valid, None otherwise.
        """
        try:
            response = self._client.get_user(AccessToken=token)
            attributes = {
                attr["Name"]: attr["Value"] for attr in response["UserAttributes"]
            }

            return AuthUser(
                id=attributes.get("sub", ""),
                email=attributes.get("email", ""),
                name=attributes.get("name", attributes.get("email", "")),
                external_id=attributes.get("sub"),
            )

        except Exception as e:
            logger.warning("Token verification failed", error=str(e))
            return None

    async def create_user(
        self,
        email: str,
        password: str,
        name: str,
    ) -> AuthUser:
        """Create a new user in Cognito.

        Args:
            email: User's email address.
            password: User's password.
            name: User's display name.

        Returns:
            The created AuthUser.

        Raises:
            UserExistsError: If a user with this email already exists.
        """
        try:
            response = self._client.sign_up(
                ClientId=self._client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "name", "Value": name},
                ],
            )

            return AuthUser(
                id=response["UserSub"],
                email=email,
                name=name,
                external_id=response["UserSub"],
            )

        except self._client.exceptions.UsernameExistsException:
            raise UserExistsError(f"User with email {email} already exists")
        except Exception as e:
            logger.exception("Cognito user creation error", error=str(e))
            raise

    async def delete_user(self, email: str) -> bool:
        """Delete a user from Cognito.

        Args:
            email: User's email address.

        Returns:
            True if user was deleted, False if user not found.
        """
        try:
            self._client.admin_delete_user(
                UserPoolId=self._user_pool_id,
                Username=email,
            )
            return True
        except self._client.exceptions.UserNotFoundException:
            return False
        except Exception as e:
            logger.exception("Cognito user deletion error", error=str(e))
            raise
