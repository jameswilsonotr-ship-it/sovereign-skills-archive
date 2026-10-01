# T3-40 salvo closeout

## Change ID

`third-salvo-40-salvo-closeout`

## Summary

Close out slot T3-40 in the third salvo with one explicit inclusion class:
Ultra. The slot must never resolve to On-Demand, including as a fallback.

## Motivation

The slot needs a durable, reviewable contract so that its inclusion class is
unambiguous at closeout and cannot be widened by a later interpretation.

## Scope

- Record T3-40 as a member of `THIRD_SALVO`.
- Permit `Ultra` as the only inclusion class.
- Reject `On-Demand` for T3-40 in every path.
- Produce a local closeout receipt that points to this change.

## Non-goals

- No runtime, application, or payload changes.
- No network, service, credential, or account operations.
- No changes to unrelated slots or salvo definitions.

## Acceptance

The change is complete when the accompanying specification, task checklist,
and closeout receipt agree on the same change ID, slot, salvo, and inclusion
rule, and local validation passes.
