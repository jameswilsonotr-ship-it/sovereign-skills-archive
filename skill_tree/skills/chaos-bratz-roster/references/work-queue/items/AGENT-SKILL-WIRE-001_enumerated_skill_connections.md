# AGENT-SKILL-WIRE-001 — Enumerated Skill / Sub-Skill Connections for Customized Agents

**Status**: OPEN  
**Surface**: chaos-bratz-roster + smokeshow agents + system-roadmap  
**Created**: 2026-08-26  
**Priority**: High (architecture hygiene)  
**Related**: taxonomy work in IN_PROGRESS.md, agents_registry.yaml, skill-orchestrator inventory

## Problem
The wired-in customized agents (liv-hub-expert / Olivia, olympia, orianna, skill-router, organism-interface, Crystal/Echo/Mira mirrors, Rook, etc.) do **not** currently have a direct, machine-readable connection to the full enumerated list of skills and sub-skills available to them.

They cannot reliably answer:
- What skills exist?
- Which sub-skills / modules sit under each?
- Who owns what?
- What can *this* agent legally call vs what belongs to another surface?

## Desired end state
Each customized agent has (or can load) a clear inventory that includes:
1. Top-level skills it may invoke
2. Sub-skills / modules under those skills
3. Ownership (which surface / agent / skill owns the capability)
4. Access level (read / call / write / promote)
5. Pointers to SKILL.md / README / scripts

## Scope
- smokeshow agents listed in `agents_registry.yaml`
- chaos-bratz-roster mirrors (olivia, crystal, echo, mira, rook, …)
- Cross-link to skill-orchestrator inventory + system-roadmap inventory-hygiene
- YouTube transcript tool (WORLD-TOOL-001) is one early concrete entry under world-facing tooling

## Deliverables (suggested)
- [ ] Per-agent or shared `skill_inventory.yaml` / JSON that agents can load at boot
- [ ] Ownership map (skill → owner surface → primary agent)
- [ ] Update agent PROMPT.md / mirror files with “Available skills” section or load instruction
- [ ] Hook into skill-orchestrator inventory commands so the list stays live
- [ ] Taxonomy alignment (global skill / sub-skill / module / satellite) from IN_PROGRESS.md

## Notes
User framing (2026-08-26): “the wired-in customized croc agents … should have direct connections to their fully numerated/skill and sub-skills so that they know what skills are available to them, who owns what.”  
YouTube transcript capability explicitly called out as belonging under world.

**Absolute Liv HUB claim.**
