# T4-12 — Mag LAND keeper receipt index

## Receipt

| Field | Value |
|---|---|
| Ticket | `T4-12` |
| Desk | Mag LAND |
| Keeper mode | `CONTINUOUS_INCLUDED` |
| Reload behavior | Included on every reload |
| On-Demand behavior | Forbidden |
| PR title | `salvo: T4-12 mag-land-receipt-index` |
| Capture date | `2026-09-17` |
| Processing mode | Offline only |

## Included record

This receipt/index is the keeper record for the Mag LAND desk. The desk is part
of the continuously included reload set; it must not be represented as an
On-Demand or opt-in item.

No payload bytes are asserted by this receipt. It records the reload contract
and the admissible scope for the desk only.

## Fences

The following are excluded from this record and from any reload represented by
it:

- `Willow SKILL.md`
- `CONV2_B`
- external/provider material
- secrets
- Vultr
- OD / On-Demand behavior

No external or provider operation, secret lookup, or Vultr operation is
required to validate this receipt. The record is intentionally local and
offline.

## Keeper checks

- [x] T4-12 is identified as the Mag LAND desk receipt/index.
- [x] Reload mode is explicitly `CONTINUOUS_INCLUDED`.
- [x] Included status applies on every reload.
- [x] On-Demand is explicitly forbidden.
- [x] The named fences are recorded as exclusions.
- [x] No payload, provider, secret, or external dependency is introduced.
