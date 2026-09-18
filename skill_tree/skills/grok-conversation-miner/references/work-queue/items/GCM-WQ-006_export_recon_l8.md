# GCM-WQ-006 — xAI export recon lane L8 (Idea 2)

**Status:** SMOKE-PASS · **Stamp:** 2026-09-10 20:44 MDT
**Owner:** grok-conversation-miner
**Protocol stub:** `references/modules/export_recon_l8.md`

New sunset lane. Does **not** run on default `sunset`. Flag: `sunset export-recon` / present zip.

## Ingest
1. Detect accounts.x.ai zip or unpacked `prod-grok-backend.json` + UUID asset tree
2. Index conversation UUIDs + asset UUIDs
3. Diff vs lake dated tree + sunset twins
4. Emit `EXPORT_RECON_<date>.md`: IN_LAKE / IN_EXPORT_ONLY / IN_SUNSET_ONLY / ASSET_MISSING

## Skill-tree pointers
- system-roadmap `references/etl-xai-export-designs-2026/` (README, COMPARATIVE_SUMMARY, MINING_LOG)
- system-roadmap `references/etl-xai-export-designs-2026-drive/`
- keep-lake-query DELTA window 2026-08-11…2026-09-06
- grok-conversation-miner `references/prompt_sunset.md` (add L8 after L7, skip-on-default)
- Do not rebuild ChronologyArc inside this skill

## Never
- Treat export zip as SSoT
- Upload secrets / cookies / tskey
- GitHub Contents API for the zip (safety gate)

## RESULT 2026-09-11: scripts/export_recon.py SMOKE-PASS.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/export_recon.py. Fixture IN_LAKE / IN_EXPORT_ONLY / IN_SUNSET_ONLY. No accounts.x.ai zip ingested.
