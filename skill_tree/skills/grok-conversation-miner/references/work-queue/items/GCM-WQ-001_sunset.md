# GCM-WQ-001 — sunset verb

**Status:** LIVE 0.1.0 · **Stamp:** 2026-09-08 22:13 EDT
**Owner:** grok-conversation-miner
**Protocol:** `references/prompt_sunset.md`

One backup verb. All archive backends that do not overlap.

Triggers: `sunset` · `sunset this conversation` · `sunset the chat` · `run sunset` · `conversation sunset` · `sunset dry-run` · `sunset lake-only` · `sunset miner-only`

Default `sunset` / `sunset full` (paranoid close, 22:18):
deep mine → refactor-if-hit → vacuum (reuse deep-mine) → global extract (sandbox+artifacts) → L0–L7.

Lake twins are turns. Global extract is the sandbox. Without the tarball you cannot delete the bubble and stay whole.

`sunset backup-only` = lanes only. `sunset dry-run` = table. Delete-test forbidden. Do not execute until Bunny says go.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** LIVE 0.1.0  
**Stamp:** 2026-09-11 03:40 EDT  
Unchanged. Sunset protocol still live. Not executed on this bubble.
