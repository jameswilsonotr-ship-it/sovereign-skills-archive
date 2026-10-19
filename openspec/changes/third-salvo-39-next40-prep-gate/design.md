# Design

## Gate contract

The gate consumes a local evidence record with these fields:

| Field | Required value |
|---|---|
| `change_id` | `third-salvo-39-next40-prep-gate` |
| `slot` | `T3-39` |
| `t3_land_ref` | A local commit, tag, or receipt identifying the landed T3-39 change |
| `execution_mode` | `Ultra` |
| `network_access` | `false` |

The record may contain additional review notes, but these fields are not
optional. No value is inferred from a missing field.

## Decision procedure

Evaluate the checks in order:

1. Check that `change_id` and `slot` match this change.
2. Check that `t3_land_ref` identifies a local landed T3-39 result.
3. Check that `execution_mode` is exactly `Ultra`.
4. Check that `network_access` is `false`.
5. Emit the result and a receipt containing the supplied evidence.

The first failed check determines the result:

| Failure | Result |
|---|---|
| Missing or non-local T3-39 land evidence | `BLOCKED_T3_NOT_LANDED` |
| Any mode other than `Ultra`, including `On-Demand` | `REJECTED_MODE` |
| Network access enabled or unverifiable | `REJECTED_OFFLINE` |
| Any other missing required field | `BLOCKED_INCOMPLETE_EVIDENCE` |

Only a result of `READY_FOR_NEXT40_PREP` may be recorded as passing.

## Fail-closed behavior

The gate must not repair evidence, select a different mode, or continue after
a failed check. A blocked or rejected receipt is still useful: it identifies
the first missing condition without authorizing next-40 preparation.

## Receipt shape

```text
change_id: third-salvo-39-next40-prep-gate
slot: T3-39
execution_mode: Ultra
t3_land_ref: <local ref or BLOCKED>
network_access: false
result: <gate result>
next_action: <prepare next-40 or resolve the first failed check>
```

The receipt is an evidence record, not an approval for next-40 execution.
