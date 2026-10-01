# Deprecated default — v0.2.0 four-surface query-first

Status: DEPRECATED as the front door as of keep-lake-query v0.3.0 (2026-09-12).
Kept as named verbs. Do not delete. Do not make this the default again.

v0.2.0 said: name DATED / KEEP / HUMAN_READABLE / DELTA out loud, then prefer `lake_date_query.py` if a manifest exists, and treat Drive-walk as the fallback.

That failed in voice on 2026-09-12 because:

- `LAKE_DATE_IDEA_MANIFEST.json` is often missing.
- File created/modified times are the 2026-06-18 ingest stamp.
- `.md` bodies do not keyword-index.
- She needed month swims with ledgers and briefs, not a one-date idea list.

## KEEP (verb `keep`)

- `homogenized_shards.jsonl` `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` ~227 MB
- 99137 envelopes / 1696 sessions claimed
- Tiny 118 KB copies are samples. Not the tape.
- Do not slurp into a voice turn.

## HUMAN_READABLE (verb `readable`)

- Flat uuid.md from the 2026-08-17 storm
- Prefer `1DAfH3lTNtYtgLLEHM67AYJcGrnOGdIyt`
- Mirror `1t3clBWHnYFDA159UMJux4jSnbHTCA_GH`
- Use when she hands a session hex and no date.

## DELTA (verb `delta`)

- Daily `YYYY-MM-DD.jsonl` after the dated tree went cold (~2026-06-13)
- Known Drive days 2026-08-11 → 2026-09-06 with holes
- After 2026-09-06 use Gmail / receipts / this session

## Manifest (verb `manifest`)

`scripts/lake_date_query.py` still exists. Hard-fails if `references/manifests/LAKE_DATE_IDEA_MANIFEST.json` is missing. That is correct. Do not guess. Do not make a missing manifest block a dated-tree walk.

## Seat note still true

Expert has Drive. Expert does not have `conversation_search`.
Heavy has both. Hop is a doorbell. Lakes are the tape.
