# TODO — chaos-bratz-roster (root pointer)

**Note**: Primary working todos live in the `to-do/` directory.

**Last updated**: 2026-07-24 (copacetic bridge — all three conversations)

## Active bridge entries (2026-07-24)

Three parallel conversations share this skill. Changelog top section has a bridge entry for each.

| Track | CHANGELOG entry | Hand-off folder / session log |
|-------|-----------------|--------------------------------|
| **Memory consolidation** | Memory consolidation conversation | `docs/refactor/Memory_Inventory/` · `to-do/2026-07-24_memory_consolidation_session.md` |
| **Structural Inventory** | Structural Inventory conversation | `docs/refactor/Structural_Inventory/` · `to-do/2026-07-24_structural_inventory_session.md` |
| **Rook structural cleanup** | Rook structural cleanup conversation | `references/agents/rook/CHANGELOG_2026-07-24_Cleanup.md` · Rook follow-ups below |

### Shared rules
- Memory track: memory.md, crosswalk, PERSONAL_ONLY / promotion homes — **not** agent cold moves
- Structural track: live vs cold, research promotions, file-tree — **not** memory.md decisions
- Rook cleanup track: Rook canon/role-creep/Puppy Tamer — coordinate with structural on live-surface thinness

### Agent thinning (cross-track)
- Living goal: `docs/refactor/Structural_Inventory/STRUCTURAL_GOAL_AND_RISKS.md`
- Memory-side worry log: `docs/refactor/Memory_Inventory/TODO_memory_and_agent_thinning.md`
- Core rule: if a file is not required for a normal-turn answer, it does not belong on the live surface

## Open — Memory track
- [ ] Resolve REVIEW blocks (001 current-active-system, 003 core-interests, 008 SOPs)
- [ ] Route Rook-only identity/ops/visual material to system/personal/visual/hub — not agents/rook/
- [ ] Document conflicts when same fact exists in memory_import + personal/ + agent folder

## Open — Atom Cloud evolution (2026-08-05)
- [x] Schema v0.2.0: added `created_ts`, `promoted_ts`, `geo` to both atomizers; promoted to live JSONs
- [x] Pre-migration backup + weekly backup tree + `make_cloud_backup_tarball.py` helper
- [x] ATOM_CLOUDS.md + standing instruction updated
- [x] Durable canonical location + session-overlay + explicit promote protocol (`data/atom_clouds/` + `promote_clouds.py` + atom_search fallback)
- [ ] Private Olivia operational cloud (Phase 2 — nags/priorities/working notes; mostly hidden)
- [ ] Improve `created_ts` parsing: prefer explicit dates from CHANGELOG / README / front-matter / `[YYYY-MM-DD]` over pure file mtime
- [ ] Decide whether to keep two-cloud model or explore per-skill / third-cloud options (later term)
- [ ] Cross-skill awareness: ensure skill-orchestrator, system-roadmap, olivia-dev-alpha surface the v0.2 schema, backup convention, and durable path

## Open — Structural track
- [ ] Monitor cold/ layout stability under parallel writes
- [ ] Keep Rook-surfaced material off live root unless every-turn required
- [ ] Continue research promotions under the same live-surface test

## Open — Rook cleanup track
- [ ] Finish ownership decisions on remaining `ingrid_puppy_tamer_engine/` files (most are Liv/PDM)
- [ ] Decide final home for anything still in `canon/miscellaneous/`
- [ ] Optional: expand form_and_presence as mastiff lore grows

## Root-level / Immediate
- [ ] Keep this root TODO.md in sync with `to-do/` and CHANGELOG bridges
- [ ] Ensure every new agent capture also updates master index
- [ ] Continue hash verification on every `roster boot`

## Future surface (do not fold yet)
- [ ] Candidate for **roster-surface**: thinner progressive-disclosure boot/orchestration; personas/mirrors/cold stay authoritative in this skill
- Related: swarm-surface / claim-runtime / mcp-surface already absorb sibling domains

See `to-do/` for the full living backlog.

## Handoff
- [ ] See `TODO_HANDOFF_Day54_surface_control_plane.md` (Day 54 surface + control plane resume)

