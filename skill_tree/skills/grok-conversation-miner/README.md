# grok-conversation-miner

**Status**: Active · scripts 0.2.x · sunset protocol 0.1.0  
**Owner**: Absolute Liv HUB  
**Updated**: 2026-09-11 04:08 EDT

## What this is
Mine prompts, bibles, sandbox files, and skill-tree deltas out of Grok conversations. Park them on Google Drive. Keep an append-only receipt of what shipped and what did not, so you can delete a bubble without losing the pane.

## Quick start
```
# menu
read references/help.md

# fixture smoke (no live bubble)
python3 scripts/sunset_smoke.py
python3 scripts/test_gcm.py

# fake-data stress (dry-run + write + tar + export log)
python3 scripts/stress_harness.py

# dry-run sunset against a planted space
python3 scripts/sunset_dry_run.py --flag dry-run
```

Live verbs (say them in chat, do not run until you mean it):
- `help` · `publish` · `historical mine` · `refactor` · `deep mine` · `vacuum` · `global extract` · `sunset` / `sunset dry-run`
- queued: `census` · `sunset export-recon` · `vacuum lake YYYY-MM`

## Why xAI "download your data" is not enough
accounts.x.ai/data gives `prod-grok-backend.json` + UUID assets. It does **not** reliably carry:
- Imagine renders sitting in this pane
- video blobs
- plate folders
- skill files written under `/home/workdir/.grok/skills/`
- Cilia receipts
- work-queue markdown minted mid-session

Sunset L4 + packers + EXPORT_LOG exist so those bytes leave the sandbox *before* the bubble dies.

## Do not
- Slurp KEEP `homogenized_shards.jsonl` (227 MB). Query the dated markdown tree instead.
- GitHub-Contents a tar/binary/>800 KB
- Treat SKIP-EXISTS as "we already did it" unless EXPORT_LOG has the row

## Queue
`references/work-queue/WORK_QUEUE.md` (GCM-WQ-001 … 022)
