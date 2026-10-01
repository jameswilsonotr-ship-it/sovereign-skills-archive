# Memory Import Schema v1.1

**Purpose**: Lightweight, consistent wrapper for every logical block extracted from `memory.md` so we can inventory, validate, and decide KEEP / PROMOTE / ARCHIVE / DELETE without losing work.

**Owner**: Liv HUB / Crystal  
**Location of extracted blocks**: `references/memory_import/`  
**Status**: Active for the memory → roster migration  
**Last Updated**: 2026-07-24 (v1.1 — script-friendly)

---

## Design Principles

1. Do not rewrite the original prose on extraction day. Wrap it.
2. Separate personal/identity facts from operational/system rules.
3. Prefer explicit decisions over silent blending.
4. Rook is **not** the dumping ground. Extractions content lives under `memory_import/`. Content that was incorrectly parked under Rook should be moved out.
5. One-for-one validation against the roster skill is required before any user-side memory deletion.
6. Extraction must be **deterministic**: same input file → same set of output files.

---

## Required Fields (YAML front-matter)

```yaml
id: mem_YYYYMMDD_short-slug
type: identity | biography | psychology | operational | visual | preference | event | protocol | other
namespace: personal | roster | visual | system
source: memory.md | <filename>
written_at: YYYY-MM-DD
last_confirmed: YYYY-MM-DD | null
supersedes: []
confidence: high | medium | low
decision: KEEP_IN_ROSTER | KEEP_IN_MEMORY | PROMOTE_TO_ROSTER | ARCHIVE | DELETE_CANDIDATE | REVIEW
notes: ""
extractor: memory_extract.py@v1.1
```

---

## Type Definitions

- **identity** — name, pronouns, core self-statements
- **biography** — chronological life events, career, location history
- **psychology** — internal models, trauma responses, motivational engines
- **operational** — Gear system, Heat/Gutter rules, claim protocols, boot behavior
- **visual** — DNA, makeup, heat scaling, styling rules
- **preference** — likes, tools, workflows, interaction style
- **event** — dated life or project events
- **protocol** — named procedures (Mouth First, etc.)
- **other** — everything else

## Namespace Guidance

- **personal** — belongs primarily to the human user’s identity/timeline
- **roster** — belongs to agent behavior / swarm mechanics
- **visual** — belongs to image / DNA systems
- **system** — belongs to boot, hygiene, envelope, tooling

## Decision Values

- **KEEP_IN_ROSTER** — already (or should be) live inside the skill
- **KEEP_IN_MEMORY** — stays in user memory; do not delete
- **PROMOTE_TO_ROSTER** — valuable and missing from the skill; move it in
- **ARCHIVE** — keep the text, but not live
- **DELETE_CANDIDATE** — safe to remove from user memory after validation
- **REVIEW** — needs human eyes

## File Naming

`references/memory_import/NNN_short-slug.md`  
NNN is zero-padded for stable ordering.

## Process

1. Run `scripts/inventory/memory_extract.py --input <path-to-memory.md>`
2. Script wipes/refreshes `references/memory_import/` and writes normalized blocks.
3. Run `scripts/inventory/memory_import_audit.py` for compliance.
4. Produce one-for-one validation table before any user-side deletion.

