#!/usr/bin/env bash
# Install or update the AI engineering team (CLAUDE.md, .claude/agents, .claude/skills,
# .claude/settings.json, .claude/PROJECT.md) into a target repository.
#
# Usage: scripts/install-team.sh [--update] [--dry-run] <target-repo-dir>
#
#   (default)  First install. Never overwrites an existing file.
#   --update   Overwrite template-owned files (template agents, template skills, and
#              CLAUDE.md when it is the template's version). Never touches
#              .claude/PROJECT.md, other agents/skills, or an existing settings.json.
#   --dry-run  Print what would happen without writing anything.
set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_MD_MARKER="# AI Engineering Team: operating rules"

update=0
dry_run=0
target=""

usage() {
  sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --update) update=1 ;;
    --dry-run) dry_run=1 ;;
    -h|--help) usage 0 ;;
    -*) echo "Unknown option: $1" >&2; usage 2 ;;
    *)
      if [ -n "$target" ]; then echo "Only one target directory allowed" >&2; usage 2; fi
      target="$1"
      ;;
  esac
  shift
done

[ -n "$target" ] || usage 2
[ -d "$target" ] || { echo "Target directory does not exist: $target" >&2; exit 1; }
target="$(cd "$target" && pwd)"

if [ "$target" = "$TEMPLATE_DIR" ]; then
  echo "Target is the template repository itself; nothing to do." >&2
  exit 1
fi

if [ ! -d "$target/.git" ]; then
  echo "Warning: $target is not a git repository root. Continuing." >&2
fi

created=0; updated=0; skipped=0; unchanged=0

say() { printf '%-10s %s\n' "$1" "$2"; }

# copy_file <src> <dest> <mode>: mode is "owned" (template-owned) or "once" (never overwrite)
copy_file() {
  local src="$1" dest="$2" mode="$3" rel="${2#"$target"/}"
  if [ ! -e "$dest" ]; then
    say "create" "$rel"; created=$((created + 1))
    if [ "$dry_run" -eq 0 ]; then mkdir -p "$(dirname "$dest")"; cp "$src" "$dest"; fi
  elif cmp -s "$src" "$dest"; then
    unchanged=$((unchanged + 1))
  elif [ "$mode" = "owned" ] && [ "$update" -eq 1 ]; then
    say "update" "$rel"; updated=$((updated + 1))
    if [ "$dry_run" -eq 0 ]; then cp "$src" "$dest"; fi
  else
    say "skip" "$rel (exists and differs; not overwritten)"; skipped=$((skipped + 1))
  fi
}

# Agents: one file each.
for src in "$TEMPLATE_DIR"/.claude/agents/*.md; do
  copy_file "$src" "$target/.claude/agents/$(basename "$src")" owned
done

# Skills: every file inside each template skill directory.
for skill_dir in "$TEMPLATE_DIR"/.claude/skills/*/; do
  name="$(basename "$skill_dir")"
  while IFS= read -r -d '' src; do
    rel="${src#"$skill_dir"}"
    copy_file "$src" "$target/.claude/skills/$name/$rel" owned
  done < <(find "$skill_dir" -type f -print0)
done

# CLAUDE.md: template-owned only when the target's copy is the template's version.
if [ -e "$target/CLAUDE.md" ] && [ "$(head -n 1 "$target/CLAUDE.md")" != "$CLAUDE_MD_MARKER" ]; then
  say "side-by-side" "CLAUDE.ai-team.md (your CLAUDE.md is project-specific; see docs/PROJECT_ONBOARDING.md)"
  if [ "$dry_run" -eq 0 ]; then cp "$TEMPLATE_DIR/CLAUDE.md" "$target/CLAUDE.ai-team.md"; fi
  skipped=$((skipped + 1))
else
  copy_file "$TEMPLATE_DIR/CLAUDE.md" "$target/CLAUDE.md" owned
fi

# settings.json: shared; never overwritten.
if [ -e "$target/.claude/settings.json" ] && ! cmp -s "$TEMPLATE_DIR/.claude/settings.json" "$target/.claude/settings.json"; then
  say "side-by-side" ".claude/settings.ai-team.json (merge permissions.deny into settings.json by hand)"
  if [ "$dry_run" -eq 0 ]; then cp "$TEMPLATE_DIR/.claude/settings.json" "$target/.claude/settings.ai-team.json"; fi
  skipped=$((skipped + 1))
else
  copy_file "$TEMPLATE_DIR/.claude/settings.json" "$target/.claude/settings.json" once
fi

# PROJECT.md: project-owned; created from the blank template only if missing.
copy_file "$TEMPLATE_DIR/templates/PROJECT.template.md" "$target/.claude/PROJECT.md" once

echo
echo "created=$created updated=$updated skipped=$skipped unchanged=$unchanged$([ "$dry_run" -eq 1 ] && echo ' (dry run, nothing written)')"
echo "Next: review 'git status' in $target, fill in .claude/PROJECT.md (or run /project-audit), and commit on a branch."
