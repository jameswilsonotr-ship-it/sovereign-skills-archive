# T4-09 — CINC-TARGET land-line handoff receipt

**Status:** landed
**Target:** Mag
**UTC:** 2026-09-17T09:41:00Z
**Mode:** offline, local text only

## Delta

T4-09 now treats `CINC-TARGET` as a continuously included reload component.
The component is present at initial target resolution, every reload boundary,
and every land-line handoff. It is not a selectable or deferred component.

The handoff contract is:

```yaml
ticket: T4-09
target: Mag
lane: CINC-TARGET
reload_policy: continuous-included
handoff: land-line
availability: always-included
```

## Reload and handoff rules

1. Resolve `CINC-TARGET` before emitting the first Mag handoff.
2. Rehydrate it on every reload, even when the target is unchanged.
3. Carry the same inclusion state across the land-line handoff boundary.
4. Do not add a selector, lazy path, fallback lane, or per-turn opt-in.
5. If the component cannot be resolved locally, fail closed and report the
   missing local input; do not substitute a remote or hosted source.

## Scope fence

- This receipt is the complete delta; no skill source was edited.
- No out-of-tree material, network call, network integration, credential,
  or hosted-compute dependency was used.
- No alternate conversation variant was read or copied.
- The reload policy is continuous inclusion only.

## Verification

```text
PASS  target is Mag
PASS  lane is CINC-TARGET
PASS  reload_policy is continuous-included
PASS  handoff is land-line
PASS  availability is always-included
PASS  receipt is local and text-only
```

**Receipt:** this file is the sole handoff artifact for the T4-09 delta.
