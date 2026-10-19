---
id: cli-export
title: CLI export command
status: accepted
owner: developer-experience
priority: medium
summary: Provide a machine-readable export command for local project data.
tags: [cli, export]
dependencies: [config-loader, filesystem]
---

# CLI export command

## Requirements

1. The command writes CSV output to stdout by default.
2. The command accepts an explicit output path.
3. Existing files are never overwritten without `--force`.

## Acceptance

- [x] Default output is valid CSV.
- [x] An explicit output path is supported.
- [ ] `--force` is required before replacement.
