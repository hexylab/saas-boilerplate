"""API router configuration.

This module configures the main API router and includes all sub-routers.
"""

from fastapi import APIRouter

from src.api.v1 import auth, users

api_router = APIRouter()

# Include v1 routers
api_router.include_router(auth.router, prefix="/v1")
api_router.include_router(users.router, prefix="/v1")
