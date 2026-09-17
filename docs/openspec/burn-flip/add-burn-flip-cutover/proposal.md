# Proposal: add-burn-flip-cutover

## Why

When included burn hits ~80% or billing reset occurs, the swarm must flip active coding from Cursor Ultra burn-chew to the Vultr headless gateway and freeze further included-burn assignment. Needs an explicit playbook depending on slices 1-5.

## What Changes

- Add `burn-flip-cutover` capability: flip triggers, dependency checks on change-ids 1-5, post-flip freeze of included burn.
- Live gateway cut requires Bunny YES (Olette asks).

## Capabilities

| Capability | Mode |
|------------|------|
| `burn-flip-cutover` | ADDED |

## Impact

- Terminates Ultra included burn-chew purpose after flip.
- Activates Vultr gateway as coding locus (paper/stub from slice 3).
- Meter-watch continues observability; does not auto-spend.
