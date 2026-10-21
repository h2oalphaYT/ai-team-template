# Agent catalog

Thirteen specialist subagents live in [`.claude/agents/`](../.claude/agents/). Each file has
YAML frontmatter (`name`, `description`, `tools`) and a body with responsibilities, method,
output format, and boundaries. The `description` tells Claude when to delegate; the `tools`
line limits what the agent can do.

Agents are selected per task. A trivial fix uses none; a substantial feature may use five or
six. See [WORKFLOW.md](WORKFLOW.md) for when each is called.

## Summary

| Agent | Role | Tools | Writes files? |
|---|---|---|---|
| [`ceo-strategy-advisor`](../.claude/agents/ceo-strategy-advisor.md) | Priorities, trade-offs, executive summaries | Read, Grep, Glob | No |
| [`business-analyst`](../.claude/agents/business-analyst.md) | Requirements, user stories, acceptance criteria | Read, Grep, Glob, Write, Edit | Requirement docs only |
| [`tech-lead-architect`](../.claude/agents/tech-lead-architect.md) | Architecture, contracts, task breakdown | Read, Grep, Glob, Bash (read-only use) | No |
| [`ui-ux-designer`](../.claude/agents/ui-ux-designer.md) | Journeys, wireframes, states, accessibility, DX | Read, Grep, Glob, Write, Edit | Design docs only |
| [`frontend-engineer`](../.claude/agents/frontend-engineer.md) | UI implementation and tests | Read, Grep, Glob, Edit, Write, Bash | Yes |
| [`backend-engineer`](../.claude/agents/backend-engineer.md) | APIs, business logic, auth, tests | Read, Grep, Glob, Edit, Write, Bash | Yes |
| [`database-engineer`](../.claude/agents/database-engineer.md) | Schema, migrations, queries, integrity | Read, Grep, Glob, Edit, Write, Bash | Yes |
| [`qa-test-engineer`](../.claude/agents/qa-test-engineer.md) | Test design, execution, verification | Read, Grep, Glob, Edit, Write, Bash | Tests |
| [`ai-ml-engineer`](../.claude/agents/ai-ml-engineer.md) | ML/DL/CV/NLP/LLM/RAG, data, evaluation | Read, Grep, Glob, Edit, Write, Bash | Yes |
| [`devops-cloud-engineer`](../.claude/agents/devops-cloud-engineer.md) | CI/CD, containers, IaC, deploy and rollback | Read, Grep, Glob, Edit, Write, Bash | Yes |
| [`security-engineer`](../.claude/agents/security-engineer.md) | Security review and scanning | Read, Grep, Glob, Bash | No |
| [`code-reviewer`](../.claude/agents/code-reviewer.md) | Diff review against requirements | Read, Grep, Glob, Bash | No |
| [`technical-writer`](../.claude/agents/technical-writer.md) | README, guides, API docs, release notes | Read, Grep, Glob, Edit, Write | Docs only |

## Why these tool sets

- **Analysis agents** (`ceo-strategy-advisor`) get read-only tools.
- **Spec writers** (`business-analyst`, `ui-ux-designer`, `technical-writer`) can write
  Markdown but have no `Bash`, so they cannot run commands or change the build.
- **Reviewers** (`tech-lead-architect`, `security-engineer`, `code-reviewer`) have `Bash` to
  run `git diff`, dependency listings, and scanners, but no `Edit` or `Write`, so they cannot
  change code. Their prompts restrict `Bash` to read-only use; this is an instruction, not a
  technical sandbox, which is why destructive commands are also denied in
  [`.claude/settings.json`](../.claude/settings.json).
- **Implementers** get edit and shell access because they must change code and run tests.
  Their approval gates are in each prompt and in [`CLAUDE.md`](../CLAUDE.md).

## Role details

### CEO and Product Strategy Advisor
Turns business objectives into ranked priorities with value, risk, dependencies, and
reversibility; writes executive summaries. Recommends only, never commits on the owner's
behalf, and marks major decisions for owner approval.

### Business Analyst
Discovers users, roles, permissions, workflows, functional and non-functional requirements;
writes user stories, Given/When/Then acceptance criteria, edge cases, assumptions, and open
questions. Every requirement is labelled Confirmed, Assumed, or Open.

### Technical Lead and Software Architect
Inspects the real architecture and stack with evidence, proposes the smallest maintainable
design, defines contracts, and breaks work into ordered tasks with owners and verification.
Blocks unjustified rewrites, migrations, and dependencies.

### UI/UX Designer
Specifies journeys, information architecture, text wireframes, components, tokens, responsive
behaviour, accessibility (WCAG 2.2 AA by default), and loading, empty, error, and success
states. Respects the existing design system. For headless projects, designs CLI/API developer
experience and docs.

### Frontend Engineer
Detects the actual frontend stack, reuses existing components, builds accessible, responsive,
authorization-aware UI with validation and state handling, integrates APIs through documented
contracts, and runs the project's own lint, type-check, test, and build.

### Backend Engineer
Detects the backend stack (Go, Node.js, Java, Python, .NET and others), implements APIs and
business logic with server-side validation and authorization, preserves public contracts,
uses parameterized data access, and adds unit and integration tests.

### Database Engineer
Identifies engine, schema, and migration tooling; writes reversible, preferably additive
migrations with rollback plans; reviews queries, indexes, constraints, and transactions.
Destructive or non-local operations require approval.

### QA and Test Automation Engineer
Maps acceptance criteria to tests, designs positive, negative, boundary, regression, security,
and integration cases, runs the real commands, reproduces defects, and reports exact commands
and passed, failed, skipped, and blocked results. Never weakens tests to pass.

### AI/ML Engineer
Clarifies the use case before choosing a model, audits data quality, provenance, and leakage,
sets baselines and fitting metrics, runs reproducible experiments, compares quality, latency,
memory, and cost, tests preprocessing and inference, and documents limitations. Never invents
results or uploads private data without approval.

### DevOps and Cloud Engineer
Inventories CI/CD, containers, and IaC; keeps workflow permissions minimal and actions pinned;
handles secrets through the platform store; validates and plans infrastructure changes but
never applies or deploys without approval; defines rollback.

### Security Engineer
Reviews access control, injection, secrets, insecure defaults, file handling, dependencies,
CI/CD permissions, and AI/ML risks. Classifies findings as Verified or Potential, with
severity, evidence, remediation, and verification steps. Never prints secrets.

### Code Review Engineer
Reviews the actual diff against requirements for correctness, regressions, security, tests,
maintainability, and performance. Reports blocking findings and suggestions with `path:line`.
Never edits code during review.

### Technical Content and Documentation Developer
Maintains README, setup, architecture, API docs, and release notes, verifying each statement
against code and config. Documents environment variable names without values and labels
unimplemented features as Planned.

## Customising agents in a target repository

- Prefer adding project facts to `.claude/PROJECT.md` over editing agent files, so template
  updates stay easy.
- To specialise a role (for example a Spring Boot backend), add a new agent with a new name,
  such as `spring-backend-engineer.md`, rather than editing the template's copy.
- To remove an agent that a project never needs, delete its file in that repository and note
  it in `.claude/PROJECT.md`.
