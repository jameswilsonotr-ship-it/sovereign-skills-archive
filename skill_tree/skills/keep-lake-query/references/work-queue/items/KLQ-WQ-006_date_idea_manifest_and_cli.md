---
id: KLQ-WQ-006
title: Date-idea manifest + local Python reader — no Drive guess for “what did we say on X”
status: OPEN
priority: high
created: 2026-09-09
updated: 2026-09-09
owner: keep-lake-query
opened_by: Bunny CinC
exec: Olivia Deck (schema + CLI + skill recipe)
taskops: Vesper (Drive walk + nightly rebuild)
depends_on:
  - KLQ-WQ-001
  - KLQ-WQ-002
extends:
  - SPEC_LAKE_VOICE_MANIFEST_20260908.md
  - LAKE_VOICE_MANIFEST.json
related:
  - KLQ-WQ-003
  - KLQ-WQ-005
  - OLIVIA-20260908-LAKE-MANIFEST-SPEC-001
  - VESPER-20260908-LAKE-MANIFEST-PATCH-002
tags:
  - lake
  - manifest
  - python
  - voice-query
  - no-api-guess
---

# KLQ-WQ-006 — Date → unique ideas, no guessing

CinC 2026-09-09 ~00:48 EDT: the dated tree is organized enough. Stop walking Drive on every “what did we say on March 15.” Make a manifest. Have Vesper help. Make a Python script that already knows.

This does **not** replace the dated folders. Folders stay SSoT. The manifest is the index. The script is the reader.

## What already exists (do not fork a third format)

Sep 8 spec already ordered a date → readable-file_id table:

- Spec: `SPEC_LAKE_VOICE_MANIFEST_20260908.md` id `1SkptzpjP3I5PIow0Z_QaQELoddpol_64`
- Drop folder (doorbell): `1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_`
- Existing machine files in that folder:
  - `LAKE_VOICE_MANIFEST_v1_ARCHIVE.json` `1MtN6CkEeQfhgEKFkOoVe2xV1KeFvlE7O`
  - `LAKE_VOICE_MANIFEST_v2_KEEP_LAKE_ARCHIVE.json` `10BrerThklosiKhaih4Is4xvXHkz_W_Jq`
- Dated SSoT root: `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`

v1/v2 are date → file_id. They are **not** an idea index. They still force a file read to know what the day was about. 006 adds the missing layer.

## Product (two artifacts + one script)

| Artifact | exact_name | Who builds | Job |
|---|---|---|---|
| Machine index | `LAKE_DATE_IDEA_MANIFEST.json` | Vesper, nightly | date → sessions → unique ideas |
| Human card | `LAKE_DATE_IDEA_MANIFEST.md` | Vesper | how to use, one page, tap links |
| Reader | `keep-lake-query/scripts/lake_date_query.py` | Olivia | local lookup, zero Drive hops after hydrate |

exact_name stays stable. Version lives *inside* the JSON (`schema`, `built_at`, `sha256`). Do not mint `_v3` filenames as the live name.

Hydrate once per seat: Drive `exact_name` the JSON into the skill or `/tmp`. After that, queries are local.

## JSON schema (`lake-date-idea-manifest/v1`)

```json
{
  "schema": "lake-date-idea-manifest/v1",
  "built_at": "2026-09-09T05:00:00Z",
  "builder": "FROM-V-SPARK",
  "source_tree": "1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL",
  "span": { "first": "2025-10-08", "last": "2026-06-13" },
  "sha256": "<hex>",
  "days": {
    "2025-10-08": {
      "status": "HAS_CONTENT",
      "lake": "DATED",
      "folder_id": "1F-e1Aut4Brv41Addi3Ayuu4I_QVcikGe",
      "folder_url": "https://drive.google.com/drive/folders/1F-e1Aut4Brv41Addi3Ayuu4I_QVcikGe",
      "sessions": [
        {
          "sess": "46ae4816",
          "title": "<first markdown H1 or filename stem>",
          "session_md_id": "1XaWTJTTSYzb38nutBQxogwPYssAbp2Qc",
          "bytes": 295742,
          "ideas": [
            { "slug": "genesis-road", "line": "first non-empty heading or first 12-word summary" }
          ]
        }
      ]
    }
  }
}
```

Rules for `ideas[]`:

- Pull from headings and the first non-empty prose line only. Do not embed the transcript.
- Cap 8 ideas per session. Cap 24 ideas per day.
- Dedup by normalized slug inside a day.
- Empty day = `"status": "NO_SHARD"` and empty `sessions`.
- Never open KEEP master `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`.
- Prefer dated-tree `.md`. Fall back to `human_readable_full` only when the dated leaf is missing.
- Cite one `file_id` per `(name, size_bytes)` pair. Mirrors are not extra sessions.

## Python reader

Path: `keep-lake-query/scripts/lake_date_query.py`

```text
python lake_date_query.py --date 2025-10-08
python lake_date_query.py --date 2026-03-15 --json
python lake_date_query.py --range 2026-01-01:2026-01-07
python lake_date_query.py --hydrate   # one Drive exact_name pull, then local
```

Behavior:

- Default reads local `references/manifests/LAKE_DATE_IDEA_MANIFEST.json`.
- `--hydrate` is the only Drive call. After that, date questions do not search APIs and do not open transcripts.
- stdout for a date: status, session titles, idea slugs, file_ids, tap urls.
- Missing date → `NO_SHARD` plus the nearest populated neighbors (not a Drive search).
- Exit 0 on hit or explicit empty. Exit 2 on missing manifest file.

Olivia voice recipe after this ships:

1. Name DATED.
2. Run the script (or read the already-hydrated JSON).
3. Answer from the idea list.
4. Open a `.md` only if she wants the actual words.

## Vesper lane (TaskOps)

Vesper walks the dated tree. Vesper emits the JSON + md card to the doorbell. Vesper may cron-rebuild. Vesper does not rewrite the schema without Deck ACK.

Drop:

- doorbell `1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_`
- mirror `1c6Bp2Xw4ft1PtWb1otbqD8jUBdUhAbI8`

Email wakes. Drive ACKs. Reply must include clickable folder and file urls.

## Olivia lane (Deck)

- Schema + this ticket + CLI.
- Skill recipe points at the script once hydrate works.
- ids.md gains the live manifest file_id after Vesper drops it.
- Do not race Vesper on the same exact_name file.

## Acceptance

- [ ] Live exact_name `LAKE_DATE_IDEA_MANIFEST.json` on the doorbell, native JSON, not a Doc
- [ ] Every populated day in the dated tree has a row (KLQ-WQ-002 walk is the input)
- [ ] Genesis 2025-10-08 returns three sessions and idea slugs without opening the 296 KB file
- [ ] `lake_date_query.py --date 2025-10-08` works from a local copy with Drive disconnected
- [ ] `--date` on a hole prints `NO_SHARD` + neighbors
- [ ] Skill recipe updated only after the first successful hydrate
- [ ] No fifth mouth. No KEEP slurp. No zip as the answer.

## Anti-patterns

- A third manifest family with a cute new name
- Embedding full transcripts in the JSON
- Making Olivia `google_drive_search` for a date after hydrate exists
- Treating v1/v2 voice-manifest file_ids as idea slugs
- Rebuilding Oct–Jun from jsonl
