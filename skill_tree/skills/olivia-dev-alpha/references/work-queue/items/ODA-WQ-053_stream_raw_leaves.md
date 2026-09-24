---
id: ODA-WQ-053
title: Stream raw / leaf_indexes without calling them binary
status: OPEN
created: 2026-09-14
owner: olivia-dev-alpha
priority: high
---

# ODA-WQ-053

Drive marks many shards `application/octet-stream`. Local envelopes + KEEP mid are JSON text (`magic 7b` = `{`).

Script `scripts/peek_shards.py` classifies magic + prints first-n keys.

Still open:

1. Peek one `leaf_YYYY-MM-DD.json` from `leaf_indexes` `17ClGCkm-G61on46K4iy0cvvUvutxPVPm` — join id to human hex.
2. Peek one raw day shard — keys only, no slurp.
3. If first byte is not `{`/`[`, stop and say binary. Do not hexdump the 227 MB tape.
4. Wire `cli.py peek PATH`.
