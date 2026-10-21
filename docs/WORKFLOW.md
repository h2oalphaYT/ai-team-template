# Delivery workflow

```
UNDERSTAND → ANALYZE → PLAN → APPROVE → IMPLEMENT → TEST → REVIEW → DOCUMENT → REPORT
```

The operative, step-by-step version is the
[`execute-task` skill](../.claude/skills/execute-task/SKILL.md). This page explains the
process for humans: what happens at each stage, who is involved, and where you, the owner,
are asked to decide.

## Task sizes

| Size | Examples | Agents | Owner approval |
|---|---|---|---|
| Trivial | typo, comment, one-line config, obvious local fix | none | not needed (unless on the approval list) |
| Standard | small change inside one component, no contract or schema change | implementer, QA, reviewer as useful | not needed; plan shown in report |
| Substantial or risky | new feature, cross-component, public API, schema, auth, infra, ML model | full set as relevant | **required after the plan** |

Anything on the approval list in [CLAUDE.md](../CLAUDE.md#5-approval-required-always-stop-and-ask)
needs approval regardless of size.

## Stages

| # | Stage | What happens | Typical agents | Output |
|---|---|---|---|---|
| 1 | Understand | Restate the outcome, inspect code and `.claude/PROJECT.md`, check `git status`, list missing information | none | restated goal, questions or assumptions |
| 2 | Analyze | Requirements, design, risk | `business-analyst`, `tech-lead-architect`, `ui-ux-designer`, `database-engineer`, `ai-ml-engineer`, `security-engineer` | requirements, design notes |
| 3 | Plan | Acceptance criteria, files, order, tests, risks, approvals | `tech-lead-architect` | [task plan](../.claude/skills/execute-task/templates/task-plan.md) |
| — | **Approve** | Owner reviews the plan for substantial or risky work | owner | go / change / stop |
| 4 | Implement | Small focused commits on a feature branch, existing conventions | `frontend-engineer`, `backend-engineer`, `database-engineer`, `ai-ml-engineer`, `devops-cloud-engineer` | code and tests |
| 5 | Verify | Format, lint, type-check, test, build; AC checks; independent QA and review | `qa-test-engineer`, `code-reviewer`, `security-engineer` | command results |
| 6 | Fix and re-test | Fix in-scope failures, re-run affected checks | implementers, QA | updated results |
| 7 | Document | Update affected docs, label anything planned | `technical-writer` | doc changes |
| 8 | Deliver | Push branch, open PR (never merge), write report | — | [delivery report](../.claude/skills/execute-task/templates/delivery-report.md) |

## Which skill starts the workflow

| You ask for | Start with |
|---|---|
| "Look at this repo first" | `/project-audit` |
| A new capability | `/feature-development` |
| A defect or failing test | `/bug-fix` |
| A schema change | `/database-migration` |
| An ML or LLM task | `/ai-ml-engineering` |
| Anything else that changes the repo | `/execute-task` |
| A review only | `/code-review`, `/security-audit` |
| A ship decision | `/release-readiness` |

See [SKILLS.md](SKILLS.md) for the full skills guide.

## Evidence rules

- Test results are reported with the exact command and outcome. "Not run" is a valid, honest
  result; "should pass" is not.
- Failures that already exist on the base branch are reported, not hidden.
- Agents listed in the report are the ones actually invoked.
- Completion is judged against the [Definition of Done](DEFINITION_OF_DONE.md).

## Writing a good task request

Use [TASK_TEMPLATE.md](TASK_TEMPLATE.md) for anything bigger than a small fix. The more
precise the acceptance criteria, the less the team has to assume.
