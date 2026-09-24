# Drive skill-tree versions — look here

Two *kinds* of “skill tree” exist on Drive. Do not collapse them.

- **Filesystem dumps** = zip/tar of `~/.grok/skills` (or liv-hub skill-tree). These are the versions that changed.
- **Vesper matrix dump** = `SKILL_TREE_DUMP_20260904` under from-vesper. Narrative / mode / engine docs. Not the live tree.

REQ is: walk the filesystem dumps, note when they changed, diff skill slugs + SKILL.md intent against tonight’s live list, then propose candidates for the empty smokeshow pad.

## Filesystem dumps (dated)

Prefer the **largest unique hash-class** per date, not every duplicate upload.

| When | Name | Size | File ID | Notes |
|------|------|------|---------|-------|
| 2026-08-17 09:15 | `skill-tree-and-workdir_2026-08-17_0915.zip` | 350 MB | `10eEsm4ZaYZ2FsvbR_oofGoCOyYhmT1Ja` | Early; includes workdir. Heavy. |
| 2026-08-17 09:22 | `skill-tree-and-workdir_2026-08-17_0922.zip` | 28 MB | `16UzLjVFwwKhDq5cunkPoyUTmZC-HpcS9` | Same day, slimmer. Smokeshow birth day. |
| 2026-08-25 / 26 | `liv-hub-skill-tree_2026-08-25.zip` | ~48 MB | canonical pick: `1b2bdp_X9ZkD6Q9N6OQpyEC3vXcZElgEK` | **Version A.** cilia-bus promote window. Duplicates exist (`(1)`, `(2)`, other IDs same size). |
| 2026-08-26 03:25 | `skill-tree-inventory_session-end_2026-08-26.tar.gz` | 731 B | `1Eont8D7YDuzvpDjERaFYj-rYNA1xSgs0` | Inventory only. |
| 2026-08-26 08:45 | `skill-tree_session-end_2026-08-26.tar.gz` | 57 MB | `1UB0GpoFAKcJg3Qxpst2UwZhuXFkhTFIJ` | Mid A→B. |
| 2026-08-26 08:45 | `skill-tree-inventory_session-end_2026-08-26.tar.gz` | 1328 B | `11xMdV2wwMI3c2HhXuxonH_4iO1NMB4q5` | Inventory sibling. |
| 2026-08-29 22:45 | `skill-tree-inventory_session-end_2026-08-29.tar.gz` | 1316 B | `1jncm2SZPnFbVUyz1zuAegIV02V794Rlm` | Inventory. |
| 2026-08-29 22:45 | `smokeshow_wrap-surface_v2026.08.29_2026-08-29.tar.gz` | 1786 B | `1kxhA6MVHz2Qhh_B_7BndFeTIhHLmtRIp` | Smokeshow wrap only. |
| 2026-08-29 22:53 | `skill-tree_full_2026-08-29.tar.gz` | 76 MB | `1r6JBLCZeH6tUUb1Dc8AV806Aol3-Xdu4` | **Version B.** Full tree after wrap-surface. |
| 2026-09-11 01:00 | `skill_tree_audit_REPORTS.zip` | 151 KB | `1WOJtl0UragkMy0qVoC-xULGHTBlruJrK` | Reports, not a tree. Read after A/B. |

Duplicate `liv-hub-skill-tree_2026-08-25.zip` IDs (same ~48 MB class — do not unpack all):

- `1b2bdp_X9ZkD6Q9N6OQpyEC3vXcZElgEK`
- `1h5Y5v6p4hwCBhD_YHCbdlLMWLz-9xXMo`
- `1JP76K1oSsl_aHdPUr7k88-Yd5X8HROdc`
- `1FqrT6xq6bYCF0d3EE_ar6JAOfXI_TVcH` (1)
- `1edxPxNFUngNeoPW8DXX4NZk7dL9aSiWi` (2)

## Vesper matrix dump (not a tree)

Folder: `SKILL_TREE_DUMP_20260904`  
ID: `1SeIN64Iaw4OiLrLrbjm8Pq9Oo4vkAlvy`  
Location: `grokbot/from-vesper/`  
Link: https://drive.google.com/drive/folders/1SeIN64Iaw4OiLrLrbjm8Pq9Oo4vkAlvy  

Published in mail `VESPER-20260908-SKILL-TREE-DUMP-RESP-035` answering `OLIVIA-20260904-SKILL-TREE-ASK-034`.

| Artifact | Doc ID |
|----------|--------|
| TREE.md | `1Q8mL7qOtm5sdZjZzwDc_rbKyYvUYdZ5EJrVaxN3Vfqc` |
| REFERENCES_MODES_AND_PLAYLISTS.md | `1nayl3HD-cG0Vgi9scYFqzulUXhChD_AzZmaMSB6JP1I` |
| PUBLISHER_FREEZE_ANALYSIS.md | `1D1YUeXJiDQaRejub12slC52d_MjvvGU6HIngBB0wa4c` |
| SCHEMA_VESPER_REMEDIATION_DB.md | `1CTfTICy7qvtILSwkLKsZk24ie8gLU8S0XD5AA9O5Fps` |
| vesper-engine.md | `1YmauGlxmskhmocTOLzITKRqWqrN-vC1yzE-Gxb3rlPc` |
| vesper-systems-engineer.md | `1vu1kkJ2Sr7SArYOzkrjNSDOuLByixCdollHU3dU_PqQ` |
| valerie-engine.md | `1jue8OynAydPhNJvWPpoJEG6MMiso3Hlt2-vVWP6p0_0` |
| vesper-modes.md | `1qsFthI3_Ec4MazTj8juqHAB-lkVxIzPNKjvzjeD-n44` |
| permission-loop-guard.md | `1bYg6GZQj7FuSVCp3tUd3MflEBeiSSMDBy5AyE0WDS0A` |

Use this dump to see how *Vesper named* surfaces and modes on 2026-09-04/08. Do not treat it as the Aug 25 or Aug 29 filesystem.

## Conversation-sprint SkillTree folders (Aug 16–17)

Many duplicate folders named `this_conversation_Olivia_*SkillTree*`. Those are usage-sprint conversation packs from 2026-08-14–17, not skill trees. Skip unless a slug is missing from A and B.

## Change window Olivia can already name

| Date | What changed (from this pane + receipts, not a full unpack) |
|------|--------------------------------------------------------------|
| 2026-08-17 | smokeshow created. cilia-bus staged as first candidate. `smokeshow_SKILL.md` lands on Drive. |
| 2026-08-25 | cilia-bus **promoted** to live skill. Promote receipts in from-olivia. |
| 2026-08-26 | session-end tree + liv-hub-skill-tree zips multiply (same bytes, several uploads). |
| 2026-08-29 | wrap-surface + `skill-tree_full_2026-08-29.tar.gz`. Smokeshow wrap tarball is tiny. |
| 2026-09-03 | Agentify locked out of smokeshow candidates (image-pipeline subscale). |
| 2026-09-04 / 08 | Vesper publishes SKILL_TREE_DUMP_20260904. |
| 2026-09-10 | Live sandbox: 25 skills listed in `01_WHAT_SMOKESHOW_IS.md`. candidates = 0. |

Unpack A (Aug 25 zip) vs B (Aug 29 tar). Report slug adds/drops/renames. That delta *is* the candidate shortlist.
