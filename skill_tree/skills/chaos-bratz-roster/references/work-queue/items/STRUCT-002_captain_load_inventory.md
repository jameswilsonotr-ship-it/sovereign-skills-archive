# STRUCT-002 — Captain prompt: load skill_inventory on boot

**Status**: OPEN (draft instruction ready)  
**Created**: 2026-08-26  
**Priority**: High  

## Problem
Captain currently says: run **"roster boot"** from chaos-bratz-roster.  
It does **not** say: load `skill_inventory.yml` so it knows specialist ownership and tool affinity.

## Change location
**Both**:
1. **Prompt history + live Captain prompt** (customized Grok / Drive source of truth for the seat)
2. **Skill tree** — chaos-bratz-roster boot path should expose inventory as a first-class boot step

## Draft instruction to insert after roster boot
```
SKILL INVENTORY — STANDING RULE
On boot and whenever ownership or routing is unclear, load:
  chaos-bratz-roster/references/configs/skill_inventory.yml
Use captain_routing + skills.*.specialist to decide whether You, Us, or World
should contribute. Do not invent ownership. World owns external tools
(including youtube-transcript). You owns kernel/architecture. Us owns
relationship and claim/open-state surfaces.
```

## Deliverables
- [x] Draft text (this item)
- [ ] Snapshot Captain v0.2.0 with this block
- [ ] Update Drive-side prompt if Bunny re-pastes
- [ ] Optional: session_boot.py prints inventory path / specialist summary

**Absolute Liv HUB claim.**
