# RECEIPT — Awesome Split extras intake (MIS-10)

Claim: Liv HUB
UTC: 2026-09-17T01:20:00Z
Ticket: MIS-10
Branch: skill-tree-intake (this PR)
Drive: https://drive.google.com/drive/folders/11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP
id: `11WEijQl3lP6Spw3kwFpE1kNC7MVGWsgP`

Ledger-only intake. Tarball bytes stay on Drive. CONV2_B 80MB split parts were **not** concatenated and were **not** unpacked into `skill_tree/`.

## What was scanned

Pane folders 1–11 plus overflow panes in Awesome Split. Diff source = Drive `FILE_MANIFEST.csv` / README / SESSION_BOOT + the ledger table, not a second 400 MB unpack.

Conversation 1 already holds the full skill surface (`SKILL_SURFACE_FULL_20260916.tar.gz`, ~188 MB). That tree is already on this branch from MIS-5.

## Live-path extras (`SKILL.md` / `WORK_QUEUE.md`)

These are the only extras that map onto `skill_tree/skills/<slug>/...`.

| pane | extra path | dump bytes | intake path | intake bytes | result |
|---|---|---:|---|---:|---|
| Conv 2 (`CONV2_C`, `15SysFFDwwlNlF-N3W-45byZB_grOH5f5`) | `.grok/skills/keep-lake-query/SKILL.md` | 8085 | `skill_tree/skills/keep-lake-query/SKILL.md` | 8085 | **no-op** (already v0.3.3) |
| Conv 2 | `.grok/skills/keep-lake-query/references/work-queue/WORK_QUEUE.md` | 3887 | `skill_tree/skills/keep-lake-query/references/work-queue/WORK_QUEUE.md` | 3887 | **no-op** |

Conv 2 SESSION_BOOT said this pane adds keep-lake-query 0.3.3 files written after the Conv 1 pack. `skill-tree-intake` already has that version (same byte counts). Same path + same bytes = no commit for those files.

Older Conv 2 artifact copies (`keep-lake-query_SKILL.md` 7811 bytes) live inside **CONV2_B**. Left on Drive.

## Artifact-only hits (not merged)

These manifests mention `SKILL.md` / `WORK_QUEUE.md` but are pane artifacts, recon copies, or a different skill family. No live `skill_tree/` path was overwritten.

| pane | hit | why not merged |
|---|---|---|
| Conv 3 smoke (`1syoB4ry6PksRB_X68RWo4Wl8clZyDZ0Y`, 5831 B) | pointer markdown only | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 4 `PANE_EXTRAS` | `schema-recon/09_live_skills/{agentify,image-pipeline,skill-orchestrator,system-roadmap}/SKILL.md` | Sept 13 recon copies; sizes already match intake (2341 / 26278 / 21309 / 6606). Not extras. |
| Conv 6 shop | trip / lake-targeting artifacts | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 6b ROAD | bundled AppBuilder `SKILL.md` (auth, building-games, generate2dmap, …) | no matching `skill_tree/skills/<slug>` on this branch; adding SKILL.md-only stubs would be incomplete. Tarball stays on Drive (`1uChAXnBu9Tdwl56ZgVPh6nA8wlXBzZbI`). |
| Conv 7 pane extras (190840 B) | ICM harness recon + 2 PNGs | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 7 heavy | `artifacts/drive-push/active-work-skills/image-pipeline/.../WORK_QUEUE.md` (7034 B) | Drive-push staging, not `.grok/skills`. Live intake WQ is 5134 B. Left on Drive. |
| Conv 09 wireup | fullstack-wireup markdown + attachments | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 9 agentify-identify | lookbook / factory plates | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 9 coven-engine | pane `wq/WORK_QUEUE.md` under artifacts (ece/gce/…) | not skill-tree `WORK_QUEUE.md` |
| Conv 9 hauler | rendered keeps / jpegs | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 10 lookbook | lookbook JSON + PROTOCOL.md | no `SKILL.md` / `WORK_QUEUE.md` |
| Conv 11 / finance / ICM / boot-pointers | pane notes + images | no `SKILL.md` / `WORK_QUEUE.md` |

## Deliberately not downloaded

- CONV2_B `part00`–`part06` (~80 MB × 6 + 23 MB)
- CONV2_A attachments (72 MB)
- CONV1 `SKILL_SURFACE_FULL` + split volumes
- Other flurry tarballs after the manifest showed no live `SKILL.md` / `WORK_QUEUE.md` merge target

## Git landing

- `snapshots/2026-09-17/AWESOME_SPLIT_LEDGER.md`
- `snapshots/2026-09-17/RECEIPT_awesome-split-extras.md`
- `MASTER-INDEX.md` (dated line prepended)
- `skill_tree/INTAKE.md` (MIS-10 extras scan note)

`skill_tree/skills/**` unchanged. Merge is clean.
