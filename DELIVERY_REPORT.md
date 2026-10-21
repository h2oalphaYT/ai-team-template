# Delivery report: AI engineering team template

## 1. Requested outcome
Turn `h2oalphaYT/ai-team-template` into a reusable, stack-agnostic Claude Code AI engineering
team: 13 specialist agents, a library of 10 skills, CLAUDE.md rules, docs, CI and validation,
delivered as a pull request for review. Nothing merged or deployed.

## 2. Changes implemented
- 13 agents in `.claude/agents/`, each with a unique name, a description written to help Claude
  delegate, a minimal `tools` list, responsibilities, an output format and a `## Boundaries` section.
  Reviewer and analyst agents can't edit files, and documentation agents can't run shell commands.
- 10 skills in `.claude/skills/`. Each has frontmatter (`name`, `description`, `argument-hint`),
  says when to use it and when not to, delegates to agents, has approval gates and gives
  `/skill` examples. `execute-task` also includes task-plan and delivery-report templates.
- `CLAUDE.md` holds the global rules: inspect before changing, the 9-stage workflow, how to
  find and route skills and agents, the approval list, security and untrusted input, truthful
  reporting and git rules. The safety rules live here and are not repeated in each skill.
- `.claude/PROJECT.md` is the project-owned profile, imported by CLAUDE.md. `templates/PROJECT.template.md`
  is a blank copy for other repositories.
- `.claude/settings.json` adds permission deny rules. They block reading `.env`, keys and
  tfstate files, and block force-push, hard reset, `terraform apply`/`destroy`,
  `kubectl apply`/`delete`, `helm upgrade`/`uninstall` and `gh pr merge`.
- `scripts/install-team.sh` installs into other repos without overwriting anything. Its
  `--update` mode refreshes only template-owned files and never touches PROJECT.md. It also
  has a `--dry-run` mode.
- `scripts/validate_template.py` is a static validator that uses only the Python standard
  library, and it has its own `--self-test`.
- `.github/workflows/ci.yml` runs with `contents: read` and needs no secrets. The checkout
  action is pinned by SHA, and the workflow runs the validator, shell lint and an installer
  smoke test.
- Docs: README, AGENT_CATALOG, WORKFLOW, SKILLS (new skills guide), PROJECT_ONBOARDING,
  SECURITY, TASK_TEMPLATE, DEFINITION_OF_DONE, a PR template and `.gitignore`.

## 3. Files created (42, all new; the repository was empty, so nothing was modified or deleted)
`.claude/agents/` ×13, `.claude/skills/*/SKILL.md` ×10, `.claude/skills/execute-task/templates/` ×2,
`.claude/PROJECT.md`, `.claude/settings.json`, `CLAUDE.md`, `README.md`, `docs/` ×7,
`scripts/install-team.sh`, `scripts/validate_template.py`, `templates/PROJECT.template.md`,
`.github/workflows/ci.yml`, `.github/pull_request_template.md`, `.gitignore`.

## 4. Agents actually used
None. I wrote everything directly and didn't delegate to subagents.

## 5–6. Commands executed and results
| Command | Result |
|---|---|
| `python3 scripts/validate_template.py --self-test` | 9/9 passed (each broken fixture was caught, and the valid fixture was clean) |
| `python3 scripts/validate_template.py` | 0 errors, 0 warnings: 13 agents, 10 skills, 63 relative links, settings JSON, secret scan |
| Planted a bad anchor in a copy and ran the validator | Caught (showing the anchor check works) |
| `bash -n scripts/install-team.sh` | OK |
| `shellcheck scripts/install-team.sh` (0.11.0, installed temporarily) | Clean |
| `actionlint .github/workflows/ci.yml` (v1.7.7 via `go run`) | Clean |
| Installer smoke test (the same steps CI runs) | Passed: fresh install, an idempotent re-run, `--update` kept PROJECT.md, an existing CLAUDE.md was left alone and CLAUDE.ai-team.md was written |
| PyYAML cross-check of all frontmatter | Passed |

- Not run: the GitHub Actions workflow itself, because nothing has been pushed yet.
- Not run: live loading of the agents and skills in a Claude Code session. **That hasn't been
  verified**; use the smoke test in `docs/SKILLS.md`.

## 7. Security findings and remaining risks
- No secrets in the diff (the scan was clean).
- Agent prompts and CLAUDE.md are instructions, not a sandbox. The deny rules are pattern-based.
  Branch protection and least-privilege credentials are still needed.
- The tech-lead, security and code-review agents have `Bash` so they can run read-only git and
  scanner commands. That limit is enforced by their prompts, not technically.

## 8. Known limitations and follow-up
- `/code-review` may clash with a built-in Claude Code command of the same name. It's
  documented, along with a rename workaround.
- Deny-rule syntax (`Bash(cmd:*)`) should be checked against your Claude Code version.
- The installer is bash, so Windows needs Git Bash or WSL. PowerShell steps for copying by hand
  are in the docs.

## 9. Branch and pull request
Branch `feat/ai-engineering-team` (commit `1182aa5`) is on top of `main` (`0d18941`, an empty
"Initial commit"). **Not pushed:** GitHub refused push access for this session. The full history
is in `ai-team-template.bundle`, and there's a plain copy of the files in `ai-team-template.zip`.

## 10. Decisions awaiting your approval
- Give me push access so I can push both branches and open the PR, or push the bundle yourself.
- Merge the PR after review (I won't merge it).
