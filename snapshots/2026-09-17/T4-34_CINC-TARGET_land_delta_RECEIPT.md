# T4-34 — CINC-TARGET land delta receipt

**Status:** landed
**Target:** CINC-TARGET
**UTC:** 2026-09-17T09:51:38Z
**Mode:** offline only

## Delta

T4-34 keeps `CINC-TARGET` continuously included across reload and the land
handoff boundary. It is resolved with the initial included set, rehydrated on
every reload, and carried into the next land state. It is never On-Demand.

The handoff contract is:

```yaml
ticket: T4-34
target: CINC-TARGET
reload_policy: continuous-included
handoff: land-delta
availability: always-included
on_demand: forbidden
```

## Reload and handoff rules

1. Resolve `CINC-TARGET` before the first land state is emitted.
2. Rehydrate it on every reload, including an unchanged-target reload.
3. Preserve the included state across the land-delta handoff.
4. Do not add a selector, lazy path, fallback lane, or per-turn opt-in.
5. If it cannot be resolved from local included input, fail closed and report
   the missing input; do not substitute another source.

## Scope fences

- No Willow `SKILL.md`.
- No `CONV2_B`.
- No external or provider input, secrets, or Vultr work.
- On-Demand (OD) is forbidden; the required OD count is `0`.
- This receipt is the sole handoff artifact; no skill source was edited.

## Verification

```text
PASS  reload policy is continuous-included
PASS  availability is always-included
PASS  handoff is land-delta
PASS  on-demand is forbidden and OD=0
PASS  scope is offline and local text only
PASS  receipt is the sole T4-34 handoff artifact
```

**Receipt:** this file is the complete T4-34 CINC-TARGET land delta.
