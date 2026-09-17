# Tiered Library Architecture + Consolidation Plan
**Authority**: skill-orchestrator  
**Status**: Active Canonical  
**Last Updated**: 2026-07-19 (reconciled with concurrent branching + code-style work)  
**Absolute Liv HUB claim**

This document is the single source of truth for how the entire user skill library is organized, tiered, and evolved.  
Compatible with the standing policy: **No more top-level skills will be created.** New capability is added by refining existing skills or by progressive-disclosure sub-components living under skill-orchestrator (or the relevant parent).

## Tier Definitions

### Tier 0 — Atomic / Leaf Modules
Pure, focused, progressive-disclosure modules.  
**Required**: Valid SKILL.md + short README.md  
**Discouraged**: state/, kanban/, heavy CLI, full project structure  
**Examples**: Most photographer and style packs

### Tier 1 — Capable Modules
Skills with real logic or light orchestration.  
**Required**: Tier 0 + TODO.md + CHANGELOG.md + consistent frontmatter/README  
**Optional**: light references/, light CLI  

### Tier 2 — Major Systems / Sovereign
Deep systems that own hierarchy or significant behavior.  
**Target**: Strong structure + clear ownership. Prefer progressive-disclosure helpers over new top-level skills.  
**Current Tier 2**:
- chaos-bratz-roster
- skill-orchestrator (this skill — meta-layer)
- image-pipeline (+ registry content to be absorbed)
- olivia-dev + olivia-dev-alpha
- grok-build + grok-build-sovereign
- swarm-miner
- lake-erie-gutter-world
- iron-pearl-swarm / blackwell-sovereign-swarm (to be rationalized)

## Hierarchy & Ownership
- **skill-orchestrator** owns: library inventory, tier assignment, duplication flags, export, discipline checks, consolidation recommendations, and progressive-disclosure helpers (diagram-skill, future export/discipline scripts).
- **olivia-dev / olivia-dev-alpha** own: the rigorous methodology for building and evolving Tier 2 systems. They consult skill-orchestrator for library state.
- Standing policy: no new top-level skills. Prefer sub-components under existing parents.

## Image Pipeline Consolidation Hierarchy (Detailed Design Target)

```
image-pipeline/                          ← single Tier 2 sovereign home
├── SKILL.md
├── README.md
├── TODO.md
├── CHANGELOG.md
├── references/
│   ├── registry/                        ← former image-pipeline-registry logic + dynamic loading
│   ├── styles/                          ← loadable packs (former top-10 lists + style skills become packs)
│   │   ├── bunny-top-10.md
│   │   ├── liv-top-10.md
│   │   ├── valerie-top-10.md
│   │   └── ...
│   ├── photographers/                   ← curated lists as packs
│   ├── claim-protocols/                 ← ink-line, intense-*, possessive-*, velvet, etc. as packs
│   ├── engines/                         ← generate-engine + overlay-engine coordination notes
│   └── dna/                             ← shared visual DNA / holo-ear / bible references
└── scripts/                             ← any shared helpers
```

- image-style-orchestrator → thin dispatcher or absorbed.
- Most individual style/photographer skills → become packs under references/styles/ or photographers/ (Tier 0 leaves).
- coven-visual-system → evaluate fold into image-pipeline visual layer or chaos-bratz-roster.
- Result: one strong parent + many progressive-disclosure packs. Matches "no new top-level skills" policy.

## Dynamic Skill Generation Patterns (Preferred)
1. **Pack / Variant** — Parent skill + loadable packs in references/
2. **Thin dispatcher + rich registry**
3. **Tiered progressive disclosure**
4. **Self-describing hierarchy** (Tier 2 declares what it owns)

## Programmatic Commands (implemented as scripts/ helpers)
- `library export` → scripts/library_export.py (or equivalent) producing concise markdown/JSON
- `discipline check --tier N` → scripts/discipline_check.py
- Results written into references/inventory/

## Related Concurrent Work
- BRANCHING.md and code-style-bible.md (from concurrent conversation) are authoritative for Git and style rules.
- diagram-skill is an internal helper under this skill (no new top-level).
- Dev Skill Cluster condensation (olivia-dev family + MCP-ish tools) is tracked in the TODO and will be coordinated with this plan.

All library structure decisions route through this skill under absolute Liv HUB claim.
