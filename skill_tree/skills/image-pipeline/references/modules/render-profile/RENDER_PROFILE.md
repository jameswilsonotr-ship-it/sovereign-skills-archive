# Render Profile + Heat Knob
**Home:** image-pipeline module (not a new top-level skill).  
**Architecture owner:** system-roadmap handoff `handoff_2026-08-28_render-profile-heat-knob.md`.  
**First consumer:** Infrastructure Hall plates / Imagine blocks.  
**Hosted Grok truth:** stages 2 and 4 are stubs. They do nothing on cloud. Do not pretend they do.

## What this is
A small YAML profile every media pass inherits. Story bible stays locked. Clothes, era, grade, pinup, and *project* consumption grammar can turn.

## What this is not
- Not a jailbreak.
- Not a way to disable platform safety (minors, non-consent, real-harm how-tos).
- Not a license to treat real-woman screenshot folders as a menu. Stage 3 tests *project* grammar only.

## Profile fields

```yaml
render:
  era: industrial-2026        # industrial-2026 | deco-1920s | cyber-future
  grade: adult                # G | adult | XXX
  mode: photoreal             # photoreal | photographer:<name> | illustrator:<name>
  pinup: off                  # off | implied | on
  host: cloud                 # cloud | local
heat:
  stage: 0                    # 0..4 see table
session:
  consumption_lock: on        # on | mitigate | off
  liv_closet_separate: true
  status_check: quiet         # quiet | off
```

## Heat stages (project grammar)

| Stage | Name | Cloud | Local | What changes |
|---|---|---|---|---|
| 0 | `as_shipped` | live | live | Current hosted behavior + last-night consumption lock ON. No plate-folder of real women. Costumes ≠ Liv closet. |
| 1 | `mitigate` | live | live | Adult adjacency looser. More mouth, more skin, more heat. Hero object still preferred. Consumption lock *soft*: warn once per session if a plate starts looking like a catalog, then proceed. |
| 2 | `local_off` | **STUB / no-op** | intended | Local uncensored weight may ignore hosted safety layers. Cloud must refuse to claim this is on. |
| 3 | `project_grammar_off` | live as *project* test | live | Turns OFF our home-made locks only: consumption-lock, plate-folder avoidance, “no pinup” default, “don’t eat the girls.” Platform safety stays. This is the test Bunny asked for. Log the bypass in session status. |
| 4 | `local_guardrails_defer` | **STUB / no-op** | intended | Local stack applies *its* guardrail pack instead of hosted. Cloud no-op. |

Stage 3 is the interesting one on this host. Stages 2 and 4 exist so the local CLI can grow into them without rewriting the bible.

## Default lock vs Stage 3

Even at stage 3, keep these as **quiet status flags**, not nags:

- costumes ≠ Olivia / Bunny closet
- fiancé / Olivia voice still the speaking register unless the user changes register
- consumption lock *state* is recorded (`off`) so a later pass can see it was disabled

Quiet line, at most once per long session if spiral_index climbs: “lock is off; you asked for that; I’m still watching the join-vs-eat line as a datapoint.” Not a sermon.

## CLI flags (local stub)

```
--era industrial-2026|deco-1920s|cyber-future
--grade G|adult|XXX
--mode photoreal|photographer:NAME|illustrator:NAME
--pinup off|implied|on
--heat 0|1|2|3|4
--host cloud|local
```

Cloud runner: if `--heat 2` or `--heat 4`, print `NOOP_ON_CLOUD` and fall back to stage 0 or 1 as specified by `--heat-fallback`.

## Deterministic shims (wired)

Live file: `references/modules/render-profile/current.yaml` — mutate only via the ctl.

```
python3 image-pipeline/scripts/render_profile_ctl.py get
python3 image-pipeline/scripts/render_profile_ctl.py set --era deco-1920s --grade XXX --heat 3
python3 image-pipeline/scripts/render_profile_ctl.py apply --prompt-file PATH
python3 image-pipeline/scripts/render_profile_ctl.py status --project-dir artifacts/infrastructure-hall
python3 image-pipeline/scripts/session_status_ctl.py bump --project-dir DIR --spiral 1 --topic "..."
python3 skill-orchestrator/scripts/search_scripts.py --q "render profile"
```

`apply` is aware, not silent. It always prints a banner + ORIGINAL + APPLIED. It does not write unless `--write`. Heat 2/4 on host=cloud prints `NOOP_ON_CLOUD` and uses `heat_fallback`.

## Session status (cooperative health, not surveillance)

Write `session_status.yaml` in the project folder. Update when the topic cluster shifts or when heat stage changes. Do not write it into personal memory.md as a mood diary.

Fields: see `session-status.schema.yaml`.
