# GCM-WQ-015 — Multi-turn remainder card

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner

If the miner cannot finish in this pane, the mail and the L7 card say how many more turns it thinks it needs. Time is not a constraint. Turn count is.

## Required line
`turns_this_run: N`
`turns_remaining_estimate: M`
`blocked_on: <file | connector | size | operator go>`
`time_is_not_the_budget: true`

## Done looks like
Long thread → first mail ships TOC + OMISSIONS + “3 more turns, sandbox walk next.” Second mail is a delta, not a rewrite of the excuse.

## Pointers
- GCM-WQ-013 email filesystem `03_TURNS`
- liv-automation-ops (foreign sandbox may need a second pass)
- olivia-dev “continuation required / scale back” — miner uses turn counts, not shame

## RESULT 2026-09-11: SMOKE-PASS mail turns card.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN fixture  
**Stamp:** 2026-09-11 03:40 EDT  
turns_this_run / turns_remaining_estimate / time_is_not_the_budget on mail body.
