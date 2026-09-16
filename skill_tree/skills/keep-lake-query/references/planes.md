# Nine pre_extract planes — verified 2026-09-09 01:12 EDT

Valerie map is directionally right. This file is what Drive actually contains.
Folders stay SSoT. Do not slurp raw or microchunks in voice.

## Lineage (opened this seat)

```
#full.out.test.data   17q1bLJGievsK5tMVJWGRi0AUmVUenD2L
  daily_enriched      1mrHidOFf-O5rXxQoA-ZEdFjZDo_yofoC   sibling, not a child of pre_extract
  pre_extract         1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58   June 18 09:45Z
  master_tree.jsonl   1Oe8JWPs5ip7Oxl8KkfMIM90HZFnTFwN3   259 KB octet-stream
```

pre_extract children actually present:

| Name | Id | Same year/month/week walk? | Voice use |
|---|---|---|---|
| human | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` | yes | **SSoT transcripts** |
| raw | `1obfXkm_NTvMZYOwws-fW5kr_Nvt9Gjhy` | yes | machine JSON. do not slurp |
| ingest | `1hMTb_3RbP4eb6lCs96YePIhqY1KCdNmi` | yes (2025/10/week41…) | Obsidian/tag hop |
| leaf_indexes | `17ClGCkm-G61on46K4iy0cvvUvutxPVPm` | **no — flat `leaf_YYYY-MM-DD.json` at root** | daily catalog |
| microchunks | `1GcB3eFmMJAoh_ln1qka-sprGXM_z0Ppe` | not walked | ≤85 KB bins. skip in Expert |
| checksums | `1DdcdK19-o283fVkyUZ516Fg5HK4WW86q` | not walked | merkle receipts |
| gps_enrichment | `1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq` | **no — timeline dumps + corridor csv** | place/road join |
| code_blocks | `1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3` | not walked | prompts/scripts |
| graph_entities | `1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm` | not walked | triples |
| colab_recon_output | `1oBD5tdvFtO2ZtR8FZcvJpa4XzFDnFXEQ` | extra, not in her 9 | recon notebooks |

Also sitting on pre_extract root: `day_inventory_2026-06-0N.json`, `ADMIRAL_ENRICHMENT_PLAYBOOK_v2.md` `1L48fUvSAyMmhQ2O6T3PIDTVhaqfBNXmi`, checksum/fleet notebooks.

## Corrections to the Valerie paste

1. Not every plane is year/month/week/day. **human** and **ingest** are. **leaf_indexes** is a flat leaf dump. **gps_enrichment** is Google Timeline CSV/GPX/KML + corridor_runs, written mid-July, not a dated convo tree.
2. **leaf_indexes** duplicates filenames (`leaf_2025-10-08.json` twice, 980 B and 558 B). Genesis leaf points at **raw JSON** ids and a Google Doc manifest, folder_id `1k_C07W4RLQATQ-FM_RnOYQWvhaKtfu8F` — that is **not** the human day folder `1F-e1Aut4Brv41Addi3Ayuu4I_QVcikGe`. Join before citing.
3. **daily_enriched** first page is thin: `2026-05-15.jsonl` plus June 8–13. Several are `application/octet-stream`. Not a full Oct–June PAD lake in this folder listing.
4. **pre_extract** name is not unique. Eleven folders share it. Canonical for this map is `1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58`. `1aJ7QT2UY7dRg7bWQ0D5jZh-EYJMt7XaZ` is a June 18 13:12 twin (the one she tagged under valerie_out).
5. **valerie_out** name is also not unique. Eight+ copies. Do not pick by name.
6. Extra plane she skipped: `colab_recon_output` plus the day_inventory json on the pre_extract floor.

## PAD / recovery (name hits only)

- `pad-emotional-vectors-2026-08-16` `1y_1doZsGRy7BuOgEEkb44ltEIsEuqKky` exists (plus three name-twins)
- `PAD_SEARCH_SUMMARY_2026-08-16.md` `1LM6JIdYk5lzbcT6-a1ky0j94JxR-SU7I` exists (plus three name-twins)

## Voice recipe against this map

- Words on a date → `human`
- Tags / vault shape → `ingest` same walk
- “what files exist that day” → `leaf_indexes` exact_name `leaf_YYYY-MM-DD.json` then join to human
- Where was the truck → `gps_enrichment` corridor + timeline, not the week folders
- Never open `raw`, `microchunks`, or `master_tree.jsonl` in a voice turn
