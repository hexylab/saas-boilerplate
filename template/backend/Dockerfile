# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# ============================================
# Development stage
# ============================================
FROM base AS development

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies (generate lock if not exists)
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ -f uv.lock ]; then \
        uv sync --frozen --no-install-project --dev; \
    else \
        uv sync --no-install-project --dev; \
    fi

# Copy application code
COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --dev

# Expose port
EXPOSE 8000

# Run development server
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Production stage
# ============================================
FROM base AS production

# Create non-root user
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home app

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies (production only, generate lock if not exists)
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ -f uv.lock ]; then \
        uv sync --frozen --no-install-project --no-dev; \
    else \
        uv sync --no-install-project --no-dev; \
    fi

# Copy application code
COPY --chown=app:app . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Run production server
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
