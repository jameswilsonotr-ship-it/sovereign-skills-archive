# T3-26 artifact hygiene pass

- **Change ID:** `third-salvo-26-artifact-hygiene-pass`
- **Slot:** `T3-26`
- **Mode:** `INCLUDED Ultra ONLY`
- **Status:** proposed

## Intent

Define a small, offline artifact-hygiene pass for the T3-26 slot. The pass
records what is eligible, what is excluded, and which repository-local checks
must be completed before an artifact is accepted.

## Scope

Included:

- Ultra artifacts explicitly assigned to T3-26.
- The repository-local hygiene checklist in
  `artifact-hygiene-pass.md`.
- A reviewable receipt for the completed documentation pass.

Excluded:

- On-Demand artifacts. They must never be added to this change.
- Any artifact not explicitly assigned to T3-26.
- Payload rewrites, unpacking, or publication.

## Constraints

- Work is offline-only and must use repository-local evidence.
- This change adds documentation only; it does not alter an artifact payload.
- The pass must be deterministic and repeatable from a clean checkout.
- A failed check blocks acceptance rather than being silently waived.

## Acceptance criteria

1. The change contains a scoped OpenSpec proposal, specification, task list,
   pass list, and receipt.
2. Every pass-list item identifies its evidence or its not-applicable reason.
3. The pass list contains Ultra only; no On-Demand item is actionable.
4. `git diff --check` passes and all new Markdown files are non-empty.
5. The change contains no generated payload, network-dependent step, or
   untracked working-tree residue.
