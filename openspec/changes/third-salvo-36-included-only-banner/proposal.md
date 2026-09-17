# Change: T3-36 included-only banner

- **Change ID:** `third-salvo-36-included-only-banner`
- **Area:** salvo documentation
- **Slot:** `THIRD_SALVO` / `T3-36`

## Summary

Add a durable, unambiguous banner to the salvo documentation stating that
`T3-36` is INCLUDED in Ultra only and is never On-Demand.

## Motivation

The entitlement classification must remain visible wherever this salvo slot is
documented. A prominent banner prevents the slot from being mistaken for an
On-Demand option.

## Scope

- Add the canonical banner to `docs/salvo/README.md`.
- Specify the required wording and placement in the salvo documentation spec.
- Record the implementation and offline validation in the change receipt.

## Non-goals

- No runtime or product behavior.
- No entitlement or billing logic.
- No integrations, deployments, credentials, or external data.

## Acceptance criteria

1. The canonical salvo documentation contains the exact INCLUDED/Ultra-only
   classification and explicitly says `never On-Demand`.
2. The OpenSpec requirements identify `THIRD_SALVO` slot `T3-36`.
3. The change is self-contained and can be reviewed offline.
