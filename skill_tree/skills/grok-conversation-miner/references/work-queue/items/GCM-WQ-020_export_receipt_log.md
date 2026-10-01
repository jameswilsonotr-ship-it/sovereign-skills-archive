# GCM-WQ-020 — Append-only export receipt log

**Status:** QUEUED / SCRIPT-STAGED · **Stamp:** 2026-09-11 04:01 EDT
**Owner:** grok-conversation-miner
**Why:** SKIP-EXISTS / SKIP-OVERLAP / "already packaged" must be a receipt, not a vibe. Every harvest publishes what shipped and what did not. Exports cite this log so later panes cannot hallucinate the skip table.

## What it is
An append-only log written **every** miner verb that parks or extracts bytes (sunset, vacuum, publish, global extract, lake-batch, L8 recon).

Two surfaces, same rows:
- machine: `references/modules/data/EXPORT_LOG.jsonl` (never rewritten, never upserted)
- human: `references/modules/data/EXPORT_LOG.md` (append a dated section each run)

A copy (or a delta slice) rides inside every package as `08_RECEIPTS/EXPORT_LOG.jsonl` + cite block in `MANIFEST.md` / `TOC.md` / `OMISSIONS.md`.

## Schema (one json object per line)
- `seq` — monotonic integer
- `stamp_utc` / `stamp_ny`
- `run_id`
- `verb` — sunset | vacuum | publish | global-extract | lake-batch | export-recon | smoke
- `conversation_key` — `YYYY-MM-DD_slug` or date
- `lane` — L0–L8 or packer class
- `path` — fixture or real path
- `class` — lake_twin | receipt | tar | imagine | video | plates | secret | other
- `action` — EXPORTED | SKIP-EXISTS | SKIP-OVERLAP | SECRET | NO_TWIN | NOT-WALKED | OPERATOR-SAID-NO | WOULD-RAN | FAIL
- `exported` — true only if bytes actually left the pane this run
- `sha256` — payload hash if present
- `pointer_id` — Drive / fake ACK / none
- `still_gettable` — can a later run still fetch it
- `prev_row_sha256` / `row_sha256` — hash chain so silent edits show up

## Rules
- Append only. `jsonl_upsert` is forbidden on this file (that is 018's ledger).
- A SKIP row is mandatory. Quiet skip is a bug.
- Dry-run writes WOULD-RAN / WOULD-SKIP rows to a *fixture* log, not the live skill log, unless `--live-log` is explicit.
- Cite the log head (`seq`, `row_sha256`) from every MANIFEST.
- Keep-everything (014): SKIP is a row + the duplicate may still EXPORTED on another row.
- Census (005) answers packed/pointed/redacted. This log answers *what left and what did not*. Do not collapse them.

## Pointers
- GCM-WQ-011 TOC + OMISSIONS
- GCM-WQ-014 keep-everything
- GCM-WQ-018 skill-tree ledger (different file; 018 may upsert by run_id)
- `references/prompt_sunset.md` lane cards
- `scripts/export_log.py`

## Never
- Rewrite the jsonl
- Hallucinate a skip without a row
- Slurp KEEP jsonl into this log
- Treat xAI export as the receipt (L8 is recon; this log is miner SSoT for *our* packages)

## Smoke
`python3 scripts/export_log.py` self-test + `python3 scripts/test_export_log.py`
