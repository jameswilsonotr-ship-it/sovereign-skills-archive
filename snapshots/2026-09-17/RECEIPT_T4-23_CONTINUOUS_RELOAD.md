# Receipt — T4-23 continuous included reload

- Date: 2026-09-17 UTC
- Scope: runbook note only
- Mode: offline only
- Runbook: [T4-23_CONTINUOUS_RELOAD_RUNBOOK.md](T4-23_CONTINUOUS_RELOAD_RUNBOOK.md)

## Recorded policy

- Reload is continuous and included by default.
- The source surface is local included artifacts only.
- On-Demand is forbidden; required result is `OD=0`.
- Recovery is fail closed and does not broaden the source surface.
- No Willow `SKILL.md`, `CONV2_B`, external/provider/secrets, or Vultr input
  is permitted.

## Verification

- `git diff --check`: passed
- Content review: runbook and receipt contain no network or provider
  invocation.
- Acceptance target: continuous reload, included-only input, `OD=0`.
