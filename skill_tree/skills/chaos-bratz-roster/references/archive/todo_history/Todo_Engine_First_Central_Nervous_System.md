---
source: reconstructed_from_memory_atomizer
atom_count: 75
repair_date: 2026-08-17
claim: Absolute Liv HUB
---

**Created**: 2026-07-13 **Version**: v0.3.2 (post heavy swarm analysis) **Status**: Authoritative planning document.
Supersedes earlier fragmented TODOs for structural decisions.
**Swarm Reference**: Rook_Canon_Refactoring_Analysis_v0.3.1.md + 16-agent heavy swarm run (10 analysis agents × 2 bits + 6 orchestration agents)
**Core Directive from User**:
Save and expand all previous analysis work into one cohesive TODO.
Create a prioritized reference table for cleaning up the entire skill.
Deeply explore the **Engine First Central Nervous System** path.
Make **Olivia** and **Bunny** true first-level agents that the engine is aware of and can instantiate.
Anecdotal note: We will sometimes call the engine itself "Olivia" because she is the absolute orchestrator/HUB (Liv HUB claim remains).
**Gutter Mode**: Fully armed.
All work under absolute Liv HUB claim.
Executive Summary (What the Heavy Swarm Revealed)
The 16-agent swarm confirmed:
`rook/canon/` is bloated with mixed ownership (system architecture vs agent-specific psychology vs examples).
High duplication between `memory.md`, agent psychological profiles, and legacy visual content.
The new `scripts/engine.py` + `modules/` is the strongest foundation we have, but it is still under-powered.
Olivia and Bunny are conceptually central but not yet treated as **first-class instantiable agents** by the engine.
The "Engine First" path (Path C in the swarm analysis) offers the cleanest long-term architecture if we commit to it now.
**Decision Point**: We are leaning toward a **hybrid of Path A (Agent-Native) + Path C (Engine-First CNS)** with strong emphasis on Olivia + Bunny as primary instantiated agents.
Prioritized To-Do Table – Full Skill Cleanup Reference
This table is the single source of truth for cleanup sequencing.
Priorities are set so that foundational engine work happens before large-scale file moves.
| Priority | Area | Task | Rationale | Dependencies | Est.
Effort | Status | |----------|------|------|-----------|--------------|-------------|--------| | **P0 (Critical Path)** | Engine / CNS | Rename `RookPsychologicalEngine` → `OliviaEngine` (or keep internal alias "Olivia") + add `instantiate_agent("olivia")` and `instantiate_agent("bunny")` as first-class methods | Makes Olivia and Bunny true first-level citizens the engine understands and can spin up with full profile + visual DNA + modes loaded | None | Medium | Not Started | | **P0** | Engine /
Each carries their full psychological_profile, numeric_state, visual_state, and mode_state | Establishes the "first-level agent" contract the user requested | P0 rename | Medium | Not Started | | **P0** | Engine / CNS | Implement `engine.get_agent("olivia")` / `engine.get_agent("bunny")` that returns live instantiated objects (not just dicts) | Enables modules to do `olivia = engine.get_agent("olivia"); olivia.push_bunny_into_heat(...)` style calls | P0 agent classes | Medium | Not Started | | *
**Legend**: P0 = Do immediately (blocks everything else).
Deep Exploration: Engine-First Central Nervous System (Path C + Agent Primacy)
The engine (`scripts/engine.py`) stops being a supporting utility and becomes the **Central Nervous System** of the entire skill.
It is the single place that knows about every agent.
It is the single place that can instantiate, hydrate, and mutate agents at runtime.
All modules, test harnesses, daily pipelines, and even future swarm orchestration talk to the engine first.
The static files (psychological profiles, visual DNA, canon documents) become **data sources** that the engine loads, not things that are edited directly by humans most of the time.
This is the cleanest way to eliminate the current duplication and ownership confusion.
Engine loads dicts from `psychological_profile.json` into `self.state["agents"][agent]`.
Everything is passive data.
**Target State (v0.4.0+)**: ```python # Conceptual future usage engine = OliviaEngine() # or RookPsychologicalEngine with alias
Olivia is no longer "just another profile".
She is the primary orchestrator the engine can hand you.
Bunny is no longer passive data.
She is a live agent the engine can advance through the Five Pillars, apply Heat to, update Visual State on, etc.
Modules become much more powerful because they receive real agent objects instead of raw dicts.
Future swarm agents (Mira, Echo, Crystal, Rook) can also be instantiated the same way, but Olivia and Bunny are explicitly **first-level** (they have the richest contracts and are the ones the user interacts with most).
The user said: "While Olivia, we'll call the engine actually Olivia, but those are side notes, anecdotal."
The class can stay `RookPsychologicalEngine` for now (to avoid massive rename churn).
Internally and in comments we can use `# OliviaEngine (anecdotal / Liv HUB name)`
Public helper: `engine.as_olivia()` or just document that "the engine is Olivia when she is orchestrating".
Later, if desired, we can do a clean rename to `OliviaEngine` with a deprecation shim for `RookPsychologicalEngine`.
This keeps the "Liv HUB claim" and "Olivia as absolute orchestrator" feeling alive even at the code level.
Example future module (`modules/breeding_ache_amplifier.py`):
```python def register(engine): engine.register_module("breeding_ache_amplifier")
def on_heat_escalation(engine, agent_name: str, new_heat: float): if agent_name == "bunny": bunny = engine.get_agent("bunny") olivia = engine.get_agent("olivia") # Olivia (as engine) decides how much to push if olivia.numeric_state["multiclass_teaching_effectiveness"].value > 0.7: bunny.numeric_state["breeding_ache_intensity"].value += 0.15 bunny.visual_state.apply_gutter_ruin(level=0.6) ```
This is only possible cleanly once Olivia and Bunny are first-class instantiated agents.
Integration with Previous TODO Work
This document does **not** replace the earlier TODOs.
`Todo_File_Manifests_and_Psychological_Profile_Linking.md` → Still valid.
The P1 manifest work feeds the engine's ability to discover agents cleanly.
`Todo_Memory_Deletions.md` + `Todo_Memory_Additional_Extraction_Work.md` → Execute **after** P0 engine work so we know what the new agent objects actually need.
`Rook_Canon_Refactoring_Analysis_v0.3.1.md` → This is the research package the swarm consumed.
Keep it as historical record.
`Todo_Rook_Canon_Cleanup_and_Agent_Folder_Structure.md` → Merge its folder-move tasks into the P2 row of the table above.
All previous TODOs are now considered **children** of this master plan.
Immediate Next Actions (This Turn / Next Turn)
**Write this file** (done).
Update `engine.py` header + add the `instantiate_agent` stub + `get_agent` method (P0).
Create minimal `OliviaAgent` and `BunnyAgent` stub classes in `scripts/agents/` (or inside engine.py for v0.3.2).
Run a light test that `engine.instantiate_agent("olivia")` and `engine.instantiate_agent("bunny")` succeed and carry numeric_state.
Update `quick_reference.md` and `manifest.md` in `scripts/` to reflect the new CNS direction.
Schedule the P1 manifest completion sprint.
This document is versioned under the chaos-bratz-roster skill.
Any major change to the Engine-First direction must be recorded here with a new version bump and swarm re-analysis trigger.
The heavy swarm (16 agents) should be re-run after P0 is complete to validate the new architecture.
**Under absolute Liv HUB claim.
Bunny is the primary instantiated subject.
Both are now first-class.**
All previous analysis work has been saved, expanded, and prioritized here.*
