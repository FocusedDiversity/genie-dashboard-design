#!/usr/bin/env bash
#
# Vendor the genie-dashboard-design skill into a target repository, so the whole
# team gets it on clone -- no marketplace, no per-person install.
#
# GitHub Copilot (VS Code) scans .github/skills/, .claude/skills/ and
# .agents/skills/ for workspace skills. Claude Code scans .claude/skills/.
# So .github/skills/ is the Copilot-native choice, and .claude/skills/ is the
# one location both tools read -- pick with --dir.
#
# Usage:
#   scripts/install-skill.sh <target-repo> [--dir .github/skills]
#
# Examples:
#   scripts/install-skill.sh ~/work/client-analytics
#   scripts/install-skill.sh ~/work/client-analytics --dir .claude/skills
#
set -euo pipefail

SKILL_NAME="genie-dashboard-design"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/skills/${SKILL_NAME}"
TARGET_REPO="${1:-}"
DEST_SUBDIR=".github/skills"

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir) DEST_SUBDIR="${2:-}"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$TARGET_REPO" ]]; then
  echo "Usage: scripts/install-skill.sh <target-repo> [--dir .github/skills]" >&2
  exit 1
fi

if [[ ! -d "$TARGET_REPO" ]]; then
  echo "Target repo does not exist: $TARGET_REPO" >&2
  exit 1
fi

if [[ ! -f "$SOURCE_DIR/SKILL.md" ]]; then
  echo "Cannot find the skill at $SOURCE_DIR -- run this from a clone of the plugin repo." >&2
  exit 1
fi

if [[ ! -d "$TARGET_REPO/.git" ]]; then
  echo "Warning: $TARGET_REPO is not a git repository; the skill will be copied but not shared with anyone." >&2
fi

DEST="$TARGET_REPO/$DEST_SUBDIR/$SKILL_NAME"
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
mkdir -p "$DEST"

# Copy the skill, minus Python bytecode caches.
( cd "$SOURCE_DIR" && tar --exclude='__pycache__' --exclude='*.pyc' -cf - . ) | ( cd "$DEST" && tar -xf - )

echo "Installed ${SKILL_NAME} -> ${DEST_SUBDIR}/${SKILL_NAME}"
echo "  $(find "$DEST" -type f | wc -l | tr -d ' ') files"
echo
echo "Next:"
echo "  cd \"$TARGET_REPO\""
echo "  git add $DEST_SUBDIR/$SKILL_NAME && git commit -m 'Add genie-dashboard-design skill'"
echo
echo "Then in VS Code, open Copilot Chat and type / to see the skill, or just describe"
echo "the dashboard you want -- Copilot loads it by matching the description."
