# GCM-WQ-014 — Keep-everything harvest (duplicates allowed)

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner

Bunny lock this pane: “I don’t give a fuck if it’s duplicated. Get everything.”

Do **not** erase skip-exists intelligence. Reclassify it.

## Old behavior (keep as annotation)
`SKIP-EXISTS` / `SKIP-OVERLAP` / “don’t put that there” — still computed, still written on the omission/audit line.

## New default for miner harvest
- Package the byte anyway if it is gettable from this pane or this sandbox
- Duplicate into the conversation space even if a twin already lives on Drive
- Point at the earlier copy *and* include this copy
- Operator-said-no stays a real skip (RACK / secret / cookies / tskey) and must appear in OMISSIONS

## Never
- Quiet drop
- Dedup that deletes the second copy
- Treat “already on Drive” as “not our problem”

## Pointers
- sunset skip table in `references/prompt_sunset.md` — becomes audit, not a delete
- GCM-WQ-011 OMISSIONS.md
- GCM-WQ-017 conversation space + deltas (later runs can be thin *because* first run kept everything)

## RESULT 2026-09-11: SMOKE-PASS annotation path.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN annotation  
**Stamp:** 2026-09-11 03:40 EDT  
SKIP-EXISTS is census/L0 annotation. Secrets still omit. No quiet drop in harness. Live harvest not flipped on sunset protocol until Bunny go for a real bubble.
