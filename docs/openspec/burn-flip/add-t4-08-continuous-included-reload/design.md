# Design: add-t4-08-continuous-included-reload

## Context

T4-08 is a reload lane, not a one-shot or spend escalation path. Its work
must stay inside the included budget for the whole reload sequence. The
contract is intentionally local and offline so it can be checked without
provider access or sensitive configuration.

## Goals

- Keep every reload iteration continuous and included-only.
- Make On-Demand fallback an explicit hard failure.
- Keep the lane deterministic, receipt-backed, and independently reviewable.
- Detect OpenSpec change-id collisions before matrix output is rendered.

## Non-Goals

- Do not create, edit, or overwrite any `SKILL.md` or skill-tree live-lock
  file.
- Do not use On-Demand capacity.
- Do not call external providers or access secrets.
- Do not provision or reference live infrastructure.
- Do not unpack `CONV2_B`.

## Decisions

1. **Continuous:** a reload remains eligible for the next included iteration
   until the lane is explicitly stopped or the included budget is exhausted.
2. **Included-only:** the lane has no fallback branch that can select
   On-Demand. An unavailable included path is a blocked result, not a reason
   to spend.
3. **Offline verification:** checks use local fixtures and the offline harness;
   no network, provider, secret, or infrastructure dependency is valid.
4. **Collision guard:** OpenSpec IDs are normalized by trimming whitespace and
   case-folding. More than one source for the same normalized ID fails before
   CSV or Markdown output is written.

## Risks

| Risk | Mitigation |
| --- | --- |
| Reload silently becomes one-shot | Require the continuous scenario in the spec |
| Included capacity is unavailable | Block the lane; never select On-Demand |
| Duplicate IDs overwrite matrix meaning | Fail deterministically with all sources |
| A test reaches an external system | Patch sockets and use local fixtures only |
