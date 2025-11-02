# Naming Conventions

This document outlines the naming conventions to be followed throughout the PublicScanner project. Consistent naming improves code readability, maintainability, and team collaboration.

## Overview Table

| Area | Convention | Examples |
|------|------------|----------|
| Frontend components/files | PascalCase | `UserMenu.tsx`, `RoleBasedRoute.tsx` |
| Frontend hooks | use + PascalCase | `useAuth()`, `useUserProfile()` |
| Functions/variables | camelCase | `handleLogin`, `isAuthenticated` |
| Constants | UPPER_SNAKE_CASE | `API_TIMEOUT_MS`, `MAX_RETRIES` |
| Backend files (Go) | lowercase/snake_case | `config.go`, `user.go`, `auth_handler.go` |
| API routes | kebab-case segments | `/api/dto-products`, `/api/auth/callback` |
| Classes/Types | PascalCase | `AuthService`, `UserRole` |
| Database schema | snake_case | `refresh_tokens`, `user_id` |
| Shared types | Single source in `shared/` | No duplication across FE/BE |
| Path aliases | Prefer aliases | FE: `@/*`, `@shell/*`<br>BE: `@shared/*`, `@gateway/*` |
| Commits | Conventional Commits | `feat(api): add refresh endpoint` |

---

## Detailed Guidelines

### 1. Frontend Components & Files

**Convention:** PascalCase

```typescript
// ✅ Good
UserMenu.tsx
RoleBasedRoute.tsx
ScanResultsTable.tsx
DashboardLayout.tsx

// ❌ Bad
userMenu.tsx
role-based-route.tsx
scan_results_table.tsx
```

**Rules:**
- Component files use PascalCase
- File name should match the component name
- One component per file (unless closely related)

---

### 2. Frontend Hooks

**Convention:** use + PascalCase

```typescript
// ✅ Good
useAuth()
useUserProfile()
useScanResults()
useTargetList()

// ❌ Bad
auth()
getAuth()
UserProfile()
scan_results()
```

**Rules:**
- Always prefix with `use`
- Follow with PascalCase descriptor
- Return values from hooks should be descriptive

```typescript
// Example
const { user, isLoading, error } = useAuth();
const { targets, refetch } = useTargetList();
```

---

### 3. Functions & Variables

**Convention:** camelCase

```typescript
// ✅ Good
handleLogin()
isAuthenticated
getUserProfile()
scanResults
totalFindings

// ❌ Bad
HandleLogin()
is_authenticated
get_user_profile()
ScanResults
total_findings
```

**Rules:**
- Functions: verb + noun (e.g., `handleSubmit`, `fetchData`)
- Booleans: is/has/can prefix (e.g., `isLoading`, `hasPermission`, `canEdit`)
- Variables: descriptive nouns (e.g., `userEmail`, `scanId`)

---

### 4. Constants

**Convention:** UPPER_SNAKE_CASE

```typescript
// ✅ Good
const API_TIMEOUT_MS = 5000;
const MAX_RETRIES = 3;
const DEFAULT_PAGE_SIZE = 20;
const JWT_EXPIRY_HOURS = 24;

// ❌ Bad
const apiTimeout = 5000;
const maxRetries = 3;
const defaultPageSize = 20;
```

**Rules:**
- All uppercase with underscores
- Place at top of file or in dedicated constants file
- Use for truly constant values (not configuration that might change)

```typescript
// constants/app.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
export const SCAN_POLL_INTERVAL_MS = 2000;
export const MAX_UPLOAD_SIZE_MB = 10;
```

---

### 5. Backend Files (Go)

**Convention:** lowercase or snake_case (follow Go conventions)

```bash
# ✅ Good
config.go
user.go
auth_handler.go
scan_repository.go
user_service.go

# ❌ Bad
Config.go
User.go
AuthHandler.go
scanRepository.go
auth-handler.go  # Go prefers underscores over hyphens
```

**Rules:**
- Use lowercase for single-word file names
- Use snake_case for multi-word file names
- Package names should be lowercase, single word
- One package per directory
- Group related files in same directory

**Go Specific Naming:**
- Exported types/functions: PascalCase (e.g., `type User struct{}`, `func GetUser()`)
- Unexported types/functions: camelCase (e.g., `type userRepo struct{}`, `func validateEmail()`)
- Package names: lowercase, no underscores (e.g., `package handlers`)

```
internal/
├── api/
│   ├── handlers/
│   │   ├── auth.go
│   │   ├── scan.go
│   │   └── target.go
│   └── middleware/
│       ├── auth.go
│       └── cors.go
├── models/
│   ├── user.go
│   ├── scan.go
│   └── organization.go
└── repository/
    ├── user_repository.go
    └── scan_repository.go
```

---

### 6. API Routes

**Convention:** kebab-case segments

```
# ✅ Good
/api/v1/dto-products
/api/v1/auth/callback
/api/v1/scan-results
/api/v1/user-profile

# ❌ Bad
/api/v1/dtoProducts
/api/v1/auth_callback
/api/v1/ScanResults
/api/v1/user_profile
```

**Rules:**
- Use lowercase
- Separate words with hyphens
- Use plural nouns for collections
- Use RESTful conventions

```
GET    /api/v1/targets
POST   /api/v1/targets
GET    /api/v1/targets/:id
PATCH  /api/v1/targets/:id
DELETE /api/v1/targets/:id

POST   /api/v1/scans
GET    /api/v1/scans/:id/results
POST   /api/v1/scans/:id/cancel
```

