# OpenSpec-to-file traceability matrix

| Field | Value |
| --- | --- |
| Change ID | `second-salvo-26-openspec-matrix` |
| Slot | `S2-26` |
| Included profile | Ultra |
| Deliverable | `docs/burn-wave/OPENSPEC_TRACE_MATRIX.md` |
| Ordering | `S2-26-R01` through `S2-26-R09` |
| Scope | Included Ultra material only |

This is a deterministic, repository-local matrix. Each row maps one
OpenSpec item to one repository file. Paths are repository-relative POSIX
paths, rows are fixed in requirement order, and the matrix contains no
timestamps, environment-dependent values, credentials, or network references.

| Requirement | OpenSpec item | Repository file | Trace anchor | Verification |
| --- | --- | --- | --- | --- |
| `S2-26-R01` | Identify the change and slot | `docs/burn-wave/OPENSPEC_TRACE_MATRIX.md` | Metadata table above | Read the `Change ID` and `Slot` fields |
| `S2-26-R02` | Keep the work atomic and reviewable | `docs/burn-wave/ATOMIC_SLICE_LOG.md` | “ATOMIC OpenSpec MONKEY” contract and handoff order | Confirm the slice has one deliverable and one changed path |
| `S2-26-R03` | Define stable slice and change naming | `docs/burn-wave/ATOMIC_SLICE_LOG.md` | “Slice identifiers” and “OpenSpec change directories” | Confirm identifiers use the documented stable naming rules |
| `S2-26-R04` | Describe the local burn corpus without requiring a service | `docs/burn-wave/corpora/MANIFEST.md` | Missing-blob behavior and local ingest command | Inspect that absent blobs use deterministic local fixtures |
| `S2-26-R05` | Provide the machine-readable corpus contract | `docs/burn-wave/corpora/MANIFEST.json` | `schema_version` and `corpora` entries | Parse JSON and confirm both corpus entries are present |
| `S2-26-R06` | Make missing corpus inputs deterministic | `harness/src/sovereign_harness/corpus.py` | `_synthetic_bytes` and `_artifact_bytes` | Run the corpus smoke tests with no local blobs |
| `S2-26-R07` | Verify deterministic corpus receipts | `harness/tests/test_corpus.py` | `test_missing_burn_wave_blobs_are_replaced_with_deterministic_fixtures` | Confirm the synthetic receipt has five records |
| `S2-26-R08` | Verify connector surfaces remain offline | `harness/tests/test_offline.py` | `test_every_connector_surface_stays_offline` | Run the offline smoke test |
| `S2-26-R09` | Deliver one traceability matrix | `docs/burn-wave/OPENSPEC_TRACE_MATRIX.md` | This table and metadata block | Confirm this is the only file added for the change |

## Local verification

```text
PYTHONPATH=harness/src pytest -q \
  harness/tests/test_corpus.py \
  harness/tests/test_offline.py \
  harness/tests/test_hygiene.py
```

The command is a local verification recipe only. This change does not require
network access or external service credentials.
