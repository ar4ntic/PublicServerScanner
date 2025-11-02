# Code Quality & Linting Setup Summary

This document summarizes all code quality tools and configurations that have been set up for the PublicScanner project.

## Overview

The project enforces code quality through:
- **Automated linting** for all languages (Go, TypeScript, Python)
- **Code formatting** tools for consistency
- **Naming conventions** enforcement
- **Conventional commits** for clear git history
- **Make commands** for easy execution

---

## Files Added

### Root Level
- `.gitignore` - Comprehensive ignore rules for all languages
- `.commitlintrc.json` - Conventional commits configuration
- `package.json` - Root package for husky and commitlint
- `Makefile` - Convenient make commands for development

### Documentation
- `docs/NAMING_CONVENTIONS.md` - Complete naming conventions guide
- `docs/DEVELOPMENT.md` - Comprehensive development guide
- `docs/CODE_QUALITY_SETUP.md` - This file

### Frontend (Next.js + TypeScript)
- `frontend/.eslintrc.json` - ESLint configuration
  - Naming convention rules
  - React hooks validation
  - Import ordering
  - TypeScript rules
- `frontend/.prettierrc.json` - Prettier code formatter
- Updated `frontend/package.json` - Added linting and formatting scripts

### Backend (Go)
- `backend/.golangci.yml` - golangci-lint configuration
  - 15+ linters enabled
  - Go naming conventions
  - Code quality checks
  - Import organization
- `backend/go.mod` - Updated with simple module path (`publicscannerapi`)

### Workers (Python)
- `workers/.flake8` - Flake8 linter configuration
- `workers/pyproject.toml` - Black, isort, mypy, pylint configuration
- Updated `workers/requirements.txt` - Added development linting tools

---

## Linting Tools by Component

### Frontend (TypeScript/React)

**ESLint** - Code quality and conventions
```bash
cd frontend
npm run lint          # Check for issues
npm run lint:fix      # Auto-fix issues
```

**Prettier** - Code formatting
```bash
cd frontend
npm run format        # Format all files
npm run format:check  # Check formatting
```

**TypeScript** - Type checking
```bash
cd frontend
npm run type-check    # Verify types
```

**Configured Rules:**
- ✅ camelCase for variables and functions
- ✅ PascalCase for components, interfaces, types
- ✅ UPPER_SNAKE_CASE for constants
- ✅ Hooks must start with `use`
- ✅ Import statement ordering
- ✅ No unused variables
- ✅ React hooks rules

---

### Backend (Go)

**golangci-lint** - Comprehensive Go linter
```bash
cd backend
golangci-lint run           # Run linter
golangci-lint run --fix     # Auto-fix
```

**Enabled Linters (15+):**
- `gofmt` - Code formatting
- `goimports` - Import formatting
- `govet` - Suspicious constructs
- `errcheck` - Unchecked errors
- `staticcheck` - Static analysis
- `unused` - Unused code
- `gosimple` - Simplify code
- `ineffassign` - Ineffectual assignments
- `typecheck` - Type checking
- `goconst` - Repeated strings
- `misspell` - Spelling
- `unparam` - Unused parameters
- `nakedret` - Naked returns
- `prealloc` - Preallocated slices
- `revive` - Fast linter
- `stylecheck` - Style checking

**Go Naming Conventions:**
- ✅ Lowercase/snake_case for file names
- ✅ PascalCase for exported types/functions
- ✅ camelCase for unexported types/functions
- ✅ Lowercase package names

**Installation:**
```bash
# macOS
brew install golangci-lint

# Linux
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s

# Windows
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

---

### Workers (Python)

**Flake8** - Style guide enforcement
```bash
cd workers
flake8 .
```

**Black** - Opinionated code formatter
```bash
cd workers
black .              # Format code
black --check .      # Check formatting
```

**isort** - Import organizer
```bash
cd workers
isort .              # Organize imports
isort --check-only . # Check organization
```

**MyPy** - Static type checker (optional)
```bash
cd workers
mypy .
```

**Pylint** - Code analysis (optional)
```bash
cd workers
pylint .
```

**Python Naming Conventions:**
- ✅ snake_case for files, functions, variables
- ✅ PascalCase for classes
- ✅ UPPER_SNAKE_CASE for constants

---

## Conventional Commits

**commitlint** enforces commit message format.

**Format:**
```
<type>(<scope>): <subject>
```

**Valid Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (no logic change)
- `refactor` - Code refactoring
- `perf` - Performance
- `test` - Tests
- `chore` - Maintenance
- `ci` - CI/CD
- `build` - Build system

**Examples:**
```bash
feat(api): add scan results endpoint
fix(auth): resolve token expiration issue
docs(readme): update installation guide
refactor(workers): simplify scan execution
test(handlers): add unit tests for auth
chore(deps): update dependencies
```

**Rules:**
- Type must be lowercase
- Subject max 72 characters
- No period at end
- Imperative mood ("add" not "added")

---

## Make Commands

Convenient shortcuts for development tasks.

```bash
make help              # Show all commands

