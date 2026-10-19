# Three-Layer Pointer — system-roadmap

Full contract: `olivia-dev-alpha/references/work-queue/THREE_LAYER_CONTRACT.md`

**This skill**: architecture target, Standing Policy, skills-refactor, handoffs.  
**Does not**: day-to-day WQ rows, completeness engine, debug idle/stale mechanics.

Delegate gaps/audit → `skill audit references`  
Delegate queue/promote → `olivia dev alpha` / `work queue`

## Work-queue map (de-conflict 2026-07-24)

System intention is **split** so roster/Rook active work does not clash with control-plane spine:

| Queue | Path | Role |
|-------|------|------|
| Alpha | `olivia-dev-alpha/references/work-queue/WORK_QUEUE.md` | System Open only (014→013→015→022→012) |
| Roster child | `chaos-bratz-roster/references/work-queue/WORK_QUEUE.md` | Roster dual/three-track (fill in roster chats) |
| Rook child | `chaos-bratz-roster/references/agents/rook/work-queue/WORK_QUEUE.md` | Rook structural (fill in Rook chats) |

Architecture items (e.g. WQ-022 playbooks, WQ-015 plan) stay visible on Alpha Open and/or `references/plans/`.  
Roadmap does not own child queue rows.

## Delegation triggers
| Need | Skill | Trigger |
|------|-------|---------|
| Missing files / audit / diff | skill-orchestrator | `skill audit references` / `skill audit diff` |
| Library shape / condensation | system-roadmap | `system roadmap` / `skills refactor` |
| What next / promote / system queue | olivia-dev-alpha | `olivia dev alpha` / `work queue` / `promote WQ-xxx` |
| Roster track work | chaos-bratz-roster | roster work-queue path above |
| Rook lightening | chaos-bratz-roster Rook | agents/rook/work-queue path above |

Wrong layer asked → name the correct skill + path; do not do the other layer’s job.
