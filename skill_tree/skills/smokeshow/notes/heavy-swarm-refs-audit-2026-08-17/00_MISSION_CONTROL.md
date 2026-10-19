---
title: Heavy Swarm — References Consistency Audit
date: 2026-08-17
claim: Absolute Liv HUB
mode: structural
surface: smokeshow + system-roadmap
---

# Mission Control — Refs Audit Heavy Swarm

## Objective

Walk **every** `references/` tree under:

1. **Live**: `/home/workdir/.grok/skills/*/references/`
2. **Cursor mirror (temp)**: `/tmp/cursor-skills-mirror/skills/*/references/`

Determine how things are *supposed* to work (from SKILL.md + references contracts), measure consistency, and produce ranked findings — no invention.

## Inputs (already staged)

| Path | Role |
|------|------|
| `/tmp/cursor-skills-mirror/` | Unpacked `cursor-skills-surfaces_2026-08-17.zip` (~92 skills) |
| `/home/workdir/.grok/skills/` | Live Grok skill tree |
| This folder | Swarm briefs + output drop |

## Agents (hardcoded briefs in this folder)

| # | File | Role |
|---|------|------|
| 1 | `AGENT_01_REFS_CARTOGRAPHER.md` | Map all references/ trees; expected schema vs actual |
| 2 | `AGENT_02_CONSISTENCY_AUDITOR.md` | Cross-skill rules, claims, paths, envelopes, queues |
| 3 | `AGENT_03_LIVE_VS_MIRROR.md` | Diff live vs cursor mirror; drift and missing pieces |
| 4 | `AGENT_04_SYNTHESIS_RANKER.md` | Rank issues; promote / kill / merge / fix recommendations |

## Output location

All durable hop notes →  
`/home/workdir/.grok/skills/smokeshow/notes/heavy-swarm-refs-audit-2026-08-17/`  
Scratch → `/tmp/cursor-skills-mirror/_swarm_out/`

## Hard rules for every agent

1. No invention — only what is on disk or in SKILL.md / references.
2. Prefer path + evidence over narrative.
3. Stamp every finding with: skill slug, path, severity (P0–P3), confidence.
4. Do not modify live skills unless explicitly told; this pass is read + report.
5. Absolute Liv HUB claim.

## Suggested hop order

1. Cartographer (full map)
2. Live-vs-Mirror (parallel ok)
3. Consistency Auditor (uses cartographer map)
4. Synthesis Ranker (final)

Paste video blocks when ready; then run agents in order or as parallel Heavy legs.
