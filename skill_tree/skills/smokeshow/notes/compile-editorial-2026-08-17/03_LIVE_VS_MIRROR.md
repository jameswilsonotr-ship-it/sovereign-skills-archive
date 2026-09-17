# Live vs Mirror Diff — 2026-08-17
**agent_id:** HEAVY-REFS-03  
**claim:** Absolute Liv HUB  
**confidence:** high (comm on sorted name lists after re-unpack; refs ls on both trees)

## Set counts
only_live: **2** | only_mirror: **70** | both: **20**

## only_in_live (list)
- **smokeshow** — experimental staging; agents (skill-router, organism-interface, …), boot, candidates/cilia-bus, notes/heavy-swarm-refs-audit-2026-08-17
- **wheelhouse-packager** — deterministic wheel + offline wheelhouse builder; references/CONTRACT.md only

## only_in_mirror (list — top categories)

### guards (6)
permission-loop-guard, rate-limit-guard, sandbox-state-guard, schedule-execution-guard, serialization-guard, workspace-schema-guard

### spark / vesper / memories (13)
memories, memories-ingest, memories-reconstitute, memories-repair, memories-verify,  
spark, spark-audit, spark-session-lifecycle, spark-session-recovery, spark-task-debugger,  
vesper-circular-recovery, vesper-context-store, vesper-engine

### takeout / drive (9)
archive-extractor, google-drive, google-drive-for-dos-index, google-drive-organize,  
google-takeout-codebase-finder, google-takeout-finder, google-takeout-manager, google-takeout-source-mover,  
grok-source-mover

### ingest (5)
grok-auto-ingest, grok-ingestion-work, keep-auto-ingest, memories-ingest, xai-ingest-parser

### other notable
- **cilia-bus** — present as top-level skill in mirror; on live only as `smokeshow/candidates/cilia-bus`
- valerie-context-store, valerie-engine, coven-visual-dna, wardrobe-layering-system
- grok-orchestrator, grok-sweep-runner, grok-split-sync, grok-web-read, grok-data-finder, …
- todo-*, perplexity-manager, claude-manager, kimi-manager, deepseek-manager
- remotion-*, frontend-design, cursor-design-hops, cursor-browser-task
- perun-cognitive-orchestrator, whisper-beat-finder, focus-my-energy, get-more-perspectives, …

## both — references drift table (selected high-value)

| skill | live refs subdirs / notes | mirror refs | richer side | notes |
|-------|---------------------------|-------------|-------------|-------|
| chaos-bratz-roster | agents, **configs**, mirrors, system, work-queue | agents, mirrors, system, work-queue | **live** | live has configs/ |
| system-roadmap | **28** packages (cilia-tracker, email-bridge, og-coven, two-way-pointers, pad-*, python-libs-*, cross-thread, …) | **17** packages | **live** | major live-ahead package set |
| skill-orchestrator | 21 entries incl inventory, protocols, roles, work-queue | similar set (no integrations dir listed same) | ~parity | control-plane SSOT |
| swarm-surface | modules, phrase_routes, work-queue | modules, phrase_routes, work-queue | parity | |
| olivia-dev | 9 entries | 9 similar | parity | |
| olivia-dev-alpha | 5 (incl integrations) | 4 (no integrations in listing) | **live** slightly | |
| format-bible | envelope suite + work-queue | same pattern | parity | |
| image-pipeline | 19 rich | 19 rich | parity | |
| mcp-surface | modules, phrase_routes, plans | same | parity | |
| cilia-bus | (not top-level live) | references/DRIVE.md | mirror-only as skill | staged under smokeshow/candidates on live |

### LIVE-only system-roadmap packages (evidence)
cilia-email-bus-tracker-2026-08-17, circular-multi-surface-recovery-2026-08-16, cross-thread-prompts-2026-08-16, email-bridge-2026-08-17, og-coven-visual-dna-2026-08-17, pad-emotional-vectors-2026-08-16, python-libs-for-circular-system-2026-08-16, python-libs-for-pipeline-2026-08-16, third-party-skills-eval-2026-08-17, two-way-pointers, vesper-briefing-2026-08-16

## Dangerous drift (P0/P1)
- **None confirmed P0** (no contradictory claim language verified by full dual SKILL.md diff this hop).
- **P1 watch:** cilia-bus exists as full skill in mirror but only as smokeshow candidate on live — intentional staging, not silent fork, if smoke rules hold.
- **P1 watch:** system-roadmap package density on live far exceeds mirror; if mirror is treated as “export truth,” live packages are unpublished to that zip (expected for same-day work).

## Cursor IDE skills note
`/tmp/cursor-skills-mirror/skills-cursor/` has **20** entries (create-skill, create-rule, create-hook, shell, review, split-to-prs, …). These are Cursor IDE automation helpers, **not** Liv HUB roster/control-plane skills. Do **not** treat as missing from live. IGNORE for promote unless explicit integration request.

## Implications for promotion / smoke testing
1. **Live-ahead keep:** smokeshow, wheelhouse-packager, system-roadmap dated packages (2026-08-16/17) — document as live SSOT; optional back-port to next mirror zip.
2. **Mirror-only triage for STAGE_SMOKE / IGNORE:**
   - cilia-bus → already staged under smokeshow/candidates
   - guards + spark/vesper/memories + ingest → candidates for future smoke or Vesper parity, not auto-promote
   - takeout/drive helpers → utility; STAGE only if bus needs them
3. No silent promote. Synthesis (Agent 04) owns ranked actions.

DIFF DONE — only_live=2 only_mirror=70 both=20
