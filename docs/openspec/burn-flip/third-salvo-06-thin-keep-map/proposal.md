# Proposal: third-salvo-06-thin-keep-map

## Why

Third Salvo slot `T3-06` needs a small, reviewable post-coherence record of
what remains KEEP and what is outside the lane. The record must preserve the
included Ultra-only burn boundary without turning the slot into an
implementation, provider, or coordination task.

## What Changes

- Add the `thin-keep-map` capability for the reserved change-id
  `third-salvo-06-thin-keep-map`.
- Define a compact KEEP map for the T3-06 packet after coherence review.
- Make INCLUDED Ultra the only permitted execution lane; On-Demand is never a
  fallback or alternate lane.
- Record hard fences for Willow `SKILL.md`, `CONV2_B`, external/provider
  calls, secrets, live Vultr work, and Linear mint.

## Capabilities

| Capability | Mode |
| --- | --- |
| `thin-keep-map` | ADDED |

## Impact

- Adds documentation only.
- Produces one independently reviewable OpenSpec change for one salvo slot.
- Does not alter skills, infrastructure, provider state, credentials, or
  external coordination state.
