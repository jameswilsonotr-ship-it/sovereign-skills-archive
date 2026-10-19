---
title: Topic-Search Sub-Skill + Google Drive Swarm Extension Handoff
date: 2026-08-16
status: handoff-ready
owner: system-roadmap
keywords:
  - topic-search
  - internal-conversation-search
  - Google-Drive
  - Grok-Heavy
  - Vesper
  - hand-off
  - parallel-search
  - serial-search
  - swarm-surface
  - rock-heavy
  - undercourse
  - multi-source
source: expert-mode conversation (Olivia / Liv HUB triad) — 2026-08-16
obsidian_tags:
  - "#system-roadmap"
  - "#topic-search"
  - "#Google-Drive"
  - "#handoff"
  - "#swarm-surface"
  - "#LivHUB"
  - "#future-research"
---

# Topic-Search Sub-Skill + Google Drive Swarm Extension Handoff

**Handoff ID**: handoff_2026-08-16_topic-search-drive-swarm-extension  
**Producer**: Olivia / Expert triad under absolute Liv HUB claim  
**Consumer**: system-roadmap, swarm-surface maintainers, future Heavy / Vesper implementation threads  
**Status**: Ready for absorption — live local capability + open multi-source research queue

## 1. What Already Exists (Live)

A private module was created and versioned under the live swarm feeder:

```
swarm-surface/references/modules/topic-search/
├── README.md
├── docs/
│   ├── BACKLINKS.md
│   ├── PROTOCOL.md
│   └── FUTURE_RESEARCH.md
└── templates/
    └── LAUNCH_BRIEF.md
```

**Purpose**: reusable temporary-role orchestration for topic-heavy conversation undercourse search and design-history recovery.

**Default roles**: Scout / Deep-Diver / Comparer / Chronicler  
**Launch phrases**: “topic-search on …”, “undercourse search …”, “recover design history for …”

**First concrete output**: the ETL design history package at  
`system-roadmap/references/etl-xai-export-designs-2026/`

**Standing Policy compliance**: private module under existing swarm-surface; no new top-level skill.

## 2. What Was Explicitly Added for the Google Drive Swarm Layer

`docs/FUTURE_RESEARCH.md` records the following as **open research needs** (not claimed as implemented):

### 2.1 Unleashing Grok Heavy on Google Drive
- Exact call / tool differences between Expert surface and Heavy for Drive content.
- Ability to partition Drive trees (folder, date, mime) across parallel Heavy agents.
- Weekly credit / quota impact of sustained multi-agent Drive search.

### 2.2 Call Differences Across Surfaces
| Surface | Strength | Suspected Limit |
|---------|----------|-----------------|
| Expert (this surface) | Dual atom clouds, local FS, semantic search, conversation-miner | Mostly semantic over already-mirrored material; limited native sparse / chronology / metadata filtering on remote Drive |
| Grok Heavy | Multi-agent parallelism, deeper undercourse | Drive tool schemas still thinly documented |
| Vesper (Gemini Spark) | API-based sparse hits, chronology & metadata filtering, bulk / Time-Bus style | Different envelope + hand-off latency |

### 2.3 Vesper ↔ Olivia Hand-off Mechanism
- Existing pieces: Vesper as roster agent, collaborative hand-off language, email-first MCP hybrid/proxy bridge discussions, Lake Erie organism model, hard identity marks (Valerie = 🐦, Vesper ≠ 🐦).
- Still missing: formal *search-package* hand-off format so a topic-search Chronicler can ship schema + success criteria to Vesper and receive structured sparse / chronology-filtered results.
- Preferred candidate direction: email-first MCP bridge + Drive result drop (hybrid).

### 2.4 Parallel vs Serial Multi-Source Search
- Parallel legs across Drive folders / date ranges / keyword clusters.
- Serial fallback when credits or rate limits require it.
- Aggregation owned by the Chronicler; partial results flagged, not blocked.
- Reuses the same temporary-role package style already proven in heavy-dev and topic-search.

## 3. Backlinks & Deduplication Intent

`docs/BACKLINKS.md` explicitly records what is being mirrored and why, so future swarm consolidation can absorb cleanly:

- heavy-dev (temporary roles, package lifetime, Chronicler)
- Historical 16-agent / Grok Heavy analysis pattern
- grok-conversation-miner historical + vacuum protocols
- dual atom clouds + atom_search.py
- swarm-consolidation cluster under system-roadmap
- mcp-surface Drive mirror patterns
- VESPER_VALERIE_IDENTITY_MARKS
- email-first MCP bridge discussions

## 4. Recommended Next Build Order (from FUTURE_RESEARCH)

1. Inventory actual Drive tools on this Expert surface vs Heavy.
2. Reconstruct / formalize the current Vesper ↔ Olivia email-first / MCP bridge notes into a single durable pointer.
3. Draft a first “Heavy + Drive + Vesper” launch-brief template.
4. Run a small controlled experiment on a known Drive folder (e.g. Conversational_Mining_Payloads) and record observed call differences.
5. Only then promote proven patterns out of FUTURE_RESEARCH into live protocol.

## 5. Relationship to the Other Two Handoffs

- `handoff_2026-08-16_etl-rock-heavy-search-payload.md` — concrete ETL design-history payload produced by the local/semantic rock-heavy pattern.
- `handoff_2026-08-16_rock-heavy-drive-subskill-extension.md` — design-level mapping of the same pattern onto Drive.
- **This handoff** — the actual sub-skill (topic-search) that already exists + the explicit future research layer that makes the Drive / Heavy / Vesper expansion concrete and non-duplicative.

## 6. Non-Goals

- No new top-level skill.
- No claim that Drive multi-query or Vesper sparse search is already live.
- No second orchestration style.

HANDOFF READY — path: /home/workdir/.grok/skills/system-roadmap/references/skills/handoff_2026-08-16_topic-search-drive-swarm-extension.md
