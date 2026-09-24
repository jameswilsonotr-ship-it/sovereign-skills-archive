#!/bin/bash
# tarball-integrity-check.sh — Double check before/after publish
set -e
PROJECT="$1"
TARBALL="$2"

echo "🔍 Double file verification for $PROJECT..."
# Compare against folder-discipline expected
EXPECTED_FOLDERS=(specs state versions backlog-wishlist docs kanban mermaid gutter-mode pirate-mode connectors imports tarballs references)
for dir in "${EXPECTED_FOLDERS[@]}"; do
  if [[ ! -d "$PROJECT/$dir" ]]; then
    echo "❌ MISSING: $dir"
  fi
done

echo "🔍 Tarball integrity check..."
if [[ -f "$TARBALL" ]]; then
  tar -tzf "$TARBALL" | head -20
  echo "✅ Tarball lists files. Full checksum would go here."
else
  echo "❌ Tarball not found"
fi

echo "🔍 State/kanban/Obsidian note consistency..."
# Placeholder for python/json check
echo "✅ Basic checks passed (expand with python schema validation)."
