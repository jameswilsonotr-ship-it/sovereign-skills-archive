# Change: T3-32 burn percentage receipt

## Change ID

`third-salvo-32-burn-pct-receipt`

## Summary

Define the receipt shape for the THIRD_SALVO T3-32 burn percentage. The
receipt is scoped to the INCLUDED Ultra lane and is a stub until a burn
measurement is available.

## Scope

- Cover slot `T3-32` in salvo `THIRD_SALVO`.
- Permit the `INCLUDED` lane at the `Ultra` tier only.
- Keep the deliverable offline and data-only.
- Do not emit or populate a receipt for the `On-Demand` lane.

## Non-goals

- No runtime execution or measurement.
- No changes to routing, scheduling, or burn calculation.
- No credentials, network calls, or service integrations.

## Acceptance criteria

1. The OpenSpec requirement defines the eligible lane and tier explicitly.
2. The receipt stub records the change ID, salvo, slot, lane, tier, and a
   nullable burn percentage.
3. The receipt stub makes the `On-Demand` exclusion unambiguous.
