# Change: third-salvo-23-offline-test-harness

## Slot

- Salvo: THIRD_SALVO
- Slot: T3-23
- Availability: Included
- Tier: Ultra
- Change ID: `third-salvo-23-offline-test-harness`

## Why

T3-23 needs a deeper test seam before any real implementation is attached. A
fixture-backed harness makes request/response behavior testable in a clean
checkout while preserving a strict boundary around this slot.

## Scope

This change adds:

1. A small OpenSpec change record.
2. A standard-library-only harness stub.
3. Deterministic fixture lookup, request recording, response assertions, and
   JSON-friendly results.
4. Unit tests covering the happy path, stable fixture keys, missing fixtures,
   and slot-policy rejection.
5. A local receipt with the verification commands and outcomes.

## Non-goals

- No live transport or service adapter.
- No credentials, environment reads, or runtime configuration discovery.
- No fallback path that broadens access beyond Included Ultra.
- No changes to unrelated skills, packages, or deployment workflows.

## Acceptance criteria

- [ ] The harness defaults to slot T3-23, Included, Ultra.
- [ ] A policy outside that exact scope is rejected at construction.
- [ ] Cases resolve only against explicitly registered fixtures.
- [ ] Missing fixtures produce a failed result rather than a fallback attempt.
- [ ] Tests run with the Python standard library only.
- [ ] The receipt records a passing offline test command.
