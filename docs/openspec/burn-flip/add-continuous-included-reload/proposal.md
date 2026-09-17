# Proposal: add-continuous-included-reload

## Why

T4-31 needs a repeatable reload contract for the MIS-6 offline work already
landed on `skill-tree-intake`. The reload must continue using included
capacity only. It must never fall back to On-Demand or perform a live
provider operation.

## What Changes

- Define a continuous, local-only reload cycle.
- Keep the existing MIS-6 fixture and its land delta as the reload baseline.
- Require one secret-free receipt per completed cycle.
- Make the included-only and no-live-I/O fences executable through offline
  acceptance scenarios.

## Capabilities

| Capability | Mode |
| --- | --- |
| `continuous-included-reload` | ADDED |

## Impact

- T4-31 owns the reload contract and receipt format.
- MIS-6 remains the preserved offline baseline; this change does not replace
  or rewrite its fixture data.
- The change is documentation-only and does not add a connector, provider
  client, secret, or live runtime.
