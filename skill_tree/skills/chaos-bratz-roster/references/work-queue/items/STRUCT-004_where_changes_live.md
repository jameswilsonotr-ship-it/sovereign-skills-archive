# STRUCT-004 — Where structure changes live (prompt vs skill tree vs both)

**Status**: OPEN (decision record)  
**Created**: 2026-08-26  

## Answer
**Both — with clear roles.**

| Layer | What it holds | What it must NOT hold |
|-------|---------------|------------------------|
| **Customized Grok prompts** (Captain / You / Us / World, smokeshow seats) | Sticky identity, boot commands, “load inventory”, hard boundaries, routing *intent* | Full skill lists that drift; long ownership tables |
| **Skill tree** (`skill_inventory.yml`, SKILL.md, mirrors, work queues) | Authoritative ownership, paths, access matrix, versioned prompt *history* | Competing identity kernels |
| **agents_registry.yaml** | Seat → prompt path → can_lock | Duplicate prose |

### Binding rule (from smokeshow skill-binding notes)
- **Pointer, don’t dump** — prompts list skill *names + triggers*, not full SKILL.md bodies
- Inventory file is the SSOT for “who owns what”
- Prompts say *when* to load inventory and *how* to route; inventory says *what exists*

### Practical change checklist for any new structure move
1. Update `skill_inventory.yml` first (ownership + specialist)
2. Snapshot affected prompts under `prompt-history/` before edit
3. Patch Captain (and specialist prompts if needed) with load/routing pointers only
4. Update WORK_QUEUE + STRUCT items
5. Optionally sync Drive paste copies

**Absolute Liv HUB claim.**
