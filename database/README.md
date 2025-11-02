# Database Documentation

## Pre-Production Approach (Current)

During development and before going live, we use a **single schema file** instead of migrations for simplicity and flexibility.

### Structure

```
database/
├── schema.sql           # Complete database schema
└── seeds/
    └── 001_dev_data.sql # Development seed data
```

### Why No Migrations Yet?

**Benefits of Schema-First Approach (Pre-Production):**
- ✅ **Easier to iterate**: Change schema freely without managing migration history
- ✅ **Simpler setup**: New developers just load one file
- ✅ **Faster development**: No migration versioning overhead
- ✅ **Clean slate**: Can reset database instantly
- ✅ **No migration conflicts**: Team members don't step on each other's migrations

**This approach is perfect when:**
- You're still designing and iterating on the schema
- No production data exists yet
- Team can reset databases without consequence
- Schema changes frequently

### Loading the Database

**With Docker:**
```bash
# Database is automatically initialized on first run
make dev-up

# Reset database (drop, load schema, seed)
make db-reset

# Load schema only
make db-schema

# Seed data only
make db-seed
```

**Manually:**
```bash
# Create database
createdb publicscanner

# Load schema
psql -d publicscanner -f database/schema.sql

# Load seed data (optional, dev only)
psql -d publicscanner -f database/seeds/001_dev_data.sql
```

### Making Schema Changes

1. **Edit schema.sql directly**
   ```bash
   vim database/schema.sql
   # Make your changes
   ```

2. **Reset local database**
   ```bash
   make db-reset
   ```

3. **Commit changes**
   ```bash
   git add database/schema.sql
   git commit -m "feat(db): add column to users table"
   ```

4. **Team members pull and reset**
   ```bash
   git pull
   make db-reset
   ```

**That's it!** No migration files, no version tracking (yet).

---

## Post-Production Approach (Future)

### When to Switch to Migrations?

**Switch to migrations when:**
- ✅ You're going live/production
- ✅ Production data exists that can't be lost
- ✅ You need to preserve existing data during schema changes
- ✅ Multiple environments need coordinated updates

### Migration Strategy (After Launch)

Once in production, you'll switch to a migration-based approach:

```
database/
├── schema.sql                    # Keep for reference
├── migrations/
│   ├── 001_initial_schema.sql   # Created from schema.sql
│   ├── 002_add_user_role.sql
│   ├── 003_add_api_keys.sql
│   └── ...
└── seeds/
    └── 001_dev_data.sql
```

### Migration Tools

You'll use one of these tools:

**Option 1: golang-migrate** (Recommended for Go projects)
```bash
# Install
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Create migration
migrate create -ext sql -dir database/migrations -seq add_user_role

# Run migrations
migrate -path database/migrations -database "postgres://localhost/publicscanner?sslmode=disable" up

# Rollback
migrate -path database/migrations -database "postgres://localhost/publicscanner?sslmode=disable" down 1
```

**Option 2: Flyway** (Popular, language-agnostic)
```bash
# Install with Docker
docker run --rm -v $(pwd)/database/migrations:/flyway/sql flyway/flyway migrate

# Config in flyway.conf
flyway.url=jdbc:postgresql://localhost/publicscanner
flyway.user=postgres
flyway.password=postgres
```

**Option 3: Custom Go migrations**
```go
// In your Go app
import "github.com/golang-migrate/migrate/v4"

func RunMigrations(db *sql.DB) error {
    m, err := migrate.New(
        "file://database/migrations",
        "postgres://localhost/publicscanner?sslmode=disable",
    )
    if err != nil {
        return err
    }
    return m.Up()
}
```

### Migration File Format

```sql
-- 002_add_user_role.sql (UP migration)
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'member';
UPDATE users SET role = 'owner' WHERE id IN (SELECT owner_id FROM organizations);

-- Add reverse migration in separate file or use golang-migrate format
-- 002_add_user_role.down.sql
ALTER TABLE users DROP COLUMN role;
```

### Best Practices for Migrations (Future)

1. **Always have a rollback plan**
   - Write DOWN migrations
   - Test rollbacks before deploying

2. **Never modify existing migrations**
   - Once deployed to production, migrations are immutable
   - Create new migration to fix issues

3. **Keep migrations small and focused**
   - One logical change per migration
   - Easier to review and rollback

