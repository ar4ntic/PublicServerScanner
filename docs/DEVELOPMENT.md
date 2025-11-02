# Development Guide

This guide covers development workflows, code quality tools, and best practices for contributing to PublicScanner.

## Table of Contents

- [Getting Started](#getting-started)
- [Code Quality Tools](#code-quality-tools)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **OR** install manually:
  - Node.js 20+
  - Go 1.21+
  - Python 3.11+
  - PostgreSQL 15+
  - Redis 7+

### Quick Setup

```bash
# Install all dependencies
make install

# Start development environment
make dev-up

# Initialize database
make db-reset

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8080
# Flower (Celery): http://localhost:5555
```

### Manual Setup

```bash
# 1. Backend dependencies
cd backend
go mod download

# 2. Frontend dependencies
cd ../frontend
npm install

# 3. Worker dependencies
cd ../workers
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Root dependencies (for linting/commitlint)
cd ..
npm install
```

---

## Code Quality Tools

We use multiple linting and formatting tools to maintain code quality across the project.

### Frontend (Next.js + TypeScript)

#### ESLint

Enforces code quality and naming conventions.

```bash
# Run linter
cd frontend
npm run lint

# Auto-fix issues
npm run lint:fix

# Or use make
make lint-frontend
```

**Configuration:** `frontend/.eslintrc.json`

Key rules:
- Naming conventions enforced via `@typescript-eslint/naming-convention`
- React hooks rules
- Import ordering
- No unused variables

#### Prettier

Code formatter for consistent style.

```bash
# Format all files
cd frontend
npm run format

# Check formatting
npm run format:check

# Or use make
make format-frontend
```

**Configuration:** `frontend/.prettierrc.json`

#### TypeScript

Type checking without emitting files.

```bash
cd frontend
npm run type-check
```

### Backend (Go)

#### golangci-lint

Comprehensive Go linter with multiple checkers.

```bash
# Run linter
cd backend
golangci-lint run

# Fix auto-fixable issues
golangci-lint run --fix

# Or use make
make lint-backend
```

**Configuration:** `backend/.golangci.yml`

Enabled linters:
- `gofmt` - Code formatting
- `goimports` - Import formatting
- `govet` - Suspicious constructs
- `errcheck` - Unchecked errors
- `staticcheck` - Static analysis
- `revive` - Fast, extensible linter
- And 10+ more...

**Installing golangci-lint:**

```bash
# macOS
brew install golangci-lint

# Linux
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin

# Windows
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

### Workers (Python)

#### Flake8

Python linter for style and errors.

```bash
cd workers
flake8 .

# Or use make
make lint-workers
```

**Configuration:** `workers/.flake8`

#### Black

Opinionated Python code formatter.

```bash
cd workers

# Check formatting
black --check .

# Format code
black .

# Or use make
make format-workers
```

**Configuration:** `workers/pyproject.toml` (`[tool.black]`)

#### isort

Import statement organizer.

```bash
cd workers

# Check imports
isort --check-only .

# Fix imports
isort .
```

**Configuration:** `workers/pyproject.toml` (`[tool.isort]`)

#### MyPy (Optional)

Static type checker for Python.

```bash
cd workers
mypy .
```

**Configuration:** `workers/pyproject.toml` (`[tool.mypy]`)

### Commit Message Linting

#### commitlint

Enforces Conventional Commits specification.

**Configuration:** `.commitlintrc.json`

Valid commit types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (no logic change)
- `refactor` - Code refactoring
- `perf` - Performance improvement
- `test` - Tests
- `chore` - Maintenance
- `ci` - CI/CD changes
- `build` - Build system

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Examples:**
```bash
feat(api): add user authentication endpoint
fix(frontend): resolve login form validation
docs(readme): update installation instructions
refactor(workers): simplify scan execution logic
```

**Rules:**
- Type must be lowercase
- Subject must not end with period
- Header max 72 characters
- Body max 100 characters per line

---

## Development Workflow

### Using Make Commands

We provide a Makefile for common development tasks:

```bash
# Show all available commands
make help

# Development
make install          # Install dependencies
make dev-up          # Start Docker environment
make dev-down        # Stop Docker environment

# Code Quality
make lint            # Run all linters
make lint-frontend   # Lint frontend only
make lint-backend    # Lint backend only
make lint-workers    # Lint workers only
make format          # Format all code
make format-frontend # Format frontend only
make format-workers  # Format workers only

# Testing
make test            # Run all tests
make test-frontend   # Test frontend
make test-backend    # Test backend
make test-workers    # Test workers

# Database
make db-schema       # Load schema (pre-production)
make db-seed         # Seed dev data
make db-reset        # Reset database (drop, schema, seed)

# Utilities
make clean           # Clean build artifacts
```

### Pre-commit Checklist

Before committing code, ensure:

1. **Code is formatted:**
   ```bash
   make format
   ```

2. **Linters pass:**
   ```bash
   make lint
   ```

3. **Tests pass:**
   ```bash
   make test
   ```

4. **Types are correct (Frontend):**
   ```bash
   cd frontend && npm run type-check
   ```

5. **Commit message is valid:**
   ```bash
   # Commit with conventional commit format
   git commit -m "feat(api): add scan endpoint"
   ```

### Setting Up Pre-commit Hooks (Optional)

Install husky for automatic pre-commit checks:

```bash
# From project root
npm install
npm run prepare

# This will create .husky/ directory with hooks
```

---

## Testing

### Frontend Tests

```bash
cd frontend
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Backend Tests

```bash
cd backend

# Run all tests
go test ./...

# Verbose output
go test -v ./...

# With coverage
go test -cover ./...

# Coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Worker Tests

```bash
cd workers
source venv/bin/activate

# Run all tests
pytest

# Verbose
pytest -v

# With coverage
pytest --cov=. --cov-report=html

# Specific test file
pytest tests/test_checks.py
```

---

## Commit Guidelines

### Conventional Commits Format

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### Type

Must be one of:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Code style changes (formatting, semicolons, etc)
- **refactor**: Code refactoring (neither fixes bug nor adds feature)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (updating dependencies, etc)
- **ci**: CI/CD changes
- **build**: Build system changes

### Scope

Optional, describes the section of codebase:

- `api` - Backend API
- `frontend` - Frontend application
- `workers` - Celery workers
- `db` - Database changes
- `auth` - Authentication
- `scan` - Scan functionality
- `docs` - Documentation
- etc.

### Subject

- Use imperative, present tense: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at the end
- Max 72 characters

### Body

- Use imperative, present tense
- Include motivation and contrast with previous behavior
- Wrap at 100 characters

### Footer

- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Simple:**
```
feat(api): add scan results endpoint
```

**With scope and body:**
```
fix(auth): resolve token expiration issue

JWT tokens were expiring immediately due to incorrect
timestamp calculation. Updated to use UTC timezone.

Fixes #234
```

**Breaking change:**
```
refactor(api): change scan response structure

BREAKING CHANGE: Scan endpoint now returns results in
a nested 'data' object instead of top-level array.

Migration guide: https://docs.example.com/migration
```

---

## Pull Request Process

### Before Creating PR

1. **Update from main:**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git rebase main
   ```

2. **Run all checks:**
   ```bash
   make lint
   make test
   ```

3. **Ensure conventional commits:**
   ```bash
   git log --oneline
   # Check all commits follow convention
   ```

### Creating the PR

1. **Push your branch:**
   ```bash
   git push origin your-branch
   ```

2. **Create PR with template:**
   - Clear title following conventional commits
   - Description of changes
   - Link related issues
   - Screenshots for UI changes
   - Test plan

3. **PR Template:**
   ```markdown
   ## Summary
   Brief description of changes

   ## Type of Change
   - [ ] feat: New feature
   - [ ] fix: Bug fix
   - [ ] docs: Documentation
   - [ ] refactor: Code refactoring
   - [ ] test: Tests

   ## Related Issues
   Closes #123

   ## Test Plan
   - [ ] Unit tests added/updated
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Screenshots (if applicable)
   [Add screenshots]

   ## Checklist
   - [ ] Code follows naming conventions
   - [ ] All linters pass
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Conventional commits used
   ```

### Code Review

- Address all review comments
- Keep commits atomic and well-formatted
- Update PR description if scope changes
- Re-request review after making changes

---

## Troubleshooting

### Common Issues

**1. ESLint errors after installing dependencies:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**2. Go module issues:**
```bash
cd backend
go mod tidy
go mod download
```

**3. Python import errors:**
```bash
cd workers
pip install -r requirements.txt --upgrade
```

**4. Docker containers not starting:**
```bash
docker-compose down -v
docker-compose up -d
```

**5. Database migration errors:**
```bash
make db-reset
```

### Getting Help

- Check [README.md](../README.md) for general setup
- Review [NAMING_CONVENTIONS.md](./NAMING_CONVENTIONS.md) for naming rules
- Open an issue on GitHub
- Contact the team

---

## Additional Resources

- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Effective Go](https://go.dev/doc/effective_go)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8 - Python Style Guide](https://pep8.org/)

---

**Happy Coding! 🚀**
