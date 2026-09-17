# Tube-3 Spent-by-Rule Draft — Post-Land

**Status:** Draft template; finalize only after the T3-37 PR lands  
**Slot:** `T3-37`  
**Change-id:** `third-salvo-37-tube3-spent-rule`  
**Execution class:** `included-ultra`  
**Accounting state:** `not-spent` until the post-land fields below are
  completed

## Rule

Tube-3 may be recorded as `spent` only when the exact T3-37 change-id has
landed as one atomic PR, the OpenSpec artifact is complete, and this receipt
has been filled from local repository evidence. The only eligible execution
class is `included-ultra`.

On-Demand is never a fallback. Any On-Demand, provider, secret, external,
Vultr, or Linear path is rejected and leaves the accounting state
`not-spent`.

## Post-land record

Fill these fields after merge:

```text
status: spent
slot: T3-37
change_id: third-salvo-37-tube3-spent-rule
execution_class: included-ultra
pr: <merged PR URL or local review reference>
land_commit: <commit>
artifact_root: docs/openspec/third-salvo/third-salvo-37-tube3-spent-rule/
receipt: <path to completed receipt>
verified_offline: true
```

## Rejection record

Use this shape for any disallowed or incomplete attempt:

```text
status: not-spent
slot: T3-37
change_id: third-salvo-37-tube3-spent-rule
reason: <on-demand | ambiguous-class | incomplete | forbidden-path>
verified_offline: true
```

This draft records a repository rule only. It does not prove that a provider
meter changed and does not initiate or authorize any spend.
