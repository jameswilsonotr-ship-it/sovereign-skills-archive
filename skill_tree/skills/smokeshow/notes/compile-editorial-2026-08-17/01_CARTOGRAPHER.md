# Cartographer Report — 2026-08-17
**agent_id:** HEAVY-REFS-01  
**claim:** Absolute Liv HUB  
**confidence:** high (directory listings + SKILL.md grep; mirror re-unpacked this session)

## Summary counts
- live skills total: **22**
- live skills with references/: **20**
- live skills WITHOUT references/: **smokeshow**, **sovereign-research-engine**
- mirror skills total: **92** (under `/tmp/cursor-skills-mirror/skills/`)
- mirror skills with references/: **41**
- skills-cursor (IDE sibling): **20** — out of scope for Liv HUB promote
- skills claiming refs heavily in SKILL.md: chaos-bratz-roster (44 hits), skill-orchestrator (54), system-roadmap (13), format-bible (6), swarm-surface (3)
- skills with references/ but SKILL.md silent on "references": wheelhouse-packager (has CONTRACT.md only), several light surfaces

## Per-skill map (LIVE)

| skill | root | #entries | subdirs / top files | SKILL mentions refs | severity notes |
|-------|------|----------|---------------------|---------------------|----------------|
| chaos-bratz-roster | live | 5 | agents, configs, mirrors, system, work-queue | yes (44) — SSOT for identity/ops | OK; live has extra `configs/` vs mirror |
| claim-runtime | live | 2 | handoffs, modules | medium | thin but present |
| coven-visual-system | live | 9 | Agent_*_Character_Bible.md ×8 + file_listing | medium | flat bible files, not subdir tree |
| format-bible | live | 10 | ENVELOPE_*, envelopes/, templates/, work-queue | yes (6) — ENVELOPE_SCHEMA SSOT | OK |
| grok-build | live | 4 | README, file_listing, grok-mirror, templates | medium | |
| grok-build-sovereign | live | 3 | README, templates | medium | thin |
| grok-conversation-miner | live | 10 | prompt_*.md suite + help/mine_orch | medium | prompt library style |
| icm-architect | live | 3 | core.md, forms.md, system-map.md | medium | |
| image-pipeline | live | 19 | modules, packs, presets, registries, visuals, work-queue, … | medium | rich |
| lake-erie-gutter-world | live | 3 | README, templates | medium | thin |
| liv-bunny-agent-swarm | live | 4 | air-crystal, diplomat, fire-echo, water-mira | medium | agent role files |
| mcp-surface | live | 3 | modules, phrase_routes.md, plans | medium | |
| olivia-dev | live | 9 | BRANCHING, folder-discipline, promotion, templates, … | medium | |
| olivia-dev-alpha | live | 5 | WHOOP_ASS_FORK, heavy-dev, integrations, work-queue | medium | |
| skill-orchestrator | live | 21 | inventory, protocols, roles, work-queue, mirrors, … | yes (54) — refs = SSOT for orchestration | richest control-plane refs |
| swarm-surface | live | 3 | modules, phrase_routes.md, work-queue | yes (3) — modules/heavy-dev, topic-search | OK |
| system-roadmap | live | 28 | work-queue, plans, skills-refactor, etl-*, cilia-*, og-coven-*, two-way-pointers, … | yes (13) — architecture + packages | **live-ahead** vs mirror (28 vs 17) |
| valerie | live | 4 | TODO, breakdowns, comparisons, file_listing | medium | |
| video-strategy-debrief | live | 3 | debriefs, e7 json, transcript | medium | demoted module |
| wheelhouse-packager | live | 1 | CONTRACT.md | no (0) | **P3** — has refs but SKILL silent |
| smokeshow | live | 0 | (agents/, boot/, candidates/, notes/, scripts/ at skill root) | no (0) | **P2** — no references/; uses agents/notes instead |
| sovereign-research-engine | live | 0 | — | — | **P2** — no references/ |

## Pattern frequency (live)
| pattern | count (approx) | notes |
|---------|----------------|-------|
| work-queue | 8+ | format-bible, image-pipeline, olivia-dev-alpha, skill-orchestrator, swarm-surface, system-roadmap, chaos-bratz, … |
| modules | 5+ | claim-runtime, image-pipeline, mcp-surface, swarm-surface |
| templates | 5+ | format-bible, grok-build*, olivia-dev, skill-orchestrator, lake-erie |
| mirrors | 2 | chaos-bratz-roster, skill-orchestrator |
| system / personal / visual / hub / archive | 1 primary | **chaos-bratz-roster** (canonical roster homes; personal/visual/hub may live under deeper paths or promoted maps) |
| plans | 2+ | system-roadmap, mcp-surface, skill-orchestrator |
| inventory | 1 | skill-orchestrator |

## Gaps for Consistency Auditor
1. **smokeshow** — no `references/`; operational content in `agents/`, `notes/`, `boot/`, `candidates/`. SKILL describes surface but does not claim a references tree. (P2 structural vs peers)
2. **sovereign-research-engine** — no references/ on live. (P2)
3. **wheelhouse-packager** — references/CONTRACT.md exists; SKILL.md does not mention references. (P3 DOC)
4. **coven-visual-system** — flat Agent_* bible files in references/ rather than agents/ subdirs; peer skills use subdirs. (P3)
5. **chaos-bratz live vs mirror** — live has extra `configs/`; both lack explicit top-level personal/, visual/, hub/, archive/ in this listing (may be nested under agents/mirrors or docs — Auditor should verify against memory pointer map).
6. **system-roadmap** — densest package drawer (28 entries); risk of junk-drawer without index (has MINING_PACKAGE_REGISTRY.md — check if complete).
7. Naming: WORK_QUEUE.md appears in multiple skills — confirm consistent casing (not work-queue.md).

## Anti-patterns observed
- Full identity prose: not verified this hop (no deep file reads of biography dumps).
- Empty modules: not flagged empty this hop; swarm-surface/modules and mcp-surface/modules exist with content expected.
- smokeshow intentionally experimental — absence of references/ may be by design (staging surface).

CARTOGRAPHER DONE — skills_mapped=22 live + 92 mirror (41 with refs)
