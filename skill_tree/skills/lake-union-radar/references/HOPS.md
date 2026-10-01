# Hop catalog — retrieve only what the index names

Date first. Catalog second. Bytes last.

## The hop that works

```
feel / near / day
        ↓
data/hops/raw_day_folders.json     221 days → raw folder_id
        ↓
leaf_indexes/leaf_YYYY-MM-DD.json  300–3000 bytes → file ids
        ↓
download ONE raw json  OR  peek human/YYYY/MM/weekNN/YYYY-MM-DD_<hex8>.md
        ↓
daily_enriched/YYYY-MM-DD.jsonl    only if day is 2026-05-15 or 2026-06-08..13
```

Proof (2026-01-24, this turn):

| Step | Piece | Bytes | Id |
|---|---|---|---|
| leaf index | `leaf_2026-01-24.json` | 740 | `1FXT4dt6RJJmUzn7uMRgNORXIBsCpUJJJ` |
| raw folder | June-18 raw twin | — | `1bRKNrC9_1ZxFfL9zVwwVMO6AkcAKmI9A` |
| raw hop | `2026-01-24_11dcb864.json` | 26 KB | `1I045a2QPV3FrJo2ZS4llnquhuG91zHcN` |
| skipped | `2026-01-24_a71b629a.json` | 925 KB | `1T4_-G0X301N9FdeJezxahrtkSwIMszOO` |
| human twin | `2026-01-24_a71b629a.md` | 164 KB | `1C3bNF8b-lqKGQVnUON-WO5ckpFo4-KyQ` |

Raw 11dcb864 keys: `conversation.id` = `11dcb864-291f-4d71-b58d-33d0f75253b0`, title AI MisID, create_time 2026-01-24T16:54:09Z. Hex8 join holds.

## What looks split but is not hoppable

**staged_envelopes_nowin.jsonl (360 MB)** and **staged_envelopes.paused-1250.jsonl (331 MB)**
are single JSONL blobs. The 1.5 / 2.0 / 6.8 KB `staged_envelopes.jsonl` files are
pipeline *seeds* (envelope_version 2.0.0 test leaves), not an offset index into
the fat file. No hop without a scan.

**bundle_letta_server.tar.gz.part0001–0022.bin**
are a split tarball of the Letta *server* (~10 MB each, last part 6.9 MB).
Concatenating them rebuilds a gzip archive. They are not conversation shards.
Usable Letta-shaped plane is `daily_enriched` (7 day files, letta_compat_v1).

## What is hoppable and small

- `leaf_indexes` `17ClGCkm-G61on46K4iy0cvvUvutxPVPm` — per-day JSON
- `fleet_run_20260723_044238.json` `1eI9cAKq43f3QYjGDHV6l_EtMysAwb2-9` — 30 KB day→folder
- `daily_enriched` `1mrHidOFf-O5rXxQoA-ZEdFjZDo_yofoC` — 7 files, 6–104 KB
- `obsidian_sieve_lake` `1QAfB5HxkPQEpZ_4zpI_dTCTnWTQVMy9k` — 10 MD notes, wiki only

daily_enriched 2026-05-15 already carries GPS: 5605 Washington Street, Ashtabula
41.874, −80.7819. That plane has coordinates. PAD envelopes do not.

## GitHub / wheels

GitHub user `jameswilsonotr-ship-it`. Repos hold skill territories and inventories
(haist-research-system: "PDF corpus on Drive; repo holds structure"). They do
not hold lake shards. Connector is live. Skill mirror still ODA-WQ-056.

Wheels already in `vendor/`: duckdb 1.5.5, ijson, orjson, geographiclib, haversine.
No new library buys a hop. The hop is Drive folder math.
