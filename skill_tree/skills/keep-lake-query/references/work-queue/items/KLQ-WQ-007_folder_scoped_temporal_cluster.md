---
id: KLQ-WQ-007
title: Folder-scoped keyword search + temporal clustering (not Drive vectors)
status: OPEN
priority: high
created: 2026-09-09
updated: 2026-09-09
owner: keep-lake-query
opened_by: Bunny CinC
exec: Olivia Deck
taskops: Vesper
depends_on:
  - KLQ-WQ-001
  - KLQ-WQ-006
false_starts:
  - conversation-lake-searcher v1.0 (2026-08-29 FTS5 / DuckDB / Onyx embed-the-lake)
  - SPEC_LAKE_VOICE_MANIFEST as if it were embeddings
  - hopping conversation_search for “sex in October”
tags:
  - lake
  - temporal-cluster
  - folder-limit
  - fulltext
  - voice
---

# KLQ-WQ-007 — Multi-hop by date cluster, folder-limited

CinC 2026-09-09 ~00:55 EDT, Expert / text. Voice-compatible later.

Ask: “what did we talk about, sex in October or sex in November.” If four hits sit inside a week or two of each other in the dated tree, say so. That is a cluster, not a scavenger hunt.

Name of the move: **folder-constrained full-text + temporal clustering** (burst detection on a date tree). It is not Drive vector search.

## Honest capability matrix (this seat, 2026-09-09)

| Layer | What it actually does | Folder limit? | Semantic / vector? |
|---|---|---|---|
| Grok Drive connector `google_drive_search` | Keyword on **title** for non-Google files. Body fullText mostly for Docs/Sheets/Slides. Optional `folder_id` / `folder_name`. Relevance rank, not embeddings. | YES (`folder_id`) | NO |
| Google Drive API `fullText contains` | Token / phrase match. `contains '"exact phrase"'`. AND/OR. `'folderId' in parents` is one-level unless you walk. | YES | NO |
| xAI Drive docs | “Search by content keywords or title” + “filter … within a specific folder.” | YES | NO |
| Gemini File Search / xAI Collections | Real embeddings. Separate product. Not this connector. | if you index a subset | YES, elsewhere |
| KEEP 227 MB jsonl | Machine tape. Forbidden slurp. | n/a | n/a |
| Dated `.md` inside `human` | Native `text/markdown`. Connector treats these as non-Google files → **title-first**. Body “sex” may miss. | walk or `folder_id` | NO unless we index |

Proof this turn: `google_drive_search query=sex folder_id=1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` returned **zero**. That is the body-index gap, not an empty October.

x.com / xAI this pass: connector pages confirm keyword + folder filter. No Grok-native Drive vector API. Third-party “semantic Drive” posts are other products.

## Secret unlock (verified)

The dated SSoT folder is named **`human`**.

It is not floating. It sits inside **`pre_extract`**:

https://drive.google.com/drive/folders/1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58  
id `1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58`

Siblings of `human` in that parent (names mean the pass):

