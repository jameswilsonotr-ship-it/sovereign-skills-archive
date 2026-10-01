---
change-id: third-salvo-04-dup-slot-audit
title: "THIRD_SALVO T3-04 duplicate-slot audit"
status: proposed
scope: docs-only
---

# THIRD_SALVO T3-04 — duplicate-slot audit

## Intent

Record an evidence-bounded audit of duplicate or circular Tube-2 slots against
the Mag board. This change is documentation only; it does not alter runtime
behavior, slot definitions, skills, or provider configuration.

## Hard scope

- **Included:** Ultra only.
- **Excluded:** On-Demand, `CONV2_B`, and every non-Ultra tier.
- **Change surface:** this OpenSpec change and its audit document only.
- **Evidence rule:** do not invent a duplicate, circularity finding, slot
  owner, or Mag-board counterpart when the authoritative source is absent.
- **Forbidden:** edits to any `Willow SKILL.md`, network/provider calls,
  secrets, live Vultr actions, and Linear minting.

## Deliverables

1. This reserved OpenSpec change.
2. `audit.md`, containing the T3-04 scope gate, source inventory, comparison
   matrix, and explicit unresolved status where source evidence is unavailable.

## Acceptance criteria

- The change-id is exactly `third-salvo-04-dup-slot-audit`.
- The audit names T3-04 and states **Included Ultra ONLY — never On-Demand**.
- Tube-2 and Mag-board comparison status is recorded without unsupported
  claims.
- No skill file or implementation artifact is modified.
