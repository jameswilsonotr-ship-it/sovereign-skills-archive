# GCM-WQ-021 — Exhaustive fake-data smoke / stress

**Status:** SMOKE-PASS 2026-09-11 04:08 EDT
**Script:** `scripts/stress_harness.py`

Plant a synthetic conversation space (fake lake twin, fake miner/extract tars, fake `prod-grok-backend.json`, imagine/plates/secrets). Run sunset dry-run + write. Require ≥8 EXPORT_LOG rows. Tar the run. Safety-gate must block GitHub.

Does not touch a live bubble. Does not slurp KEEP.
