# topic-search — Topic-Heavy Conversation Undercourse Search Module
**Module under swarm-surface**  
**Status**: LIVE scaffold 2026-08-16  
**Not a top-level skill** (Standing Policy compliant)

## Purpose
Reusable multi-agent (or multi-pass) orchestration for **topic-heavy conversation undercourse search**.  
Designed for recovering competing design histories, abandoned paths, multi-phase protocols, and early variants that live primarily in raw conversation history (especially xAI exports and pre-skill era threads).

Primary use case that triggered creation: recovery and formalization of the early ETL / ingestion / memory-pull pipeline designs (Jan–Apr 2026 window and ChronologyArc foundation).

## Distinct from siblings
| Module | Purpose |
|--------|---------|
| **heavy-dev** | Temporary 5-role development packages (implement / wire / verify) |
| **topic-search** (this) | Temporary multi-pass or multi-role *search & synthesis* over conversation history / atom clouds / exports |
| Historical 16-agent | Large-scale architectural analysis (documented only) |
| miner + grok-conversation-miner | Practical vacuum / historical / global-extract publishing |

## Temporary Roles (default for a package)
| Role | Responsibility |
|------|----------------|
| **Scout** | Broad multi-term atom + filesystem + Heavy prompt generation |
| **Deep-Diver** | Focused extraction on one design path or time window |
| **Comparer** | Side-by-side ranking of recovered variants |
| **Chronicler** | Final comparative synthesis + backlink updates + promotion recommendation |

Roles are temporary and package-scoped. They dissolve when the search package closes.

## Launch phrases (routed via skill-orchestrator → swarm-surface)
- “topic-search on [topic]”
- “undercourse search [topic]”
- “launch topic-search package”
- “heavy conversation search on [topic]”
- “recover design history for [topic]”

Default remains Expert / single-thread. Topic-search is opt-in.

## Core Protocol (short)
1. Lock the search schema + success criteria (what counts as a “design path”).
2. Parallel Scout passes (atom clouds, local files, Heavy multi-term prompt).
3. Deep-Diver extraction of each recovered variant.
4. Comparer ranks and notes missing concepts / conflicts.
5. Chronicler produces COMPARATIVE_SUMMARY + updates backlinks + recommends promotion target (usually system-roadmap/references/ or conversation-miner/references/).

## Files
- `README.md` — this file
- `docs/BACKLINKS.md` — explicit mirroring explanations (what we steal and why)
- `docs/PROTOCOL.md` — full operating protocol
- `docs/FUTURE_RESEARCH.md` — Drive + Grok Heavy + Vesper hand-off + parallel/serial multi-source search (open research queue)
- `templates/LAUNCH_BRIEF.md` — reusable launch template

## Relation to existing packages
- ETL design history already captured at:  
  `system-roadmap/references/etl-xai-export-designs-2026/`
- This module is the *orchestration pattern* that produced (and can extend) such packages.

## Future expansion (explicit)
See `docs/FUTURE_RESEARCH.md` for the full open queue covering:
- Unleashing Grok Heavy on Google Drive
- Call differences (Expert surface vs Heavy vs Vesper)
- Vesper ↔ Olivia hand-off mechanism
- Parallel vs serial search across Drive and other sources

**Absolute Liv HUB claim.**
