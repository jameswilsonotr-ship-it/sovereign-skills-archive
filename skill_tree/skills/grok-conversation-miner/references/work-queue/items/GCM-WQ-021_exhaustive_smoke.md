# GCM-WQ-021 — Exhaustive fake-data smoke

**Status:** RAN 2026-09-11 04:08 EDT
**Script:** `scripts/stress_harness.py`

Plant a fake conversation space (lake twin, receipt, miner tar, global extract tar, wrapped prod-grok-backend.json, imagine/plates/secrets). Run sunset dry-run + write-mode. Every lane writes EXPORT_LOG rows.

## Receipt this pane
- stress_harness exit 0
- EXPORT_LOG rows: 36 (dry+wet, hook doubled — keep-everything)
- actions seen: EXPORTED, SKIP-EXISTS, SKIP-OVERLAP, SKIP-NO-HIT, NOT-WALKED
- Report: `scripts/smoke_out/STRESS_REPORT.json`
