#!/usr/bin/env bash
#
# Install the genie-dashboard-design skill so GitHub Copilot (VS Code) and
# Claude Code can discover it. Two modes:
#
#   Personal  -- installs to your home directory; works in EVERY repo you open,
#                commits nothing, needs no permissions on the team repo.
#   Repo      -- vendors the skill into one repository so the whole team gets
#                it on clone. Requires commit access to that repo.
#
# Usage:
#   scripts/install-skill.sh --personal [--dir .copilot/skills]
#   scripts/install-skill.sh <target-repo> [--dir .github/skills]
#
# Examples:
#   scripts/install-skill.sh --personal
#   scripts/install-skill.sh ~/work/OSLAUNCH
#   scripts/install-skill.sh ~/work/OSLAUNCH --dir .claude/skills
#
# Copilot scans .github/skills/, .claude/skills/, .agents/skills/ in a workspace,
# and ~/.copilot/skills/, ~/.claude/skills/, ~/.agents/skills/ for personal ones.
# Claude Code scans .claude/skills/ -- so .claude/skills covers both tools.
#
set -euo pipefail

SKILL_NAME="genie-dashboard-design"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/skills/${SKILL_NAME}"

PERSONAL=0
TARGET_ROOT=""
DEST_SUBDIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --personal|--user) PERSONAL=1; shift ;;
    --dir) DEST_SUBDIR="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,25p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) TARGET_ROOT="$1"; shift ;;
  esac
done

if [[ $PERSONAL -eq 1 ]]; then
  TARGET_ROOT="$HOME"
  DEST_SUBDIR="${DEST_SUBDIR:-.copilot/skills}"
elif [[ -n "$TARGET_ROOT" ]]; then
  DEST_SUBDIR="${DEST_SUBDIR:-.github/skills}"
else
  echo "Usage: scripts/install-skill.sh --personal | <target-repo> [--dir <subdir>]" >&2
  exit 1
fi

if [[ ! -d "$TARGET_ROOT" ]]; then
  echo "Target does not exist: $TARGET_ROOT" >&2
  exit 1
fi

if [[ ! -f "$SOURCE_DIR/SKILL.md" ]]; then
  echo "Cannot find the skill at $SOURCE_DIR -- run this from a clone of the plugin repo." >&2
  exit 1
fi

DEST="$TARGET_ROOT/$DEST_SUBDIR/$SKILL_NAME"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"

# Copy the skill, minus Python bytecode caches.
( cd "$SOURCE_DIR" && tar --exclude='__pycache__' --exclude='*.pyc' -cf - . ) | ( cd "$DEST" && tar -xf - )

FILE_COUNT="$(find "$DEST" -type f | wc -l | tr -d ' ')"
echo "Installed ${SKILL_NAME} (${FILE_COUNT} files)"
echo "  -> $DEST"
echo

if [[ $PERSONAL -eq 1 ]]; then
  echo "This is a personal install: the skill is available in every repo you open,"
  echo "and nothing is added to any project's git history."
  echo
  echo "To update later, re-run this command after pulling the latest plugin repo."
else
  if [[ ! -d "$TARGET_ROOT/.git" ]]; then
    echo "Note: $TARGET_ROOT is not a git repository, so this copy is local to you."
  else
    echo "Commit it so the whole team gets it on their next pull:"
    echo "  cd \"$TARGET_ROOT\""
    echo "  git add $DEST_SUBDIR/$SKILL_NAME"
    echo "  git commit -m 'Add ${SKILL_NAME} skill'"
  fi
fi

echo
echo "In VS Code, open Copilot Chat in agent mode and type / to see the skill,"
echo "or just describe the dashboard you want -- Copilot loads it by description."
