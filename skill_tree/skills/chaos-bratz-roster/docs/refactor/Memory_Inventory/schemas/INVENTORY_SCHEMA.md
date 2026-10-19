# Shared Inventory & Memory Schema v2.0 (Superset)

**Purpose**: Single shared language for both  
- chaos-bratz-roster file inventory, and  
- memory.md import blocks  

so one-for-one validation is straightforward.

**Owner**: Liv HUB / Crystal  
**Status**: Canonical for Phase 2+ refactor  
**Last Updated**: 2026-07-24

---

## Design Principles

1. Same field names and decision vocabulary everywhere.
2. Roster inventory remains a *report* (JSON/MD artifacts). We do not require YAML front-matter on every source file.
3. Memory import blocks *do* carry YAML front-matter (already implemented).
4. Rook is not a dumping ground. Prefer explicit namespace + recommended_owner.

---

## Shared Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `path` | string | yes (roster) | Relative path from skill root. For memory blocks use the import filename. |
| `id` | string | yes (memory) / optional (roster) | Stable id, e.g. `mem_...` or `roster_...` |
| `type` | enum | yes | See Type Definitions |
| `namespace` | enum | yes | `personal` \| `roster` \| `visual` \| `system` |
| `size_bytes` | int | yes (roster) | 0 for directories |
| `owner_current` | string | yes | Current logical owner |
| `recommended_owner` | string | yes | Better long-term owner |
| `instantiation` | enum | yes (roster) | `boot` \| `on_demand` \| `static` \| `never` \| `unknown` |
| `test_surface` | string | yes (roster) | How we prove it is present/correct |
| `decision` | enum | yes | Shared decision vocabulary (below) |
| `confidence` | enum | yes | `high` \| `medium` \| `low` |
| `linked_properly` | bool | yes (roster) | Symlink / reference health |
| `memory_conflict_risk` | enum | yes | `none` \| `low` \| `medium` \| `high` |
| `source` | string | optional | Origin file or heading |
| `written_at` | date | optional | Best available date |
| `last_confirmed` | date \| null | optional | |
| `supersedes` | list | optional | |
| `notes` | string | yes | Short free-text |
| `extractor` | string | optional | Script that produced the record |

---

## Type Definitions (shared)

- `identity` — name, pronouns, core self-statements
- `biography` — chronological life events, career, location
- `psychology` — internal models, motivational engines
- `operational` — Gear, Heat/Gutter, claim, boot behavior
- `visual` — DNA, makeup, styling, image rules
- `preference` — likes, tools, workflows
- `event` — dated life or project events
- `protocol` — named procedures
- `code` — scripts, engines, modules
- `config` — manifests, hashes, indexes
- `docs` — README, plans, schemas, specs
- `other`

## Namespace (shared)

- `personal` — human identity / timeline
- `roster` — agent behavior / swarm mechanics
- `visual` — image / DNA systems
- `system` — boot, hygiene, envelope, tooling

## Decision Vocabulary (shared)

- `KEEP` — belongs where it is (roster-side shorthand)
- `KEEP_IN_ROSTER` — should live inside the skill
- `KEEP_IN_MEMORY` — stays in user memory; do not delete
- `MOVE` — relocate inside the ecosystem
- `PROMOTE_TO_ROSTER` — bring from memory (or elsewhere) into the skill
- `ARCHIVE` — keep text, remove from live surface
- `DELETE` / `DELETE_CANDIDATE` — safe to remove after confirmation
- `REVIEW` — needs human decision

## Instantiation (roster-focused)

- `boot` — loaded every new conversation
- `on_demand` — loaded by explicit trigger
- `static` — present on disk, not programmatically loaded
- `never` — orphaned
- `unknown`

---

## Output

Roster inventory continues to emit JSON + Markdown reports.  
Memory import continues to emit schema-wrapped `.md` files.  
Both use this shared field and decision language.

