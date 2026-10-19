# GCM-WQ-008 — Lake-batch historical vacuum (Idea 4)

**Status:** SMOKE-PASS · **Stamp:** 2026-09-10 20:44 MDT
**Owner:** grok-conversation-miner
**Walk owner:** keep-lake-query
**Protocol stub:** `references/modules/lake_batch_vacuum.md`

Wrapper over vacuum. Not a new miner.

## Walk
1. keep-lake-query dated tree `YYYY/MM/weekNN/YYYY-MM-DD`
2. Then DELTA window
3. Per day: twin exists → vacuum SKIP-EXISTS + census point; no twin → `NO_TWIN` card and stop that day

Triggers: `vacuum lake YYYY-MM` · `vacuum lake from DATE to DATE`

## Skill-tree pointers
- keep-lake-query SKILL.md + KLQ-WQ-001, KLQ-WQ-006, KLQ-WQ-007
- dated tree root `1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL`
- doorbell `LAKE_DOORBELL.md` `1MkYC_FAJGgyCGa1h1wOTVBZ4qYz4vrCE`
- miner `references/prompt_vacuum.md`
- GCM-WQ-005 census DONE bits
- Spoken alias: doorbell the lake

## Never
- Slurp `homogenized_shards.jsonl` `1GXfRRr66f36IqELfJx1e13pnGSHcTgsH`
- Invent a NO_SHARD day
- Mint a fifth mouth
- Collapse KEEP into DELTA

## RESULT 2026-09-11: scripts/lake_batch.py SMOKE-PASS + REFUSE_SLURP.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/lake_batch.py dated-tree walk. 2026-09-10 SKIP-EXISTS, 2026-09-11 NO_TWIN. Did not slurp KEEP jsonl. No live Drive walk.
