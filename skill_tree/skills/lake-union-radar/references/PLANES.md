# Export planes

Folder names are the passes. Canonical parent `#full.out.test.data` `17q1bLJGievsK5tMVJWGRi0AUmVUenD2L` → `pre_extract` `1U4tUEvlDdpip8IsJsW6TIIyBhhIAiP58`.

| Plane | Id | Grain | This skill |
|---|---|---|---|
| human | `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL` | dated MD | peek via keep-lake-query |
| ingest | `1hMTb_3RbP4eb6lCs96YePIhqY1KCdNmi` | Obsidian twin | peek |
| raw | `1obfXkm_NTvMZYOwws-fW5kr_Nvt9Gjhy` | shards | FORBIDDEN slurp |
| gps_enrichment | `1sdllodWD0iv8Os4aFNOtdS5LYpbveVXq` | CSV/GPX + corridors | radar + explode |
| pad envelopes | `1hnaVFAh8kfKV5ImOCX2t1ttWfITOoIh1` | 99,137 leaves | pad / day / union |
| KEEP master | `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH` | 227 MB | FORBIDDEN |
| keep mid | `18rdthMThvCUZBBU4qaPzs1-YrxUU3xfO` | 1,697 sessions | embed + day |
| daily_enriched | `1mrHidOFf-O5rXxQoA-ZEdFjZDo_yofoC` | letta_compat_v1 | thin dates only |
| code_blocks | `1UV-bw3qI2ScslqNp8M5tfK6LRQTQrlW3` | system_prompts / images / other by year | peek via `blocks` — do not slurp |
| graph_entities | `1n8gIhenlIBBWbc_xWV5IbWN9aloGynxm` | triples | catalog only |
| obsidian vaults | several name-twins | notes / MOC | catalog only |
| leaf_indexes | `17ClGCkm-G61on46K4iy0cvvUvutxPVPm` | per-day 0.3–3 KB | **hop step 3** |
| fleet_run | `1eI9cAKq43f3QYjGDHV6l_EtMysAwb2-9` | 221 days → raw folder | **hop step 2** |
| staged seeds | `1PHwxrSVCV1nh0PiQymo3NXqHZb333w0R` | 1.5–7 KB test leaves | sample only |
| staged nowin | `15Nz1UrOT_OmjV6Q0lW61Pgmx971DKZ1-` | 360 MB one blob | FORBIDDEN (no offset index) |
| letta part bins | `bundle_letta_server.tar.gz.partNNNN.bin` | ~10 MB gzip slices | FORBIDDEN concat |

Letta vault note (2026-08-16) — design only. "No Letta, no Drive upload."
Usable Letta-shaped plane is daily_enriched. Part bins are the *server* tarball.

Hop recipe: `references/HOPS.md`. Verb: `cli.py hop day 2026-01-24`.
