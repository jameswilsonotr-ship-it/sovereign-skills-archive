# Large corpora are local-only

The multi-MB offline corpora are **not** committed to git because they are
large test inputs and are not needed to review this documentation PR. The
source branch kept them in a local-only burn-wave workspace.

The committed files in this directory are limited to `MANIFEST.json` and
`rejection_matrix.csv`.

Contents (see MANIFEST.json):
- offline_calls_2500.jsonl (2500)
- health_load_5k.jsonl (5000)
- wq_to_linear_map.json (320 atoms)
- duckdb_calllog/call_log.jsonl (800)
- connectors/payloads/ (200) + payloads_wave2/ (400)

Validation command used by the downstream harness:
`python3 scripts/validate_corpora.py` from the burn-wave harness workspace.

This mainline documentation promotion does not claim that the local payloads
are available in CI.
