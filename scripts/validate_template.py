#!/usr/bin/env python3
"""Static validation for the AI engineering team template.

Checks, using only the Python standard library:
  * every required agent and skill exists
  * YAML frontmatter is present and well formed (simple `key: value` subset)
  * agent and skill names are unique, valid, and match their file or directory
  * descriptions are present and within length limits
  * agent tool lists use known tools and respect the read-only / docs-only policy
  * every agent and skill named in CLAUDE.md exists
  * relative Markdown links and their #anchors resolve
  * .claude/settings.json is valid JSON
  * no obvious secrets are committed

Usage:
  python3 scripts/validate_template.py [--root DIR] [--require-all]
  python3 scripts/validate_template.py --self-test

--root points at a repository to check (default: this template). Required agents and skills
are enforced only for the template itself, or when --require-all is given.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

REQUIRED_AGENTS = {
    "ceo-strategy-advisor",
    "business-analyst",
    "tech-lead-architect",
    "ui-ux-designer",
    "frontend-engineer",
    "backend-engineer",
    "database-engineer",
    "qa-test-engineer",
    "ai-ml-engineer",
    "devops-cloud-engineer",
    "security-engineer",
    "code-reviewer",
    "technical-writer",
}

REQUIRED_SKILLS = {
    "execute-task",
    "project-audit",
    "feature-development",
    "bug-fix",
    "code-review",
    "ai-ml-engineering",
    "go-development",
    "database-migration",
    "security-audit",
    "release-readiness",
}

KNOWN_TOOLS = {
    "Read", "Grep", "Glob", "Edit", "Write", "MultiEdit", "Bash", "NotebookEdit",
    "WebFetch", "WebSearch", "TodoWrite", "Task", "Agent", "LS",
}
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

# Agents that must never be able to modify files.
READ_ONLY_AGENTS = {"ceo-strategy-advisor", "tech-lead-architect", "security-engineer", "code-reviewer"}
# Agents that write documents only and must not run shell commands.
NO_SHELL_AGENTS = {"ceo-strategy-advisor", "business-analyst", "ui-ux-designer", "technical-writer"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MIN_DESCRIPTION = 40

SECRET_PATTERNS = [
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("OpenAI/Anthropic style key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{32,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".sh", ".py", ".txt", ".toml", ".cfg", ".ini", ""}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self, msg: str) -> None:
        self.passed.append(msg)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Parse a leading `---` block of simple `key: value` pairs.

    Returns (fields, error). fields is None when parsing failed.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "file must start with a '---' frontmatter line"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, "frontmatter is not closed with '---'"
    fields: dict[str, str] = {}
    for n, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s+(.*))?$", raw)
        if not m:
            return None, f"line {n}: expected 'key: value', got {raw!r}"
        key, value = m.group(1), (m.group(2) or "").strip()
        if key in fields:
            return None, f"line {n}: duplicate key {key!r}"
        if value[:1] in {'"', "'"}:
            if len(value) < 2 or value[-1] != value[0]:
                return None, f"line {n}: unterminated quoted value for {key!r}"
            value = value[1:-1]
        elif value.startswith(("[", "{", "|", ">")):
            return None, f"line {n}: only plain one-line values are supported for {key!r}"
        elif ": " in value or value.endswith(":"):
            return None, f"line {n}: value for {key!r} contains ': ' and must be quoted"
        fields[key] = value
    return fields, ""


def cross_check_yaml(path: Path, text: str, report: Report) -> None:
    """If PyYAML is installed, confirm it parses the frontmatter the same way."""
    try:
        import yaml  # type: ignore
    except ImportError:
        return
    block = text.split("\n---", 1)[0].lstrip("-\n")
    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:  # pragma: no cover - depends on input
        report.error(f"{path}: PyYAML cannot parse frontmatter: {exc}")
        return
    if not isinstance(data, dict):
        report.error(f"{path}: frontmatter is not a mapping according to PyYAML")


def check_name_and_description(path: Path, fields: dict[str, str], expected: str, report: Report) -> None:
    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not name:
        report.error(f"{path}: missing 'name'")
    elif not NAME_RE.match(name) or len(name) > MAX_NAME:
        report.error(f"{path}: name {name!r} must be lowercase kebab-case, at most {MAX_NAME} chars")
    elif name != expected:
        report.error(f"{path}: name {name!r} does not match {expected!r}")
    if not desc:
        report.error(f"{path}: missing 'description'")
    elif len(desc) < MIN_DESCRIPTION:
        report.error(f"{path}: description is too short to guide delegation ({len(desc)} chars)")
    elif len(desc) > MAX_DESCRIPTION:
        report.error(f"{path}: description exceeds {MAX_DESCRIPTION} chars ({len(desc)})")
    if "<" in desc or ">" in desc:
        report.warn(f"{path}: description contains angle brackets")


def check_agents(root: Path, require_all: bool, report: Report) -> set[str]:
    agent_dir = root / ".claude" / "agents"
    names: dict[str, Path] = {}
    if not agent_dir.is_dir():
        if require_all:
            report.error(".claude/agents/ directory is missing")
        return set()
    for path in sorted(agent_dir.glob("*.md")):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        fields, err = parse_frontmatter(text)
        if fields is None:
            report.error(f"{rel}: invalid frontmatter: {err}")
            continue
        cross_check_yaml(rel, text, report)
        check_name_and_description(rel, fields, path.stem, report)
        name = fields.get("name", path.stem)
        if name in names:
            report.error(f"{rel}: duplicate agent name {name!r} (also {names[name]})")
        names[name] = rel

        tools_raw = fields.get("tools")
        if tools_raw is None:
            report.error(f"{rel}: missing 'tools' (agents must declare a minimal tool list)")
            continue
        tools = [t.strip() for t in tools_raw.split(",") if t.strip()]
        unknown = [t for t in tools if t.split("(")[0] not in KNOWN_TOOLS and not t.startswith("mcp__")]
        if unknown:
            report.error(f"{rel}: unknown tools {unknown}")
        if len(set(tools)) != len(tools):
            report.error(f"{rel}: duplicate entries in tools")
        if name in READ_ONLY_AGENTS and WRITE_TOOLS & set(tools):
            report.error(f"{rel}: read-only agent must not have {sorted(WRITE_TOOLS & set(tools))}")
        if name in NO_SHELL_AGENTS and "Bash" in tools:
            report.error(f"{rel}: documentation/analysis agent must not have Bash")
        body = text.split("\n---", 1)[1] if "\n---" in text else ""
        if "## Boundaries" not in body:
            report.error(f"{rel}: body must contain a '## Boundaries' section")

    if require_all:
        missing = REQUIRED_AGENTS - set(names)
        if missing:
            report.error(f"missing required agents: {sorted(missing)}")
    report.ok(f"agents checked: {len(names)}")
    return set(names)


def check_skills(root: Path, require_all: bool, report: Report) -> set[str]:
    skill_root = root / ".claude" / "skills"
    names: set[str] = set()
    if not skill_root.is_dir():
        if require_all:
            report.error(".claude/skills/ directory is missing")
        return names
    for skill_dir in sorted(p for p in skill_root.iterdir() if p.is_dir()):
        path = skill_dir / "SKILL.md"
        rel = path.relative_to(root)
        if not path.is_file():
            report.error(f"{skill_dir.relative_to(root)}/: missing SKILL.md (file name is case-sensitive)")
            continue
        text = path.read_text(encoding="utf-8")
        fields, err = parse_frontmatter(text)
        if fields is None:
            report.error(f"{rel}: invalid frontmatter: {err}")
            continue
        cross_check_yaml(rel, text, report)
        check_name_and_description(rel, fields, skill_dir.name, report)
        name = fields.get("name", skill_dir.name)
        if name in names:
            report.error(f"{rel}: duplicate skill name {name!r}")
        names.add(name)
        body = text.split("\n---", 1)[1] if "\n---" in text else ""
        if len(body.strip().splitlines()) < 15:
            report.error(f"{rel}: body is too short to be a usable workflow")
        if f"/{name}" not in body and require_all:
            report.error(f"{rel}: body should include an example '/{name}' invocation")
        # Paths under .claude/ mentioned in backticks must exist.
        for ref in re.findall(r"`(\.claude/[^`*<>\s]+)`", body):
            if not (root / ref).exists():
                report.error(f"{rel}: referenced path does not exist: {ref}")
    if require_all:
        missing = REQUIRED_SKILLS - names
        if missing:
            report.error(f"missing required skills: {sorted(missing)}")
    report.ok(f"skills checked: {len(names)}")
    return names


def check_claude_md(root: Path, agents: set[str], skills: set[str], require_all: bool, report: Report) -> None:
    path = root / "CLAUDE.md"
    if not path.is_file():
        if require_all:
            report.error("CLAUDE.md is missing")
        return
    text = path.read_text(encoding="utf-8")
    for imp in re.findall(r"^@(\S+)", text, flags=re.M):
        if not (root / imp).exists():
            report.error(f"CLAUDE.md imports missing file: {imp}")
    tokens = set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", text))
    known_terms = {"pull-request", "e-mail"}
    for token in sorted(tokens - known_terms):
        if token not in agents and token not in skills:
            report.error(f"CLAUDE.md mentions `{token}` but no agent or skill has that name")
    if require_all:
        for name in sorted(REQUIRED_AGENTS | REQUIRED_SKILLS):
            if f"`{name}`" not in text:
                report.error(f"CLAUDE.md routing does not mention `{name}`")
    report.ok("CLAUDE.md references checked")


def github_slug(heading: str) -> str:
    heading = re.sub(r"`", "", heading.strip().lower())
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def anchors_for(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        slugs: set[str] = set()
        counts: dict[str, int] = {}
        in_fence = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
            if m and not in_fence:
                slug = github_slug(m.group(1))
                n = counts.get(slug, 0)
                slugs.add(slug if n == 0 else f"{slug}-{n}")
                counts[slug] = n + 1
        cache[path] = slugs
    return cache[path]


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            yield path


def check_links(root: Path, report: Report) -> None:
    cache: dict[Path, set[str]] = {}
    count = 0
    for path in iter_files(root):
        if path.suffix != ".md":
            continue
        rel = path.relative_to(root)
        in_fence = False
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                    continue  # http:, https:, mailto:
                file_part, _, anchor = target.partition("#")
                dest = (path.parent / file_part).resolve() if file_part else path
                count += 1
                try:
                    dest.relative_to(root.resolve())
                except ValueError:
                    report.error(f"{rel}:{n}: link leaves the repository: {target}")
                    continue
                if not dest.exists():
                    report.error(f"{rel}:{n}: broken link: {target}")
                elif anchor and dest.suffix == ".md" and anchor not in anchors_for(dest, cache):
                    report.error(f"{rel}:{n}: missing anchor #{anchor} in {file_part or rel}")
    report.ok(f"relative links checked: {count}")


def check_settings(root: Path, report: Report) -> None:
    for name in ("settings.json", "settings.local.json"):
        path = root / ".claude" / name
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                report.error(f".claude/{name}: invalid JSON: {exc}")
                continue
            allow = data.get("permissions", {}).get("allow", [])
            if any(rule in ("Bash", "Bash(*)", "Bash(:*)") for rule in allow):
                report.error(f".claude/{name}: allows all Bash commands")
            report.ok(f".claude/{name} is valid JSON")


def check_secrets(root: Path, report: Report) -> None:
    hits = 0
    for path in iter_files(root):
        if path.suffix not in TEXT_SUFFIXES or path.stat().st_size > 1_000_000:
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            report.error(f"{path.relative_to(root)}: environment file must not be committed")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.resolve() == Path(__file__).resolve():
            continue  # this file contains the patterns themselves
        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                report.error(f"{path.relative_to(root)}:{line}: possible {label} (value redacted)")
                hits += 1
    if hits == 0:
        report.ok("secret scan: no matches")


def validate(root: Path, require_all: bool) -> Report:
    report = Report()
    agents = check_agents(root, require_all, report)
    skills = check_skills(root, require_all, report)
    check_claude_md(root, agents, skills, require_all, report)
    check_links(root, report)
    check_settings(root, report)
    check_secrets(root, report)
    return report


def self_test() -> int:
    """Run the validator against broken fixtures and confirm each problem is caught."""
    good_fm = "---\nname: {n}\ndescription: A sufficiently long description used for delegation tests.\n{extra}---\n"
    cases = {
        "missing frontmatter": ("agents/a-one.md", "# no frontmatter\n## Boundaries\n", "invalid frontmatter"),
        "name mismatch": ("agents/a-two.md", good_fm.format(n="other", extra="tools: Read\n") + "## Boundaries\n", "does not match"),
        "unknown tool": ("agents/a-three.md", good_fm.format(n="a-three", extra="tools: Read, Hack\n") + "## Boundaries\n", "unknown tools"),
        "read-only agent with Write": ("agents/code-reviewer.md", good_fm.format(n="code-reviewer", extra="tools: Read, Write\n") + "## Boundaries\n", "read-only agent"),
        "unquoted colon": ("agents/a-four.md", "---\nname: a-four\ndescription: Use when: things\ntools: Read\n---\n## Boundaries\n", "must be quoted"),
        "skill missing SKILL.md": ("skills/s-one/skill.md", "x", "missing SKILL.md"),
        "broken link": ("../README.md", "[x](docs/nope.md)\n", "broken link"),
        "secret": ("../leak.txt", "key = AKIA" + "ABCDEFGHIJKLMNOP\n", "possible AWS access key"),
    }
    failures = 0
    for label, (rel, content, expect) in cases.items():
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = (root / ".claude" / rel).resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            report = validate(root, require_all=False)
            caught = any(expect in e for e in report.errors)
            print(f"[{'PASS' if caught else 'FAIL'}] self-test: {label}")
            failures += 0 if caught else 1
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / ".claude" / "agents"
        d.mkdir(parents=True)
        (d / "good-agent.md").write_text(good_fm.format(n="good-agent", extra="tools: Read, Grep\n") + "## Boundaries\n", encoding="utf-8")
        report = validate(root, require_all=False)
        clean = not report.errors
        print(f"[{'PASS' if clean else 'FAIL'}] self-test: valid fixture has no errors {report.errors if not clean else ''}")
        failures += 0 if clean else 1
    print(f"self-test: {failures} failure(s)")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--require-all", action="store_true", help="enforce the full template agent and skill set")
    parser.add_argument("--self-test", action="store_true", help="test the validator itself")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    root = args.root.resolve()
    template_root = Path(__file__).resolve().parent.parent
    require_all = args.require_all or root == template_root
    report = validate(root, require_all)
    for msg in report.passed:
        print(f"ok      {msg}")
    for msg in report.warnings:
        print(f"warning {msg}")
    for msg in report.errors:
        print(f"ERROR   {msg}")
    print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
