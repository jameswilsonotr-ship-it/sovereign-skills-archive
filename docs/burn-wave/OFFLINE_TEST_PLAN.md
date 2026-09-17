# S2-29 — Offline Test Plan

- **OpenSpec change-id:** `second-salvo-29-offline-test-plan`
- **Slot:** S2-29
- **Scope:** Included Ultra only

This plan verifies the existing BURN HARD offline harness and burn-wave corpus
fixtures. It does not add network coverage or change runtime behavior.

## Exclusions

- OD is out of scope.
- Do not edit `Willow SKILL.md`.
- Do not run tests that contact a network, install packages, resolve remote
  dependencies, or call live connectors.

## Offline command

Run from the repository root with the test dependencies already available:

```bash
NO_NETWORK=1 \
OPENSPEC_OFFLINE=1 \
PIP_NO_INDEX=1 \
PIP_DISABLE_PIP_VERSION_CHECK=1 \
python3 -m pytest -q --maxfail=1 \
  harness/tests/test_offline.py \
  harness/tests/test_corpus.py \
  harness/tests/test_hygiene.py
```

The command is intentionally explicit about the selected tests. The same
offline switches are used by the OpenSpec harness workflow; the workflow
expects `pytest` to be preinstalled and does not install packages.

## Fixtures

| Fixture or source | Used by | Expected offline behavior |
| --- | --- | --- |
| `harness/src/sovereign_harness/fixtures/{drive,github,gmail,image,linear,phone_bridge,web}.json` | `harness/tests/test_offline.py` | Every connector returns `source: "offline-fixture"` while socket creation is forbidden. |
| `docs/burn-wave/corpora/MANIFEST.json` | `harness/tests/test_corpus.py` | Missing local blobs fall back to deterministic synthetic data. |
| Synthetic phone-health entry in `MANIFEST.json` | Corpus ingestion | Writes `phone_health.json` with `status: "ok"`. |
| Four synthetic connector-call entries in `MANIFEST.json` | Corpus ingestion | Writes a four-line `connector_call_log.jsonl` for Gmail, GitHub, Linear, and Drive. |
| `harness/tests/test_hygiene.py` fixtures | Hygiene gate | Accepts the repository and rejects a simulated live `SKILL.md` write. |

Local corpus blobs under `docs/burn-wave/corpora/blobs/` are optional and are
not checked in. They must never be fetched during this plan.

## Expected evidence

Record the following with the test result:

1. The command exits `0` and reports all selected tests passing.
2. `test_every_connector_surface_stays_offline` passes with socket creation
   patched to fail; this is evidence that the connector calls used the local
   fixtures.
3. Corpus tests show the missing-blob path is deterministic:
   `record_count == 5`, phone health status is `ok`, and the call log contains
   four records.
4. The generated `INGEST_RECEIPT.json` identifies the fallback artifacts with
   `source: "synthetic"`; do not include generated output or local blobs in the
   change.
5. The hygiene test passes and its simulated negative case still rejects a
   live `SKILL.md` write.
6. The test log contains no package-install, DNS, HTTP, connector, or other
   network activity. A failure to prove this is a failed verification, not a
   reason to relax the offline switches.

No evidence from OD, Willow, or live/network tests is part of S2-29.
