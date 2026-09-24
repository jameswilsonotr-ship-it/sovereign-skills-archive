# GCM-WQ-003 — Point L7 outbox into global extract tree

**Status:** SMOKE-PASS · **Stamp:** 2026-09-10 20:44 MDT
**Owner:** grok-conversation-miner
**Protocols:** `references/prompt_sunset.md` L7 · `references/prompt_global_extract.md` step 2

Sunset L7 writes `artifacts/sunset/SUNSET_<YYYYMMDD>_<slug>.md`. Global extract L4 snapshots `/home/workdir/artifacts/` but does not name the sunset outbox as a required subtree. A pane can lose the card Bunny reads next.

## Done looks like
- `prompt_global_extract.md` output tree includes `sandbox/artifacts/sunset/` when present
- `prompt_sunset.md` L4 says “include L7 card if already written this run; else L7 writes after L4 and a one-line pointer is appended”
- No second tar

## Pointers
- `references/prompt_sunset.md` L4 / L7
- `references/prompt_global_extract.md` Output Tree
- liv-automation-ops dual-write rule (artifacts vanish from this pane)

## RESULT 2026-09-11: DONE protocol patch. Not field-proofed on live extract.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN 2026-09-11 protocol  
**Stamp:** 2026-09-11 03:40 EDT  
prompt_global_extract.md tree now names sandbox/artifacts/sunset/. prompt_sunset.md documents L7-into-L4 / no second tar.
