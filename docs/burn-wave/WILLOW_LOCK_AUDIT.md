# Willow `SKILL.md` Lock Audit

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-33-willow-lock-audit` |
| Slot | `S2-33` |
| Base | `skill-tree-intake` |
| Base commit | `4337876e6f978e77a9cd7c540603246eec3340ef` |
| Inclusion profile | **Ultra only**; OD excluded |
| Locked target | `skill_tree/skills/willow/SKILL.md` |
| Change type | Documentation-only lock receipt |

## Lock boundary

The Willow `SKILL.md` entrypoint is locked out of this slice. S2-33 does not
copy, hydrate, generate, install, or edit that entrypoint, and this receipt
does not reproduce its source content. The lock remains in force if the
entrypoint is hydrated by a later snapshot; its presence would not authorize
changes in this slice.

The `skill-tree-intake` comparison tree does not need to contain a Willow
source copy for this receipt. Absence is treated as a protected boundary, not
as permission to add one.

## Evidence

The following checks are the audit record for the PR diff:

```text
git diff --name-status origin/skill-tree-intake...HEAD -- \
  skill_tree/skills/willow/SKILL.md
# no output
```

```text
git diff --name-status origin/skill-tree-intake...HEAD -- docs/burn-wave/
# A	docs/burn-wave/WILLOW_LOCK_AUDIT.md
```

Together, these checks show that the locked target is absent from the change
and that the only burn-wave deliverable is this receipt. No other `SKILL.md`
is in scope.

## Acceptance receipt

- [x] The OpenSpec change-id and slot are recorded.
- [x] The base branch and comparison commit are recorded.
- [x] Ultra-only scope is recorded; OD is excluded.
- [x] Willow `SKILL.md` is explicitly locked and absent from the PR diff.
- [x] No Willow source content is copied into the receipt.
- [x] The change is limited to `docs/burn-wave/WILLOW_LOCK_AUDIT.md`.
