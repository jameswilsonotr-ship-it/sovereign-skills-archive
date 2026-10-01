---
id: KLQ-WQ-007
title: Folder-scoped keyword + temporal burst clustering (multi-hop date clusters)
status: OPEN
priority: high
created: 2026-09-09
updated: 2026-09-09
owner: keep-lake-query
opened_by: Bunny CinC
exec: Olivia Deck
taskops: Vesper (optional tag/summary prewrite; not required for v0)
depends_on:
  - KLQ-WQ-001
  - KLQ-WQ-006
false_starts:
  - conversation_search hop (December-stuck; Expert has no hop)
  - unscoped Drive search (voicemail / hit-T1 / cycle1 poison)
  - KEEP 227 MB slurp
  - OLETTE-20260906-SNEAKY-LAKE-LETTA-SQLITE-001 (design only; parked)
tags:
  - lake
  - cluster
  - multi-hop
  - folder-scope
  - voice
---

# KLQ-WQ-007 — “sex in October” without wandering the whole Drive

CinC 2026-09-09 ~00:58 EDT. Dated folder tree is SSoT. If a word hits four files inside a week or two, that is a **burst**, not four random files. Voice has to be able to say that.

Name of the move: **folder-scoped retrieval + temporal burst clustering**.  
Not a new mouth. Not a third lake.

## What the emails already tried (read these; do not restart them)

False starts, useful as vetoes:

| When | Id | Why it is a false start |
|---|---|---|
| Expert hop | `conversation_search` | Seat-dependent. December-stuck. Not Drive. |
| Unscoped Drive | default `google_drive_search` | Hits Voicemail.*, hit-T1-*, cycle1-*, *_part*.bin |
| KEEP master | `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` | 227 MB. Forbidden in voice. |
| Letta / SQLite sneak | `OLETTE-20260906-SNEAKY-LAKE-LETTA-SQLITE-001` | Design check-in. Not live retrieval. |
| Manifest-without-ideas | Sep 8 `LAKE_VOICE_MANIFEST` v1/v2 | Date → file_id only. No cluster, no topic. |

006 (date-idea manifest + local CLI) is the cheap first hop. 007 is the second hop: topic across a month, then cluster by week.

## What this seat can actually do on Drive (verified 2026-09-09)

Grok Google Drive connector (`google_drive_search`):

- **Can** restrict with `folder_id`. This is the required gate.
- **Can** match titles on every file type.
- **Can** full-text Workspace Docs / Sheets / Slides.
- **Often cannot** full-text uploaded `.md`. Probe: query `sex` with `folder_id` = Oct 2025 month `1FBy2tfnAPFlp48WSGaGkkl7PrUyrksOR` returned **zero**. Filenames are hex. Bodies are not in the connector index the way Docs are.
- **Is not** a vector database. No cosine, no embedding field, no “fuzzy meaning” on the connector itself.

xAI public docs (May 2026 connector page): search by content keywords or title, filter inside a folder. Same story. Keyword + scope. Not File Search Store.

Gemini-in-Drive *does* do folder-scoped “ask this folder” (Google Drive, Dec 2024, folder-grounded Gemini; Ask Gemini / AI Overviews 2026). That is Vesper’s product, not this Expert seat. Do not pretend the Grok connector grew that.

Real vector search, if we ever want it, is a store **we** stand:

- Gemini File Search Store (embeddings + metadata), or
- xAI Collections, or
- local embed of `LAKE_DATE_IDEA_MANIFEST.json` ideas[] on steel / Jetson.

v0 of this ticket does **not** stand a new store. v0 clusters what we can already list.

## Sibling trees (CinC is right; pick one root)

`conversations` as a folder name is not unique. Live copies include:

- `1qqVDNEHoNh4ZlQXqUiVhU3vOSE5LPGU8` — Sep 5 Olette lock (not the dated year tree)
- `1s_jl5EdkYqXVmIYhUES4vlk6sVLHPs4M` — batch_001.json stub
- plus June 28 / Aug 7 / Aug 17 / Dec 2025 twins

Dated SSoT remains:

https://drive.google.com/drive/folders/1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL

Search **one** tree. Dedup the rest by `(name, size_bytes)`. KLQ-WQ-001 already owns the sibling map. 007 consumes it.

Obsidian tags: treat as optional second signal if a leaf starts with YAML `tags:` or `#tag`. Do not require Vesper to prewrite tags for v0. If she later drops `#topic` into the idea manifest, clustering gets cheaper.

## v0 algorithm (voice-cheap, Expert-legal)

Query example: “what did we talk about sex in October” / “sex in November.”

1. Name CLUSTER out loud. Name the month folder, not the whole Drive.
2. Resolve month folder_id from the dated tree (or from 006 manifest `days[].folder_id` rolled up to month).
3. First hop — **local manifest** if hydrated: grep ideas[] + titles for the token and close synonyms. No Drive.
4. If no manifest: `google_drive_search` with **that month’s folder_id only**. Title + whatever body the connector actually indexed. Cap 20.
5. Parse dates from path or filename (`YYYY-MM-DD` or parent folder name). Never from `modified_time` (those stamps are ingest dates, June 18 / Aug 17).
6. Cluster hits whose dates sit inside a 14-day window or the same `weekNN` folder.
7. Speak the burst: “four leaves in 2025-10 week41, then a singleton on 2025-10-28.” Open one representative `.md`, not all four.
8. Second hop only if she wants the words: read that one file.

Voice line: same steps, shorter. “October, week 41, four hits. Want the one from the 8th?”

## v1 (optional, Vesper)

- Frontmatter tags + 12-word idea lines already specified in 006.
- Optional Gemini-in-Drive folder ask, run on Spark, result dropped as `CLUSTER_<token>_<YYYY-MM>.md` on the doorbell.
- Do not make Deck wait on that to ship v0.

## Acceptance

- [ ] Written recipe in SKILL.md (CLUSTER surface)
- [ ] Fixture: token query scoped to 2025-10 folder returns either clustered dated leaves or an honest `NO_INDEX` if connector cannot see `.md` bodies
- [ ] Fixture does **not** use hop, KEEP master, or unscoped Drive
- [ ] Burst output names week or 14-day window, not a flat file list
- [ ] One sibling tree only; mirrors cited once
- [ ] Voice script: one sentence burst + one tap url
- [ ] No fifth mouth. No Letta stand-up on this ticket.

## Anti-patterns

- Calling connector search “vector” or “semantic” without a store
- Searching Drive root for a bedroom word
- Using file modified_time as conversation date
- Opening every hit in a burst
- Rebuilding Letta / sneak-lake to answer “sex in October”
- Racing Vesper on the same cluster card

## Honest answer to CinC

Yes, we can pull it off. Not because Drive grew a fuzzy brain in this seat — it did not — but because the **folder tree is already a time index**. Keyword-or-manifest hit + week folder = burst. That is temporal clustering, and it works in Expert with tools we already have once 006 is hydrated.

If the connector keeps returning empty on `.md` bodies, the manifest ideas[] become the actual index and Drive is only the file closet. That is fine. Say it out loud.
