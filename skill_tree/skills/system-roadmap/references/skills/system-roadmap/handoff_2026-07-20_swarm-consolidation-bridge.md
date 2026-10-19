# Conversational Bridge — Swarm System Refactor
**Date**: 2026-07-20  
**From**: Active development conversation  
**Status**: Paused — ready for testing / continuation in a brand new conversation  
**Primary Cluster**: `references/refactoring-clusters/swarm-consolidation/`

---

## What We Were Talking About Before This Thread

Earlier in the broader session we had:
- Built and used the grok-conversation-miner (with missing reference files identified)
- Created a full dual-stub design (Lean vs Rich) for every missing miner reference file
- Stood up the Conversational Handoff System under `system-roadmap/references/skills/` (REGISTRY, NAMING_AND_VALIDATION, per-skill folders)
- That handoff system is now the pattern being reused here

We then pivoted hard into the swarm landscape because the user asked for a comparison of all swarm definitions across the library, grounded in both internal files and live xAI/Grok multi-agent research.

---

## Everything We Covered in the Swarm Thread

1. **Inventory of swarm definitions**
   - Olivia-owned catalog inside chaos-bratz-roster (`lake-erie-16`, `iron-pearl-hub`, `blackwell-5-tier`)
   - Standalone skills: iron-pearl-swarm, blackwell-sovereign-swarm, liv-bunny-agent-swarm, biomimetic-swarm-orchestrator, swarm-miner
   - The more fully developed Swarm Agent v0.2.0 (dual-mode: grounded-context + research) under `references/agents/swarm/`
   - Three different 16-agent semantics that currently coexist and collide

2. **Research note written**
   - Full comparative landscape (internal + xAI public multi-agent behavior)
   - xAI currently defaults to 4 parallel agents, scales to 16 at high effort, focuses on transparent parallel reasoning + merge, not persistent persona/governance stacks

3. **Observation note written**
   - Strengths of each major swarm skill
   - Pain points (especially the triple 16-agent semantics)
   - Structural tensions around context philosophy and safety models

4. **Planning feedback loop**
   - I proposed four directions (A coordinated family, B full condensation, C standardize 16-agent first, D leave biomimetic + swarm-miner out)
   - User selected **C + D** as the best immediate path
   - After C and D, move toward a modified B that still excludes biomimetic and swarm-miner
   - Critical constraint from user: **Olivia must keep ownership of Swarm Agent v0.2.0**
   - User directed creation of a sub-cluster specifically for the Olivia-owned 16-agent definitions

---

## Why I Made My Decisions

- Created `references/refactoring-clusters/` as a pre-instantiation holding area so we could collect research/observation/planning notes without prematurely creating a new top-level skill or forcing condensation.
- Treated the swarm work as the first cluster because the architecture target already flagged “Swarm cluster — still scattered”.
- Separated Research vs Observation vs Planning note classes so evidence, perception, and proposals stay distinguishable.
- Recommended standardizing the 16-agent pattern first (Idea C) because three incompatible meanings of “16-agent swarm” is the highest-friction conceptual problem.
- Suggested leaving biomimetic and swarm-miner out of the first cut (Idea D) because they are the least entangled with Liv/Bunny canon and have different primary jobs.
- Created the `olivia-owned-16-agent-family` sub-cluster immediately after user feedback so Phase 1 work has a clean home that respects Olivia’s ownership of Swarm Agent v0.2.0.

---

## Why the User Made Their Decisions

- Preferred C and D as the cleanest, lowest-risk next steps.
- Explicitly wants Olivia to retain the Swarm Agent v0.2.0 (the dual-mode grounded-context / research system).
- Directed that the definitions already living under the Olivia / chaos-bratz-roster skill should be treated as their own sub-cluster rather than being pulled into a generic mega-runtime too early.
- Wants to pause development now and test the overall system-refactor machinery in a fresh conversation before continuing implementation.

---

## Current Agreed Sequence (Frozen at Pause)

**Phase 1** (next work): Standardize the Olivia-owned 16-agent family  
- Lake Erie 16-Agent Protocol  
- Iron Pearl 16-Agent capacity definition  
- Swarm Agent v0.2.0 (primary; ownership stays with Olivia)  
Work lives in: `refactoring-clusters/swarm-consolidation/olivia-owned-16-agent-family/`

**Phase 2**: Keep biomimetic-swarm-orchestrator and swarm-miner completely out of scope for the first condensation.

**Phase 3** (later): Evaluate condensation of the remaining major runtimes (iron-pearl-swarm, blackwell-sovereign-swarm, liv-bunny-agent-swarm) once Phase 1 is stable.

---

## Key File Locations

- Cluster root: `system-roadmap/references/refactoring-clusters/swarm-consolidation/`
- Research note: `.../research/2026-07-20_swarm-landscape-research.md`
- Observation note: `.../observations/2026-07-20_initial-observations.md`
- Planning note: `.../planning/2026-07-20_planning-direction-after-feedback.md`
- Olivia-owned sub-cluster: `.../olivia-owned-16-agent-family/`
- This bridge: `system-roadmap/references/skills/system-roadmap/handoff_2026-07-20_swarm-consolidation-bridge.md`

---

## Intent for the Next Conversation

Load this bridge + the swarm-consolidation cluster.  
The new conversation should be able to understand the full context, the decisions, the ownership constraints, and the phased plan without needing the original chat history.

Development is paused here for system-refactor testing.
