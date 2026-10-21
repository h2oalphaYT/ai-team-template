---
name: feature-development
description: Build a new feature or extend existing behaviour end to end. Use when asked to add, build or implement a capability (endpoint, screen, integration, workflow, auth, CLI command). Requires acceptance criteria, an approved implementation plan for substantial work, small changes, tests, documentation and independent review.
argument-hint: "<feature description>"
---

# Feature Development

Feature: $ARGUMENTS

This skill specialises `/execute-task` for new capabilities. Follow its stages and report
format; this file only adds what is specific to features.

**Use when:** something new must exist that does not today. **Do not use** for defects
(`/bug-fix`), pure refactors with no behaviour change (`/execute-task`), or review-only
requests (`/code-review`).

## 1. Requirements first (no code yet)

- Inspect the related code, existing patterns, and `.claude/PROJECT.md`.
- Invoke `business-analyst` to produce user stories and testable acceptance criteria (AC-1…),
  with each marked Confirmed, Assumed, or Open.
- If an Open item changes scope, security, data, or a public contract, ask the owner before
  continuing. Do not fill the gap with invented requirements.

## 2. Design and plan

- Invoke `tech-lead-architect` for design, contracts, and a task breakdown into small,
  reviewable steps.
- Add `ui-ux-designer` for user-visible changes, `database-engineer` for schema changes (and
  follow `/database-migration`), `security-engineer` for auth, permissions, or sensitive data,
  `ai-ml-engineer` for ML or LLM features.
- Write the plan with `.claude/skills/execute-task/templates/task-plan.md`.
- **Approval gate:** stop and wait for the owner's go-ahead when the feature is substantial,
  changes a public contract or schema, adds a dependency or external service, or touches
  authentication or authorization.

## 3. Implement in small steps

- Branch from the default branch, for example `feat/<short-name>`.
- Implement one task from the breakdown at a time, each with its tests, in the project's
  existing stack and style. Commit after each coherent step.
- Delegate to `frontend-engineer`, `backend-engineer`, `database-engineer`,
  `ai-ml-engineer`, or `devops-cloud-engineer` as appropriate. For Go code, apply
  `/go-development` conventions.

## 4. Verify

- Every acceptance criterion maps to at least one automated test, or to documented manual
  verification when automation is impractical (say why).
- Include negative and boundary cases, and authorization failures where relevant.
- Run the project's format, lint, type-check, test, and build commands. Report real results.
- `qa-test-engineer` independently checks the change against the acceptance criteria.

## 5. Review and document

- `code-reviewer` reviews the full diff. Fix blocking findings and re-run checks.
- `security-engineer` reviews when the feature touches auth, input handling, secrets, files,
  or AI input/output.
- Update docs, API references, env var lists (`.env.example`), and the changelog via
  `technical-writer` where relevant.

## 6. Deliver

Open a pull request (never merge) and give the `/execute-task` delivery report, including the
AC → test traceability table.

## Example invocations

```
/feature-development Add JWT authentication to the Go API
/feature-development Add CSV export to the orders page
/feature-development Add a /health endpoint with database readiness
```
