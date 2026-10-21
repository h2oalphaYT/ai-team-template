# Project profile: ai-team-template

<!-- Project-specific facts for THIS repository (the template itself). In a target repository
this file is created from templates/PROJECT.template.md and filled in by /project-audit. -->

## Overview
- Name: ai-team-template
- Purpose: a reusable, stack-agnostic Claude Code configuration (agents, skills, rules, docs)
  that is copied into other repositories.
- Owner / approver for risky changes: repository owner.

## Stack (with evidence)
| Area | Technology | Evidence |
|---|---|---|
| Content | Markdown with YAML frontmatter | `.claude/agents/*.md`, `.claude/skills/*/SKILL.md` |
| Validation | Python 3 standard library | `scripts/validate_template.py` |
| Installer | POSIX shell (bash) | `scripts/install-team.sh` |
| CI | GitHub Actions | `.github/workflows/ci.yml` |
| Application code, database, frontend, AI/ML | none | no manifests in the repository |

## Commands
| Purpose | Command |
|---|---|
| Validate agents, skills, links, secrets | `python3 scripts/validate_template.py` |
| Validator self-test | `python3 scripts/validate_template.py --self-test` |
| Lint installer | `bash -n scripts/install-team.sh` (and `shellcheck` if installed) |
| Dry-run install into another repo | `scripts/install-team.sh --dry-run /path/to/repo` |

## Conventions
- Agent file name equals its `name` field; skill directory name equals its `name` field.
- Global safety rules live in `CLAUDE.md`; skills reference them rather than repeating them.
- Keep the template generic: no stack is assumed in agents or skills except stack overlays
  such as `go-development`.

## Agents that apply to this project
- Use: `technical-writer`, `code-reviewer`, `security-engineer` (CI permissions),
  `devops-cloud-engineer` (CI).
- Not needed: frontend, backend, database, AI/ML, UI/UX (no application code here).

## Known risks and unknowns
- Skills and agents are validated statically; their runtime behaviour depends on the Claude
  Code version in use.
