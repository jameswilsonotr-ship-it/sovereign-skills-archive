# T4-22 — mag SSOT snapshot stub

This is an offline schema stub. It does not claim to observe live magazine
state.

## Reload contract

- `reload`: `CONTINUOUS_INCLUDED`
- `on_demand`: `FORBIDDEN`
- The reload path is part of the continuously included surface; it is not an
  optional or deferred path.

## Snapshot

```json
{
  "task": "T4-22",
  "reload": "CONTINUOUS_INCLUDED",
  "on_demand": "FORBIDDEN",
  "spent": null,
  "wet": null,
  "fired": null
}
```

`null` means that this stub has no observed value. It must not be interpreted
as `false`, zero, or a cleared state.

## Field contract

| Field | Stub type | Meaning |
|---|---|---|
| `spent` | `boolean \| null` | Whether the magazine is marked spent |
| `wet` | `boolean \| null` | Whether the magazine is marked wet |
| `fired` | `boolean \| null` | Whether the magazine is marked fired |

This document is the single snapshot shape for T4-22. Any future populated
snapshot must preserve these keys and the `CONTINUOUS_INCLUDED` reload
contract.