4. **Test migrations on staging first**
   - Apply to staging environment
   - Verify application works
   - Then deploy to production

5. **Back up before major migrations**
   ```bash
   pg_dump publicscanner > backup_$(date +%Y%m%d).sql
   ```

6. **Include data migrations carefully**
   - Large data migrations can lock tables
   - Consider batching updates
   - Use transactions wisely

---

## Development Seed Data

### Current Seed Data

The `seeds/001_dev_data.sql` file contains:
- Test users (admin@example.com, user@example.com)
- Test organization
- Sample targets
- Sample completed scan
- Sample scan results

**Default credentials:**
- Email: `admin@example.com`
- Password: `Test1234!`

### Adding Seed Data

1. Edit `database/seeds/001_dev_data.sql`
2. Add your test data
3. Reset database: `make db-reset`

**Rules for seed data:**
- ⚠️ **Never commit production data**
- ⚠️ **Never commit real user credentials**
- ✅ Use obvious test data (example.com, test passwords)
- ✅ Keep seed data minimal but functional

---

## Schema Overview

### Core Tables

**Users & Authentication:**
- `users` - User accounts
- `api_keys` - API authentication tokens
- `audit_logs` - Security audit trail

**Organizations:**
- `organizations` - Teams/companies
- `organization_members` - User membership and roles

**Scanning:**
- `targets` - Scan targets (domains, IPs)
- `scan_jobs` - Scan execution tracking
- `scan_results` - Individual check results

**Reporting:**
- `reports` - Generated report metadata
- `webhooks` - Integration webhooks

### Key Features

**UUID Primary Keys:**
```sql
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
```

**JSONB for Flexibility:**
```sql
config JSONB DEFAULT '{}',
data JSONB NOT NULL DEFAULT '{}'
```

**Automatic Timestamps:**
```sql
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
-- Triggers auto-update updated_at
```

**Referential Integrity:**
```sql
FOREIGN KEY ... ON DELETE CASCADE
FOREIGN KEY ... ON DELETE SET NULL
```

---

## Transitioning to Migrations (Checklist)

When you're ready to go live:

- [ ] 1. **Backup current schema**
  ```bash
  cp database/schema.sql database/schema_backup_$(date +%Y%m%d).sql
  ```

- [ ] 2. **Create migrations directory**
  ```bash
  mkdir -p database/migrations
  ```

- [ ] 3. **Convert schema to first migration**
  ```bash
  cp database/schema.sql database/migrations/001_initial_schema.sql
  ```

- [ ] 4. **Choose migration tool**
  - Install golang-migrate, Flyway, or similar

- [ ] 5. **Update deployment scripts**
  - Replace `psql -f schema.sql` with migration tool

- [ ] 6. **Update Makefile**
  - Add `make db-migrate` command
  - Keep `make db-reset` for development

- [ ] 7. **Update documentation**
  - Document migration process
  - Update developer onboarding docs

- [ ] 8. **Train team**
  - Explain migration workflow
  - Review best practices

---

## FAQs

**Q: Can I still use `make db-reset` after going live?**
A: In development environments, yes. In production, NO! Use migrations instead.

**Q: What if I need to change the schema now?**
A: Edit `schema.sql` directly and run `make db-reset`. Easy!

**Q: How do I sync schema changes with the team?**
A: Commit `schema.sql` to git. Team runs `make db-reset` after pulling.

**Q: What happens to seed data in production?**
A: Seed files are for development only. Don't run them in production.

**Q: When exactly should we switch to migrations?**
A: When you deploy to production and have real user data you can't lose.

**Q: Can we go back to schema.sql after using migrations?**
A: No. Once you have production data, migrations are the only safe way.

---

## Summary

### Current Workflow (Pre-Production)
```
Edit schema.sql → make db-reset → Commit → Team pulls & resets
```

### Future Workflow (Post-Production)
```
Create migration → Test locally → Review → Deploy to staging → Deploy to prod
```

**The key insight:** Use the right tool for the right phase!
- **Pre-production:** Schema file (simple, flexible)
- **Production:** Migrations (safe, controlled, reversible)

---

**Last Updated:** 2025-11-02
**Status:** Pre-Production (Schema-First)
**Next Review:** Before Production Launch
