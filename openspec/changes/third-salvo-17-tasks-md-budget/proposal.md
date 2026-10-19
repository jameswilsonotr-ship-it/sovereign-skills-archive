# T3-17: tasks.md size budget

- Change ID: `third-salvo-17-tasks-md-budget`
- Slot: `THIRD_SALVO / T3-17`
- Eligibility: `INCLUDED` tier `Ultra` only
- Mode: offline documentation change

## Summary

Set a small, explicit size budget for the change's `tasks.md` and make the
eligibility boundary testable. This keeps the task list reviewable while
preventing accidental expansion of the slot's scope.

## Scope

- The change applies only when the execution tier is `Ultra` and the mode is
  `INCLUDED`.
- `On-Demand` is out of scope and must never inherit, activate, or fall back to
  this change.
- Validation is local and documentation-only.

## Acceptance criteria

1. The normative eligibility and exclusion rules are recorded in the change
   spec.
2. `tasks.md` states and stays within its byte and line budget.
3. No task introduces a network call, credential requirement, or additional
   execution mode.
