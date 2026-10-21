# Task specification template

Copy this into an issue, a PR description, or your message to Claude. Leave a section empty
rather than guessing; the team will list it as an open question.

```markdown
## Title
<short, specific>

## Type
feature / bug / refactor / docs / infra / ai-ml / security / migration

## Outcome
<what should be true when this is done, in one or two sentences>

## Background
<why this matters; links to issues, designs, logs>

## Users and permissions
<who uses it; which roles may do what>

## Acceptance criteria
- AC-1 Given <context>, when <action>, then <result>
- AC-2 …

## Out of scope
<what must not change>

## Constraints
<stack, performance budgets, compatibility, deadlines, dependencies not allowed>

## Data and security notes
<personal data, secrets involved (names only), external services>

## Test expectations
<specific cases that must be covered; environments available>

## Approvals already given
<e.g. "OK to add a migration that adds columns; no destructive changes">

## Suggested skill
/feature-development | /bug-fix | /execute-task | /database-migration | /ai-ml-engineering
```

## Example

```markdown
## Title
Add JWT authentication to the Go API

## Type
feature

## Outcome
All /api/v1 routes except /health and /auth/login require a valid JWT.

## Acceptance criteria
- AC-1 Given valid credentials, when POST /auth/login, then 200 with a signed access token
  that expires in 15 minutes.
- AC-2 Given no token, when GET /api/v1/patients, then 401 in the existing error format.
- AC-3 Given an expired or tampered token, when calling a protected route, then 401.
- AC-4 Given a valid token, when calling a protected route, then the handler sees the user id
  in the request context.

## Out of scope
Refresh tokens, social login, UI changes.

## Constraints
Use the existing router and middleware pattern. Signing key from env var JWT_SIGNING_KEY.

## Approvals already given
New dependency on a maintained JWT library is OK if justified.
```
