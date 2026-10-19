# T3-28 dependency inventory delta

| Field | Value |
|---|---|
| Change ID | `third-salvo-28-dep-inventory-delta` |
| Salvo slot | `T3-28` |
| Included tier | `Ultra` |
| On-Demand | `excluded` |
| Delta kind | documentation-only |
| Install performed | `no` |

## Baseline evidence

| Source | UTC timestamp | Count / fact |
|---|---:|---|
| Latest local skill-orchestrator export | 2026-09-16 20:21 | 27 scanned; 27 unassigned |
| Historical local library inventory | 2026-07-19 14:16 | 32 ledger entries |

The 27-scan export is the current observation. The 32-entry ledger is a
historical comparison point and is not modified by this change.

## Delta

| Bucket | Added | Removed | Reclassified |
|---|---:|---:|---:|
| Inventory artifacts | 1 OpenSpec change | 0 | 0 |
| Runtime dependencies | 0 | 0 | 0 |
| Build dependencies | 0 | 0 | 0 |
| Provider dependencies | 0 | 0 | 0 |
| Secret inputs | 0 | 0 | 0 |
| On-Demand dependencies | 0 | 0 | 0 |

## Included artifact

The one added artifact is the OpenSpec change documentation under
`openspec/changes/third-salvo-28-dep-inventory-delta/`. It is included in
Ultra only. There is no On-Demand counterpart, loader, fallback, or deferred
resolution path.

## Fence result

| Fence | Result |
|---|---|
| Willow `SKILL.md` | absent |
| `CONV2_B` | absent |
| External/provider input | absent |
| Secret material | absent |
| Vultr integration | absent |
| Linear integration | absent |

No package manager, dependency resolver, network data source, or installation
step was used.
