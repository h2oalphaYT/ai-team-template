---
name: project-audit
description: Read-only assessment of a repository. Use when first applying the AI team to a repository, when .claude/PROJECT.md is missing or stale, or when asked to audit, assess or explain a project's stack, architecture, dependencies, test commands, infrastructure, security concerns and unknowns. Never modifies application code.
argument-hint: "[optional focus area, e.g. backend or ci]"
---

# Project Audit

Focus (optional): $ARGUMENTS

Produce an evidence-based assessment of the repository as it actually is. Every claim cites a
file (and line where useful). Anything you could not confirm is listed as an unknown.

**Use when:** onboarding a repository, before a large task in an unfamiliar area, or when the
owner asks "what is this project?". **Do not use** to fix or change anything; hand findings to
`/execute-task`, `/bug-fix` or `/security-audit` afterwards.

## Rules for this skill

- **Do not modify application code, tests, configuration, CI, or dependencies.** The only file
  you may write is `.claude/PROJECT.md`, and only after showing the owner the proposed content
  (or when they asked you to create it).
- Do not install dependencies or run commands that change state. Allowed: listing files,
  reading files, `git log/status/diff`, version checks, and dependency listing commands that
  only read.
- Never print secret values. When you find `.env` files, credential files, or keys, report the
  path and type only. Do not open `.env` files at all; read `.env.example` instead.
- Running tests is optional and only when cheap and safe (no external services, no
  production credentials). Report exactly what ran.

## Steps

1. **Map the repository:** top-level tree (depth 2–3), README, `CLAUDE.md`, existing
   `.claude/`, docs, ADRs, `git log --oneline -20`, `git status`.
2. **Detect the stack** from manifests and lockfiles, for example: `go.mod`/`go.sum`,
   `package.json` + `pnpm-lock.yaml`/`yarn.lock`/`package-lock.json`, `pom.xml`,
   `build.gradle(.kts)`, `pyproject.toml`/`requirements*.txt`/`Pipfile`/`poetry.lock`/
   `uv.lock`, `*.csproj`/`*.sln`, `Gemfile`, `Cargo.toml`, `composer.json`. Record language
   and framework versions.
3. **Architecture:** entry points, layers or modules, API style (REST/GraphQL/gRPC), frontend
   framework, background jobs, inter-service calls.
4. **Commands:** build, run, format, lint, type-check, unit test, integration test, e2e, from
   scripts, `Makefile`, task runners, and CI workflows.
5. **Data and infrastructure:** database engines (driver packages, Compose services, ORM
   dialects), migration tool and folder, caches, queues, object storage, Dockerfiles, IaC
   (Terraform, Kubernetes, Helm), cloud provider hints, deployment workflows.
6. **AI/ML (if present):** frameworks, notebooks, datasets, model artefacts, LLM SDKs, vector
   stores.
7. **Security and configuration:** committed secrets (pattern search, report redacted), auth
   mechanism, CI `permissions`, `pull_request_target` use, unpinned actions, missing
   `.env.example`, outdated or risky dependencies (run an available read-only audit tool if
   present; otherwise say none was run).
8. **Tests:** frameworks, where tests live, rough coverage of critical paths, and whether CI
   runs them.

For a large repository, you may delegate parts to `tech-lead-architect` (architecture),
`security-engineer` (step 7), `database-engineer` (step 5), or `devops-cloud-engineer`
(CI/infra). Say which you used.

## Output

```
# Project assessment: <repo>
1. Detected stack and evidence
2. Application architecture
3. Tests and commands (verified by running / read from config only)
4. Database and infrastructure dependencies
5. Security concerns and missing configuration
6. Uncertainties that need clarification
Recommended specialists for this project: <agents that apply, and agents that do not>
```

Then propose a filled-in `.claude/PROJECT.md` (based on `templates/PROJECT.template.md` in
the template repository, or the existing file) containing only verified facts and clearly
marked unknowns.

## Example invocations

```
/project-audit
/project-audit focus on the backend and database
/project-audit ci and deployment
```
