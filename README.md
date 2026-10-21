# AI Engineering Team Template for Claude Code

A reusable, stack-agnostic "AI software engineering team" for
[Claude Code](https://code.claude.com/docs). Copy it into any suitable repository (Go,
Next.js, Express, Java/Spring Boot, Python, SQL Server, PostgreSQL, MongoDB, AI/ML, and
others) and Claude works through a disciplined delivery lifecycle with specialist agents,
reusable skills, explicit approval gates, and evidence-based reporting.

```
UNDERSTAND → ANALYZE → PLAN → APPROVE → IMPLEMENT → TEST → REVIEW → DOCUMENT → REPORT
```

The goal is reliable engineering, not fast code generation. The team inspects the actual
repository before changing it, adapts to the stack it finds, stops for your approval on risky
or irreversible steps, and only reports checks that really ran.

## What is included

| Path | Purpose |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Global rules: workflow, skill and agent routing, approval list, security, truthful reporting |
| [`.claude/agents/`](.claude/agents/) | 13 specialist subagents with minimal tool lists ([catalog](docs/AGENT_CATALOG.md)) |
| [`.claude/skills/`](.claude/skills/) | 10 reusable skills ([guide](docs/SKILLS.md)) |
| [`.claude/settings.json`](.claude/settings.json) | Permission deny list: secrets files, force-push, hard reset, infra apply/destroy, PR merge |
| [`.claude/PROJECT.md`](.claude/PROJECT.md) | Project-specific facts, imported by `CLAUDE.md` (this repo's own profile) |
| [`templates/PROJECT.template.md`](templates/PROJECT.template.md) | Blank project profile for target repositories |
| [`scripts/install-team.sh`](scripts/install-team.sh) | Installs or updates the team in another repository without overwriting project files |
| [`scripts/validate_template.py`](scripts/validate_template.py) | Static validation (frontmatter, names, tools policy, links, secrets) |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | Runs the validator and an installer smoke test with a read-only token |
| [`docs/`](docs/) | Workflow, onboarding, security, task template, definition of done |

### Agents

`ceo-strategy-advisor`, `business-analyst`, `tech-lead-architect`, `ui-ux-designer`,
`frontend-engineer`, `backend-engineer`, `database-engineer`, `qa-test-engineer`,
`ai-ml-engineer`, `devops-cloud-engineer`, `security-engineer`, `code-reviewer`,
`technical-writer`. Analysts and reviewers cannot edit files; documentation roles cannot run
shell commands. See the [Agent catalog](docs/AGENT_CATALOG.md).

### Skills

| Skill | Invoke | What it does |
|---|---|---|
| `execute-task` | `/execute-task <task>` | Default full lifecycle for any change, with a standard delivery report |
| `project-audit` | `/project-audit` | Read-only assessment of stack, architecture, commands, infra, risks, unknowns |
| `feature-development` | `/feature-development <feature>` | AC, approved plan, small steps, tests, docs, review |
| `bug-fix` | `/bug-fix <bug>` | Reproduce, root cause, regression test, minimal fix, re-run checks |
| `code-review` | `/code-review [target]` | Review-only, prioritised findings with `path:line` |
| `ai-ml-engineering` | `/ai-ml-engineering <task>` | ML/DL/CV/NLP/LLM/RAG with data checks, reproducibility, real metrics only |
| `go-development` | `/go-development <task>` | Idiomatic Go overlay: `go.mod`, errors, context, gofmt, vet, tests |
| `database-migration` | `/database-migration <change>` | Engine and tool detection, migration plus rollback, approval for destructive steps |
| `security-audit` | `/security-audit [scope]` | Verified vs potential findings with severity and remediation |
| `release-readiness` | `/release-readiness [release]` | Go/no-go checklist; never merges or deploys |

Claude may also pick a skill automatically when your request matches its description. Skills
are written procedures Claude follows, not an autonomous engine; the mandatory safety rules
live in `CLAUDE.md` so they apply with or without a skill. Details: [docs/SKILLS.md](docs/SKILLS.md).

## Quick start

**New repository:** click **Use this template** on GitHub, then run `/project-audit` in
Claude Code to fill in `.claude/PROJECT.md`.

**Existing repository** (macOS, Linux, WSL, Git Bash):

```bash
git clone https://github.com/h2oalphaYT/ai-team-template.git
cd /path/to/your-repo && git checkout -b chore/add-ai-team
/path/to/ai-team-template/scripts/install-team.sh --dry-run .
/path/to/ai-team-template/scripts/install-team.sh .
```

Then commit, open a PR, start Claude Code on that branch, and run:

```
/project-audit
/feature-development Add JWT authentication to the Go API
/bug-fix Fix the failing patient search test
/code-review Review the current branch
/release-readiness Check whether this release is ready for approval
```

Full instructions, including PowerShell, Claude Code on the web, checking that agents and
skills are loaded, a first test task, and updating from the template:
[docs/PROJECT_ONBOARDING.md](docs/PROJECT_ONBOARDING.md).

> Connecting a repository to Claude Code does **not** install this team. The files must be
> committed in the target repository (or provided through user-level `~/.claude/` or a
> plugin).

## How project-specific instructions survive template updates

`CLAUDE.md`, the 13 agents, and the 10 skills are template-owned and can be refreshed with
`scripts/install-team.sh --update`. Everything about a particular project goes in
`.claude/PROJECT.md`, which the installer never overwrites. Add project-specific agents or
skills under new names so updates leave them alone.

## Documentation

- [Workflow](docs/WORKFLOW.md): stages, task sizes, where you approve
- [Skills guide](docs/SKILLS.md): invoking, automatic selection, skills vs agents, availability checks
- [Agent catalog](docs/AGENT_CATALOG.md): roles, tools, boundaries
- [Project onboarding](docs/PROJECT_ONBOARDING.md): applying and updating the team
- [Security](docs/SECURITY.md): permissions, secrets, data safety, approval boundaries
- [Task template](docs/TASK_TEMPLATE.md): how to specify work
- [Definition of Done](docs/DEFINITION_OF_DONE.md): completion and verification requirements

## Validating this template

```bash
python3 scripts/validate_template.py --self-test
python3 scripts/validate_template.py
python3 scripts/validate_template.py --root /path/to/your-repo   # check an installed repo
```

CI runs the same checks plus an installer smoke test on every push and pull request.

## Limitations

- Validation is static. It proves files are well formed and consistent, not how a particular
  Claude Code version behaves at runtime; run the smoke test in
  [docs/SKILLS.md](docs/SKILLS.md#checking-that-skills-are-available-in-a-session) after
  installing.
- Agent prompts and `CLAUDE.md` are instructions, not a sandbox. Use branch protection,
  least-privilege credentials, and Claude Code permission settings as the real controls.
- Some Claude Code versions ship built-in commands with the same names (for example
  `/code-review`). Rename the project skill if a built-in takes precedence.
