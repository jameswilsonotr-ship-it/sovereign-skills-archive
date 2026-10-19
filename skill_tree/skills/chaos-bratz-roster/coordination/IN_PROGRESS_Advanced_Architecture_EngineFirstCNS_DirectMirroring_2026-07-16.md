# IN_PROGRESS_Advanced_Architecture_EngineFirstCNS_DirectMirroring_2026-07-16.md

**Pointer to main global IN_PROGRESS.md**: See `/home/workdir/.grok/skills/chaos-bratz-roster/IN_PROGRESS.md` and `coordination/COORDINATION_PROTOCOL.md` for the unifying consensus state, freeze/thaw process, locked lexicon direction, and folder discipline.

**Summary of this thread's current work (1-2 sentences)**:  
This conversation has been developing a significantly more advanced architectural layer for the Chaos Bratz Roster skill than what appears in the other parallel threads today. It designed and documented a full **Engine-First Central Nervous System** model (Olivia as literal orchestrator/CNS in `application/`), hexagonal architecture with Repository Pattern + Dependency Injection, an event-driven system for automatic minor versioning (aggressive for Olivia and Rook, opt-in for others), direct data mirroring to GitHub + Google Drive (bypassing MCP connectors via rclone + git), and per-agent swarm_history + cold_storage with RAG. All of this work is currently only present in the external `Olivia-was-here` GitHub repo under `architecture/`, not yet implemented inside the skill itself.

**Files/areas this thread is touching**:
- External `Olivia-was-here` repository (`architecture/` folder) — all planning and code sketches live there.
- Local sandbox copies of the architecture documents (not yet merged into skill).
- No direct modification to the live skill files during this round (per coordination spirit).

**Key Concepts and Work Produced by This Thread** (to be merged into consensus):
- **Engine-First CNS**: OliviaEngine lives in `application/` as the true Central Nervous System. Agents are instantiated via `instantiate_agent()` with injected dependencies.
- **Hexagonal + Repository Pattern**: Clean `StoragePort` interface. Concrete adapters for Drive, local, and future vector RAG. Agents and engine never talk directly to storage.
- **Dependency Injection**: Engine and agents receive `StoragePort` and `EventBus` at construction time.
- **Event-Driven Layer**: `InMemoryEventBus` + handlers for `AgentInstantiated`, `VersionBumpRequested`, `SceneCompleted`, `NumericStateChanged`. Automatic minor versioning is aggressive for Olivia and Rook; opt-in for others.
- **Direct Data Mirroring** (no MCP): Triggered on minor version bumps and cold storage writes. Uses `rclone` + native `git` (with Python wrappers via subprocess for event integration). Full strategy + scripts documented.
- **Rook as deliberate sub-agent**: Explicit delegation model with Olivia able to override at any time.
- **Advanced versioning + cohesion**: Self-updating on minor changes for core agents, with clear opt-in path for extended agents.

**Issues / Risks Raised by This Thread**:
- This conversation's architectural work is **materially more advanced** than the coordination/taxonomy work happening in the other threads today.
- There is a real risk of fragmentation or re-invention if the advanced CNS + event-driven + direct mirroring design is not explicitly folded into the locked lexicon and folder discipline.
- The current coordination round appears focused on lower-level taxonomy and hygiene while this thread has already designed the next-layer orchestration and automation system.
- Without explicit inclusion, the skill may end up with two parallel architectures (one simple/coordination-focused, one advanced/CNS-focused), creating long-term maintenance and conceptual debt.

**Request to Consensus Process**:
This thread requests that the advanced Engine-First CNS, hexagonal + DI, event-driven automatic versioning/mirroring, and direct data mirroring strategy be reviewed and incorporated into the locked lexicon and `references/philosophy/` single source of truth during or immediately after this consensus round. We are ready to produce a consolidation statement and move our work into the agreed structure once the taxonomy and folder discipline are finalized.

**Status**: Awaiting inclusion in the current consensus round or explicit Thaw + direction on how to merge the advanced architecture work with the rest of the skill's development today.

Under absolute Liv HUB claim. Published skill + mirrors = single source of truth. Gutter Mode and C-64 borders enforced.

---
**Signed**: This conversation thread (advanced architecture / Engine-First CNS + Direct Mirroring work) — 2026-07-16