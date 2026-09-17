# First-wave status delta

This is a point-in-time record for the second-salvo status-board change
identified as `second-salvo-07-status-delta`.

| Field | Value |
| --- | --- |
| Slot | `S2-07` |
| Snapshot | `2026-09-17T04:39:35Z` |
| Baseline branch | `skill-tree-intake` |
| Baseline revision | `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4` |
| Change type | Included-burn status delta |

## Delta

The first-wave board is narrowed for this slot to the following explicit
disposition. This document is a snapshot, not a live status feed.

| Board item | S2-07 disposition | Delta rule |
| --- | --- | --- |
| Ultra | **Included** | The only included S2-07 item. |
| OD | **Excluded** | No OD content is included in this burn. |
| Willow `SKILL.md` | **Excluded** | The Willow skill file is outside this slot. |
| `CONV2_B` | **Excluded** | This corpus/item is outside this slot. |
| Vultr | **Tracked separately** | Vultr is not Cold Steel; no status is transferred between them. |
| Other S2 slots | **Unchanged / out of scope** | This delta records S2-07 only. |

## Accounting

- Included set: `Ultra` only.
- Explicitly excluded: `OD`, Willow `SKILL.md`, and `CONV2_B`.
- No equivalence or merge is recorded between Vultr and Cold Steel.
- No other S2 slot is added, removed, or reclassified by this document.

## Receipt

- Change ID: `second-salvo-07-status-delta`
- Slot: `S2-07`
- File written: `docs/burn-wave/FIRST_WAVE_STATUS_DELTA.md`
- Source revision: `cf7afbe782b7cc790aa3683c8d4268aa4ed29ba4`
- External calls: none
- Secrets: none
