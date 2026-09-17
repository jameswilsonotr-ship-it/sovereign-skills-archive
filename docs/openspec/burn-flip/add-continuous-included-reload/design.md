# Design: add-continuous-included-reload

## Context

The MIS-6 fixture is already a deterministic, offline harness input. T4-31
needs to land a reload rule without changing that baseline or introducing a
live integration. "Continuous" means that an operator may run successive
local reconciliation cycles; it does not mean polling a network or invoking a
provider.

## Goals

- Reconcile each cycle from the checked-in MIS-6 fixture.
- Preserve the MIS-6 land delta byte-for-byte.
- Emit a redacted, local receipt for every completed cycle.
- Fail closed when included capacity is unavailable rather than selecting
  On-Demand.

## Non-Goals

- No `SKILL.md` or skill-tree live-lock edits.
- No `CONV2_B` material.
- No external or provider calls, secrets, or hosted provisioning.
- No On-Demand use, increase, recommendation, or fallback.
- No browser, network, billing, or remote reload.

## Decisions

1. **Source:** the checked-in MIS-6 offline fixture is the only input.
2. **Cycle:** a reload reads the fixture, validates its identity, and writes
   one receipt; it does not mutate the fixture.
3. **Continuity:** a later cycle starts from the prior local receipt and may
   advance only its local cycle number.
4. **Capacity:** the cycle is `included` or `blocked`; `on_demand` is not a
   valid state.
5. **Receipt:** receipts contain cycle/status/source/check results only. They
   contain no credentials, provider identifiers, or payload copies.

## Failure behavior

| Condition | Result |
| --- | --- |
| MIS-6 fixture is present and unchanged | Complete an `included` cycle |
| Fixture is missing or changed | Write a `blocked` receipt; do not substitute data |
| Included capacity is unavailable | Write a `blocked` receipt; do not use On-Demand |
| Any live I/O is requested | Reject the request before execution |
