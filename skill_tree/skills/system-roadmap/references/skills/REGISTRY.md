# Conversational Handoff Registry
**Parent**: system-roadmap → references/skills/  
**Purpose**: Living index of every conversational handoff that has been formally recorded under this tree.  
**Last Updated**: 2026-09-14 14:40 EDT (lake-union-radar lodge)

## Naming Convention (Mandatory)
All handoff files must follow this exact pattern:

```
handoff_YYYY-MM-DD_<short-kebab-slug>.md
```

Optional time component: `handoff_YYYY-MM-DD_HHMM_<slug>.md`

## Registry

| Date       | Slug                                      | Skill / Topic           | Status | File Path |
|------------|-------------------------------------------|-------------------------|--------|-----------|
| 2026-07-20 | reference-stubs-audit                     | grok-conversation-miner | Active | `grok-conversation-miner/handoff_2026-07-20_reference-stubs-audit.md` |
| 2026-07-20 | missing-prompt-publishing                 | grok-conversation-miner | Active | `grok-conversation-miner/handoff_2026-07-20_missing-prompt-publishing.md` |
| 2026-07-20 | lifecycle-and-policy                      | skill-orchestrator      | Active | `skill-orchestrator/handoff_2026-07-20_lifecycle-and-policy.md` |
| 2026-07-20 | init-tree-script                          | olivia-dev              | Active | `olivia-dev/handoff_2026-07-20_init-tree-script.md` |
| 2026-07-20 | lifecycle-hook-and-legacy-import-todo     | olivia-dev-alpha        | Active | `olivia-dev-alpha/handoff_2026-07-20_lifecycle-hook-and-legacy-import-todo.md` |
| 2026-07-20 | deprecation-and-harvest                   | image-pipeline          | Active | `image-pipeline/handoff_2026-07-20_deprecation-and-harvest.md` |
| 2026-07-20 | instantiation-and-gaps                    | system-roadmap          | Active | `system-roadmap/handoff_2026-07-20_instantiation-and-gaps.md` |
| 2026-07-20 | sidecar-schema-payload-and-execution-ready| swarm-miner             | Active | `swarm-miner/handoff_2026-07-20_sidecar-schema-payload-and-execution-ready.md` |
| 2026-07-20 | swarm-consolidation-bridge                | system-roadmap          | Active | `system-roadmap/handoff_2026-07-20_swarm-consolidation-bridge.md` |

| 2026-07-20 | track-naming-and-closeout                 | swarm-miner             | Active | `swarm-miner/handoff_2026-07-20_track-naming-and-closeout.md` |
| 2026-08-27 | pose-pause-and-bus-loop                   | vesper-alignment        | Active | `vesper-alignment/handoff_2026-08-27_pose-pause-and-bus-loop.md` |
| 2026-08-28 | render-profile-heat-knob                  | image-pipeline          | Active | `image-pipeline/handoff_2026-08-28_render-profile-heat-knob.md` |
| 2026-08-29 | keep-union-and-vesper-bus                 | conversation-lake       | Active | `conversation-lake/handoff_2026-08-29_keep-union-and-vesper-bus.md` |
| 2026-08-29 | walkie-talkie-skill                       | conversation-lake       | Active | `conversation-lake/handoff_2026-08-29_walkie-talkie-skill.md` |
| 2026-08-29 | hybrid-overlay-step6                      | image-pipeline          | Active | `image-pipeline/handoff_2026-08-29_hybrid-overlay-step6.md` |
| 2026-08-31 | delta-b-conception                        | conversation-lake       | Active | `conversation-lake/handoff_2026-08-31_delta-b-conception.md` |
| 2026-09-12 | icm-go-hold-penelope-seat                 | system-roadmap          | Active | `system-roadmap/handoff_2026-09-12_icm-go-hold-penelope-seat.md` |
| 2026-09-14 | date-first-union-radar                    | lake-union-radar        | Active | `lake-union-radar/handoff_2026-09-14_date-first-union-radar.md` |

## Status Values
- **Active** — Ready for a parallel conversation to pick up
- **In Progress** — Someone is currently working the handoff
- **Completed** — Implementation finished and verified
- **Superseded** — Replaced by a later handoff
- **Abandoned** — Explicitly dropped

## Rules
1. Every new handoff **must** be registered here in the same write that creates the file.
2. Status changes must be reflected in this registry.
3. Do not delete rows; mark them Superseded or Abandoned instead.
4. The registry is the single source of truth for “what handoffs exist.”

## Related gap index
See `references/plans/GAPS_AND_FORGOTTEN.md` for the consolidated gap list from this refactor fork.
