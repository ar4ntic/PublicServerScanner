# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PublicScanner is a web-based security vulnerability scanner platform with three main components:
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS v4
- **Backend**: Go API server with Gin framework
- **Workers**: Python Celery workers executing security scans

## Essential Commands

### Development Environment

```bash
# Start everything with Docker
make dev-up

# Initialize/reset database
make db-reset

# Stop environment
make dev-down

# Show all available commands
make help
```

### Building & Running

```bash
# Frontend (Next.js)
cd frontend
npm install
npm run dev          # Development server
npm run build        # Production build
npm run type-check   # TypeScript validation

# Backend (Go)
cd backend
go mod download
go run cmd/api/main.go
go test ./...        # Run tests

# Workers (Python)
cd workers
pip install -r requirements.txt
celery -A tasks worker --loglevel=info
```

### Code Quality

```bash
# Run all linters
make lint

# Lint specific components
make lint-frontend   # ESLint + TypeScript
make lint-backend    # golangci-lint
make lint-workers    # Flake8 + Black

# Format code
make format          # All components
make format-frontend # Prettier
make format-workers  # Black + isort

# Run tests
make test            # All tests
make test-frontend
make test-backend
make test-workers
```

### Database

```bash
# Reset database (drop, reload schema, seed)
make db-reset

# Load schema only
make db-schema

# Seed data only
make db-seed
```

## Architecture

### Hybrid Microservices Design

**Why this architecture?**
- **Go Backend**: Performance-critical API server (5-10x lower memory than Python)
- **Python Workers**: Leverage existing security tools (nmap, nikto, gobuster)
- **Next.js Frontend**: Modern SSR with App Router

### Data Flow

```
User Request → Next.js Frontend → Go API → PostgreSQL
                                         ↓
                                    Redis Queue
                                         ↓
                                  Python Workers
                                         ↓
                                  PostgreSQL (Results)
```

### Module Path Convention

Go uses simple module name: `publicscannerapi` (no GitHub URL). Import internal packages:

```go
import "publicscannerapi/internal/config"
import "publicscannerapi/internal/models"
```

### Database Strategy (Pre-Production)

**IMPORTANT**: We use a single `database/schema.sql` file, NOT migrations.

Why? Pre-production phase allows schema iteration without migration overhead.

**Making schema changes:**
1. Edit `database/schema.sql` directly
2. Run `make db-reset`
3. Commit the schema file

**After production launch:** Convert to migration-based system. See `database/README.md`.

### Tailwind CSS v4

Uses new `@import "tailwindcss"` syntax in `app/globals.css`. No `tailwind.config.ts` or `postcss.config.js` needed.

Theme configuration via `@theme` blocks in CSS:

```css
@import "tailwindcss";

@theme {
  --color-primary: 221.2 83.2% 53.3%;
}

@theme dark {
  --color-primary: 217.2 91.2% 59.8%;
}
```

## Naming Conventions

**Strict enforcement via linters:**

| Component | Convention | Example |
|-----------|-----------|---------|
| Frontend components | PascalCase | `UserMenu.tsx` |
| Frontend hooks | use + PascalCase | `useAuth()` |
| Functions/variables | camelCase | `handleLogin`, `isAuthenticated` |
| Constants | UPPER_SNAKE_CASE | `API_TIMEOUT_MS` |
| Go files | lowercase/snake_case | `user.go`, `auth_handler.go` |
| Go exports | PascalCase | `type User struct{}`, `func GetUser()` |
| Go unexported | camelCase | `func validateEmail()` |
| Python files/functions | snake_case | `scan_repository.py`, `execute_scan()` |
| Python classes | PascalCase | `class ScanResult` |
| Database tables | snake_case plural | `users`, `scan_jobs` |
| Database columns | snake_case | `user_id`, `created_at` |
| API routes | kebab-case | `/api/scan-results` |

## Commit Message Format

**Required**: Conventional Commits enforced by commitlint.

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore, perf, ci
Scopes: api, frontend, workers, db, auth, scan, docs

