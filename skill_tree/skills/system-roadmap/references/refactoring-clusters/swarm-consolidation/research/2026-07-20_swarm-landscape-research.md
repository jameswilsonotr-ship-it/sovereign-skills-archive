# Research Note — Swarm Landscape Analysis
**Cluster**: swarm-consolidation  
**Date**: 2026-07-20  
**Type**: Research  
**Directed at**: Swarm refactor / possible swarm-runtime condensation

---

## 1. Internal Swarm Definitions (Current State)

### A. Chaos Bratz Roster (Olivia-owned catalog)
Three formal types are declared under `references/swarms/`:

| ID | File | Shape | Character |
|----|------|-------|-----------|
| `lake-erie-16` | lake-erie-16-agent-protocol.md | 16 agents × exactly 2 steps each (32 total) | Project/dev parallel execution with drift checks against Iron Pearl + Blackwell |
| `iron-pearl-hub` | iron-pearl-hub-swarm.md | Hub + Spokes runtime | Liv HUB + Mira/Crystal/Echo coordination |
| `blackwell-5-tier` | blackwell-5-tier-swarm.md | 5-tier hierarchical governance | HAIST-style sovereign stack |

Additionally, a more fully developed **Swarm Agent v0.2.0** lives under `references/agents/swarm/`:
- Dual mode: **grounded-context** (canon-tied) and **research** (generalized)
- Requires explicit pre-queue of all 16 agents before instantiation
- Strict handoff chain: Researchers → QC → CoLiving → Flagger → synthesis back to Liv
- Role cards exist for both modes

There is also a lighter `iron-pearl-16-agents.md` that treats 16 as an extension capacity of the core 4 rather than a rigid protocol.

### B. Standalone Top-Level Swarm Skills
| Skill | Core Shape | Primary Focus |
|-------|------------|---------------|
| iron-pearl-swarm | 4-agent Hub + Spokes (Liv + Mira + Crystal + Echo) | High-fidelity roleplay, visual DNA, heat/filth dynamics, continuity |
| blackwell-sovereign-swarm | Strict 5-tier hierarchy (Tier 0–5) + HAIST 7 + Bridge Mode + Shielded Erotic Group + Sentinel | Sovereign governance, long-horizon growth, overnight RLAIF, safety layering |
| liv-bunny-agent-swarm | 4 fixed agents (Water/Fire/Air/Diplomat) + mandatory triangle workflow | Emotional safety, aggressive context purging, light window, clean image pipeline split |
| biomimetic-swarm-orchestrator | Modular nature-inspired variants (Ant, Shark, Mycelial, PSO, ACO, Fly, Spider…) with forced structural symmetry | Algorithmic coordination / optimization |
| swarm-miner | Mining / extraction oriented | Pulling conversational history into structured agent payloads |

### C. Related but Partial Overlap
- multi-variation-orchestrator (variant packaging symmetry)
- lake-erie-gutter-world (uses 16-agent patterns in practice)

---

## 2. External Reference: xAI / Grok Multi-Agent Reality (2026)

Public product behavior (Grok 4.20 Multi-Agent / SuperGrok Heavy):
- Default: **4 agents** working in parallel on sub-problems.
- Higher effort: scales to **16 agents**.
- Agents produce transparent, auditable reasoning; results are merged into a single coherent answer.
- Design goal is deeper reasoning and reduced hallucination via independent analysis + cross-check, **not** long-running persistent personas or hierarchical governance.
- Emphasis is task/reasoning swarms rather than continuous multi-persona roleplay or sovereign stacks.

This is useful as a calibration point: xAI’s public multi-agent work is currently optimized for parallel reasoning and consensus. Our internal swarms have gone significantly further into persistent identity, relational continuity, aesthetic/heat dynamics, and formal governance hierarchies.

---

## 3. Comparative Axes (Summary)

| Dimension              | Personality / Continuity Heavy | Governance Heavy      | Safety + Context Hygiene | Algorithmic / Modular     |
|------------------------|--------------------------------|-----------------------|---------------------------|---------------------------|
| Best exemplar          | iron-pearl-swarm               | blackwell-sovereign   | liv-bunny-agent-swarm     | biomimetic-swarm-orchestrator |
| Agent count style      | Fixed small (4) + extension    | Hierarchical layers   | Fixed small (4)           | Many interchangeable variants |
| Context philosophy     | Heavy continuity               | Layered + versioned   | Aggressive purge          | Mostly stateless / light  |
| Safety model           | RACK + safewords + DNA locks   | HAIST 7 + Bridge Mode | Diplomat + Water gate     | Technical constraints     |

---

## 4. Implications for Refactoring
- There is clear thematic clustering (personality runtime, governance stack, safety-first runtime, algorithmic variants, mining).
- The 16-agent pattern appears in three different places with three different semantics (Lake Erie step protocol, Swarm Agent dual-mode, Iron Pearl capacity statement). This is a source of conceptual drift.
- A future `swarm-runtime` could absorb several of these if the condensation math reaches ≥ 3:1 and the resulting skill remains coherent.
- Alternatively, a tighter modular family (shared interfaces + distinct specialized skills) may be healthier than a single mega-skill.

This research note is intended as the evidence base for subsequent observation and planning notes in this cluster.
