# Change Proposal: T3-25 Evidence Bundle Template

- **Change ID:** `third-salvo-25-evidence-bundle-template`
- **Salvo:** `THIRD_SALVO`
- **Slot:** `T3-25`
- **Inclusion:** `INCLUDED`
- **Tier:** `Ultra`
- **Status:** Proposed

## Summary

Add a copy-ready evidence-bundle template for slot T3-25. The template
standardizes identity, local artifact records, integrity checks, and reviewer
sign-off while keeping the delivery path explicitly included and Ultra-only.

## Scope

- Add one OpenSpec change for the T3-25 evidence-bundle contract.
- Add a Markdown template that can be copied for each evidence bundle.
- Add a local receipt documenting the delivered change and validation.

## Non-goals

- No runtime, automation, service, or dependency changes.
- No collection from networked systems.
- No handling or storage of credentials or other sensitive values.
- No changes to unrelated slots or delivery modes.

## Acceptance criteria

1. The change ID is used consistently in the OpenSpec files and receipt.
2. The template identifies `THIRD_SALVO` / `T3-25` and fixes the inclusion
   tier to `INCLUDED` / `Ultra`.
3. The template records `on_demand: false` and defines any On-Demand value as
   invalid.
4. Evidence entries are local, traceable, hashable, and reviewable without
   requiring network access.
5. The receipt and OpenSpec content pass whitespace and fence checks.
