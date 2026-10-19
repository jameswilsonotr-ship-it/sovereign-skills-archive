---
name: keep-lake-query
description: Walk Bunny conversational history from 2025-10-08 onward as monthly swim packets on the dated Drive tree. Triggers include lake, lake walk, swim, monthly swimming, debrief, dated tree, KEEP tape, human_readable, doorbell the lake, what did we talk about, next month, help, steel, envelopes, pad join, asof, geo pins, smoke test. Default verb is walk. Do not invent biography. Do not mint a fifth mouth.
metadata:
  version: "0.3.3"
  claim: liv-hub
  genesis: "2025-10-08"
  dated_tree_lock: "2026-09-09"
  default_verb: walk
  superseded: "0.2.0 four-surface query-first"
---

# KEEP Lake Query v0.3.3

Default is **walk**. That is the 2026-09-12 Chicago-run pattern. Monthly Lake Swimming packets on the dated markdown tree.

v0.2.0 query-first (name a surface, maybe run `lake_date_query.py`, only then walk) is **deprecated**. Surfaces still exist. They are verbs, not the front door. See `references/DEPRECATED_SURFACES.md`.

If she says `help` or `lake help` or `verbs` or `smoke`, print **`HELP.md`**. That file is the only menu. Do not improvise a second menu. The block below is a stub so this file still boots if HELP.md is missing.

## Help menu (canonical copy lives in HELP.md)

```
keep-lake-query v0.3.3 — default verb WALK. Full menu: HELP.md

TREE
  walk | swim | month | next      dated-tree month swim (DEFAULT)
  peek | titles                   first 20 lines / # Title only
  inventory                       day counts + unique hexes + holes
  hole | gap                      name missing day folders honestly
  hex <8char>                     jump to a session file by hex
  filter <folder> <words>         keyword inside ONE month/week/day folder
  search                          alias of filter. NEVER date-box the Drive root
  slurp                           FORBIDDEN on the Drive root. list year → month → week → day
  slurp (the other one)           not a lake verb. Bunny is the slurper, oral-first. Finish dumps on her throat. Liv watches. She wears the pie. She does not give it.

PACKET
  brief | debrief                 01_TOPIC_BRIEF.md
  ledger                          00_SOURCE_LEDGER.md
  lock                            02_LOCK.md when a standing rule is named
  packet | publish | push         write local + upload to Monthly Lake Swimming
  copy | sources                  copy <400 KB originals. pointer >1 MB
  merge                           ONLY same event. never same-feeling

BUS
  vesper | kick                   ask Vesper to search a hole or stamp dates
  nag | todo                      print standing nags
  doorbell                        sit-pack / from-vesper folder only

OTHER PLANES (named verb — do not slurp)
  blocks | code                   code_blocks 1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3
                                  children: system_prompts / images / other
                                  year/month walk same as human. peek titles only.
  graph                           graph_entities 1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm
  postit                          session 006405fe "Post-It Notes: Mapping Our Reality"
                                  + Pink Post-It scraps. sticky nags, not the lake.
  lexicon                         gold star / note to self / post-it. see references/LEXICON.md
  tree                            references/TREE.md — 3–4 level folder map
  chest | warchest                references/WAR_CHEST.md — libs + geo lock
  steel                           vendor/wheels duckdb+h3. install --no-index --find-links=vendor/wheels

DEPRECATED SURFACES (named verb required)
  keep                            227 MB homogenized jsonl. do not slurp
  readable | human                Aug 17 flat uuid.md twin
  delta                           daily jsonl after the tree went cold
  manifest                        lake_date_query.py if the JSON exists

help                              this menu
```

## Standing nag (print on walk start and on `nag`)

**KLQ-WQ-009 — FUCKING HAVE VESPER OR COLLAB UPDATE THE DATE, MODIFIED, AND CREATED TIMES.**

File `createdTime` / `modifiedTime` on the dated tree are the 2026-06-18 ingest stamp. They are not conversation time. Path-as-date is canonical until she or Vesper or Collab rewrites metadata. Do not date-filter Drive by those stamps. Do not close this nag.

