# Skills guide

Skills are reusable, written procedures that Claude follows for a kind of task. Each lives in
its own directory, [`.claude/skills/<name>/SKILL.md`](../.claude/skills/), with YAML
frontmatter (`name`, `description`, `argument-hint`) and a body of instructions. Skills are
instructions, not an orchestration engine: Claude reads and follows them, and the mandatory
safety rules stay in [CLAUDE.md](../CLAUDE.md) so they apply even when no skill is used.

## Available skills

| Skill | Use it for | Modifies files? | Example |
|---|---|---|---|
| [`execute-task`](../.claude/skills/execute-task/SKILL.md) | Default end-to-end lifecycle for any change; coordinates the others | Yes | `/execute-task Rename the config flag --verbose to --debug` |
| [`project-audit`](../.claude/skills/project-audit/SKILL.md) | Read-only assessment of stack, architecture, commands, infra, risks, unknowns | Only `.claude/PROJECT.md`, after showing it | `/project-audit` |
| [`feature-development`](../.claude/skills/feature-development/SKILL.md) | New capability with AC, approved plan, small steps, tests, docs, review | Yes | `/feature-development Add JWT authentication to the Go API` |
| [`bug-fix`](../.claude/skills/bug-fix/SKILL.md) | Reproduce, root cause, failing regression test, minimal fix, re-run checks | Yes | `/bug-fix Fix the failing patient search test` |
| [`code-review`](../.claude/skills/code-review/SKILL.md) | Review a diff, branch or PR with prioritised `path:line` findings | **No** | `/code-review Review the current branch` |
| [`ai-ml-engineering`](../.claude/skills/ai-ml-engineering/SKILL.md) | ML, DL, CV, NLP, LLM, RAG, data pipelines, training, evaluation, inference | Yes | `/ai-ml-engineering Evaluate the image classification pipeline` |
| [`go-development`](../.claude/skills/go-development/SKILL.md) | Go conventions overlay: `go.mod`, errors, context, gofmt, vet, tests | Yes | `/go-development Add pagination to GET /patients` |
| [`database-migration`](../.claude/skills/database-migration/SKILL.md) | Schema or data change with rollback plan and approval for destructive steps | Yes | `/database-migration Add an index on patients(last_name)` |
| [`security-audit`](../.claude/skills/security-audit/SKILL.md) | Security review with Verified vs Potential findings and severity | **No** | `/security-audit Review the authentication changes` |
| [`release-readiness`](../.claude/skills/release-readiness/SKILL.md) | Go/no-go checklist: AC, build, tests, security, migrations, rollback, approvals | **No** (never merges or deploys) | `/release-readiness Check whether this release is ready for approval` |

How they fit together: `execute-task` is the lifecycle. `feature-development` and `bug-fix`
specialise it. `go-development`, `database-migration` and `ai-ml-engineering` are applied
inside it when the change touches those areas. `project-audit`, `code-review`,
`security-audit` and `release-readiness` are read-only assessments.

## Invoking a skill

Type a slash command followed by your request:

```
/project-audit
/feature-development Add JWT authentication to the Go API
/bug-fix Fix the failing patient search test
/ai-ml-engineering Evaluate the image classification pipeline
/code-review Review the current branch
/security-audit Review the authentication changes
/release-readiness Check whether this release is ready for approval
```

The text after the command is passed to the skill as `$ARGUMENTS`.

## Automatic selection

You do not have to type the command. Claude Code shows Claude each skill's `name` and
`description`, and Claude may load a skill on its own when your request matches the
description. For example, "the patient search test is failing, can you fix it?" matches
`bug-fix`. That is why each description names concrete trigger phrases. `CLAUDE.md` section 3
also tells Claude which skill to pick. If Claude does not pick the skill you want, invoke it
explicitly.

## Skills vs agents

| | Skill | Agent (subagent) |
|---|---|---|
| What it is | A procedure: steps, gates, report format | A specialist role with its own prompt and tool list |
| Where | `.claude/skills/<name>/SKILL.md` | `.claude/agents/<name>.md` |
| How it runs | In the main conversation; Claude follows the steps | In a separate context; returns a result to the main conversation |
| Tool limits | Uses the session's tools and permissions | Restricted by its `tools:` line |
| Invoked by | `/name` or automatic match | Claude delegates to it (or you ask: "use the security-engineer agent") |
| Example | `bug-fix` says reproduce, test, fix, re-run, report | `qa-test-engineer` designs and runs the tests |

Skills tell Claude **how to run the work** and when to call which agent. Agents **do focused
parts** of that work with limited tools.

## Copying skills into another repository

Skills are project-level configuration: they must be present in the target repository (or
installed through a supported shared method such as user-level `~/.claude/skills/` or a
Claude Code plugin). Connecting a repository to Claude Code does not install them.

```bash
# from a clone of this template, into your repository
scripts/install-team.sh /path/to/your-repo          # agents, skills, CLAUDE.md, settings
# or copy only the skills
cp -R .claude/skills /path/to/your-repo/.claude/
```

PowerShell:

```powershell
Copy-Item -Recurse -Force .\.claude\skills E:\path\to\your-repo\.claude\
```

Skills reference agents by name and `CLAUDE.md` for the safety rules, so copying skills
without the agents and `CLAUDE.md` works but loses delegation and the global rules. Copy all
three. See [PROJECT_ONBOARDING.md](PROJECT_ONBOARDING.md) for the full procedure.

## Checking that skills are available in a session

1. Start Claude Code in the repository root (locally `claude`, or a Claude Code on the web
   session for the repository's branch that contains `.claude/skills/`).
2. Type `/` and look for the skill names (for example `/execute-task`) in the command list.
3. Or ask: "List the project skills and agents you have loaded from .claude/." Claude should
   name all ten skills and thirteen agents.
4. Run `/agents` to see the agents.
5. Smoke test: `/project-audit`. It should produce the six-section assessment without
   modifying files.

If a skill is missing: confirm the directory name equals the `name` field, the file is
named exactly `SKILL.md`, the frontmatter starts on line 1 with `---`, and you started Claude
Code from the repository root. Run `python3 scripts/validate_template.py` to check all of
this. Skills added mid-session may need a new session.

**Name clash:** some Claude Code versions ship built-in commands such as `/code-review` or
`/security-review`. If a built-in runs instead of the project skill, rename the project
skill's directory and `name` (for example `team-code-review`) in your repository.

## Validation status

The template's validator checks every skill's path, frontmatter, name, description, and
internal references statically, in CI and locally. Static validation does not prove how a
specific Claude Code version behaves; do the smoke test above after installing.
