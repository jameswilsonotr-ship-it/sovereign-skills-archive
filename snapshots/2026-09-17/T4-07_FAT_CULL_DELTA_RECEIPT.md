# Receipt — T4-07 fat-cull reject-list delta

- **Change ID:** `fourth-salvo-07-fat-cull-delta`
- **Salvo slot:** `T4-07`
- **Status:** `documented`
- **Reload:** `CONTINUOUS`
- **Lane:** `INCLUDED`
- **On-Demand:** `NEVER`
- **Execution:** offline-only

## Recorded delta

T4-07 preserves the fat-cull reject list across every continuous included
reload. The following classes are rejected from cull consideration:

| Reject class | State |
|---|---|
| Willow `SKILL.md` and skill-tree live locks | `reject` |
| `CONV2_B` | `reject` |
| Unproven runtime or build inputs | `reject` |
| External/provider, secret, credential, or Vultr material | `reject` |

This receipt does not claim that any payload was culled. It authorizes no
delete, move, archive, regeneration, packaging, or tier change.

## Verification

- [x] T4-07 is continuously included on reload.
- [x] On-Demand is forbidden and no On-Demand receipt is emitted.
- [x] The reject classes are recorded in the OpenSpec and this receipt.
- [x] Documentation-only files were added.
- [x] No runtime, provider, secret, credential, or hosted-compute operation
  was performed.
- [x] No Willow `SKILL.md`, skill-tree lock, or `CONV2_B` material was edited
  or processed.

## Paths

- `openspec/changes/fourth-salvo-07-fat-cull-delta/`
- `snapshots/2026-09-17/T4-07_FAT_CULL_DELTA_RECEIPT.md`
