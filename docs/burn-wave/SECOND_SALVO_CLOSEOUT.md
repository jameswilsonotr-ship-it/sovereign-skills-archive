# Second Salvo Closeout — S2-40

This is the closeout record for OpenSpec change-id
`second-salvo-40-closeout`.

| Field | Decision |
| --- | --- |
| Slot | `S2-40` |
| Included scope | **Ultra only** |
| Excluded scope | **OD** |
| Delivery | One docs-only draft PR against `skill-tree-intake` |

## Landed

- The Ultra-only boundary is recorded as the source of truth for this
  closeout.
- The existing burn-wave corpus and offline harness remain the landed
  foundation for this slot:
  - `docs/burn-wave/corpora/MANIFEST.json`
  - `docs/burn-wave/corpora/MANIFEST.md`
  - `harness/`
  - `.github/workflows/harness.yml`
- No OD deliverable is represented as landed by this change.

## Deferred

- Any follow-up that expands beyond the Ultra-only boundary.
- Any additional integration, rollout, or operational work that does not have
  an explicit S2-40 acceptance decision.
- OD work is not part of this deferred queue; it is excluded from this salvo
  and requires a separately scoped change if it is requested later.

## Blocked

- There is no implementation blocker for this documentation-only closeout.
- Unnamed work cannot be accepted into S2-40 without a human owner,
  acceptance criteria, and an explicit scope decision.

## Human decisions

The following decisions are binding for this closeout:

1. Include **Ultra only**.
2. Include **no OD**.
3. Keep the change to one pull request.
4. Target `skill-tree-intake` as the base branch.
5. Open the pull request as a draft.

Anything outside those decisions is out of scope for `second-salvo-40-closeout`
and must not be inferred as landed.
