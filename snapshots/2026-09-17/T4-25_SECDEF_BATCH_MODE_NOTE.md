# T4-25 — SecDef batch-mode desk note

## Decision

T4-25 uses **CONTINUOUS INCLUDED** reload semantics. `INCLUDED` is part of
the continuous reload path; it is never an On-Demand mode or fallback.

## Batch gate

A wet jump enters batch mode when `SecDef >= 10`. The threshold is inclusive:
10 qualifies, while 9 does not.

```text
reload_mode = CONTINUOUS
included = true
SecDef >= 10 wet jump => batch_mode
On-Demand = forbidden
```

## Desk handling

- Keep the reload continuously included.
- Treat a qualifying wet jump as one batch-mode desk event.
- Do not add an On-Demand selector, fallback, or alternate reload path.
- Keep this note and its decision record offline-only.

## Fences

- Do not add a Willow `SKILL.md`.
- Do not add `CONV2_B`.
- Do not add external/provider integrations, secrets, or Vultr references.
- `OD` is forbidden.