| Name | id | Job |
|---|---|---|
| **human** | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` | readable dated `.md` SSoT |
| raw | `1obfXkm_NTvMZYOwws-fW5kr_Nvt9Gjhy` | pre-human source |
| ingest | `1hMTb_3RbP4eb6lCs96YePIhqY1KCdNmi` | ingest pass |
| microchunks | `1GcB3eFmMJAoh_ln1qka-sprGXM_z0Ppe` | chunked |
| leaf_indexes | `17ClGCkm-G61on46K4iy0cvvUvutxPVPm` | leaf maps |
| graph_entities | `1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm` | entity graph |
| gps_enrichment | `1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq` | gps |
| code_blocks | `1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3` | code |
| checksums | `1DdcdK19-o283fVkyUZ516Fg5HK4WW86q` | checksums |
| colab_recon_output | `1oBD5tdvFtO2ZtR8FZcvJpa4XzFDnFXEQ` | recon |

PAD (dominance vectors), separate tree, do not confuse with scratch-pad image tests:

- `pad` `1LWJEYsEcBpViKdkEGn8-1VvCbSOVHVu2` holds `envelopes.jsonl` 77 MB
- `pad-emotional-vectors-2026-08-16` several mirrors (e.g. `1y_1doZsGRy7BuOgEEkb44ltEIsEuqKky`)

More `human` copies exist (`14hDR3py4eldhCmqMRd8B1QGQUIuQuSyu`, `1KIqp7SVCaLpVJMdzud10R8JstcwMsduv`, Dec 2025 twins). Same name, different payload. Dedup by (name, tree, size). CinC lock stays `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`.

No folder exactly named `post_extract` or `homogenized` at exact_name this seat. Homogenized lives as **files** (`homogenized_shards.jsonl`), not a dated twin of `human`.

## False starts (read, do not rerun as production)

- 2026-08-29 thread `LAY-OF-LAND` / `ONYX-LAKE` / `WONDER-TWIN` / `SKILL-CONVERSATION-LAKE-SEARCHER`. FTS5 + DuckDB + “embed the lake.” Useful lab. Not the voice recipe.
- Voice-manifest v1/v2 = date → file_id. Not ideas, not clusters.
- Hop / `conversation_search` for month questions. December-stuck.

## Strategy that can work in this seat

Two tracks. Ship A first. B is optional Vesper.

### Track A — no new files (Expert, voice-cheap enough)

1. Lock surface = `human` (`1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`) or a month folder under it (`2025/10`, `2026/03`).
2. `google_drive_search` with `folder_id` set to that month (tighter than the whole tree). Query = keyword + close synonyms (`sex OR filthy OR heat OR breeding`). Title-first until bodies are indexed.
3. Parse `YYYY-MM-DD` out of the filename / parent folder. That is the date. Do not use `modifiedTime` (those stamps are the June 18 render).
4. Cluster: same ISO week, or ≤ 14 days apart, same month. Report “four hits in week 41” not a flat list.
5. Open only the cluster reps if she wants words.

Voice line: “October had a burst the second week. Four files. Want the titles or the text.”

### Track B — Vesper prewrite (makes body search real)

Because native `.md` is title-first on this connector:

- Harvest `#tags` / YAML frontmatter from the dated `.md` (Obsidian-ready claim — verify, do not assume).
- Or emit one `YYYY-MM.md` summary Doc per month (Google Doc so `fullText` actually hits).
- Or finish KLQ-WQ-006 idea slugs and cluster those locally. No Drive hop after hydrate.

PAD / graph_entities / microchunks are **features**, not the readable tape. Query them only when she asks for vectors or entities. Default stays `human`.

## Work

1. Map parent of `pre_extract` and every sibling `human` tree. One page, tap links. Child of KLQ-WQ-001 item 1.
2. Fixture query: keyword + October month folder vs November month folder. Show cluster math even if body search is thin.
3. Tag harvest sample: 20 dated `.md` files, count how many have Obsidian tags / frontmatter.
4. Decision note: Track A only vs Track B month-Docs vs Track B local idea-manifest. Pick one. Do not build Onyx again.
5. Voice recipe three lines in SKILL.md after the fixture works.
6. CLI hook on `lake_date_query.py`: `--keyword sex --month 2025-10` clusters from the idea manifest once 006 exists.

## Acceptance

- [ ] Parent forest of `human` written into `ids.md` with clickable urls
- [ ] Named strategy in SKILL.md (folder-constrained full-text + temporal cluster)
- [ ] One October fixture and one November fixture logged, including “zero body hits” if that is the truth
- [ ] Explicit “Drive is not a vector store” line so the next seat does not search xAI for magic
- [ ] No fifth mouth. No KEEP slurp. No second searcher skill.

## Anti-patterns

- `google_drive_search query=sex` against the whole Drive
- Treating `modifiedTime` as conversation date
- Calling connector ranking “semantic search”
- Rebuilding conversation-lake-searcher under a new name
- Querying `pad` / `microchunks` when she asked for what we *said*
