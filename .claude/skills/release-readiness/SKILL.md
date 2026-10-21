---
name: release-readiness
description: Go/no-go assessment before a release, merge or deployment. Use when asked whether a branch, PR or version is ready to ship. Verifies acceptance criteria, build and test results, security findings, documentation, migration readiness, rollback plan and required human approvals. Produces a checklist and recommendation; never merges or deploys.
argument-hint: "[release, version, branch or PR]"
---

# Release Readiness

Release: $ARGUMENTS (default: the current branch)

**Use when:** deciding whether something is ready for approval to merge or deploy. **Do not
use** to perform the release. This skill never merges, tags, publishes, or deploys; those are
owner actions (see the approval list in `CLAUDE.md`).

## Steps

1. **Scope:** list what is in the release: PRs, commits (`git log --oneline <last-tag>..HEAD`
   or `<base>..HEAD`), linked issues, and the acceptance criteria for each.
2. **Acceptance criteria:** for each AC, find the verifying test or documented manual check.
   Mark verified / not verified.
3. **Build and tests:** run the project's build, lint, type-check, and test commands from
   `.claude/PROJECT.md` (or read the latest CI run for the exact commit, and say which source
   you used). Record failures, skips, and flaky tests.
4. **Security:** collect open findings from `/security-audit` or run it for risky changes.
   Any open Critical or High finding is a blocker unless the owner accepts the risk in writing.
5. **Dependencies and config:** new dependencies justified, lockfile committed, new
   environment variables documented in `.env.example` and docs, feature flags defaulted
   safely.
6. **Database:** migrations reviewed (`/database-migration`), order relative to deploy
   defined, rollback tested or explained, destructive steps approved.
7. **Infrastructure and deploy:** CI/CD changes reviewed, deployment steps written, rollback
   plan written (what to revert, how, how to verify), monitoring and alerts identified.
8. **Documentation:** README, API docs, changelog or release notes updated and accurate.
9. **Approvals:** list each required human approval and whether it has been given (by whom,
   where). Missing approvals block a "ready" verdict.

Delegate where useful: `qa-test-engineer` (2–3), `security-engineer` (4),
`database-engineer` (6), `devops-cloud-engineer` (7), `technical-writer` (8),
`ceo-strategy-advisor` for an executive summary.

## Output

```
# Release readiness: <name>
## Verdict: Ready for approval / Ready with conditions / Not ready
## Blockers
## Checklist
| Area | Status (pass / fail / not verified) | Evidence |
| Acceptance criteria | | |
| Build | | |
| Tests | | |
| Security | | |
| Dependencies & config | | |
| Database migrations | | |
| Rollback plan | | |
| Documentation | | |
| Human approvals | | |
## Commands run (command → result)
## Risks accepted / awaiting owner decision
```

"Ready for approval" means the evidence supports release. It is not itself an approval.

## Example invocations

```
/release-readiness Check whether this release is ready for approval
/release-readiness v1.4.0
/release-readiness PR 57
```
