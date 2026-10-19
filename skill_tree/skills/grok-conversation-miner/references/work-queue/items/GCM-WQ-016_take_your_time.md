# GCM-WQ-016 — Long-conversation patience rule

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner
**Lands in:** SKILL.md + help.md + every miner protocol header

When the conversation is long and the miner is being exhaustive, nobody cares how long it takes. Do not shrink the harvest to look fast. Do not skip sandbox files to stay under a fake turn budget without writing GCM-WQ-015.

## Sentence to stamp into SKILL.md (when we code)
“Exhaustive on a long thread is correct. Take the turns. Mail the remainder. Do not perform speed.”

## Never
- Truncate TOC to look tidy
- Drop Imagine/video/plates because they are slow
- Refuse a vacuum because the thread is “too long”

## Pointers
- GCM-WQ-011, 014, 015
- global extract purpose line (“everything that happened”)

## RESULT 2026-09-11: DONE sentence lock.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN protocol  
**Stamp:** 2026-09-11 03:40 EDT  
Sentence stamped into SKILL.md + help.md + locked in smoke test.
