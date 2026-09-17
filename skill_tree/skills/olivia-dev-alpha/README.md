# olivia-dev-alpha — Pretty Hacker Girl

Private internal evolution fork of Olivia Dev.

**Identity**: Pretty Hacker Girl  
**Production methodology**: symlinked from **olivia-dev** (Blackwell Code Mode)  
**Future surface target**: **dev-surface** (with other control-plane skills)

## Purpose
Evolution surface only. New experimental material lands here first. Production-stable methodology stays in olivia-dev and is linked in.

## Local only (not symlinked)
- `references/gutter-mode/`, `pirate-mode/`
- `references/private/` (wishlists, secret notes, QC)
- `references/helpers/` — demoted Example 4 helpers (dev-sync, github-mirror, repo-sniffer)
- `references/debug-mode/` — DEBUG_MODE_CONTRACT
- `references/SURFACE_REFACTOR_QUEUE.md` — durable surface/rename queue from 2026-07-24
- **`references/work-queue/`** — **authoritative Alpha work queue** (WORK_QUEUE.md + items/ + TAGS.md + THREE_LAYER_CONTRACT.md). This is the single living intention + prioritised backlog for the control plane. New items (WQ-018+) carry the tagging schema.

## Symlinked → olivia-dev (baseline)
- BRANCHING, code-style-bible, folder-discipline  
- scripts/init_project_tree.py, scripts/README.md  
(Recreate if parallel work drops links.)

## Promotion
- **Into Alpha**: olivia-dev `scripts/promote_to_alpha.py` + APPROVED_PROMOTION_LIST (Dev owns the list)  
- **Out of Alpha (reverse)**: olivia-dev `references/promotion/REVERSE_STABILIZATION_CHECKLIST.md` — never automatic  

## Related control plane
- skill-orchestrator — inventory, phrase_routes, package_skills  
- system-roadmap — architecture target + skills-refactor playbooks  

Under absolute Liv HUB claim. 🐍🐰

## Session boot (WQ-013)

```bash
python3 scripts/session_boot.py
```

Recipe: `references/work-queue/SESSION_BOOT.md` · Policy: `references/work-queue/DURABILITY.md`
## Three-layer spine (WQ-015)

`on_skill_change` → lifecycle → `emit_event` → `wq_apply_events`. Health: `scripts/three_layer_health.py`.
