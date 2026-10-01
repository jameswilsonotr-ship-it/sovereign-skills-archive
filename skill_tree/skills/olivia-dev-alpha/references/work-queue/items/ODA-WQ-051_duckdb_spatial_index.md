---
id: ODA-WQ-051
title: DuckDB spatial — honest limit plus optional LOAD
status: OPEN
created: 2026-09-14
owner: olivia-dev-alpha
priority: medium
---

# ODA-WQ-051

Screenshot ticket. Official `duckdb/duckdb-spatial` README (v1.5-variegata):

- `INSTALL spatial; LOAD spatial;`
- **No spatial indexing**
- **No spherical lat/lon**

So "Investigate DuckDB spatial indexing" answers: **there is none yet.** Do not advertise R-tree. Radar haversine stays canonical.

Open work when DuckDB is installable in the slice:

1. `LOAD spatial` smoke.
2. `ST_Point(lon, lat)` table of Timeline hits (planar, not WGS84 — label it).
3. Revisit when upstream ships an index + sphere.

FRONT saved at `lake-union-radar/references/github-first-touch/duckdb-spatial-GITHUB-FRONT.md`.
Do not clone the C repo into skills.
