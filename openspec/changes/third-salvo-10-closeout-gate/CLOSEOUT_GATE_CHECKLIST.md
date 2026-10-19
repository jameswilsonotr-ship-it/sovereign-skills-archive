# THIRD_SALVO T3-10 closeout gate

Status: `CLOSED` only when every checkbox in this document is checked.

## Identity and lane

- [x] The change ID is exactly `third-salvo-10-closeout-gate`.
- [x] The slot is exactly `T3-10`.
- [x] The lane is exactly `INCLUDED Ultra`.
- [x] `On-Demand` is explicitly recorded as non-qualifying.

## Meter separation

- [x] Any meter value is treated as an observation only.
- [x] No meter threshold authorizes a spawn.
- [x] No meter value triggers a spawn, retry, queue release, escalation,
      schedule, or capacity allocation.
- [x] No meter is interpreted as proof that work was spawned.
- [x] The closeout decision is independent of meter values.

**Required invariant:** `meters ≠ spawn`.

## Hard fences

- [x] No Willow `SKILL.md` is edited.
- [x] No `CONV2_B` content, dependency, or work is included.
- [x] No external or provider call is made.
- [x] No secret is read, created, copied, or stored.
- [x] No Vultr live operation is performed.
- [x] No Linear issue, project, or other artifact is minted.

## Offline evidence

- [x] Evidence is limited to repository-local files and static inspection.
- [x] No external response or live-resource status is used as evidence.
- [x] The OpenSpec package contains the proposal, design, tasks, checklist,
      and receipt.

## Closeout decision

- [x] All identity, lane, meter-separation, hard-fence, and evidence checks
      above pass.
- [x] The receipt records the final state as `CLOSED`.
- [x] The receipt states that this closeout does not authorize spawning or
      any live operation.

If any item is unchecked, the state is `BLOCKED`; do not mark the change
closed.
