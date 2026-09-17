---
name: lake_batch_vacuum
version: 0.0.1-stub
owner: grok-conversation-miner
walk: keep-lake-query
queue: GCM-WQ-008
status: scripted walker — scripts/lake_batch.py; fixture RAN; no live lake walk
---

# Lake-batch historical vacuum (Idea 4)

Walk dated tree then DELTA. Per day SKIP-EXISTS or NO_TWIN. Never slurp jsonl.

See `references/work-queue/items/GCM-WQ-008_lake_batch_vacuum.md`.
