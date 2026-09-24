#!/usr/bin/env bash

# Show the command used to inspect the repository's open pull requests.
set -euo pipefail

readonly GH_COMMAND=(gh pr list --limit 30)

echo "To list up to 30 open pull requests, run: ${GH_COMMAND[*]}"

if command -v gh >/dev/null 2>&1; then
  "${GH_COMMAND[@]}"
else
  echo "GitHub CLI (gh) is not installed; showing the command only."
fi
