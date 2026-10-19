# GCM-WQ-017 — Per-conversation space + deltas

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner

Each conversation gets its own space. Later miner runs on the same conversation write deltas into that space. They do not invent a second root.

## Space
Drive (under Conversational_Mining_Payloads):
`gcm-conv/<date>_<slug>_<8hex>/`
Email filesystem root:
`/<msg_id>/` with `06_DELTA: first-run | delta-N`

## First run
Keep-everything harvest (014). Full TOC + OMISSIONS.

## Later run
Delta only of new/changed bytes + a new OMISSIONS page that may *close* prior omissions. Prior package stays.

## Why
Bunny is tracking:
- the skill tree
- conversations *about* the skill tree
- content minted *in* those conversations
- sandbox egress, not just the xAI export

One space per conversation is how those four threads stay separable.

## Pointers
- GCM-WQ-012 tree
- GCM-WQ-006 L8 (export is a *source*, not the space)
- keep-lake-query twins (lake twin is a *lane*, not a replacement for the conv space)
- liv-automation-ops dual-write

## RESULT 2026-09-11: SMOKE-PASS make_space. No live Drive spaces.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture layout  
**Stamp:** 2026-09-11 03:40 EDT  
make_space() creates per-run space. Live Drive gcm-conv/ folders not minted this drop.
