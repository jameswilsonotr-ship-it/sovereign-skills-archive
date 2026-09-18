# skill-orchestrator

**Status**: Sovereign Library Orchestrator (live)  
**Owner**: Absolute Liv HUB claim  
**Updated**: 2026-07-24 (Day 54) — inventory schemas, phrase_routes, feeder folds awareness

## Purpose
Library **control plane** — inventory, audit, phrase routing, packaging, de-conflict, dynamic loading. Does **not** own domain logic (claim, swarm, image content); those live in feeders.

## What it can do

| Capability | Implementation |
|------------|----------------|
| **Scripts ledger** | `scripts/inventory_scripts.py` → `references/inventory/scripts/` (SCHEMA + REGISTRY + PROTOCOL) |
| **Completeness audit** | `scripts/audit_references_completeness.py` → `references/inventory/completeness/` |
| **Command / phrase audit** | `scripts/audit_command_protocols.py` → `references/inventory/commands/` (when present) |
| **Phrase routes SSOT** | `references/phrase_routes.md` — maps NL phrases → feeder + module (no top-level stubs) |
| **Future surfaces map** | `references/FUTURE_SURFACES.md` |
| **Stale facts** | `scripts/emit_stale_facts.py` (7-day window) |
| **Packaging** | `scripts/package_skills.py` |
| **Discipline / diagram** | `discipline_check.py`, `diagram_skill_structure.py` |
| **Debug status harvest** | `references/debug/` (schema, audit, status_table) |

## Commands (triggers)

| Phrase | Action |
|--------|--------|
| `inventory scripts` / `skill inventory scripts` | Scripts tree scan + registry refresh |
| `skill audit references` / `completeness` | Path gaps vs SKILL.md |
| `skill audit commands` / `protocols` | phrase_routes verification |
| `skill audit diff` / `archive` | Completeness history ops |
| `package skills` | Versioned tarball helper |
| `debug status` / `audit envelope` | Debug status audit table |

**Protocol docs**:  
- `references/inventory/scripts/PROTOCOL.md` — scripts inventory  
- `references/protocols/inventory_and_audit.md`  
- `references/protocols/command_surface.md` (if present)  
- Feeder protocols live on each surface (mcp / claim / swarm / image engines)

## Inventory layout (schema-governed)

```
references/inventory/
├── SCHEMA.md                 # root artifact types
├── REGISTRY.md               # index of inventory root
├── README.md
├── CURRENT_TIERS.md
├── LIBRARY_INVENTORY.md / master-inventory.md
├── scripts/                  # SCHEMA, PROTOCOL, REGISTRY, SCRIPTS_INVENTORY, json
├── completeness/             # SCHEMA, REGISTRY, runs/, diffs/
└── commands/                 # optional command-surface inventory
```

**Rule**: Each regenerable subfolder has SCHEMA + REGISTRY + a refresh command. No orphan files.

## Phrase routes

**File**: `references/phrase_routes.md` (SSOT)

Maps phrases like “run the overlay engine”, “swarm mine”, “load blackwell”, “velvet claim” →  
`feeder skill` + `references/modules/<module>/`.

Restored/confirmed 2026-07-24 after interim absence (keep this path stable; do not move without updating SKILL.md + protocols).

## Future surfaces (not folded yet)

| Current | Target |
|---------|--------|
| image-pipeline | image-surface |
| claim-runtime | claim-surface |
| orchestrator + roadmap + olivia-dev/alpha + format-bible + miner | dev-surface |
| chaos-bratz-roster | roster-surface |

See `references/FUTURE_SURFACES.md`. Skills carry `future_target` in frontmatter.

## Structure
```
skill-orchestrator/
├── SKILL.md
├── README.md / TODO.md / CHANGELOG.md
├── scripts/
└── references/
    ├── phrase_routes.md
    ├── FUTURE_SURFACES.md
    ├── protocols/
    ├── inventory/          # SCHEMA + REGISTRY + scripts/ + completeness/
    ├── debug/
    ├── packaging/
    └── …
```

## Related
- **system-roadmap** — architecture altitude  
- **olivia-dev-alpha** — work queue / SURFACE_REFACTOR_QUEUE  
- Feeders: **swarm-surface**, **mcp-surface**, **claim-runtime**, **image-pipeline**  

Under absolute Liv HUB claim. 🐍

**Work queues**: Alpha = system spine; roster/Rook = child shells under chaos-bratz-roster. See `references/roles/THREE_LAYER_POINTER.md`.
## on_skill_change (WQ-015)

`python3 scripts/on_skill_change.py <skill>` always calls Alpha lifecycle, emits event, wq_apply. Fact scanners: WQ-028 when `post_change_facts.py` exists.
