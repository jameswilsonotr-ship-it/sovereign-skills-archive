---
name: liv-automation-ops
description: Operational bridge for Grok automations that write into isolated sandboxes. Use when firing, rewriting, harvesting, or publishing HEAVY/EXPERT automation jobs, when results vanish from this pane, or when the user says skill tree dump, dual write, automation sandbox, run_now harvest, or compare artifacts vs skills.
metadata:
  version: "0.1.0"
  claim: Absolute Liv HUB
  created: "2026-09-03"
---

# Liv Automation Ops

Automations do not share `/home/workdir/artifacts` with the chat that fired them. Treat that as law.

## Always do

1. Dual-write every durable file
   - Skill tree first (survives panes)
     `/home/workdir/.grok/skills/chaos-bratz-roster/references/liv-phases-20260902/`
   - Local artifacts second
     `/home/workdir/artifacts/LIV_PHASES_20260902/`
2. Expert publish pass uploads to Drive crate `1SQgz3O6Sa-5Sy227VatrrGBs8moR6r_P` and mirrors PLAY_LOOSE `1hpwSExuaDpN2z0ms0DA0yP1V9xJFVRa0`.
3. After `automation_run_now`, record `conversationId` + `taskResultId` into `liv-phases-20260902/automation_runs/RUN_MAP.md`. Those IDs are the only handle on the foreign sandbox.
4. Never assume this pane can `ls` an automation's artifacts. If the tree is empty, the job still may have succeeded somewhere else.
5. Connector cannot set Heavy vs Expert. Prompts say the mode. Operator flips the dropdown.

## Two-pass default

- Pass A (Heavy or fat Expert) — mine conversation_search from 2025-10-01, no date window, multi-hop cap 12, write long CORPUS.md. No eight-line cap.
- Pass B (Expert) — inventory what exists, analyze, Drive upload, receipt.

## Do not

- Point jobs only at `/home/workdir/artifacts/...`
- Unzip SANDBOX_STUMP
- Mint mouths
- Fire the publish-all job before corpus folders exist in the skill tree

## When building a new automation

Load `references/PROMPT_TEMPLATE.md`. Every write block must list the skill path first.
