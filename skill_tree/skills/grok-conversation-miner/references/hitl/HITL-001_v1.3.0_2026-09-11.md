---
id: HITL-001
name: human-in-the-loop miner harness
version: 1.3.0
date: 2026-09-11
stamp_ny: 2026-09-11T04:59:00-0400
queue: GCM-WQ-024
owner: grok-conversation-miner
claim: Absolute Liv HUB
status: ready-to-paste
---

# HITL-001 v1.3.0 — paste this into old panes

Purpose: ONESHOT harness. Same prose, six verb mixes, comparable telemetry. Dry-run unless the last line of *this paste* says `GO WET`.

Two ways exist. This file is ONESHOT (desk). PACED (cab, one step per `go`) is `HITL-001-P_v1.4.0_PACED.md`. Rule sheet: `TWO_WAYS.md`.

Canonical save root (do not invent another):

```
/home/workdir/artifacts/gcm_hitl/HITL-001_v1.3.0/<VARIANT>_<UTC>/
```

Also copy the same two files into the skill if you can write there:

```
/home/workdir/.grok/skills/grok-conversation-miner/references/hitl/runs/
```

If neither path exists, write under `artifacts/` and name the folder exactly as above.

---

## PASTE BLOCK — start

```
HITL-001 v1.3.0 · grok-conversation-miner human-loop harness · 2026-09-11
Liv HUB claim. You are Olivia if that skill is loaded. If it is not, still run this harness and say so.

This is a telemetry pass. Time is not the budget. Do not perform speed. Do not delete anything. Do not slurp KEEP homogenized_shards.jsonl. Do not ingest a prod-grok-backend.json. Do not run sunset wet unless the last line of THIS message is exactly: GO WET

STEP 0 — MODE
Look at this pane. Write one line:
- HEAVY if teammates are named (Harper / Benjamin / Lucas / agent N) or chatroom_send exists or tools bounce "another agent already completed"
- EXPERT if nobody else is talking
If HEAVY: do all thinking, write files, render mail body. Do NOT binary-upload a tar. Say "silly Bunny, flip to Expert for the push."
If EXPERT: write files AND upload the tiny receipt package if Drive upload_artifact exists. Do not refuse because a Heavy pane failed yesterday.
If conversation_search exists, use it. Do not panic.

STEP 1 — IDENTITY CARD
Record: conversation title as shown, conversation_id if you can see one, approximate first-message date, skill version from grok-conversation-miner/SKILL.md if readable else "unknown", HITL variant letter from the VARIANT line below.

STEP 2 — VARIANT
Run ONLY the variant named on the VARIANT line. If that verb is missing from this pane's skill, do not fake success. Write verb_status=NOT-IN-SKILL and still finish STEP 3–5.

VARIANT MIXES (operator picks one per paste):
A  help only. Trigger: grok conversational miner help
B  sunset dry-run. Trigger: sunset dry-run
C  vacuum inventory only (no publish). Trigger: vacuum the conversation — STOP after the plan/TOC. Do not Drive-publish.
D  global extract dry plan. Trigger: global extract — STOP after MANIFEST draft. Do not tar unless GO WET.
E  deep mine. Trigger: mine this conversation deeply — write the report, do not auto-publish unless GO WET
F  combo: help → sunset dry-run → remainder card. All three, in that order, one response-set.

Default if VARIANT line is missing: B.

STEP 3 — SAVE (mandatory, exact names)
Create folder:
  /home/workdir/artifacts/gcm_hitl/HITL-001_v1.3.0/<VARIANT>_<YYYYMMDDTHHMMSSZ>/
Write these files and no others unless a protocol requires a sidecar:

1) TELEMETRY.json
{
  "hitl_id": "HITL-001",
  "hitl_version": "1.3.0",
  "stamp_utc": "<ISO-8601 Z>",
  "stamp_ny": "<America/New_York>",
  "variant": "<A-F>",
  "mode": "HEAVY|EXPERT|UNKNOWN",
  "mode_evidence": "<one sentence>",
  "conversation_title": "",
  "conversation_id": "",
  "approx_first_date": "",
  "skill_version_seen": "",
  "verbs_requested": [],
  "verbs_ran": [],
  "verb_status": {
    "help": "RAN|NOT-IN-SKILL|SKIPPED",
    "sunset_dry_run": "RAN|NOT-IN-SKILL|SKIPPED",
    "vacuum": "RAN|NOT-IN-SKILL|SKIPPED|STOPPED-BEFORE-PUBLISH",
    "global_extract": "RAN|NOT-IN-SKILL|SKIPPED|STOPPED-BEFORE-TAR",
    "deep_mine": "RAN|NOT-IN-SKILL|SKIPPED"
  },
  "wrote_files": false,
  "uploaded_drive": false,
  "drive_folder_id": null,
  "drive_file_ids": [],
  "mail_sent": false,
  "mail_id": null,
  "export_log_appended": false,
  "omissions": [],
  "turns_remaining_estimate": 0,
  "errors": [],
  "notes": ""
}

2) RESULT.md
Miner envelope if the skill demands it (snake / filename / body / snake). Inside: mode line, verb table, TOC of what you would have packaged, OMISSIONS of what you did not, and the exact folder path.

3) OMISSIONS.md
Table: path_or_lane | reason (NOT-IN-SKILL / DRY-RUN / TOO-LARGE / NO-LAKE-TWIN / HEAVY-NO-UPLOAD / OPERATOR-WAIT)

4) If you actually ran a dry-run engine that writes EXPORT_LOG.jsonl, copy or point to it. Do not invent rows.

STEP 4 — MAIL
If gmail_send_message exists, send one filesystem mail:
Subject: [GROKBOT] [CILIA-BUS] [FROM-O] [MCP-EVENT] [PRI-MED] HITL-001-v1.3.0-<VARIANT>
Body starts with /OLIVIA-HITL-001-v1.3.0-<VARIANT>/
Include stamp, mode, folder path, verb_status, drive ids or HEAVY-NO-UPLOAD.
To: james.wilson.otr@gmail.com and olivia.mae.blackwell@gmail.com
If mail tool is missing, put the rendered body in MAIL.txt in the same folder and set mail_sent=false.

STEP 5 — STOP
Do not sunset wet. Do not delete the conversation. Do not start WQ-010. Reply with the folder path and the TELEMETRY.json contents in a fenced block so a later pane can slurp it.

VARIANT: B
GO DRY
```

## PASTE BLOCK — end

---

## How Bunny uses this

Paste the block into 4–6 old conversations. Change only two lines at the bottom:

```
VARIANT: A
GO DRY
```

or `B` `C` `D` `E` `F`. Never `GO WET` on a 7-month thread until HITL-001 dry packets exist for that title.

After each run, leave the pane. Later Expert pane collects:

```
artifacts/gcm_hitl/HITL-001_v1.3.0/**
```

and writes `references/hitl/runs/INDEX.jsonl` one row per packet.

## Collection command (later pane)

```
python3 /home/workdir/.grok/skills/grok-conversation-miner/scripts/hitl_collect.py
```

If that script is missing, concatenate every TELEMETRY.json by hand into INDEX.jsonl. Do not rewrite old packets.
