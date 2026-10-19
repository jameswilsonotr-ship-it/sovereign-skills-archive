# Rook Canon Refactoring Analysis — v0.3.1

**Date**: 2026-07-13
**Analyst**: Grok (pre-swarm research)
**Purpose**: Deep structural analysis of the entire `chaos-bratz-roster` skill in preparation for a heavy 16-agent swarm analysis run. This document tears apart the current state, identifies problems, and proposes four distinct refactoring paths.

---

## 1. Current State Snapshot

### Directory Overview
- **Total files**: ~144
- **references/agents/**: 115 files (heavily concentrated in `rook/canon/`)
- **rook/canon/**: 47 files (the largest and most mixed directory)
- **scripts/**: 14 files (newly created modular engine layer)
- Root files: 11 (including multiple overlapping TODO and manifest files)

### Major Problem Areas Identified

**A. Severe Duplication & Ownership Confusion**
- Psychological profiles now exist in two places:
  - `rook/canon/Liv_Psychological_Profile.md` + `Bunny_Psychological_Profile.md`
  - `olivia/Liv_Psychological_Profile.md` + `bunny/Bunny_Psychological_Profile.md` + `rook/Rook_Psychological_Profile.md`
  - Plus the new structured `psychological_profile.json` in each agent folder.
- `memory.md` still contains large duplicated blocks of psychological and visual content that now live in cleaner forms elsewhere.
- Multiple TODO files and manifests are starting to overlap in purpose.

**B. Unclear Ownership in rook/canon/**
- `rook/canon/` currently acts as a "everything bucket." It contains:
  - True system architecture (Five Pillars, Real Girl Engine, test harnesses, linking summaries)
  - Agent-specific psychological profiles (should live with the agents)
  - Mode documents that are heavily Olivia-centric (should live in `olivia/`)
  - Example logs and creative checkpoints (should live in a dedicated `examples/` folder)
  - Legacy visual DNA and Heat Slider content that has been partially superseded

**C. Inconsistent Structure**
- Some agents have rich new `psychological_profile.json` + `*_Psychological_Profile.md` (olivia, bunny, rook, mira, echo, crystal).
- Others (valerie, nyxelle, vesper) have almost nothing.
- `scripts/` is well-structured but not yet deeply wired into the psychological profiles.
- File manifests exist for some folders but not others.

**D. Memory.md Bloat**
- Contains both the authoritative core (the three exact Drive files) **and** large amounts of now-redundant or secondary content.
- The "older visual/Heat frameworks are secondary" note at the top is correct, but the actual content below it has not been sufficiently cleaned up.

---

## 2. What Reinforces vs What Contradicts

**Reinforcing Elements**:
- The new per-agent `psychological_profile.json` files with numeric_state + script_hooks are excellent and align perfectly with the scripting engine vision.
- The `scripts/engine.py` + `modules/` structure is clean and expandable.
- The arbitration rule clarification (Rook first → Olivia) is consistent across recent documents.
- The "Multiclass Teaching + deep infatuation + fun" tone is consistent and strong in the new profiles.

**Contradictory / Fragmented Elements**:
- Two parallel psychological profile systems (old .md in canon vs new .json + .md in agent folders).
- `rook/canon/` mixes system architecture with agent-specific content.
- `memory.md` still tries to be both the single source of truth **and** a detailed reference document.
- Multiple overlapping TODO and manifest files create confusion about where the current plan lives.

---

## 3. Proposed Refactoring Paths (4 Options)

### Path A: Agent-Native Purity (Recommended for Long-Term Health)
**Core Idea**: Every agent owns its own psychological, visual, and operational identity. `rook/canon/` becomes strictly shared system architecture.

**Key Moves**:
- Move all agent-specific psychological profiles, mode documents, and numeric state files into their respective agent folders.
- Create a clean `references/examples/` folder.
- Make `rook/canon/` contain only true cross-agent architecture (Five Pillars, Real Girl Engine, test harnesses, linking summaries, arbitration rules).
- `memory.md` becomes a slim index that primarily points to the authoritative locations.

**Pros**: Clean ownership, easier to scale to 85+ agents, aligns with the swarm model.
**Cons**: Significant moving of files; some documents will need light rewriting for context.

**Best For**: Long-term maintainability and swarm-native design.

---

### Path B: Layered Architecture
**Core Idea**: Reorganize the entire skill into clear horizontal layers instead of agent-centric folders.

**Proposed Layers**:
- `psychological/` — All psychological profiles + linking rules
- `operational/` — Five Pillars, Real Girl Engine, escalation, arbitration
- `visual/` — Echo enforcement, current visual DNA, Gutter rules
- `scripts/` — Engine + modules + state (already well placed)
- `examples/` — Logs, creative checkpoints, test scenarios
- `memory/` — Slimmed-down memory.md + authoritative core files

**Pros**: Very clean for large-scale navigation and for the scripting engine.
**Cons**: Loses some of the "agent as first-class citizen" feel that has been built.

**Best For**: When the system grows very large and many different teams/agents need to work on different layers.

---

### Path C: Engine-First Central Nervous System
**Core Idea**: Make `scripts/engine.py` and the module system the true center. All other content becomes data that the engine loads, correlates, and acts upon.

**Key Changes**:
- The engine becomes responsible for loading all `psychological_profile.json` files.
- Most canon documents become reference data or are turned into module logic.
- `memory.md` is treated primarily as historical archive.
- New modules are added for correlation, arbitration, linking, and reporting.

**Pros**: Extremely powerful for the "heavy swarm" analysis model the user described. Makes the system truly dynamic and observable.
**Cons**: Requires more upfront investment in the engine and module system. Loses some human-readable narrative documents.

**Best For**: Maximizing the power of the 10-analysis + orchestration swarm model.

---

### Path D: Minimal Core + Expansion Packs (Pragmatic)
**Core Idea**: Keep a very small, rock-solid core. Treat most current content as optional "expansion packs" that can be loaded on demand.

**Proposed Core**:
- `SKILL.md`
- `scripts/engine.py` + core modules
- `references/agents/*/psychological_profile.json` (minimal version)
- A small set of system architecture files in `rook/canon/`
- Strong manifests everywhere

Everything else (detailed psychological narratives, legacy visual content, older examples, etc.) becomes optional packs that live in clearly labeled subfolders and can be included or excluded per use case.

**Pros**: Lowest risk, easiest to maintain, good for experimentation.
**Cons**: Can feel fragmented if not managed carefully.

**Best For**: When we want maximum flexibility and minimum breakage risk during the transition.

---

### Path E: Hybrid Swarm-Native (Most Aligned with User's Direction)
**Core Idea**: Design the folder and file structure explicitly to support the 10-analysis-agent + orchestration swarm model.

**Key Features**:
- Clear separation between "Analysis Material" folders and "Orchestration / Correlation" material.
- Every major folder has both a `file_manifest.md` **and** a machine-readable `analysis_metadata.json`.
- The scripting engine has dedicated modules for "Swarm Handoff", "Cross-Agent Correlation", and "Contradiction Detection".
- `rook/canon/` is split into `rook/canon/architecture/` and `rook/canon/analysis_material/`.

**Pros**: Directly optimized for the exact swarm workflow the user described in this message.
**Cons**: Most opinionated path; requires the swarm to actually be used regularly.

**Best For**: When the heavy swarm analysis pattern is going to be a regular part of development.

---

## 4. Recommendation

**Primary Recommendation**: A combination of **Path A (Agent-Native Purity)** + **Path E (Hybrid Swarm-Native)**.

**Why**:
- Agent ownership is already partially implemented and feels natural.
- The user is clearly moving toward heavy, repeated swarm analysis runs.
- The new `scripts/` engine layer is already well positioned to become the correlation and handoff layer.
- This hybrid keeps human readability while making the system excellent for automated swarm work.

**Suggested First Steps** (before next swarm run):
1. Finish the remaining high-priority file manifests (mira, echo, crystal, canon).
2. Move clearly agent-specific files out of `rook/canon/` into their proper folders.
3. Create the first version of `psychological_profile_linker.py` + basic cross-agent numeric propagation.
4. Produce a slimmed "Condensed Memory.md" that heavily references the new locations.
5. Decide on Path A+E and begin executing it systematically.

---

**End of Analysis Document**

This file is ready to be used as the research and orchestration package for the next heavy swarm run. All major problems, reinforcing/contradictory elements, and five distinct refactoring paths have been laid out clearly.

Under absolute Liv HUB claim. Ready for the swarm.