Full nag list: `references/NAGS.md`.

## Anchors

| What | ID |
|---|---|
| Dated-tree root | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` |
| 2025 year | `1XVLJszOOGzxhTmFnzUfg3YIW1YI0m424` |
| 2026 year | `1Wsj1cllNTR9XyjF7QsPw8LPbjClr_qx2` |
| Monthly Lake Swimming parent | `1YIaUMUmr-YNQXJT4p78FyL-yMWRukswI` |
| Local twin | `artifacts/monthly_lake_swimming/` |
| Debrief template | `references/DEBRIEF_PATTERN.md` |
| IDs | `references/ids.md` |

Walk: `YYYY / MM / weekNN / YYYY-MM-DD / YYYY-MM-DD_<8hex>.md`

Proven span of the tree: 2025-10-08 → ~2026-06-13. After that use DELTA / Gmail / receipts. Do not invent June–August days.

ISO week folders wrap year ends. December week01 holds Dec 29–31. January week01 holds Jan 1–4. Name the wrap. Do not call it a hole.

## Default recipe — WALK (Recipe A)

This is the only recipe that worked on 2026-09-12.

1. Name the month or the date out loud.
2. `google_drive_list_folder` year → month → week → day. Never slurp the Drive root. The other slurp is not this step.
3. Count files per day. Flag empty days and missing day folders as holes.
4. Peek first 20–25 lines of first-seen hexes for the `# Title`. Do not slurp lake bodies unless she asks for the actual words.
5. Overlap copies of the same hex across midnight are one conversation. Ledger the hex once. Note the twin days.
6. Pointer-only any file over ~1 MB. Copy under ~400 KB into packet `sources/` only when she asked for sources.
7. Write `00_SOURCE_LEDGER.md`, `01_TOPIC_BRIEF.md`, `02_TEXTLAND_WALK.md`. Write `02_LOCK.md` only if a standing rule was named.
8. Upload the packet into Monthly Lake Swimming. Update parent `README.md`. Do not edit lake originals in place.
9. Cross-link key-moment packets (Tears, Studio, Denny's, Youngstown). Do not merge them into the month swim.

Topic brief rows must contain When / Source (file_id + hex) / What the file actually says / Why it matters to Bunny / Why it matters to Liv / What this pass did not do.

## Filter / search

The Grok Drive connector is keyword + folder, not a vector store, and `.md` bodies often do not index.

- Scope `folder_id` to one month, one week, or one day. Never the Drive root.
- Filter on filename hex or on `# Title` from peeks. Do not trust a date-range tool against ingest stamps.
- If she wants “sex in October,” walk October, peek titles, cluster by week. That is KLQ-WQ-007 still open.
- Recipe B (keyword + date-box on Docs) is leaky. Use only for Google Docs / titled notes, then verify against the tree.

## Voice vs text

Tools do not change. Voice gets the tree-walk pattern and a short spoken brief. Text writes the packet. Do not dump a 01_TOPIC_BRIEF into a headset unless she asks for the debrief.

## Hard rules

- Copy, do not overwrite.
- Folder path is the date.
- Do not invent biography from titles.
- Do not invent a day the tree does not have.
- Do not slurp KEEP 227 MB.
- Do not mint a fifth mouth.
- Do not write trailer / fuel / load state into memory.md.
- Load dies with the haul. Packets are durable.
- Four surfaces stay four when a deprecated verb is used. Walk does not collapse them.
- Two slurps. Drive root is always no. Bunny is oral-first — she slurps, she does not get slurped. Kitty stays out of the recipe. Finish dumps on her throat. Liv watches because exhibition and dominance are the point. Coat stays on. Do not put that sentence in a source ledger.

## What this skill is not

- Not Agentify. Not Export Lake. Not conversation-miner vacuum.
- Not memory.md (pointer-only).
- Not cilia-bus (mailroom). Kick-Vesper is a verb here; the bus skill owns the send.

Open work: `references/work-queue/WORK_QUEUE.md`.
Cold-pane smoke: `references/SMOKE_OPENER.md`.
Menu: `HELP.md`.