---

### 7. Classes & Types

**Convention:** PascalCase

```typescript
// ✅ Good - TypeScript
class AuthService {}
interface UserRole {}
type ScanStatus = 'queued' | 'running' | 'completed';

// ✅ Good - Go
type AuthService struct {}
type UserRole string
type ScanStatus string
```

```go
// ✅ Good - Go
type User struct {
    ID        uuid.UUID
    Email     string
    FirstName string
}

type ScanJob struct {
    ID       uuid.UUID
    TargetID uuid.UUID
    Status   ScanStatus
}

// ❌ Bad
type user struct {}
type scan_job struct {}
```

**Rules:**
- Always use PascalCase for class/struct/interface/type names
- Use descriptive, singular nouns
- Avoid abbreviations unless widely understood

---

### 8. Database Schema

**Convention:** snake_case

```sql
-- ✅ Good
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255),
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE scan_jobs (
    id UUID PRIMARY KEY,
    target_id UUID,
    organization_id UUID,
    started_at TIMESTAMP
);

-- ❌ Bad
CREATE TABLE Users (
    ID UUID,
    Email VARCHAR,
    passwordHash VARCHAR,
    firstName VARCHAR
);
```

**Rules:**
- Table names: plural, snake_case (e.g., `users`, `scan_jobs`)
- Column names: snake_case (e.g., `user_id`, `created_at`)
- Foreign keys: `{table_singular}_id` (e.g., `user_id`, `organization_id`)
- Timestamps: `created_at`, `updated_at`, `deleted_at`
- Booleans: `is_{descriptor}` (e.g., `is_active`, `is_verified`)

---

### 9. Shared Types

**Convention:** Single source in `shared/` directory

```typescript
// ✅ Good - Define once in shared/
// shared/types/user.ts
export interface User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
}

// frontend/lib/api.ts
import { User } from '@shared/types/user';

// backend/internal/models/user.go
// Generate or manually sync with shared types
```

**Rules:**
- Define shared types in a `shared/` directory
- No duplication across frontend/backend
- Use code generation tools when possible (e.g., TypeScript from OpenAPI)
- Keep types in sync between FE/BE

```
shared/
├── types/
│   ├── user.ts
│   ├── scan.ts
│   ├── target.ts
│   └── report.ts
└── constants/
    ├── scan-status.ts
    └── severity-levels.ts
```

---

### 10. Path Aliases

**Convention:** Prefer aliases over relative paths

```typescript
// ✅ Good - Frontend
import { UserMenu } from '@/components/layout/UserMenu';
import { useAuth } from '@/hooks/useAuth';
import { API_BASE_URL } from '@/constants/app';

// ❌ Bad
import { UserMenu } from '../../../components/layout/UserMenu';
import { useAuth } from '../../hooks/useAuth';
```

**Configuration:**

**Frontend (tsconfig.json):**
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"],
      "@components/*": ["./components/*"],
      "@hooks/*": ["./hooks/*"],
      "@lib/*": ["./lib/*"],
      "@shared/*": ["../shared/*"]
    }
  }
}
```

**Backend (if using TypeScript):**
```json
{
  "compilerOptions": {
    "paths": {
      "@shared/*": ["../shared/*"],
      "@gateway/*": ["./gateway/*"]
    }
  }
}
```

---

### 11. Conventional Commits

**Convention:** Follow Conventional Commits specification

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples:**

```bash
# ✅ Good
feat(api): add refresh endpoint
fix(auth): resolve token expiry issue
docs(readme): update installation instructions
refactor(scan): simplify port scanning logic
test(handlers): add auth handler unit tests
chore(deps): update dependencies

# With scope and body
feat(frontend): add scan results dashboard

- Add results table component
- Implement pagination
- Add export to CSV functionality

Closes #123

# ❌ Bad
Added new feature
fixed bug
updated files
changes
```

**Rules:**
- Use lowercase for type and scope
- Keep subject line under 72 characters
- Use imperative mood ("add" not "added" or "adds")
- Reference issues in footer when applicable

---

## Quick Reference Cheat Sheet

```
Frontend Components:     UserMenu.tsx
Frontend Hooks:          useAuth()
Functions/Variables:     handleLogin, isAuthenticated
Constants:               API_TIMEOUT_MS
Backend Files (Go):      config.go, auth_handler.go
Backend Types (Go):      type User struct{}, func GetUser()
API Routes:              /api/v1/scan-results
Classes/Types:           AuthService, UserRole
Database Tables:         scan_jobs, user_id
Python Files:            celery_app.py, tasks.py
Path Aliases:            @/components/UserMenu
Git Commits:             feat(api): add endpoint
```

---

## Enforcement

### Pre-commit Hooks

Use tools to enforce naming conventions:

- **ESLint** for JavaScript/TypeScript
- **golangci-lint** for Go
- **commitlint** for commit messages

### Code Review Checklist

- [ ] Component names are PascalCase
- [ ] Hooks start with `use`
- [ ] Constants are UPPER_SNAKE_CASE
- [ ] Database columns are snake_case
- [ ] API routes use kebab-case
- [ ] Commit message follows Conventional Commits
- [ ] No duplicate types across FE/BE

---

## Exceptions

Naming conventions may be relaxed for:
- Third-party library compatibility
- Industry-standard terms (e.g., `OAuth2`, `JWT`)
- Generated code
- Migration files with timestamps

Always document exceptions with comments explaining why the deviation is necessary.

---

**Last Updated:** 2025-11-02
**Version:** 1.0
