# Synthesis — Refs Audit — 2026-08-17
**agent_id:** HEAVY-REFS-04  
**claim:** Absolute Liv HUB  
**inputs:** 01_CARTOGRAPHER.md, 02_CONSISTENCY.md, 03_LIVE_VS_MIRROR.md  
**confidence:** high on set counts and path evidence; medium on promote priorities for mirror-only families

## Executive paragraph
Live tree has **22** skills (**20** with references/); Cursor mirror has **92** skills (**41** with references/) plus **20** IDE-only skills-cursor entries. Only live-ahead top-level skills are **smokeshow** and **wheelhouse-packager**. System-roadmap is materially richer on live (28 vs 17 references packages), including same-day cilia tracker, email-bridge, og-coven, two-way-pointers, and python-libs packages. Highest-priority consistency issue is **stale memory pointers** claiming chaos-bratz `references/personal|visual|hub|archive` which **do not exist on disk**. Work-queue gold standard (WORK_QUEUE.md + items/) is held by system-roadmap, skill-orchestrator, chaos-bratz, olivia-dev-alpha; several peers have WQ without items/. No P0 broken architecture path found in sampled system-roadmap citations. Cursor IDE skills must stay IGNORE. No skill was promoted or copied this series (read-only).

## Ranked actions

| pri | action | skill/path | why | evidence ref |
|-----|--------|------------|-----|--------------|
| 1 | **FIX_LIVE** or **DOC** | chaos-bratz-roster references map vs memory pointers | personal/visual/hub/archive cited in memory SSOT block but dirs absent; agents/configs/mirrors/system/work-queue present | 02 §P1; 01 gaps |
| 2 | **DOC** | system-roadmap live-ahead packages | 11 packages only on live; document as live SSOT; optional next mirror zip | 03 LIVE-only list |
| 3 | **STAGE_SMOKE** (already) | cilia-bus | Mirror has top-level skill; live correctly stages under smokeshow/candidates — keep one path | 03; smokeshow/candidates |
| 4 | **DOC** | smokeshow layout | No references/; agents/notes/boot/candidates by design — note exception to peer convention | 01 P2; 02 |
| 5 | **DOC** | wheelhouse-packager SKILL.md | Add one-line pointer to references/CONTRACT.md | 01 P3; 02 |
| 6 | **FIX_LIVE** (optional tier) | swarm-surface, format-bible, image-pipeline work-queue | Add items/ or mark WQ as light-tier in skill README | 02 cross-cutting |
| 7 | **STAGE_SMOKE** / triage | guards, spark/vesper/memories, ingest families | Mirror-only; useful for bus/Vesper parity — do not auto-promote | 03 categories |
| 8 | **IGNORE** | skills-cursor/* (20) | Cursor IDE automation, not Liv HUB | 03 |
| 9 | **IGNORE** / low | remotion-*, frontend-design, manager skills (claude/kimi/…) | Outside current Liv HUB control plane unless requested | 03 other |
| 10 | **DOC** | SR-WQ-028/029 | Already on work-queue; 028 DONE initial, 029 OPEN pointer receipts | Drive work-queue folder; mission control |

## Promote blockers
- Standing policy: default **no new top-level skills** without system-roadmap / skill-orchestrator GO.
- smokeshow remains experimental; candidates stay non-live until explicit GO.
- Mirror-only operational skills need human triage before STAGE_SMOKE batch.
- chaos-bratz path map must be coherent before further memory promotion claims.

## Safe quick wins (P2/P3 doc fixes)
1. One sentence in wheelhouse-packager SKILL.md → `See references/CONTRACT.md`.
2. Note in smokeshow SKILL.md that references/ is intentionally omitted in favor of agents/notes/candidates.
3. HANDOFF or WQ note listing system-roadmap packages unique to live (for next export zip).
4. Optional: swarm-surface WQ “light tier — no items/” label.

## Explicit non-claims
- Did **not** promote any skill into live.
- Did **not** merge or copy mirror → live.
- Did **not** invent SSOT ownership beyond written SKILL.md / system-roadmap / skill-orchestrator policy.
- Did **not** treat skills-cursor as missing Liv HUB skills.
- Did **not** deep-diff every file pair under both trees (name-level + refs subdir level only).
- personal/visual/hub/archive absence is disk evidence; content may exist under other names (agents/mirrors) — full content migration audit is out of scope for this hop.

## Next swarm hop suggestions
1. **Memory-pointer repair hop:** Align chaos-bratz memory block with actual references/ layout (or restore dirs from atom cloud / docs/refactor if content still exists elsewhere).
2. **Mirror triage hop:** One pass per category (guards, spark/vesper, ingest) with STAGE vs IGNORE recommendations into smokeshow notes.
3. **WQ normalization hop:** Library-wide items/ requirement decision under system-roadmap.
4. **Export hop:** Refresh cursor-skills zip from live so system-roadmap packages and smokeshow/wheelhouse-packager appear in next mirror.

## Drive citations (published copies)
- Smoke Show Prep: `11x6GnGGg73tkkiS7MQilWaDtyjSSwHzC`
- work-queue subfolder: `1tpIX2vczSuYNpOhg1J89ZUEHQ0Ep7ZDA`
- Reports live at: `/home/workdir/.grok/skills/smokeshow/notes/heavy-swarm-refs-audit-2026-08-17/`

SYNTHESIS DONE — actions=10 p0=0 p1=1
