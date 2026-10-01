# Proposal: add-t4-06-continuous-included-reload

## Why

The post-T3 Keeper handoff needs a small, repeatable reload contract. The
reload must consume only already-included local state and must leave the
On-Demand path untouched. Keeper needs a map delta, not another copy of the
KEEP lake or a rebuild of historical material.

## What Changes

- Add the `continuous-included-reload` capability for T4-06.
- Define a continuous, offline reload loop over a post-T3 local delta.
- Append a thin Keeper map overlay containing pointers and state, while
  preserving the existing KEEP surface as immutable input.
- Make duplicate deltas idempotent and report missing twins or shards without
  inventing content.
- Record the hard offline and no-provider fences in the contract and receipt.

## Capabilities

| Capability | Mode |
|------------|------|
| `continuous-included-reload` | ADDED |

## Impact

- Keeper receives one append-only post-T3 map delta under its references
  work-queue surface.
- No live skill prompt, historical KEEP body, external service, provider,
  credential, or cloud-host change is required.
- The deliverable is one documentation-only change-id and one receipt.
