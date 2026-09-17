# S2-32 skill-path inventory

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-32-skill-path-inventory` |
| Slot | `S2-32` |
| Base | `skill-tree-intake` |
| Inclusion profile | **Ultra only**; OD excluded |
| Selected path | [`skill_tree/skills/keep-lake-query/`](../../skill_tree/skills/keep-lake-query/) |
| Inventory boundary | The selected directory and its tracked descendants only |
| Source mode | Repository-local metadata; no external calls |

## Purpose

This document inventories one hydrated skill-tree path without changing its
live entrypoint or any other skill path. The inventory records names, sizes,
and roles only; it does not reproduce source contents, credentials, payloads,
or provider data.

## Path summary

The selected path contains **22 tracked files**:

| Surface | Count | Treatment |
| --- | ---: | --- |
| Live entrypoint | 1 | `SKILL.md` is source-only and unchanged |
| Help and reference material | 18 | Indexed as local documentation/reference files |
| Script | 1 | Indexed as a local executable surface; not run as a provider action |
| Vendored artifacts | 2 | README and one wheel; not installed or upgraded |
| **Total** | **22** | One path only |

The path has no nested `SKILL.md` entrypoint. Its live entrypoint is
[`SKILL.md`](../../skill_tree/skills/keep-lake-query/SKILL.md); it is listed
for completeness but is not copied into this document or modified by S2-32.

## Tracked file inventory

| Relative path | Role | Bytes |
| --- | --- | ---: |
| `HELP.md` | Help/menu reference | 4,681 |
| `SKILL.md` | Live entrypoint; read-only for this change | 8,085 |
| `references/DEBRIEF_PATTERN.md` | Reference template | 5,216 |
| `references/DEPRECATED_SURFACES.md` | Deprecated-reference note; not activated by this inventory | 1,673 |
| `references/LEXICON.md` | Terminology reference | 2,455 |
| `references/NAGS.md` | Standing-nags reference | 3,198 |
| `references/SEARCH_STRATEGY.md` | Search reference | 4,501 |
| `references/SMOKE_OPENER.md` | Smoke-opener reference | 2,908 |
| `references/TREE.md` | Tree-map reference | 6,003 |
| `references/WAR_CHEST.md` | Local/provider-boundary reference | 5,774 |
| `references/ids.md` | Identifier reference | 5,197 |
| `references/planes.md` | Plane reference | 3,523 |
| `references/work-queue/WORK_QUEUE.md` | Work-queue index | 3,887 |
| `references/work-queue/items/KLQ-WQ-001_dated_md_tree_ssot.md` | Work-queue item | 5,542 |
| `references/work-queue/items/KLQ-WQ-006_date_idea_manifest_and_cli.md` | Work-queue item | 6,134 |
| `references/work-queue/items/KLQ-WQ-007_folder_scoped_temporal_cluster.md` | Work-queue item | 7,256 |
| `references/work-queue/items/KLQ-WQ-007_temporal_cluster_multihop.md` | Work-queue item | 6,550 |
| `references/work-queue/items/KLQ-WQ-008_nine_plane_verify.md` | Work-queue item | 1,546 |
| `references/work-queue/items/KLQ-WQ-014_to_025_war_chest.md` | Work-queue item | 2,495 |
| `scripts/lake_date_query.py` | Local executable script | 5,101 |
| `vendor/README.md` | Vendored-artifact note | 796 |
| `vendor/wheels/duckdb-1.5.5-cp312-cp312-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl` | Vendored wheel; not installed | 21,510,909 |

## Boundary notes

- **Ultra only:** this is an included, offline inventory; OD is outside the
  scope and no on-demand/provider work is authorized.
- **No `CONV2_B`:** no such surface is added, indexed, or assumed.
- **Vultr ≠ Cold Steel:** the selected path's provider/compute references
  remain distinct from its local-steel references; this document does not
  alias or reconcile them.
- **No secrets:** no credentials, tokens, private keys, account secrets, or
  unredacted payloads are included.
- **No live mutation:** no `SKILL.md` is modified, and no source file under
  the selected path is rewritten.
- **One slot:** only S2-32 and this single documentation deliverable are
  covered; other S2 slots are not touched.

## Acceptance receipt

- [x] Exactly one skill-tree path is inventoried.
- [x] The tracked file count and byte sizes are recorded from the base tree.
- [x] The live `SKILL.md` is identified as read-only.
- [x] Ultra-only, no-OD, no-`CONV2_B`, Vultr/Cold Steel separation, and
      no-secrets fences are explicit.
- [x] No external service, provider, connector, or installation action is
      required.
