.PHONY: help install lint format test clean dev-up dev-down

help:
	@echo "PublicScanner - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install all dependencies"
	@echo "  make dev-up        - Start development environment with Docker"
	@echo "  make dev-down      - Stop development environment"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Run all linters"
	@echo "  make lint-frontend - Lint frontend code"
	@echo "  make lint-backend  - Lint backend code"
	@echo "  make lint-workers  - Lint worker code"
	@echo "  make format        - Format all code"
	@echo "  make format-frontend - Format frontend code"
	@echo "  make format-workers  - Format worker code"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests"
	@echo "  make test-frontend - Test frontend"
	@echo "  make test-backend  - Test backend"
	@echo "  make test-workers  - Test workers"
	@echo ""
	@echo "Database:"
	@echo "  make db-schema     - Load database schema"
	@echo "  make db-seed       - Seed database with dev data"
	@echo "  make db-reset      - Reset database (drop, schema, seed)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         - Clean build artifacts"

# Installation
install:
	@echo "Installing dependencies..."
	npm install
	cd frontend && npm install
	cd backend && go mod download
	cd workers && pip install -r requirements.txt
	@echo "✅ All dependencies installed"

# Development Environment
dev-up:
	@echo "Starting development environment..."
	docker compose up -d
	@echo "✅ Development environment running"
	@echo "   Frontend: http://localhost:3000"
	@echo "   API: http://localhost:8080"
	@echo "   Flower: http://localhost:5555"

dev-down:
	@echo "Stopping development environment..."
	docker compose down
	@echo "✅ Development environment stopped"

# Linting
lint: lint-frontend lint-backend lint-workers
	@echo "✅ All linting passed"

lint-frontend:
	@echo "Linting frontend..."
	cd frontend && npm run lint

lint-backend:
	@echo "Linting backend..."
	cd backend && golangci-lint run

lint-workers:
	@echo "Linting workers..."
	cd workers && flake8 . && black --check . && isort --check-only .

# Formatting
format: format-frontend format-workers
	@echo "✅ All code formatted"

format-frontend:
	@echo "Formatting frontend..."
	cd frontend && npx prettier --write .

format-workers:
	@echo "Formatting workers..."
	cd workers && black . && isort .

# Testing
test: test-frontend test-backend test-workers
	@echo "✅ All tests passed"

test-frontend:
	@echo "Testing frontend..."
	cd frontend && npm test

test-backend:
	@echo "Testing backend..."
	cd backend && go test -v ./...

test-workers:
	@echo "Testing workers..."
	cd workers && pytest -v

# Database
db-schema:
	@echo "Loading database schema..."
	docker compose exec postgres psql -U postgres -d publicscanner -f /docker-entrypoint-initdb.d/01-schema.sql
	@echo "✅ Schema loaded"

db-seed:
	@echo "Seeding database..."
	docker compose exec postgres psql -U postgres -d publicscanner -f /docker-entrypoint-initdb.d/02-seeds/001_dev_data.sql
	@echo "✅ Database seeded"

db-reset:
	@echo "Resetting database..."
	docker compose exec postgres psql -U postgres -d publicscanner -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	@$(MAKE) db-schema
	@$(MAKE) db-seed
	@echo "✅ Database reset complete"

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	cd frontend && rm -rf .next node_modules
	cd backend && go clean
	cd workers && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cd workers && find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"