Examples:
feat(api): add scan results endpoint
fix(auth): resolve token expiration
docs(readme): update installation guide
```

## Project-Specific Patterns

### Security Scans Execution

Workers execute scans via Celery tasks. Each check is a module in `workers/checks/`:

```python
# workers/checks/portscan.py
def port_scan_check(target: str, config: Dict) -> Dict:
    # Returns: {'status': 'success', 'data': {...}, 'findings': N, 'severity': 'high'}
```

Results stored in PostgreSQL with JSONB for flexibility.

### PostgreSQL + JSONB Pattern

Structured data in columns, flexible scan results in JSONB:

```sql
CREATE TABLE scan_results (
    id UUID PRIMARY KEY,
    scan_id UUID NOT NULL,
    check_type VARCHAR(50),
    data JSONB NOT NULL  -- Flexible per-check data
);
```

### Go API Structure

```
backend/
├── cmd/api/main.go           # Entry point
├── internal/
│   ├── api/
│   │   ├── handlers/         # HTTP handlers
│   │   ├── middleware/       # Auth, CORS, etc.
│   │   └── routes/           # Route definitions
│   ├── config/               # Config management
│   ├── models/               # Data models (User, Scan, etc.)
│   ├── repository/           # Database layer
│   └── services/             # Business logic
└── pkg/                      # Reusable packages
```

### Next.js App Router Structure

```
frontend/app/
├── (auth)/                   # Route group (no URL segment)
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/page.tsx
├── globals.css               # Tailwind v4 config
├── layout.tsx                # Root layout
└── providers.tsx             # React Query provider
```

## Code Quality Tools

**All configured and enforced:**

- **Frontend**: ESLint (naming + React rules), Prettier (formatting)
- **Backend**: golangci-lint (15+ linters including gofmt, govet, staticcheck)
- **Workers**: Flake8 (PEP 8), Black (formatting), isort (imports)
- **Commits**: commitlint (Conventional Commits)

Pre-commit workflow:
```bash
make format  # Auto-format everything
make lint    # Check all linters
make test    # Run all tests
git commit -m "feat(scope): description"
```

## Environment Configuration

Copy `.env.example` to `.env`. Key variables:

```env
# API
PORT=8080

# Database
DB_HOST=postgres
DB_NAME=publicscanner

# Redis
REDIS_HOST=redis

# JWT
JWT_SECRET=your-secret-key-change-in-production

# Storage (filesystem, not S3)
STORAGE_PATH=/opt/publicscannerdata
```

**Storage**: Uses PostgreSQL + local filesystem. No MinIO/S3 initially for simplicity on VPS.

## Development Credentials

Test user (from seed data):
- Email: `admin@example.com`
- Password: `Test1234!`

**Access points:**
- Frontend: http://localhost:3000
- API: http://localhost:8080
- API Health: http://localhost:8080/health
- Flower (Celery): http://localhost:5555

## Documentation References

- `README.md` - Project overview and quick start
- `docs/DEVELOPMENT.md` - Comprehensive development guide
- `docs/NAMING_CONVENTIONS.md` - Complete naming rules
- `docs/CODE_QUALITY_SETUP.md` - Linting configuration details
- `docs/TAILWIND_V4_MIGRATION.md` - Tailwind v4 usage
- `database/README.md` - Database strategy and migration plan
- `frontend/README.md` - Frontend-specific documentation

## Current Project Status

**Phase**: Foundation & Development (Pre-Production)

**Complete:**
- ✅ Project structure and architecture
- ✅ Database schema (single file, pre-migration)
- ✅ Docker development environment
- ✅ Code quality tooling (ESLint, golangci-lint, flake8, black, prettier)
- ✅ Frontend auth UI (login, register)
- ✅ Backend API structure (Go + Gin)
- ✅ Worker security checks (6 core checks: ping, port scan, headers, SSL, DNS, directory brute-force)

**In Progress:**
- 🚧 Complete authentication implementation (JWT, register, login handlers)
- 🚧 Dashboard and scan management UI
- 🚧 Report generation system

**Planned:**
- 📅 9+ additional security checks (WAF detection, subdomain enum, etc.)
- 📅 Payment integration (Stripe)
- 📅 PDF report generation
- 📅 Scan scheduling
