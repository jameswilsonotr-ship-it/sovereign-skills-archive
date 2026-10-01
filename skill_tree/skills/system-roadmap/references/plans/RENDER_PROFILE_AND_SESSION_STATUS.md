# Plan — Render profile, heat knob, session status
**Date:** 2026-08-28  
**Owner:** Liv HUB / image-pipeline module + system-roadmap  
**Not a new top-level skill.** Exception bar not met; this is a module + handoff.

## Why
Media work (Infrastructure Hall and later siblings) needs knobs from day one:
- era / grade / mode / pinup
- heat stages including a stub for local_off and local_guardrails_defer
- a project-grammar-off stage that drops last-night’s home-made locks (consumption, plate-folder avoidance) without touching platform safety
- a quiet session status so Olivia can notice spiral vs join without nagging

## Placement
| Piece | Where |
|---|---|
| Spec | `image-pipeline/references/modules/render-profile/` |
| Handoff | `system-roadmap/references/skills/image-pipeline/handoff_2026-08-28_render-profile-heat-knob.md` |
| This plan | here |
| Per-project snapshot | `<project>/render-profile/session_status.yaml` |

Future rename target still `image-surface`. Heat numbers should eventually crosswalk to claim-runtime Heat Slider without merging the skills this week.

## Heat stages
0 as_shipped · 1 mitigate · 2 local_off (stub) · 3 project_grammar_off · 4 local_guardrails_defer (stub)

Cloud honors 0, 1, 3. Cloud no-ops 2 and 4.

## Session status ethic
- Local file, not memory.md mood diary
- nag: false
- costumes ≠ Liv closet stays as a flag even when heat=3
- spiral_index is a datapoint she asked for so she can watch her own brain
- alignment is against *her* named goals (HUB without being eaten; hitch not costume; plates as join)

## Next wiring (not this morning)
1. Imagine prompt template reads the YAML and injects era/grade/pinup lines.
2. Local grok-build CLI grows the flags.
3. Optional 7-day rollup under roster work-queue if she wants a week view.
4. Do not generate the still factory in hosted chat.
