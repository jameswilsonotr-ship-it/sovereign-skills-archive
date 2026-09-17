# T4-17 — Tube-4 spent-by-rule (draft)

**Date:** 2026-09-17 UTC  
**Status:** Draft  
**Reload mode:** `CONTINUOUS INCLUDED`

## Rule

Tube-4 is part of every reload by baseline inclusion. Its reload state is
spent by the continuous-included rule itself:

```text
tube4_reload = CONTINUOUS_INCLUDED
tube4_spend  = baseline_reload_inclusion
```

Tube-4 must never be activated through On-Demand (`OD`). There is no
On-Demand fallback, promotion, or override for this tube.

## Acceptance checks

- A reload includes Tube-4 without a request-time activation.
- The mode remains exactly `CONTINUOUS INCLUDED`.
- No Tube-4 path is labeled or routed as On-Demand (`OD`).
- A repeated reload re-applies the same inclusion rule; it does not create a
  second activation mode.

## Fences

This draft is offline-only and intentionally excludes:

- `Willow SKILL.md`
- `CONV2_B`
- external or provider integrations
- secrets
- Vultr
- `OD` activation

No external source, provider, credential, or runtime state is required to
interpret this draft.
