# Change: T3-18 design.md fence

## Change ID

`third-salvo-18-design-md-fence`

## Slot

`T3-18`

## Inclusion

This change is `INCLUDED` for the `Ultra` lane only. It is never eligible for
On-Demand handling.

## Summary

Add a durable OpenSpec design record that makes the lane, execution boundary,
and dependency fence unambiguous for T3-18.

## Scope

- Add the design record and its implementation checklist.
- Keep the change documentation-only.
- Require offline, repository-local validation.

## Non-goals

- No runtime behavior or deployment configuration.
- No network calls, credentials, integrations, or live service access.
- No changes outside this change directory and its receipt.
