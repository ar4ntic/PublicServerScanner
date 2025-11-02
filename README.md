# PublicScanner - Security Vulnerability Scanner Platform

[![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](LICENSE)
[![Go Version](https://img.shields.io/badge/go-1.21+-00ADD8.svg)](https://golang.org)
[![Node Version](https://img.shields.io/badge/node-20+-339933.svg)](https://nodejs.org)
[![Python Version](https://img.shields.io/badge/python-3.11+-3776AB.svg)](https://python.org)

A comprehensive web-based security assessment platform for public-facing servers. Built with Next.js, Go, and Python, PublicScanner provides automated security scanning, vulnerability detection, and detailed compliance reporting.

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#-quick-start)
- [Manual Setup](#manual-setup)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Security Checks](#security-checks)
- [Development](#-development)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Support](#support)

## ✨ Features

- **15+ Security Checks**: Port scanning, SSL/TLS analysis, HTTP headers, DNS enumeration, directory brute-force, and more
- **User Authentication**: Secure JWT-based authentication with role-based access control
- **Organization Support**: Multi-user teams with different permission levels
- **Real-time Progress**: WebSocket-based live scan progress tracking
- **Comprehensive Reports**: PDF, HTML, JSON, and CSV export formats
- **Compliance Mapping**: OWASP Top 10, CIS Benchmarks, PCI-DSS
- **REST API**: Full-featured API for programmatic access
- **Scheduled Scans**: Automated recurring security assessments
- **Code Quality**: Automated linting, formatting, and conventional commits

## Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS v4** - Utility-first CSS framework (new @import syntax)
- **React Query** - Data fetching and state management
- **Zod** - Schema validation

### Backend
- **Go (Golang)** - High-performance API server
- **Gin** - Web framework
- **PostgreSQL 15** - Primary database with JSONB support
- **Redis** - Caching and job queue

### Workers
- **Python 3.11** - Security scan execution
- **Celery** - Distributed task queue
- **Security Tools**: nmap, nikto, gobuster, openssl, dig

## Project Structure

```
PublicServerScanner/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   └── lib/              # Utilities and API clients
├── backend/              # Go API server
│   ├── cmd/api/          # Main entry point
│   ├── internal/         # Private application code
│   │   ├── api/          # HTTP handlers and routes
│   │   ├── config/       # Configuration management
│   │   ├── models/       # Data models
│   │   ├── repository/   # Database layer
│   │   └── services/     # Business logic
│   └── pkg/              # Public packages
├── workers/              # Python Celery workers
│   ├── checks/           # Security check modules
│   ├── tasks.py          # Celery task definitions
│   └── database.py       # Database operations
├── database/             # Database files
│   ├── schema.sql        # Database schema (pre-production)
│   └── seeds/            # Development seed data
├── docker/               # Docker configurations
│   ├── Dockerfile.api
│   ├── Dockerfile.frontend
│   └── Dockerfile.worker
└── docker-compose.yml    # Development environment
```

## Prerequisites

- **Docker** and **Docker Compose** (recommended for local development)
- OR install manually:
  - Go 1.21+
  - Node.js 20+
  - Python 3.11+
  - PostgreSQL 15+
  - Redis 7+
  - Security tools: nmap, nikto, gobuster, openssl, dig

## 🚀 Quick Start

### With Docker (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd PublicServerScanner

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Start development environment
make dev-up

# 4. Initialize database
make db-reset

# 5. Access the application
# Frontend:  http://localhost:3000
# API:       http://localhost:8080
# Flower:    http://localhost:5555

# 6. Login with test credentials
# Email:    admin@example.com
# Password: Test1234!
```

### Essential Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install all dependencies |
| `make dev-up` | Start development environment |
| `make dev-down` | Stop development environment |
| `make db-reset` | Reset and seed database |
| `make lint` | Run all linters |
| `make format` | Format all code |
| `make test` | Run all tests |
| `make clean` | Clean build artifacts |

💡 **Tip:** Run `make help` to see the complete list of available commands.

## Manual Setup

### 1. Database Setup

```bash
# Create database
createdb publicscanner

# Load schema
psql -d publicscanner -f database/schema.sql

# Load seed data (development only)
psql -d publicscanner -f database/seeds/001_dev_data.sql
```

### 2. Backend (Go API)

```bash
cd backend

# Install dependencies (go.mod already created)
go mod download

# Run the API server
go run cmd/api/main.go
```

### 3. Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### 4. Workers (Python/Celery)

```bash
cd workers

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Celery worker
celery -A tasks worker --loglevel=info

# Optional: Start Flower for monitoring
celery -A tasks flower
```

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Server
PORT=8080
ENVIRONMENT=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=publicscanner

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-secret-key-change-in-production
JWT_ACCESS_TTL=15
JWT_REFRESH_TTL=168

# Storage
STORAGE_PATH=/opt/publicscannerdata

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## API Documentation

### Authentication Endpoints

```
POST /api/v1/auth/register    - Register new user
POST /api/v1/auth/login       - Login and get JWT token
POST /api/v1/auth/refresh     - Refresh access token
GET  /api/v1/users/me         - Get current user profile
```

### Scan Endpoints

```
GET    /api/v1/targets        - List all targets
POST   /api/v1/targets        - Create new target
GET    /api/v1/targets/:id    - Get target details
PATCH  /api/v1/targets/:id    - Update target
DELETE /api/v1/targets/:id    - Delete target

GET    /api/v1/scans          - List all scans
POST   /api/v1/scans          - Initiate new scan
GET    /api/v1/scans/:id      - Get scan details
GET    /api/v1/scans/:id/results - Get scan results
DELETE /api/v1/scans/:id      - Cancel/delete scan
```

### Report Endpoints

```
GET  /api/v1/reports          - List all reports
POST /api/v1/reports/generate - Generate new report
GET  /api/v1/reports/:id      - Get report details
GET  /api/v1/reports/:id/download - Download report file
```

## Security Checks

PublicScanner includes the following security checks:

1. **Ping/Availability** - Target reachability testing
2. **Port Scanning** - TCP/UDP port enumeration with service detection
3. **HTTP Security Headers** - Missing security headers detection
4. **SSL/TLS Certificate** - Certificate validation and expiry checking
5. **DNS Enumeration** - DNS record discovery and zone transfer testing
6. **Directory Brute-Force** - Web directory/file enumeration
7. **WAF Detection** (planned)
8. **Subdomain Enumeration** (planned)
9. **Technology Stack Detection** (planned)
10. **Vulnerability Scanning** (planned)
11. **API Security Testing** (planned)
12. **JavaScript Analysis** (planned)
13. **Email Security (SPF/DKIM/DMARC)** (planned)
14. **CORS Misconfiguration** (planned)
15. **Rate Limiting Testing** (planned)

## 👨‍💻 Development

### Code Quality & Standards

PublicScanner enforces strict code quality standards across all components:

- ✅ **ESLint** - TypeScript/React linting with naming conventions
- ✅ **Prettier** - Automatic code formatting
- ✅ **golangci-lint** - 15+ Go linters for backend quality
- ✅ **Flake8, Black, isort** - Python code quality and formatting
- ✅ **Conventional Commits** - Standardized git commit messages
- ✅ **Automated Testing** - Unit and integration tests

### Quick Development Commands

```bash
# Code Quality
make lint              # Run all linters
make lint-frontend     # Lint Next.js + TypeScript
make lint-backend      # Lint Go code
make lint-workers      # Lint Python code
make format            # Format all code
make format-frontend   # Format TypeScript/React
make format-workers    # Format Python

# Testing
make test              # Run all tests
make test-frontend     # Test frontend
make test-backend      # Test backend (Go)
make test-workers      # Test workers (Python)

# Development Workflow
make dev-up            # Start development environment
make dev-down          # Stop development environment
make db-schema         # Load database schema
make db-seed           # Seed with test data
make db-reset          # Reset database (drop, schema, seed)
make clean             # Clean build artifacts
```

### Pre-commit Workflow

Before committing code:

```bash
# 1. Format your code
make format

# 2. Run linters
make lint

# 3. Run tests
make test

# 4. Commit with conventional format
git commit -m "feat(api): add user authentication endpoint"
```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Scopes: api, frontend, workers, db, auth, scan, docs

Examples:
feat(api): add scan results endpoint
fix(auth): resolve token expiration issue
docs(readme): update installation guide
```

### Documentation

- 📘 [Development Guide](docs/DEVELOPMENT.md) - Comprehensive development workflow
- 📐 [Naming Conventions](docs/NAMING_CONVENTIONS.md) - Coding standards and naming rules
- 🔧 [Code Quality Setup](docs/CODE_QUALITY_SETUP.md) - Linting and tooling configuration

### IDE Setup

**Recommended VS Code Extensions:**
- ESLint
- Prettier
- Go
- Python
- GitLens

**Auto-format on save:** See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#integration-with-ides) for configuration.

## Deployment

### Production Docker Build

```bash
# Build all images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### VPS Deployment

Minimum requirements:
- 4 vCPU
- 8GB RAM
- 100GB SSD
- Ubuntu 22.04 LTS

See `docs/deployment.md` for detailed deployment instructions.

## Roadmap

### Phase 1 (Current)
- [x] Core project structure
- [x] Database schema design
- [x] Authentication system
- [ ] Complete Go API implementation
- [ ] Dashboard UI
- [ ] Basic scan execution

### Phase 2
- [ ] PDF report generation
- [ ] Scan scheduling
- [ ] Email notifications
- [ ] Organization management
- [ ] Payment integration (Stripe)

### Phase 3
- [ ] Advanced security checks
- [ ] Compliance framework mapping
- [ ] Webhook integrations
- [ ] API rate limiting
- [ ] SSO support

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/PublicServerScanner.git
   cd PublicServerScanner
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow [naming conventions](docs/NAMING_CONVENTIONS.md)
   - Write clean, documented code
   - Add tests for new features

4. **Ensure code quality**
   ```bash
   make format  # Format code
   make lint    # Check linting
   make test    # Run tests
   ```

5. **Commit with conventional commits**
   ```bash
   git commit -m "feat(scope): description of changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Open a Pull Request on GitHub
   ```

### Code Quality Requirements

All PRs must:
- ✅ Pass all linters (`make lint`)
- ✅ Pass all tests (`make test`)
- ✅ Follow naming conventions
- ✅ Use conventional commit messages
- ✅ Include documentation updates
- ✅ Add tests for new features

### Pull Request Template

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

## Checklist
- [ ] Code follows naming conventions
- [ ] All linters pass
- [ ] Tests pass
- [ ] Documentation updated
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed contribution guidelines.

## License

Copyright © 2025 Arantic Digital. All rights reserved.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - project overview and quick start |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Comprehensive development guide with tooling |
| [NAMING_CONVENTIONS.md](docs/NAMING_CONVENTIONS.md) | Coding standards and naming rules |
| [CODE_QUALITY_SETUP.md](docs/CODE_QUALITY_SETUP.md) | Linting and code quality configuration |
| [TAILWIND_V4_MIGRATION.md](docs/TAILWIND_V4_MIGRATION.md) | Tailwind CSS v4 migration guide |
| [Database README](database/README.md) | Database schema and migration strategy |
| [FUNCTIONALITY_SUMMARY.md](FUNCTIONALITY_SUMMARY.md) | Legacy system functionality analysis |

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/arantic/PublicServerScanner/issues)
- **Email**: support@arantic.com
- **Website**: https://arantic.com

## 🙏 Acknowledgments

- Built on the foundation of PublicServerScanner (Legacy)
- Uses industry-standard security tools: nmap, nikto, gobuster, openssl, dig
- Inspired by OWASP best practices and security frameworks
- Powered by Next.js, Go, Python, PostgreSQL, and Redis

## 📊 Project Status

### Current Phase: Foundation & Development
- ✅ Project structure and architecture
- ✅ Database schema designed and implemented
- ✅ Docker development environment
- ✅ Code quality tooling configured
- ✅ Frontend authentication UI
- ✅ Backend API structure
- ✅ Worker security checks (6 core checks)
- 🚧 Complete authentication implementation
- 🚧 Dashboard and scan management UI
- 🚧 Report generation system
- 📅 Advanced security checks (planned)
- 📅 Payment integration (planned)

### Tech Stack Status
| Component | Technology | Status |
|-----------|-----------|---------|
| Frontend | Next.js 14 + TypeScript | ✅ Setup Complete |
| Backend | Go + Gin | ✅ Structure Ready |
| Workers | Python + Celery | ✅ 6 Checks Working |
| Database | PostgreSQL 15 | ✅ Schema Complete |
| Cache/Queue | Redis | ✅ Configured |
| DevOps | Docker Compose | ✅ Working |
| Code Quality | ESLint, golangci-lint, flake8 | ✅ All Configured |

---

<div align="center">

**Made with ❤️ by [Arantic Digital](https://arantic.com)**

⭐ Star this repo if you find it helpful!

</div>
