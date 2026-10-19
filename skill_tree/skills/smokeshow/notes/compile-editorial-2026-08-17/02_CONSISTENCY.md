# Consistency Report — 2026-08-17
**agent_id:** HEAVY-REFS-02  
**claim:** Absolute Liv HUB  
**confidence:** high on WQ/path listings; medium on full claim-language parity (sampled, not every SKILL)

## Method
Consumed `01_CARTOGRAPHER.md` + `03_LIVE_VS_MIRROR.md`. Priority skills checked for claim, SSOT, work-queue shape, path existence, envelope anchors, cross-links. Read-only.

## Priority skill matrix

| skill | claim ok | ssot ok | wq ok | paths ok | envelope | cross-links | issues |
|-------|----------|---------|-------|----------|----------|-------------|--------|
| chaos-bratz-roster | yes (roster-surface) | **partial** | yes (WQ + items/) | **partial** | implied via format-bible | mirrors/agents exist | **P1** memory map cites personal/visual/hub/archive under references/ — **dirs absent** on disk |
| system-roadmap | yes (Liv HUB / dev-surface) | yes (plans + packages) | **yes** (table + items/ 13) | yes (SYSTEM_ARCHITECTURE_TARGET, skills-refactor, WQ) | n/a | OK | densest package drawer; index present (MINING_PACKAGE_REGISTRY) |
| skill-orchestrator | yes | yes (refs = orchestration SSOT) | yes (WQ + items/) | yes | links format-bible role | OK | richest control-plane |
| olivia-dev | yes | yes | thin | yes | — | OK | |
| olivia-dev-alpha | yes | yes | yes (table + items/) | yes | — | OK | |
| swarm-surface | yes | yes (modules) | **partial** (WQ yes, **items/ no**) | yes | — | phrase_routes OK | P2 missing items/ |
| format-bible | yes | **yes** (ENVELOPE_SCHEMA + envelopes/) | partial (WQ yes, items/ no) | **yes** | **canonical** | OK | envelope SSOT healthy |
| mcp-surface | yes | modules/plans | no WQ at refs root pattern | yes | — | OK | |
| image-pipeline | yes | rich | partial (WQ yes, items/ no) | yes | — | OK | P2 no items/ |
| grok-conversation-miner | yes | prompt suite | no standard WQ dir seen | yes | — | OK | |
| wheelhouse-packager | yes (Absolute Liv HUB) | CONTRACT.md only | no | yes | — | OK | P3 SKILL silent on references/ |
| smokeshow | yes (Absolute Liv HUB) | agents/notes/candidates (no references/) | no | n/a | — | OK | P2 intentional experimental layout |
| lake-erie-gutter-world | yes | thin | no | yes | — | OK | |
| claim-runtime | yes | handoffs/modules | no | yes | — | OK | |
| cilia-bus (mirror / smoke candidate) | — | DRIVE.md in mirror | — | — | — | staged under smokeshow/candidates | not live top-level |

## Cross-cutting findings
1. **Work-queue shape drift:** Gold pattern = `WORK_QUEUE.md` table + `items/` detail files (system-roadmap, skill-orchestrator, chaos-bratz, olivia-dev-alpha). Weaker pattern = WQ file only, no items/ (swarm-surface, format-bible, image-pipeline).
2. **Status vocab** on system-roadmap is healthy: OPEN, DONE, QUEUED, VALIDATED, PENDING, IN PROGRESS appear in table.
3. **Memory ↔ disk mismatch (P1):** User/system memory pointer block lists chaos-bratz `references/personal|visual|hub|archive` as homes; **those top-level dirs do not exist**. Present: agents, configs, mirrors, system, work-queue. Docs/refactor and atom clouds may still describe the intended map — treat as stale pointer until repaired or memory updated.
4. **Envelope SSOT** lives correctly in format-bible/references/ENVELOPE_SCHEMA.md + envelopes/.
5. **No P0 broken path** found among system-roadmap SKILL-cited references paths sampled (SYSTEM_ARCHITECTURE_TARGET, skills-refactor, work-queue).
6. **smokeshow** deliberately omits references/; uses skill-root agents/boot/candidates/notes — consistent with experimental-surface description, inconsistent with peer skill folder convention (P2 structural, not claim failure).

## P0/P1 list with evidence paths
- **[P1]** chaos-bratz-roster: memory/SSOT pointer map claims `references/personal/`, `references/visual/`, `references/hub/`, `references/archive/` — **NO dir** under `/home/workdir/.grok/skills/chaos-bratz-roster/references/` (only agents, configs, mirrors, system, work-queue). Evidence: `ls references/` + memory pointer block.
- **[P1 watch]** cilia-bus dual presence: mirror top-level skill vs live `smokeshow/candidates/cilia-bus` — intentional smoke staging if rules held; document so no one promotes both.
- **[P2]** swarm-surface, format-bible, image-pipeline: work-queue without `items/` while table/ID style may imply detail files.
- **[P2]** smokeshow, sovereign-research-engine: no references/ directory.
- **[P3]** wheelhouse-packager: references/CONTRACT.md exists; SKILL.md has 0 mentions of “references”.

## Questions for Synthesis (not answers)
1. Should chaos-bratz personal/visual/hub/archive be restored as dirs, or should memory pointers be rewritten to actual agents/mirrors/system paths?
2. Which mirror-only families (guards, spark/vesper, ingest) are STAGE_SMOKE vs IGNORE for Liv HUB?
3. Back-port system-roadmap 2026-08-16/17 packages into next cursor zip, or keep live-only until promote cycle?
4. Normalize work-queue items/ requirement library-wide, or accept two tiers (full vs light)?

CONSISTENCY DONE — priority_skills=15 issues=6
