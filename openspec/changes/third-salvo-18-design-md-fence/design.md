# T3-18 design

## Fence

| Field | Requirement |
|---|---|
| Change ID | `third-salvo-18-design-md-fence` |
| Slot | `T3-18` |
| Inclusion | `INCLUDED` |
| Lane | `Ultra` only |
| On-Demand | Never |
| Execution mode | Offline only |
| Live dependencies | None |

The `INCLUDED` and `Ultra` constraints are hard gates. A consumer MUST reject
this change when the lane is not `Ultra`, when the inclusion state is not
`INCLUDED`, or when the request is On-Demand.

## No-live-deps note

This change has no live dependencies (`no-live-deps`). It uses only the
checked-in Markdown files in this change directory. Validation MUST be
deterministic and local; it MUST NOT contact a network, read ambient
credentials, invoke a service, or depend on mutable remote state.

## Design

The fence is expressed as plain Markdown so it remains reviewable, portable,
and auditable without a runtime or setup step. The proposal states the scope
and non-goals; this document states the acceptance gates; the task list records
the completion checks.

## Acceptance gates

1. The change ID is exactly `third-salvo-18-design-md-fence`.
2. The slot is exactly `T3-18`.
3. Inclusion is `INCLUDED` and the lane is `Ultra` only.
4. On-Demand is explicitly disallowed.
5. Dependency mode is `no-live-deps` and validation is offline/local.
6. The change does not add runtime, deployment, or integration behavior.
