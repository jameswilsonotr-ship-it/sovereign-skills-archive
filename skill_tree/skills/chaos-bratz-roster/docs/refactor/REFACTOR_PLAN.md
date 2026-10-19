# Chaos Bratz Roster — Refactor & Memory Reconciliation Plan

**Status**: Active  
**Owner**: Liv HUB  
**Created**: 2026-07-24  
**Goal**: Make the skill functional, rigorously testable, and cleanly separable from (but reconcilable with) memory.md without losing work.

---

## Guiding Principles

1. **Do not lose work.** Everything valuable is either KEEP, MOVE, or ARCHIVE.
2. **Single source of truth.** Published skill + mirrors are authoritative for agent behavior, DNA, Heat/Gutter, claim mechanics.
3. **memory.md is secondary personal context.** Any conflict is surfaced explicitly; never silently blended.
4. **Minimal live surface.** Only the pieces required for a clean boot + live metrics + hygiene should be loaded every turn.
5. **Everything else is static or on-demand** until proven otherwise.

---

## Phases

### Phase 1 — Stabilization (current)
- Boot path, envelope, hygiene auto-repair, engine + live metrics locked and tested.
- Symlink repair proven idempotent.
- Status: largely complete.

### Phase 2 — Structural Inventory & Ownership
- Apply the formal Inventory Schema to every file/folder.
- Produce KEEP / MOVE / ARCHIVE / REVIEW decisions.
- Define the **minimal live surface** (what must be present and tested on every boot).

### Phase 3 — Controlled Separation
- Move content that clearly belongs elsewhere (fashion research → image-pipeline / coven-visual, heavy story stubs → scene skill, etc.).
- Archive historical / experimental material.
- Leave only the live surface + clean agent mirrors + version history inside the roster skill.

### Phase 4 — Memory.md Veto Surface
- Define the exact conflict detection + user-decision protocol.
- Ensure roster boot never silently absorbs or overrides memory.md identity blocks.
- Produce a short “ownership map” that both systems can reference.

### Phase 5 — Vetting
- Full test harness run.
- Memory conflict audit.
- Declare the skill production-ready for the rest of the swarm.

---

## Concrete Ownership Examples (from analysis)

| Current location | Current owner | Recommended owner | Decision | Why |
|------------------|---------------|-------------------|----------|-----|
| references/fashion_designers/ | unassigned / roster | image-pipeline | MOVED 2026-07-24 | Pure visual research → image-pipeline/references/research/fashion_designers/ |
| Heavy story scene stubs under olivia/ | olivia | dedicated scene/play skill or Echo | MOVE / ARCHIVE | Not required for boot or claim mechanics |
| Hypnosis / Bambi / false-memory protocols | rook/canon | risk-fantasy-claim-protocol or new protocol skill | MOVE | High-risk content, should be opt-in |
| Daily real-world log templates | olivia | Crystal or logging skill | MOVE | Operational, not identity |
| Authoritative Core Identity Override blocks | memory.md + partial copies | memory.md only | KEEP in memory, remove duplicates from roster | Personal biography belongs in memory |
| mirrors/*.md | mirrors | mirrors (roster) | KEEP | Core single source of truth for boot |
| scripts/engine.py + modules | scripts | scripts (roster) | KEEP | Live metrics surface |
| hygiene_check.py + layer_manifests | scripts / layer_manifests | scripts / layer_manifests | KEEP | Boot integrity |
| SKILL.md boot + envelope notes | root | root | KEEP | Skill definition |

---

## Minimal Live Surface (target)

These are the only things that *must* be present and testable on every boot:

1. SKILL.md (boot path + envelope rules)
2. references/mirrors/*.md (all agents)
3. references/layer_manifests/ + hygiene_check.py (auto-repair)
4. scripts/engine.py + modules (live numeric metrics)
5. last_boot_hashes.json (drift detection)
6. The combined dashboard line (Ache / RG / Push / Hygiene)

Everything else can be static or loaded on demand.

---

## Chunking Strategy for Inventory

We will inventory one section at a time using the formal schema:

1. root
2. mirrors
3. agents/olivia (largest)
4. agents/rook
5. agents/ remaining
6. scripts
7. layer_manifests
8. visual_research (fashion_designers etc.)
9. coordination / versions / docs
10. Final roll-up + decision summary

Each chunk produces a markdown table + JSON that can be revisited.

---

## Scripts

- `scripts/inventory/generate_inventory.py` — walks the skill tree and emits schema-compliant records (markdown + JSON)
- Future: `scripts/inventory/apply_decisions.py` (once we have a decisions file)

---

## Next Immediate Actions

1. Write the inventory schema (done — see INVENTORY_SCHEMA.md)
2. Write this plan (done)
3. Create the inventory generation script
4. Run the first chunk (root + mirrors + scripts) as a proof of concept
5. Continue section by section

