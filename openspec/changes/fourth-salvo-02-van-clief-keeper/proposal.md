# Change: T4-02 Van Clief keeper

- **Change ID:** `fourth-salvo-02-van-clief-keeper`
- **Target:** `CinC-TARGET` / `Van Clief keeper`
- **Reload:** `CONTINUOUS`
- **Lane:** `INCLUDED`

## Summary

Record T4-02 as the atomic Van Clief keeper slice for the CinC target. The
keeper is continuously included and is never an On-Demand lane.

## Scope

- Define the T4-02 identity, target, lane, and continuous reload mode.
- Publish one OpenSpec change and one offline receipt.
- Keep the deliverable documentation-only and independently reviewable.

## Non-goals and fences

- No Willow `SKILL.md` or skill-tree lock edits.
- No `CONV2_B` unpack or processing.
- No external or provider integrations.
- No secrets, credentials, tokens, or connection strings.
- No Vultr work.
- No On-Demand usage; the lane is forbidden.
- No runtime, deployment, billing, entitlement, or account changes.

## Acceptance criteria

1. T4-02 is identified as the `CinC-TARGET` / `Van Clief keeper`.
2. The classification is `CONTINUOUS` + `INCLUDED`, and explicitly never
   On-Demand.
3. The atomic deliverable contains exactly one change scope and one receipt.
4. The change is offline-only documentation with all fences recorded.
