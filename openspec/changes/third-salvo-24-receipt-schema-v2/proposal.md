# Change: T3-24 receipt schema v2

## Change ID

`third-salvo-24-receipt-schema-v2`

## Summary

Define an additive receipt schema v2 for `THIRD_SALVO` slot `T3-24`. The
receipt records that this slot is `INCLUDED` at the `ULTRA` tier and cannot be
classified as On-Demand.

## Motivation

The existing receipt documents are useful for human audit, but they do not
carry a stable machine-readable identity for a salvo slot or its inclusion
class. Adding these fields makes T3-24 receipts unambiguous without requiring
existing v1 fields or consumers to change.

## Scope

- Add a machine-readable v2 field contract.
- Add normative OpenSpec requirements for the T3-24 receipt.
- Add a completed local receipt for this change.

## Non-goals

- No changes to existing v1 receipt files.
- No network, service, account, or runtime integration.
- No migration of historical receipts.

## Compatibility

Schema v2 is additive. A v2 receipt retains any v1 fields and permits unknown
fields so older readers can continue to consume the original receipt content.
New readers validate the T3-24 fields defined by this change.

## Acceptance criteria

1. The change is identified by `third-salvo-24-receipt-schema-v2`.
2. The receipt identifies `THIRD_SALVO`, slot `T3-24`, and `INCLUDED` /
   `ULTRA` classification.
3. `on_demand` is explicitly `false`.
4. Execution is explicitly offline and complete.
5. The schema and receipt are local repository artifacts only.
