# OpenSpec offline acceptance harness

This directory contains 20 executable mappings from
[`docs/openspec/04-acceptance-tests.md`](../../../docs/openspec/04-acceptance-tests.md).
They exercise deterministic in-process fakes for the provider, MCP gateway,
memory adapter, durable store, phone session, and Spark router. No socket,
subprocess, model, provider, mail, or credential is used.

The tests are intentionally red before a system under test exists. The
`OPENSPEC_SUT=unimplemented` selector uses a backend that raises
`NotImplementedError`; the default selector supplies the contract-only stubs:

```text
OPENSPEC_SUT=unimplemented python3 -m pytest -q harness/tests/openspec
python3 -m pytest -q harness/tests/openspec
```

The first command is the red phase and the second is the stub-backed green
phase. The offline guard in `conftest.py` turns accidental network access into
an immediate test failure. Replace the stub backend with the real adapter only
after these contracts are implemented; a passing stub is not production proof.

## Generated scenario corpus

The sibling [`generated/`](../generated/) directory contains 1,000 deterministic
synthetic stubs covering all 80 documented cases. These are contract-shaped
records, not 1,000 claims that production behavior is implemented. They can be
verified without pytest, package installation, credentials, or external
services:

```text
python3 -m harness.tests.generated.runner
python3 -m harness.tests.generated.generate --check
python3 -m unittest discover -s harness/tests/generated -p 'test_*.py'
```

The generated verifier is the CI path. The existing pytest suite remains the
small executable mapping against the in-process fakes, and its own offline
socket guard is unchanged.

## Mapping

| OpenSpec case | Test | Stub-backed proof |
|---|---|---|
| CT-001 | `test_ct_001_valid_phone_event_normalization` | Required canonical envelope and provenance fields |
| CT-002 | `test_ct_002_provider_event_deduplication` | Duplicate callback produces one accepted event |
| CT-003 | `test_ct_003_conflicting_sequence_is_rejected` | Reused sequence with different payload is rejected |
| CT-005 | `test_ct_005_invalid_signature_does_not_ingest_payload` | Invalid callback is rejected without payload ingestion |
| CT-008 | `test_ct_008_missing_mcp_context_rejected_before_dispatch` | Gateway rejects before downstream dispatch |
| CT-009 | `test_ct_009_unknown_normalized_tool_rejected` | Unknown tool is rejected and never dispatched |
| CT-010 | `test_ct_010_receipt_schema` | Artifact receipt has required evidence fields |
| PH-002 | `test_ph_002_denied_consent_stays_out_of_memory` | Denied consent cannot write Recall |
| PH-004 | `test_ph_004_partial_transcript_cannot_mutate` | Partial transcript creates no mutation |
| PH-005 | `test_ph_005_exact_confirmation_executes_once` | Exact confirmation executes once |
| PH-007 | `test_ph_007_stale_confirmation_has_no_side_effect` | Expired confirmation has no side effect |
| PH-013 | `test_ph_013_secret_redaction_across_evidence_paths` | Synthetic secrets are absent from evidence |
| MCP-006 | `test_mcp_006_idempotent_tool_call` | Repeated key replays one dispatch |
| MCP-008 | `test_mcp_008_downstream_timeout_is_retryable_not_success` | Timeout is typed retryable failure, not success |
| LT-006 | `test_lt_006_memory_write_requires_provenance` | Memory write without source refs is rejected |
| ES-001 | `test_es_001_durable_before_wake_ordering` | Payload, queue, and handoff precede wake |
| ES-006 | `test_es_006_duplicate_wake_is_idempotent` | Duplicate wake runs worker once |
| ES-016 | `test_es_016_stub_source_remains_unresolved` | Empty source remains unresolved, not fabricated |
| ES-017 | `test_es_017_source_conflict_is_returned_with_refs` | Contradictory sources return conflict refs |
| OP-007 | `test_op_007_trace_continuity_across_escalation` | One trace links phone, gateway, store, queue, and wake |
