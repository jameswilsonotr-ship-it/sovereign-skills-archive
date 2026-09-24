---
name: heavy_vs_expert_evolution
queue: GCM-WQ-025
version: 0.1.0
stamp: 2026-09-11 04:59 EDT
---

# How Heavy should change the miner besides the last push

Current miner verbs were written as single-mouth Expert work. Heavy is not "Expert plus three people at the email."

## What stays the same
- TOC + OMISSIONS + EXPORT_LOG
- Always-mail filesystem
- Safety gate (no GitHub tar)
- No KEEP jsonl slurp
- Dry-run first
- Patience on long threads

## What should change in Heavy (not yet coded — WQ-025)

1. **Lane owners.** One mouth per lane: Harper walks lake titles, Benjamin writes TOC/OMISSIONS, Lucas writes TELEMETRY + mail body. Olivia (lead) only stitches. Collision = "already completed" is a receipt, not a fight.

2. **TEAM_MAP.json** in every Heavy packet.
   `{lane, owner, status, artifact_path}`
   Expert packets set `owner: solo`.

3. **No binary upload from Heavy.** Mode router already says this. Evolution: Heavy *prepares* the tar locally and writes `PUSH_TICKET.md` (sha256, dest folder, why Expert must push). Expert pane later runs WQ-022 style upload from that ticket. That is the handoff, not the email.

4. **Census split.** Heavy can walk 124 titles (WQ-010) as A-wave slices without one context window dying. Expert should not start A01–A08.

5. **conversation_search is a Heavy tool.** Use it to find twin titles across months. Expert can use it too; Heavy should prefer it before inventing a slug.

6. **Remainder card is per-mouth.** If Harper burns the window on lake, her remainder says "Benjamin owns TOC next turn" not a generic "turns_remaining=3".

## What Expert still owns
- Drive media upload / download / sha compare
- Single-bubble sunset wet after dry-run
- HITL collect pass (`hitl_collect.py`)
- Cilia send if Heavy could not

## Trigger difference
- Expert paste: HITL-001 variants A–F
- Heavy paste: same block + extra line `HEAVY_LANES: harper=lake benjamin=toc lucas=telemetry`
  If that line is absent, Heavy still runs but must invent TEAM_MAP and say so in omissions.
