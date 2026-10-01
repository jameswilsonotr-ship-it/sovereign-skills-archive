# Planning Note — Refined Direction After Feedback
**Cluster**: swarm-consolidation  
**Date**: 2026-07-20  
**Type**: Planning  
**Status**: Active direction (post-feedback)

---

## Feedback Received
- Idea C (Standardize the 16-agent pattern first) is preferred.
- Idea D (Leave biomimetic-swarm-orchestrator and swarm-miner out of the first cut) is preferred.
- After C + D are complete, move toward a condensation closer to Idea B, but **explicitly excluding** biomimetic and swarm-miner.
- Critical constraint: **Olivia should keep ownership of Swarm Agent v0.2.0**.
- Proposed structure: Create a sub-cluster for the swarm definitions that are already defined underneath the Olivia / chaos-bratz-roster skill.

## Agreed Direction

### Phase 1 — Standardize the Olivia-owned 16-agent family (Idea C + ownership constraint)
Treat the following as one coherent sub-family owned by Olivia / chaos-bratz-roster:

- Lake Erie 16-Agent Protocol (`lake-erie-16-agent-protocol.md`)
- Iron Pearl 16-Agent capacity definition (`iron-pearl-16-agents.md`)
- Swarm Agent v0.2.0 (grounded-context + research modes) — **this remains the primary operational 16-agent system and stays under Olivia**

Work to be done in this phase:
1. Clarify and document the single intended semantics (or cleanly separated modes) for “16-agent swarm” when invoked under Olivia.
2. Reduce conceptual collision between the three existing 16-agent descriptions.
3. Keep Swarm Agent v0.2.0 as the living, versioned runtime that Olivia owns and controls.
4. Record the cleaned relationship in a sub-cluster under this refactoring effort.

### Phase 2 — Leave biomimetic + swarm-miner out (Idea D)
- biomimetic-swarm-orchestrator stays independent (algorithmic / nature-inspired family).
- swarm-miner stays independent for now (extraction / mining focus).
- Neither is in scope for the first condensation.

### Phase 3 — Later condensation of the remaining runtimes (modified Idea B)
Once the Olivia-owned 16-agent family is cleaned up, evaluate condensation of the major personality/governance/safety runtimes:

- iron-pearl-swarm
- blackwell-sovereign-swarm
- liv-bunny-agent-swarm

…into a tighter structure (either a real `swarm-runtime` or a well-interfaced small family).  
Biomimetic and swarm-miner remain outside that cut.

## Sub-cluster Created
```
swarm-consolidation/
└── olivia-owned-16-agent-family/     ← new sub-cluster for Phase 1 work
```

This sub-cluster will hold future notes that specifically concern cleaning up and standardizing the three Olivia-owned 16-agent definitions while preserving her ownership of Swarm Agent v0.2.0.

## Next Actions
1. Populate the `olivia-owned-16-agent-family` sub-cluster with a focused observation + research note on just those three definitions.
2. Propose a concrete standardization (single semantics vs. cleanly separated modes).
3. Only after that is stable do we return to the broader runtime condensation question.

---

This planning note supersedes the earlier open planning ideas (A/B/C/D) with the refined direction above.
