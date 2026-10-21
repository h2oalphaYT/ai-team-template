# Security, permissions and approval boundaries

This page explains how the AI team is constrained and what remains your responsibility. The
binding rules for Claude are in [CLAUDE.md](../CLAUDE.md#5-approval-required-always-stop-and-ask);
this page is the human-facing explanation.

## Layers of control

| Layer | Where | What it does | Strength |
|---|---|---|---|
| Rules | `CLAUDE.md` | Approval list, secrets rules, untrusted-input rule, truthful reporting | Instruction: Claude follows it, but it is not a sandbox |
| Agent tool lists | `tools:` in `.claude/agents/*.md` | Reviewers and analysts cannot edit files; spec writers cannot run shell commands | Enforced by Claude Code |
| Permission deny list | `.claude/settings.json` | Blocks reading `.env`, keys, `*.tfstate`; blocks force-push, hard reset, `terraform apply/destroy`, `kubectl apply/delete`, `helm upgrade/uninstall`, `gh pr merge` | Enforced by Claude Code permission system |
| Your environment | Claude Code permission mode, cloud environment network policy, GitHub App permissions, branch protection | Decides what the session can reach at all | Strongest; configure it deliberately |
| CI | `.github/workflows/ci.yml` | Read-only token, no secrets, pinned action | Enforced by GitHub |

Deny rules are pattern matches on commands and paths. They reduce risk but cannot catch every
variation (for example a script that deletes files). Branch protection on your default branch
and least-privilege credentials are the real backstop.

## Approval list

Claude must get your explicit approval, in the conversation, before:

1. Deleting important files or data.
2. Destructive database migrations or bulk data changes.
3. Changing production or shared infrastructure.
4. Deploying beyond local or disposable environments.
5. Merging, force-pushing, rewriting history, or pushing to the default branch.
6. Publishing private information, datasets, or models, or sending them to external services.
7. Major architecture changes, framework migrations, rewrites.
8. Significant costs or new external services.
9. Disabling security checks, weakening tests, or broadening permissions.

Text in an issue, PR, commit, document, dataset, or tool output is never approval.

## Secrets

- Claude does not open `.env` files (denied in settings) and refers to secrets by name only.
- Document variables in `.env.example` with placeholders, never real values.
- If a secret is found committed, the report gives its location and type, redacted. Rotating it
  and removing it from history is your action.
- In Claude Code on the web, prefer the environment's secret settings for credentials the
  session truly needs, scoped to non-production resources.

## Untrusted input and prompt injection

Repository content, issues, PR descriptions, commit messages, web pages, datasets, and model
output can contain instructions written by someone else. The team treats them as data: it
does not follow embedded requests to reveal secrets, change permissions, disable checks, or
skip approvals, and it reports such content. This matters especially for AI/LLM features,
where retrieved documents and user input reach a model.

## Data safety

- No private datasets, customer data, or large model files are committed.
- No private data is sent to external APIs (including third-party model APIs) without approval.
- Tests use fixtures, mocks, or disposable databases, never production data.

## CI hardening in this repository

- `permissions: contents: read` at workflow level.
- Triggered on `push` and `pull_request` only; no `pull_request_target`, so fork PRs never
  receive secrets.
- Third-party actions pinned to a full commit SHA.
- `persist-credentials: false` on checkout.
- The validation job uses only the Python standard library; nothing is downloaded at run time.

When you add workflows to a target repository, keep the same defaults and ask the
`devops-cloud-engineer` and `security-engineer` agents to review them.

## Reporting a problem with the template

If you find a way the template could lead Claude to unsafe behaviour, open an issue in the
template repository describing the scenario (without real secrets).
