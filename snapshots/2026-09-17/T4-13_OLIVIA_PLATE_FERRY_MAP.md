# T4-13 — Olivia plate ferry map stub

Status: documentation stub
Owner: Olivia
Mode: `CONTINUOUS_INCLUDED`
Reload: included continuously; **never On-Demand**

## Purpose

Describe the local handoff shape for an Olivia plate without claiming that a
source plate has been fetched, hydrated, or deployed. This file is the
contract for a later implementation, not an implementation itself.

## Ferry map

```text
Olivia plate
    |
    v
local documentation stub
    |
    v
continuous included reload lane
    |
    v
included consumer state
```

| Stage | Input | Output | Allowed behavior |
|---|---|---|---|
| Plate | Olivia plate reference | Stable local label | Record only; do not resolve a live source |
| Ferry | Stable local label | Stub handoff record | Keep the handoff deterministic and offline |
| Reload | Stub handoff record | Included consumer state | Reload continuously as part of the included lane |
| Consumer | Included consumer state | Documentation-visible state | Read the documented state; no runtime side effects |

## Contract

- `reload_policy` is `continuous-included`.
- The reload lane is included by default and has no user-invoked alternate
  path.
- There is no On-Demand transition, queue, or fallback in this map.
- The source of truth for this stub is the checked-in documentation only.
- The stub performs no reads or writes against live Drive and requires no
  network, credentials, dependencies, or service configuration.
- This change does not add runtime code, a skill file, provider integration,
  infrastructure configuration, or secrets.

## Non-goals

- Fetching or mirroring a plate.
- Defining a live ferry protocol.
- Selecting a provider or deployment target.
- Resolving consumer behavior beyond the included reload contract.

## Acceptance checks

1. A reviewer can identify Olivia as the plate owner.
2. A reviewer can identify `CONTINUOUS_INCLUDED` as the only reload mode.
3. The map contains no On-Demand route.
4. The artifact remains useful with network access disabled.
