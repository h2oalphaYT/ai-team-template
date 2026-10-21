---
name: database-migration
description: Plan, write and verify a database schema or data migration in the project's actual engine and migration tool (Flyway, Liquibase, golang-migrate, goose, Atlas, Prisma, TypeORM, Knex, Alembic, Django, EF Core, Mongoose and others). Use for any table, column, index, constraint, collection or data change. Requires a rollback plan and explicit approval for destructive operations.
argument-hint: "<schema or data change>"
---

# Database Migration

Change: $ARGUMENTS

Use inside the `/execute-task` lifecycle. Delegate the technical work to the
`database-engineer` agent. This skill defines the mandatory steps and gates.

**Use when:** a schema, index, constraint, seed, or bulk data change is needed. **Do not use**
for query-only tuning with no schema change (use `/execute-task` with `database-engineer`), or
to run migrations against shared or production databases (that is a deployment step that needs
explicit approval).

## 1. Identify engine and tooling (evidence required)

- Engine and version: driver packages, ORM dialect, Compose services, docs. Never read or print
  credentials; ignore `.env` and use `.env.example`.
- Migration tool, migration directory, naming and ordering convention, and how migrations run
  (CLI, app start-up, CI step).
- If engine or tool cannot be determined, stop and ask.

## 2. Inspect the current schema

Read existing migrations, models, and schema dumps to learn the real tables, columns, types,
indexes, constraints, and relationships affected. Find all code that reads or writes them
(grep). Never assume a schema.

## 3. Plan (write it down)

- Forward change, and whether it is **additive** (safe) or **destructive** (drop, rename,
  narrowing type change, NOT NULL on existing data, bulk update/delete).
- Prefer expand → migrate → contract across releases for anything running code depends on.
- Locking and downtime impact for the engine (for example `CREATE INDEX CONCURRENTLY` in
  PostgreSQL, online index options in SQL Server, `ALGORITHM=INPLACE` in MySQL). State table
  size if known, otherwise "unknown".
- Data backfill strategy (batched, idempotent) and integrity constraints.
- **Rollback plan:** a down migration, or written steps when the tool does not support down
  migrations, plus whether rollback loses data.
- Application compatibility: old code with new schema and new code with old schema during
  deployment.

## 4. Approval gates

Stop and get explicit owner approval before:
- Any destructive operation, even in development, if the database holds shared data.
- Running a migration on any non-local database.
- Changing personal-data columns, retention, or encryption.

## 5. Implement and verify

- Write the migration in the project's tool and naming convention, with its rollback.
- Update models, repositories, and queries; parameterized queries only.
- If a local or disposable database is available (Docker, testcontainers, SQLite), apply the
  migration, run the rollback, apply again, and run the affected tests. Report commands and
  results. If not available, state that the migration was **not executed** and why.
- Have `code-reviewer` review the diff, and `security-engineer` if sensitive data is involved.

## Output additions to the delivery report

```
## Migration summary: engine, tool, files
## Classification: additive / destructive (approval reference)
## Rollback plan and data-loss impact
## Execution evidence: applied / rolled back / re-applied locally, or not executed (reason)
## Deployment notes: order relative to app deploy, locking, backfill duration
```

## Example invocations

```
/database-migration Add an index on patients(last_name, date_of_birth)
/database-migration Split users.full_name into first_name and last_name
/database-migration Add a soft-delete column to orders
```