# Development
make install           # Install all dependencies
make dev-up           # Start Docker environment
make dev-down         # Stop Docker environment

# Linting
make lint             # Run all linters
make lint-frontend    # Lint frontend
make lint-backend     # Lint backend
make lint-workers     # Lint workers

# Formatting
make format           # Format all code
make format-frontend  # Format frontend
make format-workers   # Format workers

# Testing
make test             # Run all tests
make test-frontend    # Test frontend
make test-backend     # Test backend
make test-workers     # Test workers

# Database
make db-migrate       # Run migrations
make db-seed          # Seed database
make db-reset         # Reset database

# Utilities
make clean            # Clean build artifacts
```

---

## Pre-commit Workflow

Before committing code, run:

```bash
# 1. Format code
make format

# 2. Run linters
make lint

# 3. Run tests
make test

# 4. Check types (frontend)
cd frontend && npm run type-check

# 5. Commit with conventional format
git commit -m "feat(scope): description"
```

---

## Audit Results

All existing files were audited against naming conventions:

### ✅ Frontend (Next.js/TypeScript)
- All framework files follow Next.js conventions
- Component structure ready for PascalCase components
- Configuration files properly named

### ✅ Backend (Go)
- All files follow Go conventions
- Package names: lowercase, single word
- File names: lowercase/snake_case
- Exported types: PascalCase
- Unexported: camelCase

### ✅ Workers (Python)
- All files follow Python conventions (snake_case)
- Modules, functions, variables: snake_case
- Classes would be: PascalCase
- Constants: UPPER_SNAKE_CASE

### ✅ Database Schema
- Tables: snake_case plural
- Columns: snake_case
- Foreign keys: `{table}_id` format
- Timestamps: `created_at`, `updated_at`

**Result:** No files needed renaming - all already compliant! ✅

---

## Integration with IDEs

### VS Code

**Recommended Extensions:**
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "golang.go",
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.isort"
  ]
}
```

**Settings (.vscode/settings.json):**
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[go]": {
    "editor.defaultFormatter": "golang.go"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "go.lintTool": "golangci-lint",
  "go.lintOnSave": "workspace",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black"
}
```

---

## CI/CD Integration

These tools can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Code Quality

on: [push, pull_request]

jobs:
  lint-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: cd frontend && npm ci && npm run lint

  lint-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v4
      - run: cd backend && golangci-lint run

  lint-workers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: cd workers && pip install -r requirements.txt && flake8 .

  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: wagoid/commitlint-github-action@v5
```

---

## Enforcement Summary

| Tool | Language | Enforces | Auto-fix |
|------|----------|----------|----------|
| ESLint | TypeScript/React | Naming, style, best practices | ✅ Partial |
| Prettier | TypeScript/React | Code formatting | ✅ Yes |
| golangci-lint | Go | Naming, style, errors, quality | ✅ Partial |
| Flake8 | Python | Style guide (PEP 8) | ❌ No |
| Black | Python | Code formatting | ✅ Yes |
| isort | Python | Import organization | ✅ Yes |
| MyPy | Python | Static types | ❌ No |
| commitlint | Git | Commit message format | ❌ No |

---

## Next Steps

1. **Install tools locally:**
   ```bash
   make install
   ```

2. **Try linting:**
   ```bash
   make lint
   ```

3. **Format code:**
   ```bash
   make format
   ```

4. **Read development guide:**
   - [docs/DEVELOPMENT.md](DEVELOPMENT.md)

5. **Review naming conventions:**
   - [docs/NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md)

6. **Set up IDE** with recommended extensions

7. **Practice conventional commits:**
   ```bash
   git commit -m "feat(api): add user endpoint"
   ```

---

## Support

If you encounter issues:

1. Check tool versions match requirements
2. Review configuration files
3. Consult [DEVELOPMENT.md](DEVELOPMENT.md)
4. Open an issue on GitHub

---

**Code quality maintained! 🎯**
