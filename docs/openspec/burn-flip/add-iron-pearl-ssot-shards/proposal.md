# Proposal: add-iron-pearl-ssot-shards

## Why

Burn Flip / Iron Pearl BASIC needs a durable Awesome Split / HANDOFF single
source of truth (SSoT) with eight owned shard slots and delta compare-and-swap
(CAS), so handoffs remain coherent across Hi agents, Engineer, and gateway
cutover without relying on Google Docs.

## What Changes

- Add the `iron-pearl-ssot` capability.
- Declare the repository SSoT roots:
  - `docs/iron-pearl/ssot/awesome-split/`
  - `docs/iron-pearl/ssot/handoff/`
- Define exactly eight shard slots and an ownership label for every slot.
- Require `base_version` and `next_version` on every delta write.
- Reject stale writes and require retry from the current SSoT head.
- Explicitly refuse Google Docs as the SSoT, handoff medium, or shard store.

## Capabilities

| Capability | Mode |
|------------|------|
| `iron-pearl-ssot` | ADDED |

## Impact

- Provides durable handoff state for chew lanes and cutover.
- Coordinates with the Tailscale/gateway world without becoming Steel- or
  Docs-based.
- This change adds OpenSpec documentation only. It does not edit or add any
  `SKILL.md` file and contains no credentials or other secrets.
