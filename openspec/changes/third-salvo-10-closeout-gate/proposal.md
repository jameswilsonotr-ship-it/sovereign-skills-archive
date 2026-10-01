# Change: THIRD_SALVO T3-10 closeout gate

## Change ID

`third-salvo-10-closeout-gate`

## Slot

`T3-10`

## Scope

Define the closeout gate for the THIRD_SALVO slot when the slot is
`INCLUDED` for `Ultra`.

This is a contract and documentation change only. It does not add a
runtime, provider integration, live infrastructure action, secret, or
Linear artifact.

## Non-negotiable inclusion rule

T3-10 is `INCLUDED Ultra ONLY`.

- An `Ultra` inclusion may satisfy this closeout gate.
- An `On-Demand` request never satisfies this closeout gate.
- `On-Demand` must not be silently promoted, counted, or treated as an
  alternate path to closeout.

## Problem

Closeout evidence can be confused with capacity or activity meters. That
confusion creates a dangerous implicit behavior: a meter crossing a
threshold can be read as permission to spawn work. T3-10 needs a small,
auditable gate that separates evidence collection from execution authority.

## Outcome

The change establishes a checklist that:

1. verifies the slot and inclusion lane;
2. records evidence and meter observations;
3. explicitly proves that meters do not spawn, authorize, or schedule work;
4. rejects `On-Demand` and any live/provider-dependent evidence; and
5. records a human-readable closeout receipt.

## Out of scope

- Editing any `Willow SKILL.md`.
- Any `CONV2_B` work or reference.
- Provider, external service, or network calls.
- Secret creation, reading, or storage.
- Vultr live operations.
- Linear issue creation or other Linear minting.
- Implementing spawn, scheduling, autoscaling, or meter-triggered execution.

## Acceptance criteria

- The change is stored under the reserved change ID.
- The closeout checklist labels the lane as `INCLUDED Ultra ONLY`.
- The checklist has an explicit `meters ≠ spawn` gate.
- The checklist rejects `On-Demand` as non-qualifying.
- The package contains no runtime or provider operation.
- A receipt identifies the files, fences, and offline verification result.
