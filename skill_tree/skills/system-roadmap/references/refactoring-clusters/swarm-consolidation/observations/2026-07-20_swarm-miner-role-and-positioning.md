# Observation Note — swarm-miner Role and Positioning

**Cluster**: swarm-consolidation  
**Date**: 2026-07-20  
**Type**: Observation  
**Based on**: Live inspection of swarm-miner after the 2026-07-20 architecture session + prior cluster research/observation notes

---

## What Is Strong (swarm-miner specific)

1. **Clear extraction focus**. Unlike iron-pearl-swarm, blackwell-sovereign-swarm, or liv-bunny-agent-swarm, swarm-miner is not trying to be a persistent multi-persona runtime. Its primary job is mining conversational history into structured, agent-ready payloads. This focus is a strength.

2. **New internal maturity**. As of 2026-07-20 the skill possesses:
   - A formal, versioned Sidecar Note Schema with four formats and explicit validation rules
   - A local payload storage + lifecycle stub
   - A documented conversion helper with expansion paths
   - Its own research log discipline  
   None of the other swarm-family skills currently publish an equivalent formal schema for run-time discoveries.

3. **Controlled comparison design**. The first real payload deliberately re-uses the exact eight Track B topics that were manually extracted earlier. This gives the skill a built-in validation set and a concrete success criterion (gap analysis against the manual baseline).

## What Is Painful / Positioning Tension

1. **Naming and mental model**. The skill is called “swarm-miner” and is routinely discussed as part of the swarm family, yet its core job is extraction rather than orchestration or persistent agent runtime. This creates a mild category mismatch with the other members of the cluster.

2. **Still incomplete runtime surface**. The schema, formats, and payload system are designed and documented, but the visible mining engine does not yet emit schema-valid sidecar notes or enforce the validation rules. The payload nag is also still only designed. Until those are wired, the new architecture is “on paper.”

3. **Relationship to the 16-agent pattern**. The broader cluster already suffers from three different 16-agent semantics. swarm-miner’s multi-agent payload approach (harper / sebastian / crystal / echo) is a fourth, lighter, extraction-oriented pattern. It does not currently conflict, but it adds another variant that any future consolidation must account for.

## Structural Observation

swarm-miner currently sits in a useful but slightly awkward position:

- Too extraction-focused to be a natural module *inside* a pure runtime skill such as iron-pearl-swarm or blackwell-sovereign-swarm without diluting those skills.
- Too swarm-flavored (multi-agent payloads, visible C-64 output, agent hand-offs) to be cleanly moved into a generic “conversation-miner” or “memory-ingestion” feeder without losing its identity.
- Mature enough in its internal design that any future `swarm-runtime` proposal must explicitly decide what to do with it rather than treating it as an afterthought.

## Open Questions Reinforced by This Observation

- Does the condensation math for a single `swarm-runtime` still look attractive once swarm-miner’s extraction role is taken seriously?
- Is the healthier long-term shape a small family of well-interfaced skills (runtime family + extraction/mining peer) rather than forced absorption?
- Should the formal sidecar / payload / research-log pattern that swarm-miner just acquired be considered a candidate *shared interface* for other swarm-family skills, or kept local?

---

These are pure observations. No consolidation proposal is made in this note.

**Observation recorded**: 2026-07-20
