# Proposal: add-t4-08-continuous-included-reload

## Why

T4-08 needs a deterministic reload lane that continuously uses the included
budget. A reload that falls back to On-Demand would violate the burn order and
make the lane unsafe to run.

## What Changes

- Add the `continuous-included-reload` capability for T4-08.
- Require reload work to remain continuous and included-only.
- Reject On-Demand fallback, provider calls, secret material, and live
  infrastructure actions.
- Require one atomic, receipt-backed change-id per reviewable PR.

## Capabilities

| Capability | Mode |
| --- | --- |
| `continuous-included-reload` | ADDED |

## Impact

- T4-08 can be reloaded repeatedly through the local offline harness.
- The lane cannot silently switch to On-Demand when included capacity is
  unavailable.
- This change adds contract and guard documentation only; it does not touch
  live skill files or external systems.
