"""FastAPI application entry point.

This module creates and configures the FastAPI application instance.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.config import get_settings
from src.core.logging import logger, setup_logging
from src.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    Performs startup and shutdown tasks.

    Args:
        app: The FastAPI application instance.

    Yields:
        None
    """
    # Startup
    setup_logging()
    logger.info("Application starting up")

    yield

    # Shutdown
    logger.info("Application shutting down")
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        The configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix="/api")

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint.

        Returns:
            Health status information.
        """
        return {
            "status": "healthy",
            "version": settings.version,
        }

    return app


# Create application instance
app = create_app()
