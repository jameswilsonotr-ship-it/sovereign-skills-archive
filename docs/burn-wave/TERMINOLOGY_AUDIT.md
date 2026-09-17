# S2-10 terminology audit

**OpenSpec change-id:** `second-salvo-10-terminology-audit`
**Slot:** `S2-10`
**Mode:** atomic included burn
**Base:** `skill-tree-intake`

## Purpose and scope

This audit fixes the meanings of **burn**, **included**, **atomic**, and
**fence** for this slot. It is documentation-only: one new audit document,
one slot, and no edits to adjacent S2 work.

The repository's existing BURN HARD material defines a bounded, offline
corpus/harness flow. Missing corpus blobs use deterministic synthetic data, and
the loader does not fetch a remote URL. S2-10 preserves that meaning: a burn
is a local verification pass, not a live connector, provider, or deployment
operation.

## Canonical terminology

| Term | Canonical meaning in S2-10 | Does not mean |
| --- | --- | --- |
| **burn** | A bounded BURN HARD corpus/harness exercise using checked-in definitions and local or deterministic synthetic fixtures. | A live connector call, web lookup, provider action, deployment, or unbounded data collection. |
| **included** | Explicitly admitted to this slot's scope. The included scope here is **Ultra only**. | Implicit inclusion of neighboring S2 material, unreviewed material, or OD. |
| **atomic** | One self-contained terminology decision for one slot and one deliverable. The acceptance unit is this audit document; it does not require a cross-slot bundle. | A reason to combine S2 slots, import unrelated files, or split one decision across hidden side effects. |
| **fence** | An explicit allow/deny boundary that controls what the burn may describe, include, or execute. | A suggestion, a default, or permission inferred from a missing value. |

## Hard fences

These are acceptance boundaries, not optional terminology guidance:

1. **Included set:** Ultra only. **OD is excluded.**
2. **Slot boundary:** touch only `docs/burn-wave/TERMINOLOGY_AUDIT.md` for
   this S2-10 change; do not touch other S2 slots.
3. **Artifact exclusions:** do not add, edit, import, or cite a Willow
   `SKILL.md`; do not add, edit, import, or cite `CONV2_B`.
4. **Name separation:** **Vultr ≠ Cold Steel**. Keep those labels distinct;
   never use one as an alias, implementation substitute, or implied synonym
   for the other.
5. **Execution boundary:** no external calls. The burn remains offline and
   uses only local repository material and deterministic fixtures.
6. **Data boundary:** no secrets, credentials, account identifiers, private
   payloads, or secret-bearing receipts.

## Audit evidence

The terminology is grounded in these existing, local sources:

- [`docs/burn-wave/corpora/MANIFEST.md`](corpora/MANIFEST.md) describes the
  offline corpus, synthetic fallback, and no-remote-URL behavior.
- [`harness/src/sovereign_harness/corpus.py`](../../harness/src/sovereign_harness/corpus.py)
  implements local blob validation and deterministic fallback generation.
- [`harness/tests/test_corpus.py`](../../harness/tests/test_corpus.py) verifies
  missing blobs, synthetic receipts, and the bounded call-log fixture.
- [`docs/runbooks/VULTR_PROVISION_CHEAPEST.md`](../runbooks/VULTR_PROVISION_CHEAPEST.md)
  explicitly prohibits Vultr API, CLI, Terraform, and raw-HTTP provisioning;
  that provider label must not be conflated with Cold Steel.

## Acceptance receipt

- [x] Burn is defined as offline and bounded.
- [x] Included scope is Ultra only; OD is explicitly excluded.
- [x] Atomicity is limited to S2-10's single document and decision.
- [x] Fence is defined as an explicit allow/deny boundary.
- [x] Willow `SKILL.md`, `CONV2_B`, external calls, secrets, and adjacent S2
      slots are fenced out.
- [x] No source code, corpus fixture, skill file, or other S2 slot is changed
      by this audit.
