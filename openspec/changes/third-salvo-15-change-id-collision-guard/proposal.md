# Change: T3-15 change-id collision guard

- **Change ID:** `third-salvo-15-change-id-collision-guard`
- **Salvo:** `THIRD_SALVO`
- **Slot:** `T3-15`
- **Inclusion:** `Ultra`
- **Availability:** Included only; never On-Demand

## Why

Reserved OpenSpec change IDs need a deterministic, reviewable collision check
before a change is accepted. Without one, a second change can reuse the same
ID (including a case-only variant) and make paths, review comments, and
receipts ambiguous.

## Scope

This change defines an offline contract and fixture for checking reserved
change IDs. It does not add a runtime implementation, call a provider, mint
coordination records, or alter any skill implementation.

## Acceptance criteria

1. A candidate ID is compared with reserved IDs after ASCII whitespace trimming
   and ASCII lower-casing.
2. An exact or case-only duplicate of a reserved ID is rejected as a collision.
3. A candidate with a distinct canonical ID is accepted by the collision
   check.
4. A request that marks this change as On-Demand is rejected; this change is
   Included Ultra only.
5. The fixture records expected outcomes for both collision and non-collision
   cases without network access or secrets.
