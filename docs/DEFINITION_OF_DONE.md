# Definition of Done

A task is done when the evidence says so, not when code is written. Items that do not apply
are marked "n/a" with a reason in the delivery report.

## Every task

- [ ] The requested outcome is restated and matches what was delivered.
- [ ] Repository was inspected before changes; no unrelated files or user changes were touched.
- [ ] Each acceptance criterion is verified by a named test or documented manual check, or the
      gap is stated plainly.
- [ ] Relevant format, lint, type-check, test, and build commands were run, with exact commands
      and results reported. Anything not run is listed with the reason.
- [ ] No test was skipped, deleted, or weakened without written justification and approval.
- [ ] No secrets, credentials, private data, or large binaries were added (diff checked).
- [ ] Work is on a feature branch; a PR is open for review if the environment supports it.
      Nothing was merged, force-pushed, or deployed.
- [ ] The delivery report is complete, including agents actually used and decisions awaiting
      approval.

## Standard and larger tasks (add)

- [ ] Independent review by `code-reviewer`; blocking findings fixed or explicitly deferred
      by the owner.
- [ ] `qa-test-engineer` traceability table (AC → tests → result).
- [ ] Documentation affected by the change is updated, and nothing unimplemented is described
      as complete.

## Substantial or risky tasks (add)

- [ ] The plan was approved by the owner before implementation (link or quote).
- [ ] `security-engineer` review when the change touches auth, input handling, files, secrets,
      dependencies, CI permissions, or AI input/output; no open Critical or High findings
      unless the owner accepted the risk.
- [ ] Backward compatibility of public contracts confirmed, or the breaking change approved
      and documented.

## Database changes (add)

- [ ] Migration follows the project's tool and conventions, with a rollback migration or plan.
- [ ] Destructive steps approved explicitly.
- [ ] Migration applied, rolled back, and re-applied on a local or disposable database, or the
      report states it was not executed and why.

## AI/ML changes (add)

- [ ] Data provenance, quality, and leakage checks recorded.
- [ ] Baseline and metrics defined; every reported number comes from a run in the experiment
      log (or a cited artefact).
- [ ] Limitations and failure cases documented.
- [ ] No private data or models sent externally without approval.

## Infrastructure and CI changes (add)

- [ ] Permissions are minimal and not broadened without approval.
- [ ] `fmt` / `validate` / `plan` (or equivalent) run where available; nothing applied to live
      infrastructure without approval.
- [ ] Rollback steps written.
