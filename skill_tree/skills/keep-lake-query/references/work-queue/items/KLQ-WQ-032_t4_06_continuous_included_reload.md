# KLQ-WQ-032 — T4-06 continuous included reload

Status: COMPLETE
Change-id: `add-t4-06-continuous-included-reload`
Mode: `CONTINUOUS_INCLUDED`
Lineage: post-T3 Keeper thin-map delta

## Thin map delta

This item records the map overlay only. It is not a copy of the KEEP lake
and it does not change the Keeper recipe.

| Field | Value |
|---|---|
| `delta_id` | `t4-06-post-t3-keeper-thin-map` |
| `source_ref` | `local://post-t3-delta` |
| `map_key` | `keeper/t4-06/continuous-included-reload` |
| `status` | `included-only` |
| `disposition` | `append-overlay; idempotent` |
| `recorded_at` | `2026-09-17T09:41:00Z` |

## Reload rule

Each local review cycle may append this pointer once. A repeated
`delta_id` returns `SKIP_EXISTING`. A missing local input returns `NO_TWIN`;
an input with no resolvable `map_key` returns `NO_SHARD`. Neither outcome
authorizes inference or an outside lookup.

The dated tree, DELTA, KEEP, and receipt surfaces remain separate. Historical
KEEP content is pointer-only and is never slurped, copied, or rebuilt by this
delta.

## Fences

- Offline repository-local review only.
- No `SKILL.md` or Willow live-lock write.
- No `CONV2_B` unpack.
- No external/provider/secret access.
- No Vultr work.
- On-Demand is forbidden, including fallback or spend mutation.

See the change contract under
`docs/openspec/burn-flip/add-t4-06-continuous-included-reload/`.
