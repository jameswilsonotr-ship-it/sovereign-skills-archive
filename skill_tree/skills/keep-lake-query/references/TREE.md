# Human Lake folder tree — walked 2026-09-14 20:40 EDT

Label is the query key. IDs are SSoT. Do not pick folders by name — `pre_extract` and `valerie_out` both have twins.

```
#full.out.test.data / valerie_out
17q1bLJGievsK5tMVJWGRi0AUmVUenD2L
│
├── daily_enriched/                         1mrHidOFf-O5rXxQoA-ZEdFjZDo_yofoC
│     sibling of pre_extract, not a child
│     peek: 7 jsonl days only (2026-05-15 + 2026-06-08..13). 6–104 KB. Thin Letta-shaped pilot.
│
├── master_tree.jsonl                       1Oe8JWPs5ip7Oxl8KkfMIM90HZFnTFwN3  259 KB
│     octet-stream catalog. do not slurp in voice.
│
└── pre_extract/                            1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58
      June 18 09:45Z canonical. Name is NOT unique. This ID is.
      │
      ├── human/                            1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL   VOICE SSoT
      │     └── 2025/                       1XVLJszOOGzxhTmFnzUfg3YIW1YI0m424
      │           └── 10/                   1FBy2tfnAPFlp48WSGaGkkl7PrUyrksOR
      │                 └── week41/         1DtrppE-a_ohmZZniW9aqU6yzJZwEQWhF
      │                       └── 2025-10-08/  1F-e1Aut4Brv41Addi3Ayuu4I_QVcikGe
      │                             *.md   grain = year/month/weekNN/YYYY-MM-DD
      │     └── 2026/                       1Wsj1cllNTR9XyjF7QsPw8LPbjClr_qx2
      │           months 01–06 present
      │     peek: 2025-10-08 has 3 md (2.7K / 64K / 296K). Turn-pair **human** / **assistant**.
      │
      ├── ingest/                           1hMTb_3RbP4eb6lCs96YePIhqY1KCdNmi
      │     same year/month/week walk as human. Obsidian/tag twin. Peek titles, do not slurp.
      │
      ├── raw/                              1obfXkm_NTvMZYOwws-fW5kr_Nvt9Gjhy
      │     machine JSON shards. FORBIDDEN slurp.
      │
      ├── code_blocks/                      1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3
      │     ├── system_prompts/             1tV-xwbq6r3c6y3-v6n8yh2VhrneBgmvt
      │     │     └── 2025/ + 2026/         year then month. extracted ``` prompt fences
      │     ├── images/                     1znaTBsw-RR4AYOmdZ_H6wqV-y1mTsrYt
      │     │     └── 2025/ + 2026/         extracted imagine / image fences
      │     └── other/                      1o1yhV45Rqze4ygLQF9DNynVj4PaL3E7C
      │           leftover fences (scripts, json, mixed)
      │     verb: blocks. STILL UNWALKED.
      │
      ├── graph_entities/                   1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm
      │     LIVE LIST 2026-09-14: EMPTY. Zero files. Graphiti seed named, never filled.
      │
      ├── gps_enrichment/                   1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq
      │     NOT a dated convo tree. Timeline dumps + already-flat tables.
      │     ├── Timeline (3).json           1Kmn-TJIsWQNtIwAmgm944xzn8KnV_EJW  43.6 MB
      │     ├── backup_google-timeline-export_2026-07-19.csv   6.8 MB
      │     ├── backup_google-timeline-export_2026-07-19.gpx   8.5 MB
      │     ├── backup_google-timeline-export_2026-07-19.kml   3.0 MB
      │     ├── corridor_runs.csv + away_only + summary.json
      │     ├── home_geofence_and_corridors.json + home_stays.csv
      │     ├── GPS_CONVERSATION_JOIN_PLAYBOOK.md  1-VeLckWhuGwzWkOWBzWnVxuUD9UAWzME
      │     ├── gap_map_seed.json + day_leaf_stats.csv
      │     └── how_we_met_october_2025.zip
      │
      ├── leaf_indexes/                     17ClGCkm-G61on46K4iy0cvvUvutxPVPm
      │     FLAT. leaf_YYYY-MM-DD.json (~0.3–3 KB). Often DUPLICATE pairs from two fleet runs.
      │     + fleet_checkpoint_YYYY_MM.json stubs ~81 B
      │
      ├── checksums/                        1DdcdK19-o283fVkyUZ516Fg5HK4WW86q
      │     checksums_day_YYYY-MM-DD_HHMMSS.json ~0.4–3 KB. Often twins (two fleet passes).
      │
      ├── microchunks/                      1GcB3eFmMJAoh_ln1qka-sprGXM_z0Ppe
      │     ≤85 KB bins. skip in Expert / voice.
      │
      └── colab_recon_output/               1oBD5tdvFtO2ZtR8FZcvJpa4XzFDnFXEQ
            recon_priority_days_20260723_033125.json 41 KB
```

## Root files sitting on pre_extract (not folders)

- `GOOGLE_TIMELINE_FORMAT_AND_DATE_RANGES.md` `1DVaLWnjc9ALcFFyATl5lImC-jDbKANOV` — schema lock
- `ADMIRAL_ENRICHMENT_PLAYBOOK_v2.md` `1L48fUvSAyMmhQ2O6T3PIDTVhaqfBNXmi`
- `Pre-Extraction Folder Index` Doc `1Gw4CKPCJvzqtXnh_UVTCfqkQQYIb7kGo_TFI-ZiRuwU` (stale: listed 8 LIVE June days; tree grew later)
- `ingest_catalog.json` 100 KB
- `pre_extract_file_folder_registry` v1 / v2 / v2.1
- fleet_worker + leaf_index_builder + checksum_builder notebooks v0.1–v0.6
- `day_inventory_2026-06-01` … `06-13`.json
- `SPARK_MICROCHUNK_README.md`

## Siblings / other lakes (not under this parent)

| What | Id | Rule |
|---|---|---|
| KEEP master | `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` | FORBIDDEN slurp 227 MB |
| keep mid | `18rdthMThvCUZBBU4qaPzs1-YrxUU3xfO` | 1,697 session titles |
| pad envelopes | `1hnaVFAh8kfKV5ImOCX2t1ttWfITOoIh1` | 99,137 leaves. date-join only |
| doorbell | `1w4toLxJW5DbiUTcPNw8CqitTko0LvsV_` | sit-pack / from-vesper |
| dated-tree human (same as above) | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` | voice words |
| Aug 17 flat twin | `1DAfH3lTNtYtgLLEHM67AYJcGrnOGdIyt` | uuid.md |

## Peek rules

- Words on a date → `human` year/month/week/day. Path IS the date.
- Tags → `ingest` same walk.
- What files exist that day → `leaf_indexes` exact_name `leaf_YYYY-MM-DD.json`, then join. Watch duplicates.
- Where was the truck → `gps_enrichment` CSV first, JSON second. Not the week folders.
- Prompts squeezed out of chats → `code_blocks/system_prompts`.
- Graphiti seed → `graph_entities` is empty. Do not pretend it is full.
- Never open `raw`, `microchunks`, KEEP master, or `master_tree.jsonl` in a voice turn.
