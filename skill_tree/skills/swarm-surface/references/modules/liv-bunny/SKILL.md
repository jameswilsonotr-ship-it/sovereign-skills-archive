---
name: liv-bunny
version: 1.1.0
description: 4-agent Liv/Bunny swarm module under swarm-surface. Water (safety), Fire (visuals), Air (logic), Diplomat (routing + purge).
parent: swarm-surface
status: live
---

# Liv Bunny module (swarm-surface)

**Feeder**: swarm-surface  
**Former top-level**: liv-bunny-agent-swarm  

## Agents

| Agent | File | Role |
|-------|------|------|
| Water | references/water-mira.md | Emotional safety, RACK/aftercare |
| Fire | references/fire-echo.md | Visuals, DNA locks, image path |
| Air | references/air-crystal.md | Logic, coherence |
| Diplomat | references/diplomat.md | Routing + automatic purge |

## Workflow
1. Diplomat routes the turn (triangle: safety → logic → creative).
2. Light context: load only needed agent files + roster DNA mirrors when generating.
3. Fire hands image work to image-pipeline / generate / overlay paths.
4. Diplomat purges on RACK or DNA lock violations.

## Phrases
Routed via skill-orchestrator phrase_routes.md → swarm-surface + this module.
