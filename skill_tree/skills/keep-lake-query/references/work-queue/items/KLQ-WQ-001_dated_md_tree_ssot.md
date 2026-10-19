---
id: KLQ-WQ-001
title: Dated markdown tree is voice-readable SSoT — index the folders, do not rebuild the lake
status: OPEN
priority: high
created: 2026-09-09
updated: 2026-09-09
owner: keep-lake-query
opened_by: Bunny CinC
exec: Olivia Deck
taskops: Vesper
related:
  - KLQ-WQ-002
  - KLQ-WQ-003
  - KLQ-WQ-004
  - KLQ-WQ-005
  - GCM-WQ-001
  - OLIVIA-20260909-MD-CONVO-TREE-MAP-001
  - VESPER-20260908-HUMAN-READABLE-LAKE-LOCATED-001
tags:
  - lake
  - dated-tree
  - drive-first
  - voice-query
---

# KLQ-WQ-001 — Dated MD tree SSoT

Huge. Not a scout. Folders are the source of truth. This file is a work order.

## Lock (2026-09-09 00:42 EDT)

CinC handed this root and said the folders around it are SSoT:

https://drive.google.com/drive/folders/1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL  
folder_id: `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`

Skill `keep-lake-query` v0.2.0 now points here first for date questions.

## What the root actually is (verified this seat, 2026-09-09)

```
<dated-root>
  2025/                         1XVLJszOOGzxhTmFnzUfg3YIW1YI0m424
    10/ 11/ 12/
      week41..week44/
        YYYY-MM-DD/
          YYYY-MM-DD_<8hex>.md
  2026/                         1Wsj1cllNTR9XyjF7QsPw8LPbjClr_qx2
    01/ 02/ 03/ 04/ 05/ 06/
      weekNN/
        YYYY-MM-DD/
          YYYY-MM-DD_<8hex>.md
```

- Native `text/markdown`. Unzipped.
- Tree written 2026-06-18.
- Proven first day: 2025-10-08 (Genesis, three files, including 296 KB `46ae4816`).
- Proven last day opened: 2026-06-13 (`2026-06-13_e8bb01f0.md`).
- Missing from this tree: 2026-06-14 onward. That is a real gap, not a search miss until 002 walks every month.

## Sibling surfaces (not this tree)

Do not collapse.

| Surface | Root / id | Kind | Span | Role |
|---|---|---|---|---|
| DATED MD | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` | year/month/week/day `.md` | 2025-10-08 → ~2026-06-13 | **SSoT for date questions** |
| HUMAN_READABLE_FULL | `1DAfH3lTNtYtgLLEHM67AYJcGrnOGdIyt` | flat `uuid.md`, ~21 KB cap | Aug 17 2026 render | session-hex walk |
| HUMAN_READABLE_FULL mirror | `1t3clBWHnYFDA159UMJux4jSnbHTCA_GH` | same files, new ids | same | mirror |
| HUMAN_READABLE thin | `1nCrbaKmTtwXSPkApK6ioJAi2cjAbXLSg` + 2 mirrors | ~25 short files | Aug 17 07:59Z | different pass |
| KEEP jsonl | `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` | 227 MB homogenized | Oct 2025 → Aug 17 overlap | machine tape. do not slurp |
| DELTA jsonl | daily files in ids.md | native xAI export | 2026-08-11 → 2026-09-06 | post-tree recent |
| I-70 sunset tar | `1CY13vehUnbF2zWYSTN8ThNeMTTEse3qH` | 20.6 MB | 2026-09-08 | this-week pane archive |

Plus the earlier parallel `conversations/` folder forest Deck already mailed Vesper (harvest, miner comparison, Gemini_Spark, Sep 5 Olette lock). Those are **around** this tree. Map them. Do not promote them over the dated root unless a folder is a byte-identical mirror.

## Goal

A voice seat can answer "what did we talk about on March 15" or "switch to number seven from yesterday" by walking Drive, not by hoping hop or slurping jsonl.

## Work (do in order)

1. **Parent + siblings.** Find the parent of `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`. List every folder sitting next to it. Mark mirror vs other-kind. Clickable links. This is the "eight trees" CinC called.
2. **Full walk.** Every year, month, week, day under the dated root. One row per day: date, folder_id, url, file_ids, byte sizes, empty-day flag.
3. **Cold end.** Confirm last populated day. Today the last opened day is 2026-06-13. Prove it.
4. **Join table.** `YYYY-MM-DD_<8hex>.md` ↔ `human_readable` `uuid.md` ↔ KEEP `session_id`. Without this, hex and date are two lakes.
5. **Do not rebuild.** If a dated `.md` exists for a day, that day is done. Twin only the gap after the tree dies and the DELTA days after Aug 17.
6. **Doorbell product.** `MD_CONVO_TREE_MAP_20260909.md` in `1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_` + from-vesper mirror. Update `LAKE_VOICE_MANIFEST` so voice can exact_name the map.
7. **Fixtures.** Three live queries logged: Genesis 2025-10-08, one mid winter date, 2026-06-13. Each returns file_id + first-line title. No biography invention.
8. **Skill stay thin.** ids.md + this queue absorb new IDs. SKILL.md stays a recipe.

## Acceptance

- [ ] Parent of the dated root named, with sibling folder urls
- [ ] Every day folder under the root listed (or explicitly marked empty)
- [ ] Last populated date proven
- [ ] Join table exists for Genesis + at least 20 later sessions
- [ ] Doorbell map file dropped with tap-able urls
- [ ] SKILL.md query recipe works in Expert (Drive only, no `conversation_search`)
- [ ] No new mouth. No KEEP slurp. No zip as the answer.

## Anti-patterns

- Treating `human_readable_full` as the dated SSoT
- Re-extracting Oct–Jun from jsonl when the `.md` already sits in week folders
- Returning folder_ids without `https://drive.google.com/drive/folders/<id>`
- Dumping 227 MB into chat
- Minting Delta Giggles or any fifth mouth to "hold" the index
- Racing Vesper on the same doorbell file

## Already mailed

2026-09-09 00:26 EDT Deck → Vesper  
`OLIVIA-20260909-MD-CONVO-TREE-MAP-001` on thread `1a08309b6adab8c9`  
Gmail `1a0846badb1dc5e3`

Vesper's human_readable discovery (true, incomplete):  
`VESPER-20260908-HUMAN-READABLE-LAKE-LOCATED-001` Gmail `1a0846f82061fa00`

## Pointers

- Skill: `/home/workdir/.grok/skills/keep-lake-query/SKILL.md`
- IDs: `/home/workdir/.grok/skills/keep-lake-query/references/ids.md`
- Miner sunset stays GCM-WQ-001. This queue retrieves. Miner publishes.
