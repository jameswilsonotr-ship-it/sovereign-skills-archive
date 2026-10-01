# Change: T3-35 OD-forbidden stamp

- **Change ID:** `third-salvo-35-od-forbidden-stamp`
- **Salvo:** Third
- **Slot:** `T3-35`
- **Inclusion:** `INCLUDED`
- **Audience:** `Ultra` only
- **On-Demand:** forbidden

## Intent

Record the T3-35 inclusion boundary as an explicit, desk-visible rule:
T3-35 is included for Ultra and must never be admitted, labeled, or
reclassified as On-Demand.

## Scope

This atomic change adds:

1. An OpenSpec requirement for the T3-35 inclusion boundary.
2. A copyable desk stamp that makes the boundary fail-closed.
3. A repository receipt documenting the offline check.

No runtime behavior, provider integration, credentials, or source skill content
is changed.

## Decision

If a T3-35 item does not carry the `Ultra` inclusion classification, the desk
must stop and hold it for clarification. It must not silently fall back to
On-Demand.
