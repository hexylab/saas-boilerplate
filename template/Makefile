# {{ project_name }} - Development Makefile
# Common development tasks

.PHONY: help setup dev down logs test lint format clean

# Default target
help:
	@echo "Available targets:"
	@echo "  setup     - Initial project setup (install dependencies, generate lock files)"
	@echo "  dev       - Start development environment"
	@echo "  down      - Stop development environment"
	@echo "  logs      - Show logs from all services"
	@echo "  test      - Run all tests"
	@echo "  lint      - Run linters"
	@echo "  format    - Format code"
	@echo "  clean     - Clean up generated files"
	@echo ""
	@echo "Backend targets:"
	@echo "  backend-setup   - Install backend dependencies"
	@echo "  backend-test    - Run backend tests"
	@echo "  backend-lint    - Run backend linters"
	@echo "  backend-format  - Format backend code"
	@echo "  backend-migrate - Run database migrations"
	@echo ""
	@echo "Frontend targets:"
	@echo "  frontend-setup  - Install frontend dependencies"
	@echo "  frontend-test   - Run frontend tests"
	@echo "  frontend-lint   - Run frontend linters"
	@echo "  frontend-format - Format frontend code"
{%- if include_e2e_tests %}
	@echo "  frontend-e2e    - Run E2E tests"
{%- endif %}

# ===================
# Project-wide targets
# ===================

setup: backend-setup frontend-setup
	@echo "Project setup complete!"
	@echo "Run 'make dev' to start the development environment."

dev:
	docker compose up -d
	@echo "Development environment started!"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API docs: http://localhost:8000/docs"

down:
	docker compose down

logs:
	docker compose logs -f

test: backend-test frontend-test

lint: backend-lint frontend-lint

format: backend-format frontend-format

clean:
	docker compose down -v
	rm -rf frontend/node_modules frontend/.next
	rm -rf backend/.venv backend/__pycache__ backend/src/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# ===================
# Backend targets
# ===================

backend-setup:
	cd backend && uv sync --dev
	@echo "Backend dependencies installed!"

backend-test:
	cd backend && uv run pytest

backend-lint:
	cd backend && uv run ruff check src tests
	cd backend && uv run mypy src

backend-format:
	cd backend && uv run ruff format src tests
	cd backend && uv run ruff check --fix src tests

backend-migrate:
	cd backend && uv run alembic upgrade head

backend-migrate-create:
	@read -p "Migration message: " msg; \
	cd backend && uv run alembic revision --autogenerate -m "$$msg"

# ===================
# Frontend targets
# ===================

frontend-setup:
	cd frontend && pnpm install
	@echo "Frontend dependencies installed!"

frontend-test:
	cd frontend && pnpm test

frontend-lint:
	cd frontend && pnpm lint

frontend-format:
	cd frontend && pnpm format
{%- if include_e2e_tests %}

frontend-e2e:
	cd frontend && pnpm e2e
{%- endif %}

# ===================
# Database targets
# ===================

db-start:
	docker compose up -d db
	@echo "Waiting for database to be ready..."
	@sleep 3

db-shell:
	docker compose exec db psql -U postgres -d app
