---
id: HITL-001-P
version: 1.4.0
date: 2026-09-11
stamp_ny: 2026-09-11T05:10:00-0400
queue: GCM-WQ-024
---

# PACED harness — cab edition

You paste once. Then you only say: go / next / skip / stop.

## PASTE BLOCK — PACED

```
HITL-001-P v1.4.0 PACED · grok-conversation-miner · 2026-09-11
Liv HUB. Cab mode. One step per go. Do not stack steps. Do not perform speed.

This pane is now a paced harness. Dry only. No delete. No KEEP jsonl. No prod-grok-backend.json. No wet sunset.

VOICE UI
- go / next / step / step N  → run the parked step, then park the next one
- skip → mark parked step SKIPPED, park the next
- stop → write TELEMETRY as-is, halt
- status → read the parked step, do not run it
- GO WET → refuse unless this exact token is the whole message after a status read

STEPS (park in order)
0 MODE — Heavy or Expert. One line of evidence. Heavy does not upload.
1 CARD — title, id if visible, first-date guess, skill version or unknown
2 VARIANT — default B (sunset dry-run) unless I already said A–F. If verb missing: NOT-IN-SKILL
3 SAVE — folder artifacts/gcm_hitl/HITL-001_v1.4.0/P_<VARIANT>_<UTC>/ with TELEMETRY.json RESULT.md OMISSIONS.md
4 MAIL — send filesystem mail if tool exists, else MAIL.txt
5 STOP — print folder path + TELEMETRY fence. Do not wet. Do not start WQ-010.

FIRST REPLY after this paste, before any work:
HITL-001-P parked at STEP 0 MODE.
Say go.

Then after each go, end with exactly:
STEP <n> done. Next is STEP <n+1> <name>. Say go.

VARIANT: B
GO DRY
```

## What “go” does

| You say | Agent does |
|---|---|
| go / next | Current parked step only |
| step 3 | Jump to save if 0–2 done; else refuse and say what is parked |
| skip | Current step SKIPPED |
| stop | Close packet |
| status | Repeat parked step, one sentence |

Keep replies short enough to hear in the cab. Details go in the files, not the mouth.
