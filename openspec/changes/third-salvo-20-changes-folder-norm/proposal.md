# Change: Changes-folder naming norm

- Change ID: `third-salvo-20-changes-folder-norm`
- Slot: `T3-20`
- Availability: Included Ultra only
- Delivery mode: never On-Demand

## Why

OpenSpec changes need a predictable path so that tooling and reviewers can
resolve a change ID without aliases, spelling variants, or directory nesting.
The repository currently has no written contract for the names and shape of
directories under `openspec/changes/`.

## What changes

- Establish lowercase kebab-case as the canonical naming convention for
  change directories.
- Require the directory name to match the `Change ID` in `proposal.md`.
- Document the required change directory shape and capability-directory
  convention.
- Add this change as the first example using the convention.

## Scope

This change covers repository organization and OpenSpec authoring conventions.
It does not rename existing content or add validation tooling.

## Compatibility

The convention is additive. Existing repository content outside
`openspec/changes/` is unaffected.
