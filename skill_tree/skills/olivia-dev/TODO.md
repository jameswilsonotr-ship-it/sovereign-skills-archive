# TODO — olivia-dev

**Last updated**: 2026-07-19

## High Priority
- [ ] Keep SKILL.md description and body in sync with actual capabilities
- [ ] Document tarball one-pass publish flow
- [ ] Crystal review every 5 turns protocol

## Medium
- [ ] Agentic budgeting (16/4 split) notes
- [ ] Pirate mode / gutter mode application to technical outputs

## Completed
- [x] Initial SKILL.md (frontmatter cleaned of length and <> issues)
- [x] Root README / TODO / CHANGELOG + local git init (2026-07-19)

## Future surface (do not fold yet)
- [ ] Candidate for **dev-surface** (or develop-surface): control-plane feeder that links skill-orchestrator, system-roadmap, olivia-dev / olivia-dev-alpha, format-bible, grok-conversation-miner, and related methodology without merging their private state.
- Phrases would route via skill-orchestrator phrase_routes.md (same pattern as swarm-surface / image-pipeline modules).
- Recorded 2026-07-24 so this is not stuck in one conversation only.

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


