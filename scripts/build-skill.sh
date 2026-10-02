#!/usr/bin/env bash
# Package a skill as a zip for upload in Claude desktop (Settings > Capabilities > Skills).
# Usage: scripts/build-skill.sh [skill-name]   (default: authoring-docs)
set -euo pipefail

skill="${1:-authoring-docs}"
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
out="$repo_root/dist/$skill.zip"

if [ ! -f "$repo_root/skills/$skill/SKILL.md" ]; then
  echo "error: skills/$skill/SKILL.md not found" >&2
  exit 1
fi

# The upload rejects a skill whose folder name differs from its `name:` field.
declared="$(sed -n 's/^name: *//p' "$repo_root/skills/$skill/SKILL.md" | head -1)"
if [ "$declared" != "$skill" ]; then
  echo "error: SKILL.md declares name '$declared' but folder is '$skill'" >&2
  exit 1
fi

mkdir -p "$repo_root/dist"
# zip updates an existing archive in place, which would keep files deleted since the last build.
rm -f "$out"

# Zip from skills/ so the skill folder, not skills/, is the archive root.
# Exclude macOS and Python cache files that should not ship.
cd "$repo_root/skills"
zip -rq "$out" "$skill" -x "*.DS_Store" "*__pycache__*" "*.pyc"

echo "built $out"
unzip -l "$out" | tail -1
