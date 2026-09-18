# War chest — use-as-is vs transform

Steel-first on K15 / Jetson. VULTR second. Do not re-ingest the 1.5–1.7 GB conversation lake to fix a geo parse miss. Geo is a parallel layer.

## Vendor wheels (this box, 2026-09-14)

`keep-lake-query/vendor/wheels` and `lake-union-radar/vendor/wheels`.

```
python3 -m pip install --no-index --find-links=vendor/wheels duckdb h3
```

duckdb 1.5.5 (21 MB) + h3 4.5.0 (1.1 MB) installed here. Community DuckDB `h3` extension loaded once. Offline fallback: Python h3 + SQL haversine.

Staged local (not KEEP):

- GPS CSV 6.6 MB `artifacts/gps/backup_google-timeline-export_2026-07-19.csv` (120,938 rows)
- envelopes.jsonl 74 MB `artifacts/lake/envelopes.jsonl` (99,137 leaves) — the 77 MB PAD plane
- Timeline JSON 52 MB `artifacts/timeline/Timeline2_20240622.json`

CSV is thinner than JSON path crumbs. Pittsburgh 0.259 mi is in the JSON on 2025-08-22; CSV nearest that calendar day is ~43 mi. Do not treat the CSV as a complete twin of Timeline (2).

## Geo encoding lock (why the dock looks 1.4 mi out)

Our Timeline files are **Android on-device `semanticSegments`**, not legacy Takeout `timelineObjects` / E7.

| Shape | Encoding | Example |
|---|---|---|
| Android on-device | degree-sign string | `"latLng": "43.6268685°, -88.4446116°"` |
| iOS on-device | geo URI | `"geo:43.6268685,-88.4446116"` |
| Legacy Takeout | integer / 1e7 | `"latitudeE7": 436268685` |

Traps:

1. A regex that only hunts `°` misses `geo:` and E7 and `activity.start`.
2. `visit.topCandidate.placeId` snaps to Love's / US-151, not the Quad apron.
3. `timelinePath` is a sampled breadcrumb. Phone asleep on the dock → visit object, sparse path.
4. `activity.topCandidate` `IN_PASSENGER_VEHICLE` at 70 mph is a flyby, not a dwell.
5. Takeout E7 western longs sometimes wrap unsigned 32-bit (+2³²) and land on the wrong continent.
6. `startTime` already carries the offset (`-05:00`). A second TZ shift double-moves the day.

Sources: time-mile.com/guides/timeline-json-format, Dawarich Timeline export guide, our own `GOOGLE_TIMELINE_FORMAT_AND_DATE_RANGES.md` `1DVaLWnjc9ALcFFyATl5lImC-jDbKANOV`.

CSV already sitting in the lake: `backup_google-timeline-export_2026-07-19.csv` 6.8 MB, ~17,685 pts, 2024-12-23 → 2026-06-21. Try that table before declaring the JSON corrupt.

## Use as-is (no ETL)

| Plane | How |
|---|---|
| human `*.md` | keep-lake-query walk / peek / filter inside one month folder |
| leaf_indexes JSON | day → file_id catalog. Do not open raw. |
| checksums JSON | sha compare before any re-ingest |
| gps CSV | `pandas.read_csv` |
| gps GPX/KML | geopandas |
| pad envelopes.jsonl | stream lines, live tertile bin |
| code_blocks/system_prompts | walk year/month like human, peek titles |
| keep mid titles | TF-IDF / embed verb already in lake-union-radar |

## Transform — local steel first

### 1. DuckDB + spatial + H3  (do this first)

- `duckdb` + `INSTALL spatial; LOAD spatial;`
- community `h3` extension (isaacbrodsky/h3-duckdb)
- Point-in-ring on official Quad aprons without loading 146k pts into RAM
- Fits K15. No docker.

### 2. MovingPandas StopDetector  (honest docks)

- GitHub `movingpandas/movingpandas`
- Install from **conda-forge**, not pip
- `TrajectoryStopDetector.get_stop_points(max_diameter=meters, min_duration=timedelta(minutes=10))`
- Pair with `ObservationGapSplitter` for battery-sleep gaps
- This is the “was she parked or flying by” instrument

### 3. scikit-mobility / trackintel

- TrajDataFrame + DBSCAN stay clusters
- trackintel staypoints as a second opinion next to MovingPandas
- Contrast columns, do not pick a winner in the first pass

### 4. Graphiti  (bi-temporal graph — second, not first)

- GitHub `getzep/graphiti` · pip `graphiti-core`
- Edges carry four clocks: `valid_at` / `invalid_at` (world) + `created_at` / `expired_at` (ingest)
- That is the “what did we know on Christmas Eve” vs “what was true on Christmas Eve” split
- Backends: Neo4j docker, FalkorDB (lighter), Kuzu
- Paper trail: Zep / Graphiti temporal model docs
- Seed plane `graph_entities/` is **empty**. Fill from human titles + code_blocks, or mark the plane dead.
- VULTR: FalkorDB or Neo4j container. Not on the Jetson first.

### 5. Poor-man's vectors upgrade

- lake-union-radar `embed` is sparse TF-IDF
- Next: local LanceDB / sqlite-vec on keep-mid titles + code_block first lines
- We already had a 480k Lance experiment Dec 2025. Do not rebuild KEEP to get it.

### 6. Timeline parsers (union, not one blessed)

- Dawarich / time-mile field maps
- `timelinize/timelinize` on-device Android + iOS decoder
- `BrandonML/google-maps-timeline-converter` old↔new
- Do **not** use a Takeout-only E7 parser as the only reader

### 7. Event stream / warehouse (later)

- Google Temporian for multi-rate event streams (PAD daily + GPS seconds)
- pg_bitemporal only if we stand Postgres on VULTR
- Arctic BitemporalStore only if we stay document-local

## What is NOT a reason to re-ingest 1.7 GB

- JSON regex missed docks but CSV has the points
- leaf_index duplicate pairs (two fleet runs, same day)
- checksum twins (ingest transaction time ≠ event day)
- Timeline (3) starts 2025-12-31 so it cannot see 2025 Quad — that is a file window, not corruption
- lake human tree starts 2025-10-08 so pre-October GPS has nothing to join

Re-ingest is for: checksum mismatch against raw, or human `.md` bodies that do not match raw JSON for a named day. Run KLQ-WQ-019 first.

## VULTR vs steel

| Job | Where |
|---|---|
| DuckDB + H3 + CSV dock rings | K15 now |
| MovingPandas StopDetector | K15 now (conda env) |
| Graphiti + FalkorDB | VULTR when memory manager is up |
| Moshi voice | not with Letta on the same small box. Separate later. |
| Full KEEP slurp | never |
