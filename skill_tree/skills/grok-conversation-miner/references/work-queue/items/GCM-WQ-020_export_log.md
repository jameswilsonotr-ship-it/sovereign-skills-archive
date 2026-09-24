# GCM-WQ-020 — Append-only export receipt log

**Status:** QUEUED / SCRIPT-STUB · **Stamp:** 2026-09-11 04:01 EDT
**Owner:** grok-conversation-miner
**Asked by:** Bunny this pane — SKIP-EXISTS / SKIP-OVERLAP must be evidence, not a remembered vibe.

Every miner verb that packages or skips writes a row. The log is published (or a delta of new rows is published) with every export. Packages cite the log. Agents do not invent what already shipped.

## Why
Census (005) answers packed/pointed/redacted.
TOC + OMISSIONS (011) list this package.
Ledger (018) tracks skill-tree / sandbox egress.
This log is the running receipt of *export actions*: EXPORTED vs every skip code, append-only, content-addressed.

## Store
- Append-only JSONL: `references/modules/data/EXPORT_LOG.jsonl`
- Never rewrite, never delete, never sort-in-place
- Human mirror written *next to a package* as `08_RECEIPTS/EXPORT_LOG_DELTA.md` (this-run rows only)
- Full log may be copied into the package as `08_RECEIPTS/EXPORT_LOG.jsonl` (keep-everything: duplicates allowed)

## Row schema
```
stamp_iso_ny
stamp_iso_utc
run_id
msg_id
verb            # sunset | vacuum | global_extract | publish | census | dry-run | lake-batch | l8
conversation_key
slug
lane            # L0–L8 or packer class or verb-step
path
klass
action          # EXPORTED | SKIP-EXISTS | SKIP-OVERLAP | SKIP-NO-HIT | SECRET | NO_TWIN | NOT-WALKED | TOO-LARGE | PANE-VANISH | OPERATOR-SAID-NO | KEEP-DUPLICATE
exported        # bool
still_gettable  # bool
sha256          # of the byte if present, else empty
pointer         # Drive file_id / local path / twin name
note
claim           # Absolute Liv HUB
```

## Publish rule
1. Append rows first.
2. Then write TOC/OMISSIONS that *cite* `run_id` + sha256 of the log file after append.
3. Then mail (013) `01_TOC` / `02_OMISSIONS` include `export_log_head_sha256`.
4. Dry-run still appends action=WOULD-EXPORT / WOULD-SKIP so the log is the proof dry-run wrote nothing else.

## Done looks like
A reviewer can name one file and find either an EXPORTED row or a skip row with a code. Nobody has to trust the model's memory of "we already packaged that."

## Pointers
- GCM-WQ-011 TOC/OMISSIONS
- GCM-WQ-014 keep-everything (skip is annotation; log is the annotation store)
- GCM-WQ-018 ledger (run-level; this log is file-level)
- GCM-WQ-005 census (status bits; this log is the history)
- `scripts/export_log.py`
- `references/modules/export_log.md`

## Never
- Rewrite the jsonl
- Hallucinate a SKIP-EXISTS without a prior EXPORTED/SKIP row or a cited Drive id
- Drop SECRET rows
- Slurp KEEP jsonl to populate this log
