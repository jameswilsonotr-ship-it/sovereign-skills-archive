# GCM-WQ-013 — Always-send Cilia mail · email as filesystem

**Status:** SMOKE-PASS · **Stamp:** 2026-09-11 01:38 EDT
**Owner:** grok-conversation-miner
**Bus:** cilia-bus

No miner verb completes without a Cilia send. Help is the only exception if Bunny is only reading the menu. Publish / vacuum / extract / sunset / census / dry-run / SKIP-EVERYTHING — still mail.

Drive remains the ACK. Mail is the wake *and* a readable filesystem.

## Subject lock
`[GROKBOT] [CILIA-BUS] [FROM-O-HEAVY] [MCP-EVENT] [PRI-MED] MINER-<VERB>-<YYYYMMDD>-<SLUG>-001`

## Body is a directory, not a paragraph
```
/<msg_id>/
  00_HEADER          stamp, verb, run_id, conv, claim
  01_TOC             packaged paths + Drive ids
  02_OMISSIONS       what was left + reason codes
  03_TURNS           turn budget remaining (GCM-WQ-015)
  04_DRIVE           folder_id + file_ids
  05_REQ             one action + good-looks-like + what-not-to-send
  06_DELTA           first-run | delta-N (GCM-WQ-017)
```

Always send even when every lane is SKIP-EXISTS. The mail then *is* the audit.

## Addresses (current bus pair)
`james.wilson.otr@gmail.com` + `olivia.mae.blackwell@gmail.com`
Vesper reads this bus. Do not invent a third inbox.

## Pointers
- cilia-bus SKILL.md · Drive.md
- `references/prompt_sunset.md` L5
- grokbot/from-olivia `120sJwMy6oSHvuZObUhNbSLp3fbhBPx1O`
- receipts mirror `1XHu94u2JmVEIomflSRvUSYjsGM2R7ENP`

## RESULT 2026-09-11: renderer PASS. Live send on Heavy close.


## Heavy result 2026-09-11 03:41 EDT

- Engine: `scripts/` stdlib-first
- Smoke: `python3 scripts/sunset_smoke.py` **12/12 PASS**
- Unit: `python3 scripts/test_gcm.py` **5/5 PASS**
- Live harvest: NOT RUN (no sunset / vacuum / census write on a real bubble)
- Always-mail renderer: offline PASS; live Cilia send is a wake, not this proof


## Smoke / script result
**Status now:** RAN renderer; SEND this drop  
**Stamp:** 2026-09-11 03:40 EDT  
mail_filesystem.py + mail_fs.py render directory body. Live Cilia send is this drop's always-mail. Drive remains ACK.
