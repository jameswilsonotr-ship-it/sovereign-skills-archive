# GCM-WQ-012 — Deterministic package layout + stamps

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner

Same inputs → same tree. No vibes pathing.

## Required envelope on every file and every mail
- `stamp_iso` (America/New_York + UTC)
- `msg_id` / `run_id`
- `conversation_id` or slug
- `skill` + `verb` + `protocol_version`
- `claim: Absolute Liv HUB`

## Canonical tree (target)
```
<conv-space>/
  00_HEADER.md
  01_TOC.md
  02_OMISSIONS.md
  03_TURNS.md
  04_DECISIONS.md
  05_SKILL_DELTA/
  06_SANDBOX/
  07_MAIL/
  08_RECEIPTS/
  MANIFEST.md
```

Do not invent a new root per mood. Deltas later = GCM-WQ-017.

## Pointers
- `references/prompt_publishing.md` versioned folder rule
- `references/mine_orch.md`
- format-bible envelope (do not fight it; miner tree is the payload)
- skill-orchestrator `package_skills`

## RESULT 2026-09-11: SMOKE-PASS layout.py + stamps.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/layout.py + gcm_lib.LAYOUT canonical tree. Stamps NY+UTC.
