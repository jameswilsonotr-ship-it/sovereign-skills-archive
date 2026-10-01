# duckdb/duckdb-spatial — FRONT (ODA-WQ-036)

Captured 2026-09-14 from https://github.com/duckdb/duckdb-spatial

- Stars: 708 · language C · default branch `v1.5-variegata`
- License: MIT
- About rail: empty on the page; README is the manual
- Install: `INSTALL spatial; LOAD spatial;`
- Model: Simple Features `GEOMETRY` + DuckDB-native columnar types
- Docs: `docs/functions.md`, `docs/example.md`
- **Limitations written in the README (do not wish these away):**
  - No spherical / lat-lon geometry
  - **No spatial indexing (no R-tree)**
- Status: still labeled work-in-progress; storage format may change

Import decision: **do not vendor the C repo into the skill tree.** Optional LOAD when DuckDB is present. Radar stays haversine until spherical + index exist.
