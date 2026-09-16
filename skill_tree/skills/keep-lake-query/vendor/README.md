# Vendor — keep-lake-query

Installed 2026-09-14 21:16 EDT in this sandbox.

```
python3 -m pip install --no-index --find-links=vendor/wheels duckdb h3
```

Wheels (cp312 manylinux):

- duckdb-1.5.5 21 MB
- h3-4.5.0 1.1 MB

DuckDB community `h3` extension also loaded here (`INSTALL h3 FROM community`) when the box had net. Offline path is the Python `h3` wheel + DuckDB haversine.

Local staged data this pane (not in git):

- `/home/workdir/artifacts/gps/backup_google-timeline-export_2026-07-19.csv` 6.6 MB, 120,938 rows, 2024-12-23 → 2026-06-21
- `/home/workdir/artifacts/lake/envelopes.jsonl` 74 MB, 99,137 leaves
- `/home/workdir/artifacts/timeline/Timeline2_20240622.json` 52 MB

Do not slurp KEEP 227 MB or staged_envelopes_nowin 360 MB. envelopes.jsonl is the 77 MB whoopass plane.
