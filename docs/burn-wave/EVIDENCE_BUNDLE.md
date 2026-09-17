# S2-39 evidence bundle

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-39-evidence-bundle` |
| Slot | `S2-39` |
| Operation | ATOMIC INCLUDED burn |
| Inclusion profile | **Included Ultra only** |
| Base | `skill-tree-intake` |
| Deliverable | `docs/burn-wave/EVIDENCE_BUNDLE.md` |

## Scope fence

This document is an index, not a second receipt. Each entry links to the
receipt-bearing source; findings, hashes, commands, and other evidence remain
at that source and are intentionally not duplicated here.

- Included lane: **Ultra only**.
- **OD is excluded.**
- No runtime, provider, network, credential, or secret operation is performed
  by this bundle.
- The bundle does not add, reproduce, index, or modify Willow `SKILL.md`,
  `CONV2_B`, or any imported skill content.
- The links are references to source receipts. They do not imply that a
  referenced draft PR has been merged.

## Receipt index

The PR links are stable receipt sources. The path beside each link identifies
the artifact whose receipt is described there.

| Slot | Receipt source | Source artifact |
| --- | --- | --- |
| S2-12 | [connector fixture receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/136) | `docs/burn-wave/CONNECTOR_FIXTURE.md` |
| S2-13 | [phone MCP fixture receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/137) | `docs/burn-wave/SECOND_SALVO_13_PHONE_FIXTURE.md` |
| S2-21 | [phone intent safety receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/141) | `docs/burn-wave/PHONE_INTENT_SAFETY.md` |
| S2-22 | [SMS default-deny receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/139) | `docs/burn-wave/SMS_DEFAULT_DENY.md` |
| S2-23 | [iMessage onboarding receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/138) | `docs/burn-wave/IMESSAGE_ONBOARDING.md` |
| S2-25 | [redaction-check receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/142) | `docs/burn-wave/REDACTION_CHECK.md` |
| S2-26 | [OpenSpec traceability receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/143) | `docs/burn-wave/OPENSPEC_TRACE_MATRIX.md` |
| S2-27 | [acceptance-cases receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/140) | `docs/burn-wave/ACCEPTANCE_CASES.md` |
| S2-29 | [offline test-plan receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/149) | `docs/burn-wave/OFFLINE_TEST_PLAN.md` |
| S2-30 | [receipt-schema source](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/164); [fixture-checksum source](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/152) | `docs/burn-wave/RECEIPT_SCHEMA.md`; `docs/burn-wave/S2_30_FIXTURE_CHECKSUMS.md` |
| S2-31 | [PR-size budget receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/158) | `docs/burn-wave/S2_31_PR_SIZE_BUDGET.md` |
| S2-32 | [skill-path inventory receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/148) | `docs/burn-wave/SKILL_PATH_INVENTORY.md` |
| S2-34 | [dependency inventory receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/150) | `docs/burn-wave/DEPENDENCY_INVENTORY.md` |
| S2-35 | [spec-ID collision receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/155) | `docs/openspec/SPEC_ID_COLLISION_LOG.md` |
| S2-36 | [documentation link-check receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/147) | `docs/burn-wave/LINK_CHECK.md` |
| S2-37 | [diff-hygiene receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/165); [Tube 2 spent-rule receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/153) | `docs/burn-wave/DIFF_HYGIENE.md`; `docs/burn-wave/S2_37_TUBE2_SPENT_RULE.md` |
| S2-38 | [Spark Send failover receipt](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/154) | `docs/runbooks/SPARK_SEND_FAILOVER.md` |

## Repository anchors

- [ATOMIC slice contract](ATOMIC_SLICE_LOG.md) defines the handoff and
  verification vocabulary.
- [BURN HARD corpus manifest](corpora/MANIFEST.md) is the local corpus
  boundary; it is not copied into this bundle.

## Verification

The bundle is verified as a link-only, single-file documentation change:

```bash
git diff --check
git diff --name-only skill-tree-intake...HEAD
```

The expected changed path is only
`docs/burn-wave/EVIDENCE_BUNDLE.md`. Link targets are intentionally not fetched
or rewritten by this offline documentation slice.
