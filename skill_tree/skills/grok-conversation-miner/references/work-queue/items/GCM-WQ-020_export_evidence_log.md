# GCM-WQ-020 — Append-only export evidence log

**Status:** QUEUED / SCRIPT-STUB · **Stamp:** 2026-09-11 04:01 EDT
**Owner:** grok-conversation-miner
**Asked by:** Bunny this pane — SKIP-EXISTS must be a receipt, not a vibe

Sunset already prints RAN / SKIP-EXISTS / SKIP-OVERLAP / SKIP-NO-HIT. Those cards die with the pane unless they land in a published, append-only log that every export cites.

## What this is
A running evidence file of what *was* exported and what *was not*, for every miner verb.

## Store
- Append-only: `references/modules/data/EXPORT_LOG.jsonl` (never rewrite a prior line)
- Human mirror: `references/modules/data/EXPORT_LOG.md` (regenerated FROM jsonl, not the other way around)
- Per-package copy: `08_RECEIPTS/EXPORT_LOG.tail.jsonl` + sha256 of the full log in MANIFEST / TOC
- Mail: `02_OMISSIONS` and `01_TOC` cite `log_sha256` + last run_id

## Schema (one jsonl object per action)
```
stamp_utc, stamp_ny, run_id, verb, conversation_key, slug, lane,
path, class, action, exported, skip_code, sha256, bytes, pointer,
still_gettable, note, claim
```

`action` enum:
EXPORTED | SKIP-EXISTS | SKIP-OVERLAP | SKIP-NO-HIT | SKIP-NO-SHARD |
SECRET | NO_TWIN | NOT-WALKED | TOO-LARGE | PANE-VANISH | OPERATOR-SAID-NO |
KEEP-DUPLICATE

## Rules
1. Every publish / vacuum / extract / sunset / census / dry-run / smoke writes at least one row, including all-SKIP runs.
2. Do not delete or edit old rows. Correction = new row with `note: corrects <run_id>`.
3. Hallucinated skip is a bug. If the log does not contain the skip, the package does not get to claim it.
4. 011 TOC/OMISSIONS cite this log. 014 skip-annotation writes here. 018 ledger may point here; this log is export evidence, ledger is skill-tree conversation tracking.
5. Never slurp KEEP `homogenized_shards.jsonl` to build this log.

## Done looks like
A reviewer can name a file and find either an EXPORTED row with sha256 or a skip row with a reason code and pointer. Smoke proves append-only (rewrite attempt fails or is refused).

## Pointers
- `scripts/export_log.py`
- `references/modules/export_log.md`
- GCM-WQ-011, 014, 018
- `references/prompt_sunset.md` lane cards
- cilia-bus always-mail 013
