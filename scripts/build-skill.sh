#!/usr/bin/env bash
# Package this repo for upload in Claude desktop (Settings > Customize).
#   scripts/build-skill.sh [skill-name]   skill zip, default authoring-docs (Skills > Add)
#   scripts/build-skill.sh --plugin       dist/<plugin-name>.plugin, skill + agent + manifest
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$repo_root/dist"

# macOS and Python cache files that should not ship.
excludes=(-x "*.DS_Store" "*__pycache__*" "*.pyc")

if [ "${1:-}" = "--plugin" ]; then
  # First "name" in the manifest is the plugin's; the author's comes later.
  name="$(grep -m1 '"name"' "$repo_root/.claude-plugin/plugin.json" | sed 's/.*: *"\(.*\)".*/\1/')"
  out="$repo_root/dist/$name.plugin"
  # zip updates an existing archive in place, which would keep files deleted since the last build.
  rm -f "$out"

  # Only the plugin's components, with .claude-plugin/plugin.json at the archive root.
  # marketplace.json is repo-level catalogue metadata, not part of the plugin.
  cd "$repo_root"
  zip -rq "$out" .claude-plugin agents skills "${excludes[@]}" "*/marketplace.json"
else
  skill="${1:-authoring-docs}"
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
  rm -f "$out"

  # Zip from skills/ so the skill folder, not skills/, is the archive root.
  cd "$repo_root/skills"
  zip -rq "$out" "$skill" "${excludes[@]}"
fi

echo "built $out"
unzip -l "$out" | tail -1
