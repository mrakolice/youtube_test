.PHONY: help setup-env build up down logs migrate-up migrate-down \
        seed-db seed-test-db test test-auth test-videos test-views test-likes \
        test-all migrate-create migrate-current migrate-branches \
        auth-service video-service view-service like-service install-deps \
        clean docker-clean test-one lint format type-check

SHELL := /bin/bash
PYTHON := python3
UV := uv

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'

# Environment Setup
setup-env: ## Create .env file from example
	@if [ ! -f .env ]; then cp .env.example .env; echo ".env file created"; else echo ".env already exists"; fi

install-deps: ## Install dependencies for all services using uv
	@echo "Installing shared dependencies..."
	cd backend && $(UV) sync
	@echo "Setting up services..."
	cd backend/services/auth && $(UV) sync
	cd backend/services/videos && $(UV) sync
	cd backend/services/views && $(UV) sync
	cd backend/services/likes && $(UV) sync

# Docker
build: setup-env ## Build all Docker images
	docker compose build

up: ## Start all services
	docker compose up -d
	@echo "Services started. Waiting for them to be ready..."
	sleep 5
	make migrate-up
	@echo "All services are running!"

down: ## Stop all services
	docker compose down

logs: ## Show logs from all services
	docker compose logs -f

logs-auth: ## Show logs from auth service
	docker compose logs -f auth-service

logs-video: ## Show logs from video service
	docker compose logs -f video-service

logs-view: ## Show logs from view service
	docker compose logs -f view-service

logs-like: ## Show logs from like service
	docker compose logs -f like-service

ps: ## Show running containers
	docker compose ps

# Database Migrations
migrate-up: ## Run all migrations
	@echo "Running migrations for auth service..."
	cd backend/services/auth && alembic upgrade head
	@echo "Running migrations for video service..."
	cd backend/services/videos && alembic upgrade head
	@echo "Running migrations for view service..."
	cd backend/services/views && alembic upgrade head
	@echo "Running migrations for like service..."
	cd backend/services/likes && alembic upgrade head
	@echo "All migrations completed!"

migrate-down: ## Rollback all migrations
	@echo "Rolling back migrations..."
	cd backend/services/auth && alembic downgrade -1
	cd backend/services/videos && alembic downgrade -1
	cd backend/services/views && alembic downgrade -1
	cd backend/services/likes && alembic downgrade -1

migrate-create: ## Create migration files (SERVICE=auth NAME=add_user_table)
	@if [ -z "$(SERVICE)" ] || [ -z "$(NAME)" ]; then echo "Usage: make migrate-create SERVICE=auth NAME=add_user_table"; exit 1; fi
	cd backend/services/$(SERVICE) && alembic revision --autogenerate -m "$(NAME)"

migrate-current: ## Show current migration version for service (SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then echo "Usage: make migrate-current SERVICE=auth"; exit 1; fi
	cd backend/services/$(SERVICE) && alembic current

migrate-branches: ## Show migration branches for service (SERVICE=auth)
	@if [ -z "$(SERVICE)" ]; then echo "Usage: make migrate-branches SERVICE=auth"; exit 1; fi
	cd backend/services/$(SERVICE) && alembic branches

# Database Seeding
seed-db: ## Seed development database with mock data
	@echo "Seeding development database..."
	$(PYTHON) backend/scripts/seed_db.py
	@echo "Database seeding completed!"

seed-test-db: ## Seed test database with mock data
	@echo "Seeding test database..."
	TEST_ENV=true $(PYTHON) backend/scripts/seed_test_db.py
	@echo "Test database seeding completed!"

# Testing
test-all: ## Run all tests with coverage
	@echo "Running all tests..."
	cd backend/services/auth && pytest -v --tb=short -n auto --cov
	cd backend/services/videos && pytest -v --tb=short -n auto --cov
	cd backend/services/views && pytest -v --tb=short -n auto --cov
	cd backend/services/likes && pytest -v --tb=short -n auto --cov

test-auth: ## Run auth service tests
	@echo "Running auth service tests..."
	cd backend/services/auth && pytest -v --tb=short -n auto

test-videos: ## Run video service tests
	@echo "Running video service tests..."
	cd backend/services/videos && pytest -v --tb=short -n auto

test-views: ## Run view service tests
	@echo "Running view service tests..."
	cd backend/services/views && pytest -v --tb=short -n auto

test-likes: ## Run like service tests
	@echo "Running like service tests..."
	cd backend/services/likes && pytest -v --tb=short -n auto

test-one: ## Run specific test (SERVICE=auth TEST=test_login)
	@if [ -z "$(SERVICE)" ] || [ -z "$(TEST)" ]; then echo "Usage: make test-one SERVICE=auth TEST=test_login"; exit 1; fi
	cd backend/services/$(SERVICE) && pytest -v --tb=short tests/system_tests/$(TEST).py

# Individual Service Startup (for local development without Docker)
auth-service: ## Run auth service locally
	cd backend/services/auth && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

video-service: ## Run video service locally
	cd backend/services/videos && uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload

view-service: ## Run view service locally
	cd backend/services/views && uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

like-service: ## Run like service locally
	cd backend/services/likes && uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload

# Code Quality
lint: ## Run linters on backend code
	cd backend && $(PYTHON) -m flake8 services/ --max-line-length=120 --ignore=E501,W503
	cd backend && $(PYTHON) -m pylint services/ --disable=C0111,C0103

format: ## Format code with black and isort
	cd backend && $(PYTHON) -m black services/ --line-length=120
	cd backend && $(PYTHON) -m isort services/ --profile=black

type-check: ## Run mypy type checking
	cd backend && $(PYTHON) -m mypy services/ --ignore-missing-imports

# Cleanup
clean: ## Clean up cache files and directories
	find backend -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find backend -type f -name "*.pyc" -delete
	find backend -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find backend -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup completed!"

docker-clean: clean ## Clean docker volumes and containers
	docker compose down -v
	docker system prune -f
	@echo "Docker cleanup completed!"

# Reset all
reset-all: docker-clean setup-env ## Reset everything to initial state
	@echo "Project reset completed!"
