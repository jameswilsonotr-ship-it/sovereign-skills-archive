# GCM-WQ-009 — scripts/sunset_smoke.py fixture harness

**Status:** SMOKE-PASS · **Stamp:** 2026-09-10 20:44 MDT
**Owner:** grok-conversation-miner
**Stage first:** smokeshow
**Script target:** `scripts/sunset_smoke.py` (not written until smoke stage)

Plant 12 files / 6 classes in a sandbox fixture tree. Dry-run sunset against fixtures only.

## Six classes
1. lake twin markdown
2. lake receipt
3. miner publish tar pointer
4. global extract tar pointer
5. sunset L7 outbox card
6. census row (packed/pointed/redacted mix)

Exit 0 only if census rows + fake Drive ACK ids match. Unblocks GCM-WQ-004 without touching a live bubble.

## Skill-tree pointers
- smokeshow SKILL.md (stage here)
- `references/prompt_sunset.md`
- GCM-WQ-004, GCM-WQ-005
- liv-automation-ops: do not point the harness only at `/home/workdir/artifacts`

## Never
- Run against a live conversation first
- Invent Drive ACKs

## RESULT 2026-09-11: DONE. sunset_smoke.py 12/12 RC 0.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN GREEN  
**Stamp:** 2026-09-11 03:40 EDT  
scripts/sunset_smoke.py + test_gcm.py. 12 files / 6 classes. unittest 5/5 OK. sunset_smoke exit 0. Report scripts/smoke_out/SMOKE_REPORT.json.
