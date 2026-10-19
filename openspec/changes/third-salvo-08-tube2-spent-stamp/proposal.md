# Change: THIRD_SALVO T3-08 Tube-2 spent-by-rule stamp

- **Change ID:** `third-salvo-08-tube2-spent-stamp`
- **Slot:** `T3-08`
- **Salvo:** `THIRD_SALVO`
- **Inclusion:** `INCLUDED`
- **Tier:** `Ultra`
- **PR title:** `salvo: T3-08 tube2-spent-stamp`

## Why

The T3-08 allocation needs a durable, reviewable record that Tube-2 is
spent by rule. The record must preserve the allocation boundary without
turning the slot into an execution request.

## What changes

- Add a normative OpenSpec requirement for a Tube-2 spent-by-rule stamp.
- Add the stamp artifact as documentation.
- Add a receipt that records the exact scope and offline verification.

## Scope

This change is documentation-only. It records one `THIRD_SALVO` slot as
`INCLUDED` at the `Ultra` tier.

The stamp is **never On-Demand**. No alternate tier, fallback lane, runtime
hook, provider integration, secret, live infrastructure action, or external
service interaction is introduced.

## Non-goals

- No implementation or runtime behavior.
- No changes to skill files.
- No conversion, deployment, or provider execution.
- No issuance of an external tracking item.
