# Change: THIRD_SALVO T3-39 next-40 prep gate

- **Change ID:** `third-salvo-39-next40-prep-gate`
- **Slot:** `T3-39`
- **Status:** Proposed
- **Execution mode:** Ultra only

## Summary

Define the offline preparation gate for the next-40 work item after the
THIRD_SALVO T3-39 change has landed. The gate records whether the T3-39 land
evidence is present, confirms that the requested lane is Ultra, and produces a
small receipt that can be reviewed before next-40 preparation begins.

This change defines the gate and its evidence contract. It does not claim that
T3-39 has landed and it does not start next-40 work.

## Scope

### Included

- A post-land prerequisite for T3-39.
- An explicit Ultra-only mode check.
- A deterministic, offline evidence checklist.
- A receipt format for the gate decision.
- A fail-closed result when a prerequisite or mode check is missing.

### Excluded

- On-Demand execution, fallback, or promotion.
- Any network access or service call.
- Changes to the T3-39 implementation itself.
- Starting, scheduling, or approving next-40 execution.

## Sequencing

1. T3-39 lands on the target baseline.
2. The gate is run against that local baseline.
3. A passing receipt authorizes preparation only.
4. Next-40 remains a separate change and decision.

Until step 1 is evidenced, the gate result is `BLOCKED_T3_NOT_LANDED`.

## Acceptance criteria

- The change is identified by the exact change ID above.
- The gate cannot pass without local evidence that T3-39 landed.
- The only accepted execution mode is `Ultra`.
- `On-Demand` is rejected rather than treated as an alternate path.
- The gate can be evaluated without network access, service access, or
  environment credentials.
- The receipt distinguishes `READY_FOR_NEXT40_PREP` from a blocked result.
