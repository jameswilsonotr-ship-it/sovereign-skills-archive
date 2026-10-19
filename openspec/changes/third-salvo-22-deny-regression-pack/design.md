# Design

## Decision contract

The pack evaluates a request shaped like:

```json
{
  "slot": "T3-22",
  "entitlement": "INCLUDED",
  "tier": "Ultra"
}
```

The evaluator uses exact string matching. It does not normalize casing,
coerce values, infer missing fields, or consult another source of truth.

| Slot | Entitlement | Tier | Decision |
| --- | --- | --- | --- |
| `T3-22` | `INCLUDED` | `Ultra` | `ALLOW` |
| `T3-22` | `INCLUDED` | anything else | `DENY` |
| `T3-22` | `ON_DEMAND` | `Ultra` or anything else | `DENY` |
| missing or malformed | any | any | `DENY` |

## Denial behavior

The result always contains:

- `decision`: `ALLOW` or `DENY`
- `slot`: `T3-22`
- `reason_codes`: a deterministic, sorted list
- `fallback`: `null`

`ON_DEMAND` receives `ON_DEMAND_NOT_ALLOWED`, independently of its tier.
Non-`Ultra` values receive `TIER_NOT_ULTRA`. Missing or non-`INCLUDED`
entitlements receive `ENTITLEMENT_NOT_INCLUDED`. Invalid requests also
receive `INVALID_REQUEST`.

The evaluator is a pure function over in-memory data. The pack deliberately
contains no network, filesystem, subprocess, credential, or environment
lookups in the decision path.

## Compatibility

The JSON cases are a contract fixture, not an application configuration
source. A runtime integration may map its own request type into this contract,
but it must preserve the exact allow/deny outcomes and terminal denial
behavior.
