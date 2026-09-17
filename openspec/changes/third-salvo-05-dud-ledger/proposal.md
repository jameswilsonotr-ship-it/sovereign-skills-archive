# Change: THIRD_SALVO T3-05 dud ledger

## Reserved change ID

`third-salvo-05-dud-ledger`

## Summary

Add an offline, reviewable ledger for Tube-2 candidates that cannot be
promoted because the evidence or handoff is incomplete. The ledger is seeded
with the known Tube-2 gap classes and is intentionally a template: it records
what is missing without claiming that a provider was queried or that a
candidate is ready for a pull request.

## Slot contract

- Salvo: `THIRD_SALVO`
- Slot: `T3-05`
- Inclusion lane: `Ultra` only
- `On-Demand` is not an allowed lane for this change
- State: included as an offline documentation/fixture artifact

## Scope

### In scope

- OpenSpec proposal, tasks, and requirement for the dud/no-PR ledger.
- A Markdown ledger template under this change directory.
- Seed rows for the known Tube-2 evidence and handoff gaps.
- Explicit no-PR and no-provider-call states.

### Out of scope

- Provider, host, or live Tube-2 lookups.
- Candidate promotion, ranking, or recommendation.
- Creating, editing, or linking a pull request from a ledger row.
- Changes to runtime skills or unrelated conversation artifacts.

## Acceptance criteria

1. The change uses the reserved ID exactly.
2. Every seeded row remains `Ultra` and `included`; no row uses an
   `On-Demand` state.
3. Each seeded row is marked as a dud/no-PR record until a human supplies
   reviewable evidence.
4. The ledger can be filled in offline without secrets or external calls.
5. The PR description contains one concise, reviewable receipt for this
   atomic change.
