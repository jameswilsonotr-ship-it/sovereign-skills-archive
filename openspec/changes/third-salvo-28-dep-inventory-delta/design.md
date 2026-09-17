# Design

## Inventory source and precedence

The delta uses the most recent local inventory evidence available to this
checkout:

| Evidence | Timestamp | Observation |
|---|---:|---|
| `skill-orchestrator` export | 2026-09-16 20:21 UTC | 27 skills scanned; all 27 unassigned |
| `skill-orchestrator` library inventory | 2026-07-19 14:16 UTC | 32 entries in the older ledger |
| 2026-09-16 intake receipt | 2026-09-16 | Identifies inventory exports as the meaningful tree drift |

The dated export is authoritative for the observed scan. The 32-entry ledger is
retained as historical comparison evidence; this change does not rewrite it.

## Delta model

The inventory delta has four independent buckets:

1. **Added:** artifacts introduced by this change.
2. **Removed:** artifacts removed by this change.
3. **Reclassified:** existing artifacts whose tier or dependency class changed.
4. **Dependency surface:** runtime, build, provider, secret, and On-Demand
   dependencies required by the change.

For T3-28, only one documentation artifact is added. The other three buckets
are empty.

## Inclusion boundary

The change artifact is included in **Ultra**. It has no On-Demand representation,
lazy loader, fallback, or deferred dependency. Consumers must treat an absent
On-Demand entry as intentional rather than as a missing install.

## Offline validation

Validation is limited to local text and Git metadata checks:

- confirm the change files exist;
- confirm the delta contains no install command or package manifest;
- confirm the dependency counts and fence fields are zero;
- confirm no forbidden path is introduced.

No dependency resolver, package manager, provider, or secret lookup is part of
the design.
