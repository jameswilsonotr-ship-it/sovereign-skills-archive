# S2-11 fixture inventory

| Field | Value |
| --- | --- |
| Slot | `S2-11` |
| OpenSpec change-id | `second-salvo-11-fixture-inventory` |
| Included scope | Ultra-only, repository-tracked offline fixtures |
| Source of truth | This checkout; no external or provider data |

## Inventory

The current offline surface is deliberately small and deterministic. It
contains eight JSON fixtures under
`harness/src/sovereign_harness/fixtures/`:

| Fixture | Stable payload represented | Exercised by |
| --- | --- | --- |
| `drive.json` | One mock Markdown file with an offline source marker | `DriveConnector.list_files()` and the Drive call-log corpus |
| `github.json` | One mock repository issue with an offline source marker | GitHub search/get/list-pull-request call shapes and the GitHub call-log corpus |
| `gmail.json` | One mock thread with one message | Gmail search/get-thread call shapes and the Gmail call-log corpus |
| `linear.json` | One mock issue with an in-progress state | Linear list/get-issue call shapes and the Linear call-log corpus |
| `image.json` | One mocked image asset | `ImageConnector.render()` |
| `web.json` | One `example.invalid` page whose body states that no network is used | `WebConnector.fetch()` and URL/call-shape tests |
| `phone_bridge.json` | Health-only phone bridge capabilities; SMS and camera are false | `PhoneBridgeStub.health()` and fixture tests |
| `phone_health.json` | `ok` phone-bridge status, version `0.1.0`, and `health`/`offline-fixtures` capabilities | `health_payload()` and the local `/health` endpoint |

The connector implementation in
`harness/src/sovereign_harness/connectors.py` provides the stable call
envelopes for these fixtures. It has no provider client or network transport:
`WebConnector` only normalizes a URL, and the phone stub explicitly rejects
SMS and camera operations.

## BURN corpus layer

`docs/burn-wave/corpora/MANIFEST.json` declares two optional local artifacts:

1. `phone-health` writes `phone_health.json`. When its local blob is absent,
   the loader creates the deterministic health payload.
2. `connector-call-log` writes JSONL containing four deterministic calls:
   Gmail `search_threads`, GitHub `search_repositories`, Linear `list_issues`,
   and Drive `list_files`.

The corresponding `MANIFEST.md` records that local blobs are not checked in.
`sovereign_harness.corpus.ingest_manifest()` uses a local blob only when it is
present (and, if declared, has the matching SHA-256); otherwise it writes the
synthetic fallback and an `INGEST_RECEIPT.json`. It never fetches a remote URL.
The clean-checkout fallback therefore produces five records total: one health
artifact and four call-log records.

## Verification surface

The inventory is covered by the existing offline tests:

- `harness/tests/test_offline.py` blocks socket use while invoking every
  connector surface.
- `harness/tests/test_connectors.py` checks account-bound validation and stable
  call envelopes.
- `harness/tests/test_corpus.py` checks synthetic fallback, local-blob
  precedence, receipts, and call-log ingestion.
- `harness/tests/test_phone_mcp.py` checks the health-only endpoint and the
  absence of SMS/camera capabilities.
- `harness/tests/test_stress.py` and `harness/tests/test_properties.py` cover
  bounded concurrency and account-id invariants without provider access.

## One bounded gap

There is no deterministic not-found or other error-result fixture. Every
tracked connector payload is a successful or mocked-success response, while
`FixtureConnector._reply()` returns the same fixture data regardless of the
operation name. The tests distinguish operation and request shape, but do not
exercise an offline error outcome.

Bounded follow-up: add one local synthetic not-found case and one contract
test for a single connector operation. That follow-up must preserve the
offline-only boundary and existing fixture semantics; it does not require a
provider call, a secret, a new skill file, or changes outside S2-11.
