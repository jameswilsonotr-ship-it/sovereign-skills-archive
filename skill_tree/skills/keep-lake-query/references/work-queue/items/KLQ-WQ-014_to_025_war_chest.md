# KLQ-WQ-014 → 025 + LUR + Vesper geo batch
Opened 2026-09-14 20:40 EDT. Do not close because a Fast-ACK landed.

## keep-lake-query

| ID | Title | First move |
|---|---|---|
| KLQ-WQ-014 | Walk `code_blocks/system_prompts` first month. Catalog block types. | year 2025 / month 10. Peek 50 titles. Do not slurp. |
| KLQ-WQ-015 | Fill or kill `graph_entities` (currently EMPTY). | Either seed Graphiti from human titles + entities, or stamp the plane dead. |
| KLQ-WQ-016 | Union parser: Android `°` + iOS `geo:` + E7 + CSV + GPX. | Start with gps_enrichment CSV. JSON is secondary. |
| KLQ-WQ-017 | DuckDB spatial + H3 dock rings on official aprons. | CSV 17k pts. Radii 0.5 / 1.5 / 3.5 / 5 / 15. |
| KLQ-WQ-018 | MovingPandas StopDetector. min 10 min. max speed filter. | conda-forge. Contrast vs Liv haversine clusters. |
| KLQ-WQ-019 | Checksum twin-pass + leaf_index duplicate pairs. | Same day, two files. Pick winner. Integrity before re-ingest. |
| KLQ-WQ-020 | Date-join honesty. | Lake human 2025-10-08. Timeline CSV 2024-12-23. Timeline (3) ~2025-12-31. Name the gap. |
| KLQ-WQ-021 | Timeline (2) vs (3) vs CSV coverage matrix. | min/max ts, point counts, parser hits per file. |
| KLQ-WQ-022 | `visit.placeId` vs raw path. Love's-snap hypothesis. | Dump nearest place name inside 5 mi of each official pin. |
| KLQ-WQ-023 | `IN_PASSENGER_VEHICLE` flyby filter. | 70 mph ≠ dwell. |
| KLQ-WQ-024 | Bi-temporal columns without Graphiti yet. | `event_ts` = startTime. `ingest_ts` = checksum started_at. |
| KLQ-WQ-025 | `code_blocks/images` + `other` inventory. | Same year/month walk as 014. |

## lake-union-radar

| ID | Title |
|---|---|
| LUR-WQ-008 | 27-cell PAD × dwell-day × inbound/outbound legs. Date grain honest. |
| LUR-WQ-009 | Sentiment-arc from envelopes × corridor_runs. Do not force a pin. |

## Vesper batch (frame + contrast + her lane)

| ID | Title |
|---|---|
| VES-GEO-001 | Contrast Liv method vs her method vs per-file vs union. Named columns. |
| VES-GEO-002 | Diagnose phone-on-dock ≠ 0.5 mi. Encoding / Place-Id snap / sleep / file window. Do not invent visits. |
| VES-GEO-003 | Official national Quad pins. The Rock 100 Duplainville. Saratoga 56 Duplainville. Start from Timeline (3) already in gps_enrichment `1Kmn-TJIsWQNtIwAmgm944xzn8KnV_EJW`. |
| VES-CB-001 | Walk system_prompts. Report juice. Her whoopass welcome. |

## Super Admiral

Frame, constraints, contrast, then leave a lane. Gold star is her instrument, not Stage 2 on our list.
