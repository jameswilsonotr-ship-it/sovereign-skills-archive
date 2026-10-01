# TODO — system-roadmap

**Created**: 2026-07-20  
**Exception grant**: Crucial to the active refactoring process (Standing Policy exception #1)

## High Priority
## 2026-08-12 — Deterministic wiring (Teaching Mode honesty)
- [ ] **SR-WQ-001** Stub/skeleton hunt across all skills → script-based legitimate deterministic functionality. See `references/work-queue/items/SR-WQ-001_stub_skeleton_deterministic_wiring.md`.

## Global hydration launcher (2026-07-26)
- [ ] **Global Skill Hydration / Launch Script** — single Python entrypoint that walks enabled skills, refreshes registries/inventories/wrapper maps/atom indexes, and is the forever baseline for skill discovery/format. Re-runnable when drift or errors appear. See SYSTEM_ARCHITECTURE_TARGET.md work item.

- [ ] Flesh out skills-refactor modules (memory-surgeon, boot-rebuild, inventory-hygiene, condensation-validation)
- [ ] Keep SYSTEM_ARCHITECTURE_TARGET.md current as the living plan
- [ ] Coordinate with skill-orchestrator so the pointer stays accurate
- [ ] Drive Memory.md Surgeon + Boot Sequence Rebuild as the next real work

## Completed
- [x] Top-level skill instantiated
- [x] Architecture target moved/copied in
- [x] skills-refactor sub-skill structure created
- [x] Exception recorded

## Hygiene Integration (2026-07-20)
- [x] Olivia Dev + Alpha folder hygiene and internal-only attributes engaged
- [x] folder-discipline.md, BRANCHING.md, code-style-bible.md copied into references/olivia-dev-hygiene/
- [x] SKILL.md declares the pack and that alpha attributes are ON for this internal work

## Handoffs & Gaps (2026-07-20)
- [x] GAPS_AND_FORGOTTEN.md written under references/plans/
- [x] Per-skill handoff subfolders + handoff_2026-07-20_*.md for: skill-orchestrator, olivia-dev, olivia-dev-alpha, image-pipeline, system-roadmap, grok-conversation-miner
- [x] REGISTRY.md updated with all new rows
- [ ] Close High gaps: legacy import-process, prompt_publishing.md, memory-surgeon/boot-rebuild playbooks (content)

## 2026-07-24 library hygiene
- [x] Three-layer roles documented; pointer under references/roles/
- [x] Completeness + work-queue loop established (alpha owns queue)
- [ ] Memory-surgeon / boot-rebuild playbook content still open
- [ ] Optional: note mcp-surface absorption in SYSTEM_ARCHITECTURE_TARGET domain table (done in session update)

## Future surface (do not fold yet)
- [ ] Candidate for **dev-surface** (or develop-surface): control-plane feeder that links skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, format-bible, grok-conversation-miner, and related methodology without merging their private state.
- Phrases would route via skill-orchestrator phrase_routes.md (same pattern as swarm-surface / image-pipeline modules).
- Recorded 2026-07-24 so this is not stuck in one conversation only.


## 2026-07-24 session close
- [x] Architecture target updated for mcp/claim/swarm/image folds
- [x] Skills-refactor playbooks fleshed out
- [x] Condensation session CHANGELOG + README
- [ ] Batch rename image-pipeline → image-surface, claim-runtime → claim-surface (with reference rewrite + phrase_routes)
- [ ] Scaffold dev-surface / roster-surface only when ready
- [ ] Optional Blackwell reclassification note still open
- [ ] Roster boot rebuild tracked in other conversation (boot-rebuild playbook)

## WQ-015 — Three-layer programmatic spine (TRACKING)

**State**: open | **Priority**: high | **Owner intention**: olivia-dev-alpha  
**Item**: `olivia-dev-alpha/references/work-queue/items/WQ-015_three_layer_programmatic_spine.md`  
**Plan**: `system-roadmap/references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md`

### To-do (phases)
- [ ] Phase 0: Symlink THREE_LAYER_CONTRACT into orchestrator + roadmap roles/
- [ ] Phase 1: EVENT_SCHEMA + events jsonl under Alpha work-queue
- [ ] Phase 2: on_skill_change always calls Alpha lifecycle (symlink path)
- [ ] Phase 3: post_change_facts.py (inventory ± completeness + event)
- [ ] Phase 4: wq_apply_events.py
- [ ] Phase 5: roadmap architecture event inbox (thin)
- [ ] Phase 6: health checks (symlink, WQ vs live skills, no Alpha REGISTRY)
- [ ] Phase 7: session-close UX in all three READMEs

### Awareness rule (going forward)
When **any** development is in progress on olivia-dev / olivia-dev-alpha / skill-orchestrator / system-roadmap:
- Load or cite WQ-015 until state is `promoted`
- Alpha is always in the loop via lifecycle hook once Phase 2 lands
- Do not duplicate WORK_QUEUE outside Alpha

## 2026-07-24
- [x] Surface UI labels (WQ-016) — skills list shows LIVE / candidate / rename pending / misc

## 2026-07-24 work-queue de-conflict
- [x] Roster + Rook child queues created (empty); Alpha system Open slimmed
- [x] THREE_LAYER pointers (orchestrator + roadmap) map the three queues
- [ ] WQ-015 phases still open on Alpha (spine); do not fold into roster queues

## Durability (WQ-014)
- [x] Hybrid Option E documented: `references/plans/DURABILITY.md` + Alpha work-queue twin
