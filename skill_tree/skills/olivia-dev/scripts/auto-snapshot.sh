#!/bin/bash
# auto-snapshot.sh — Save Mermaid render or generated image to assets/code_snapshots on trigger
# Usage: ./auto-snapshot.sh <source-path> <context-name>
set -e
SOURCE="$1"
CONTEXT="$2"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DEST="assets/code_snapshots/${CONTEXT}-${TIMESTAMP}.png"

if [[ -f "$SOURCE" ]]; then
  cp "$SOURCE" "$DEST"
  echo "✅ Snapshot saved: $DEST (trigger: $CONTEXT)"
else
  echo "⚠️ Source not found: $SOURCE"
fi
