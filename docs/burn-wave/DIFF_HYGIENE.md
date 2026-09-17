# Diff Hygiene

## Burn metadata

| Field | Value |
| --- | --- |
| Burn | ATOMIC INCLUDED |
| Slot | S2-37 |
| OpenSpec change-id | `second-salvo-37-diff-hygiene` |
| Included scope | Ultra only |
| Excluded scope | OD |
| Base branch | `skill-tree-intake` |

## Review contract

This slot is one atomic, docs-only change. The diff MUST:

1. contain only `docs/burn-wave/DIFF_HYGIENE.md`;
2. describe or enforce Included Ultra scope only;
3. contain no OD behavior, requirements, fixtures, or implementation;
4. avoid unrelated formatting, generated output, snapshots, and binaries;
5. remain small enough to review as one focused change.

The work MUST be delivered in one draft pull request against
`skill-tree-intake`. Do not split this slot into follow-up PRs or combine it
with another burn slot.

## Acceptance checks

Before review, verify:

```text
git diff --check
git diff --stat skill-tree-intake...HEAD
git diff --name-only skill-tree-intake...HEAD
```

The final name-only diff must list exactly this file, and the PR description
must identify `S2-37` and `second-salvo-37-diff-hygiene`.
