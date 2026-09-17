# Change: Reaffirm Willow T3-30 inclusion lock

## Change ID

`third-salvo-30-willow-lock-reaffirm`

## Summary

Record the T3-30 Willow lock as an audit-only invariant: the slot is
`INCLUDED` for `Ultra` and is never available to `On-Demand`.

## Why

The third salvo needs a durable, reviewable record of the slot boundary
without changing Willow implementation content.

## Scope

- Document the T3-30 availability invariant.
- Capture the audit result and verification boundary.
- Keep the change repository-local and documentation-only.

## Non-goals

- No edits to any Willow `SKILL.md`.
- No implementation, routing, packaging, or runtime behavior changes.
- No changes to any other slot or availability tier.

## Impact

This change adds OpenSpec documentation and an audit receipt only. It does
not alter the skill tree or any executable surface.
