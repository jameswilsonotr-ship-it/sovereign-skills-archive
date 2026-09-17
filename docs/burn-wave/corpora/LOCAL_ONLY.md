# Large corpora live on box only

The multi-MB offline corpora are **not** committed to git (size). They remain at:

`/home/box/workspace/burn-wave/corpora/`

Contents (see MANIFEST.json):
- offline_calls_2500.jsonl (2500)
- health_load_5k.jsonl (5000)
- wq_to_linear_map.json (320 atoms)
- duckdb_calllog/call_log.jsonl (800)
- connectors/payloads/ (200) + payloads_wave2/ (400)

Validate: `python3 scripts/validate_corpora.py` from burn-wave root.
