# Applying the AI team to a repository

The team is a set of files: `CLAUDE.md`, `.claude/agents/`, `.claude/skills/`,
`.claude/settings.json`, and a project-specific `.claude/PROJECT.md`. Claude Code reads them
from the repository it is working in. **Connecting a repository to Claude Code does not install
the team.** The files must be committed in the target repository, or made available through a
supported shared method (user-level `~/.claude/agents/` and `~/.claude/skills/`, or a Claude
Code plugin).

## What is template-owned and what is project-owned

| File | Owner | Updated from template? |
|---|---|---|
| `CLAUDE.md` | template | Yes. Do not put project facts here |
| `.claude/agents/<13 template agents>.md` | template | Yes |
| `.claude/skills/<10 template skills>/` | template | Yes |
| `.claude/settings.json` | shared | Only if absent; otherwise merged by hand |
| `.claude/PROJECT.md` | **project** | **Never** |
| Agents or skills you add with new names | **project** | **Never** |

This split is what lets you update the shared template without losing project instructions.

## 1. New GitHub repository from the template

1. On GitHub, open this template repository and enable **Settings → General → Template
   repository** (once, by the template owner).
2. Click **Use this template → Create a new repository**.
3. Clone it, add your application code, then fill in `.claude/PROJECT.md` from
   [`templates/PROJECT.template.md`](../templates/PROJECT.template.md), or run
   `/project-audit` and accept its proposal.
4. Replace the template's `README.md`, `docs/` and `.github/workflows/ci.yml` with your
   project's own (they describe the template, not your app). Keep `CLAUDE.md` and `.claude/`.

## 2. Existing repository

Using the installer (macOS, Linux, WSL, or Git Bash on Windows):

```bash
git clone https://github.com/h2oalphaYT/ai-team-template.git
cd your-repo && git checkout -b chore/add-ai-team
../ai-team-template/scripts/install-team.sh --dry-run .   # preview
../ai-team-template/scripts/install-team.sh .             # install
git status                                                # review before committing
```

The installer never overwrites existing files on first install:

- `CLAUDE.md` exists → it writes `CLAUDE.ai-team.md` next to it. Move your existing project
  rules into `.claude/PROJECT.md`, then replace `CLAUDE.md` with `CLAUDE.ai-team.md`.
- `.claude/settings.json` exists → it writes `.claude/settings.ai-team.json`; merge the
  `permissions.deny` entries into your file by hand.
- An agent or skill with the same name exists → it is skipped and reported.
- `.claude/PROJECT.md` is created from the template only if missing.

Manual copy (PowerShell, from the template clone):

```powershell
$target = "E:\path\to\your-repo"
New-Item -ItemType Directory -Force "$target\.claude" | Out-Null
Copy-Item -Recurse .\.claude\agents "$target\.claude\"
Copy-Item -Recurse .\.claude\skills "$target\.claude\"
if (-not (Test-Path "$target\CLAUDE.md")) { Copy-Item .\CLAUDE.md $target }
if (-not (Test-Path "$target\.claude\settings.json")) { Copy-Item .\.claude\settings.json "$target\.claude\" }
if (-not (Test-Path "$target\.claude\PROJECT.md")) { Copy-Item .\templates\PROJECT.template.md "$target\.claude\PROJECT.md" }
```

Commit on a branch and open a PR so the change is reviewed like any other.

## 3. Project-specific stack and test instructions

Put them in `.claude/PROJECT.md`: stack with evidence, exact format/lint/test/build commands,
environments and who approves deploys, environment variable names, conventions, and which
agents apply. Examples of what to write for common stacks:

| Stack | Typical commands to record |
|---|---|
| Go | `gofmt -l .`, `go vet ./...`, `go test ./...`, `golangci-lint run` |
| Next.js / React | `pnpm lint`, `pnpm tsc --noEmit`, `pnpm test`, `pnpm build` |
| Express / Node.js | `npm run lint`, `npm test`, `npm run build` |
| Java / Spring Boot | `./mvnw -B verify` or `./gradlew check build` |
| Python | `ruff check .`, `ruff format --check .`, `mypy .`, `pytest` |
| SQL Server / PostgreSQL / MySQL | migration tool and command, local DB (Docker) for tests |
| MongoDB | schema/validation approach, migration tool (e.g. migrate-mongo), local instance |
| AI/ML | training and evaluation commands, dataset locations (no data in git), hardware |

Use the project's real commands; the table is only a hint. `/project-audit` will detect and
propose them.

## 4. Connecting the repository to Claude Code on the web

1. Go to [claude.ai/code](https://claude.ai/code) and connect GitHub (install the Claude GitHub
   App on the repository or organisation and grant it access to this repository).
2. Create or pick an environment. Choose a network policy that allows what your tests need,
   and add only non-production secrets the session truly needs.
3. Start a session on the repository. The session clones the repository, so the team is
   available only on branches where `CLAUDE.md` and `.claude/` are committed. Until the
   installation PR is merged, start sessions on that branch.

Details change between releases; see the
[Claude Code on the web docs](https://code.claude.com/docs/en/claude-code-on-the-web).

## 5. Checking that agents and skills are loaded

In a session at the repository root:

- `/agents` lists the thirteen agents.
- Typing `/` shows the skills (`/execute-task`, `/project-audit`, …).
- Ask: "Which project agents and skills are loaded from .claude/?"
- Locally, run `python3 scripts/validate_template.py --root /path/to/your-repo` from the
  template clone to check the files statically.

See [SKILLS.md](SKILLS.md#checking-that-skills-are-available-in-a-session) for
troubleshooting.

## 6. Running a test task and reviewing the PR

1. Start with a read-only task: `/project-audit`. Check that the stack and commands it reports
   match reality, then let it write `.claude/PROJECT.md`.
2. Run a small, safe change, for example
   `/execute-task Add a unit test for <some small function>` or
   `/bug-fix <a known small defect>`.
3. Check the delivery report: commands actually run with results, agents actually used, files
   changed, and decisions awaiting approval.
4. Review the PR on GitHub: diff limited to the task, tests added, no secrets, CI green.
5. Optionally run `/code-review` on the branch in a fresh session for a second opinion.
6. Merge yourself if satisfied. The team never merges.

## 7. Updating from the shared template

```bash
cd ai-team-template && git pull
cd ../your-repo && git checkout -b chore/update-ai-team
../ai-team-template/scripts/install-team.sh --update --dry-run .
../ai-team-template/scripts/install-team.sh --update .
git diff     # review every change
```

`--update` overwrites only template-owned files: `CLAUDE.md` (when it is the template's
version), the thirteen template agents, and the ten template skills. It never touches
`.claude/PROJECT.md`, agents or skills you added under other names, or an existing
`.claude/settings.json`. If you edited a template agent in place, `--update` will replace it.
Move such customisations to `.claude/PROJECT.md` or a renamed agent first.
