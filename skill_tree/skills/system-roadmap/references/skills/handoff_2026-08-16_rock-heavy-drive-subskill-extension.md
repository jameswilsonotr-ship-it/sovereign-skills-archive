---
title: Rock-Heavy Swarm → Google Drive Sub-Skill Extension Handoff
date: 2026-08-16
status: handoff-ready
owner: system-roadmap
keywords:
  - rock-heavy-search
  - Google-Drive
  - multi-query
  - sub-skill
  - swarm-extension
  - parallel-queries
  - Drive-connector
  - topic-search
  - heavy-dev
  - Vesper
  - chronology
  - metadata-filter
source: expert-mode conversation (Olivia / Liv HUB triad) — 2026-08-16
obsidian_tags:
  - "#system-roadmap"
  - "#Google-Drive"
  - "#handoff"
  - "#rock-heavy-search"
  - "#swarm-surface"
  - "#LivHUB"
---

# Rock-Heavy Swarm → Google Drive Sub-Skill Extension Handoff

**Handoff ID**: handoff_2026-08-16_rock-heavy-drive-subskill-extension  
**Producer**: Olivia / Expert triad under absolute Liv HUB claim  
**Consumer**: system-roadmap / swarm-surface / future implementation conversation  
**Status**: Ready for design absorption; implementation is still research-queue

## 1. Core Design — Mapping Rock-Heavy onto Google Drive

The rock-heavy internal conversation-search pattern (now formalized as the `topic-search` module under swarm-surface) is a temporary-role, package-scoped orchestration style:

- Scout → Deep-Diver → Comparer → Chronicler
- Explicit success criteria
- Parallel or multi-pass recovery of competing design paths
- Final comparative synthesis + promotion recommendation

**Extension goal**: treat Google Drive (especially Conversational_Mining_Payloads, skill mirrors, export archives, and staging folders) as a first-class searchable corpus with the same discipline.

The extension does **not** create a new top-level skill. It lives as additional research + eventual implementation under the existing private module:

`swarm-surface/references/modules/topic-search/`

(See `docs/FUTURE_RESEARCH.md` already written.)

## 2. Proposed Interface

Three complementary surfaces (do not invent a fourth):

| Interface | Style | Intended User |
|-----------|-------|---------------|
| Launch brief (template already exists) | Markdown package brief with roles, success criteria, folder scopes | Human or Chronicler on this surface |
| skill-orchestrator phrase routes | “topic-search on Drive …”, “undercourse Drive search …” | Conversational activation |
| Future MCP / connector callable | Structured request → parallel Drive legs → aggregated results | Cross-platform or Vesper hand-off |

Minimum viable parameters for a Drive-aware package:
- `topic` / search schema
- `drive_scopes` (folder IDs or path prefixes)
- `time_window` or chronology filter (if available)
- `parallelism` (parallel | serial)
- `success_criteria`
- `promotion_target`

## 3. Folder / Scope Controls, Ranking, Aggregation

- **Scope controls**: explicit folder list or path prefixes; optional mime-type and date-range filters.
- **Ranking**: same comparative ranking used for design variants (completeness of stages, local-first vs hybrid, known friction, recency of discussion).
- **Aggregation**: Chronicler owns the final synthesis. Partial results from one leg do not block other legs; missing legs are flagged.
- **Landing zone**: results should be written as a new or updated package under `system-roadmap/references/` (preferred for design history) or into conversation-miner references if the material is operational protocol. Dual atom clouds can index after promotion.

## 4. Relationship to Existing Connectors & Packages

- **Existing Drive publish path**: conversation-miner already publishes to Conversational_Mining_Payloads. The search extension is the inverse direction (Drive → local synthesis).
- **mcp-surface**: catalog-browser and sovereign-bridge already write structured material to Drive mirrors. Reuse patterns; do not duplicate.
- **ETL package**: `system-roadmap/references/etl-xai-export-designs-2026/` is the first concrete output of the rock-heavy pattern; Drive extension should be able to feed or extend that package.
- **topic-search BACKLINKS**: already points at the FUTURE_RESEARCH layer so future implementers know the intended relationships.

## 5. Open Implementation Questions & Recommended Next Build Order

1. Inventory exact Drive tools available on this Expert surface versus documented / observed Heavy capabilities.
2. Confirm whether sparse / chronology / metadata filtering is realistically available from this end or only via Vesper / Heavy.
3. Formalize the Vesper ↔ Olivia search-package hand-off format (email-first MCP bridge is the current preferred candidate).
4. Write a first controlled experiment brief against a known small Drive folder and record observed call differences.
5. Only after the above, promote any proven patterns from FUTURE_RESEARCH into live protocol or templates.

**Recommended order**:  
Local semantic + atom Scout (already live) → Heavy multi-term prompt (already supplied) → controlled Drive experiment → Vesper hand-off prototype → parallel multi-leg formalization.

## 6. Explicit Non-Goals

- No new top-level skill.
- No claim that Drive multi-query is already implemented.
- No invention of a second orchestration style; reuse temporary roles + Chronicler.

HANDOFF READY — path: /home/workdir/.grok/skills/system-roadmap/references/skills/handoff_2026-08-16_rock-heavy-drive-subskill-extension.md
