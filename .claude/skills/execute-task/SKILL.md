---
name: execute-task
description: Mandatory end-to-end workflow for any development task in this repository (feature, change, fix, refactor, docs, infra). Use when asked to implement, change, build or deliver something and no narrower skill fits, or to coordinate one. Runs understand, analyze, plan, approve, implement, verify, document and report, with evidence-based testing and a standard delivery report.
argument-hint: "<what you want done>"
---

# Execute Task

Task: $ARGUMENTS

This is the default lifecycle for work in this repository. The global rules in `CLAUDE.md`
(approval gates, secrets, untrusted input, truthful reporting) always apply and are not
repeated here. Narrower skills plug into this lifecycle:

| Situation | Use instead of, or inside, this skill |
|---|---|
| First contact with a repository, or `.claude/PROJECT.md` is missing or stale | `/project-audit` first |
| New user-facing capability | `/feature-development` |
| Something is broken | `/bug-fix` |
| Schema or data change | `/database-migration` (inside stage 4) |
| Go code | `/go-development` conventions (inside stage 4) |
| ML, LLM, RAG, data pipeline | `/ai-ml-engineering` |
| Review only, no edits | `/code-review` or `/security-audit` |
| "Can we ship?" | `/release-readiness` |

**Do not use this skill** for pure questions, explanations, or read-only investigations. Answer
those directly.

## Size the task first

- **Trivial** (typo, one-line config, comment, obviously local fix): skip specialist agents.
  Inspect, change, run the relevant check, and give a short report (sections 1, 2, 3, 5, 6).
- **Standard** (a few files, one component, no contract or schema change): use the agents that
  add real value, typically the implementing engineer plus `qa-test-engineer` and
  `code-reviewer`.
- **Substantial or risky** (new feature, cross-component, public contract, schema, auth,
  infra, ML model, anything on the approval list in `CLAUDE.md`): full workflow, and **stop for
  owner approval after the plan**.

State the size you chose and why, in one line.

## Stage 1: Understand

1. Restate the requested outcome in one or two sentences.
2. Inspect before modifying: read `CLAUDE.md`, `.claude/PROJECT.md`, and the files involved.
   Run `git status` and note uncommitted changes. Never overwrite or discard them.
3. Identify affected components and the current behaviour (with `path:line` evidence).
4. List missing information. Ask concise questions if an answer changes a risky or
   irreversible decision; otherwise record an assumption and proceed conservatively.

## Stage 2: Analyze

Delegate only where it helps, and only claim agents you actually invoked:

- `business-analyst`: requirements and acceptance criteria for features or behaviour changes.
- `tech-lead-architect`: design, contracts, and task breakdown for non-trivial changes.
- `ui-ux-designer`: any user-visible or developer-experience change.
- `database-engineer`: schema, migration, or query changes.
- `ai-ml-engineer`: models, prompts, embeddings, datasets, pipelines.
- `security-engineer`: auth, input handling, secrets, dependencies, CI permissions, AI input.
- `ceo-strategy-advisor`: competing priorities or business trade-offs.

## Stage 3: Plan

Write the plan using `.claude/skills/execute-task/templates/task-plan.md`. It must contain
acceptance criteria, files or components to change, order and dependencies, test strategy,
security and data risks, and decisions requiring approval.

**Approval gate:** for substantial or risky tasks, present the plan and wait for the owner's
go-ahead before stage 4. For trivial and standard tasks, proceed and show the plan in the report.

## Stage 4: Implement

- Work on a feature branch, never directly on the default branch.
- Make small, focused changes that follow existing conventions. Preserve unrelated code.
- No new frameworks or major dependencies without justification (and approval if significant).
- Delegate implementation to `frontend-engineer`, `backend-engineer`, `database-engineer`,
  `ai-ml-engineer`, or `devops-cloud-engineer` when the change is substantial in their area.

## Stage 5: Verify

- Run the project's formatter, linter, type-checker, tests, and build, as listed in
  `.claude/PROJECT.md` or detected from manifests and CI. Narrow first, then wider.
- Test each acceptance criterion and the important failure paths.
- Use mocks or local services when external services are unavailable. Never test against
  production.
- For standard and larger tasks, have `qa-test-engineer` and `code-reviewer` inspect the change
  independently. Add `security-engineer` when risk warrants.
- If a check cannot run, record why. Never substitute an assumption for a result.

## Stage 6: Fix and re-test

Investigate each failure, fix defects that are in scope, and re-run the affected checks. Do not
hide failures, skip tests silently, or weaken assertions. Out-of-scope failures (for example
already failing on the base branch) are reported, not "fixed" by disabling them.

## Stage 7: Document

Update the README, API, architecture, migration, testing, or operations docs that the change
affects (delegate to `technical-writer` for substantial updates). Only document implemented
behaviour, or label it **Planned**.

## Stage 8: Deliver

Commit with a clear message, push the branch, and open a pull request if the environment
supports it. **Never merge, force-push, or deploy.** Produce the report in
`.claude/skills/execute-task/templates/delivery-report.md`. The task is complete only when each
acceptance criterion has verification evidence, or its gap is stated plainly.
