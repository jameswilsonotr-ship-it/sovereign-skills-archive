# GCM-WQ-018 — Skill-tree conversation ledger + sandbox egress

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner
**Why Bunny is doing this:** keep track of the skill tree, the conversations about it, the content those conversations mint, and get that content out of the sandbox — not only out of the xAI export.

## Ledger row (one per miner run)
- `stamp`
- `conversation_space` (017)
- `skills_touched[]` (path in `/home/workdir/.grok/skills/`)
- `content_minted[]` (files written this pane)
- `sandbox_egressed[]` (artifacts → Drive ids)
- `export_recon` pointer if L8 ran (006)
- `toc_id` / `omissions_id`

## Rule
xAI `prod-grok-backend.json` is recon. It is not the skill tree. Sandbox files that never hit the account zip must still leave the pane.

## Pointers
- chaos-bratz-roster work-queue + atom clouds (identity SSOT; miner does not dump biography)
- skill-orchestrator inventory
- system-roadmap (shape of the library)
- liv-automation-ops (do not point jobs only at artifacts)
- GCM-WQ-006, 007, 011, 017

## RESULT 2026-09-11: SMOKE-PASS ledger.py.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/ledger.py JSONL upsert. Live skill-tree ledger file not published as SSoT yet.
