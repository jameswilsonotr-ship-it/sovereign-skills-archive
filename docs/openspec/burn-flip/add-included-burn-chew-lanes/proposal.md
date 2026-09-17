# Proposal: add-included-burn-chew-lanes

## Why

Included Cursor Models sit at approximately 1% with reset Sep 17. Burn Flip
Swarm needs deterministic OpenSpec chew lanes so Hi Cursor agents burn
**included** quota toward approximately 80% via packetized atomic PRs—without
On-Demand spend, vibe, or Willow SKILL touch.

## What Changes

- Add the `burn-chew` capability: included-only lanes, one change-id per agent
  PR, and a hard Non-Goals fence.
- Align with Architect-authored change-ids so CDR Engineer and LT Code Monkey
  can apply while Hi agents chew.

## Capabilities

| Capability | Mode |
| --- | --- |
| `burn-chew` | ADDED |

## Impact

- Hi (`6aae45db`) spawns Cursor agents on sovereign against these lanes.
- Consume included Models only; On-Demand is already OVER and must not climb.
- Feed progress toward cutover arming (approximately 80% or reset).
