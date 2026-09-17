# Agentic Mapping — from Perun Decision Language to Swarm Operators

This document is the living bridge between extracted decision operators and concrete Chaos Bratz / Liv HUB primitives.

## Design rule
Every operator must be expressible as one of:
- a mode flag
- a Rook call / gate
- a shared model object
- a task-graph attachment
- a scheduler re-rank rule

No free-floating advice. Everything becomes enforceable machinery.

## Current operator → primitive map (E7 seed)

### COMMITMENT_GATE
- **Trigger**: numeric threshold crossed + irreversible language
- **Primitive**: Rook-owned gate that can set `swarm.mode = "total_commitment"` and disable certain rollback options
- **File target**: `references/system/commitment_gates.md` (to be created)

### TEMPORAL_REORDER
- **Trigger**: explicit countdown or “before X arrives”
- **Primitive**: Olivia clock service re-ranks the active work queues of all agents
- **Integration**: already compatible with existing `⏱️Clock` dashboard line

### MIN_VIABLE_FORCE
- **Trigger**: “enough / five ships is enough / not leaning heavy”
- **Primitive**: resource-cap rule that Rook can enforce on any allocation request
- **Effect**: prevents economy-of-force violations across the swarm

### INTEL_VALUE_SCORE
- **Trigger**: research / probe / audit that collapses multi-agent uncertainty
- **Primitive**: Crystal scores the action; high scores can preempt lower-priority tasks
- **Future**: feed into the dual-atom search priority

### OPPONENT_MODEL_UPDATE
- **Trigger**: new observation about external system or other agent behaviour
- **Primitive**: shared writable model object under `references/models/`
- **Consumers**: every agent can read; only Olivia / Crystal write

### CONTINGENCY_ATTACH
- **Trigger**: any plan statement that contains an explicit if-then
- **Primitive**: every high-level task object gains an optional `contingency` field that is itself a first-class task graph
- **Owner**: the agent that created the parent task

### MULTI_FRONT_BALANCE
- **Trigger**: simultaneous talk about multiple competing resource sinks
- **Primitive**: Olivia attention-budget allocator that keeps a soft cap on how many fronts can be “hot” at once

## Extension path
When a new transcript is acquired:
1. Run `extract_decision_ops.py`
2. Manually or automatically promote high-frequency / high-value operators into this document
3. Generate thin skill or mode stubs if the operator is stable enough
4. Version the operator set under the skill

This keeps the cognitive library growing without turning every video into a permanent new skill.
