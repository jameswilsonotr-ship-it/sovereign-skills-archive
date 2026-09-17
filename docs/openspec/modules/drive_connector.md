# OpenSpec: `drive_connector`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `system-roadmap` / `skill-orchestrator`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define the narrow Drive data-plane connector used to stage and retrieve
artifacts, with a deterministic receipt path for publish workflows. The
connector is not a general-purpose filesystem, wake-up bus, or OAuth token
minting service.

## Context

The repository already has a native Drive upload bridge at
`skill_tree/skills/skill-orchestrator/scripts/drive_connector_bridge.py`.
That bridge writes an outbox envelope and expects an authorized native
connector to flush it. `system-roadmap` also records the rule that email is a
wake signal while Drive carries the payload. This spec turns those conventions
into a provider-neutral contract.

## Problem statement

Drive uploads can become unverifiable when an agent writes directly, loses the
provider response, or treats a path as proof that the artifact is remote.
Callers need bounded operations, explicit folder scope, duplicate protection,
and a durable receipt before a downstream GitHub or email step can claim
success.

## Goals

- Stage and retrieve Markdown, CSV, JSON, and archive artifacts.
- Require an explicit destination folder and preserve the source filename.
- Make upload, download, metadata lookup, and receipt recording idempotent.
- Keep credentials in the native connector boundary.
- Support dry-run and human approval for every externally visible write.

## Non-goals

- Converting files to Google Docs or editing collaborative documents.
- Searching an entire organization without a folder or query boundary.
- Sending notifications, minting OAuth tokens, or publishing to GitHub.
- Deleting or overwriting a remote object in BASIC_TIER.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Calling skill or runtime | Validates intent and supplies `request_id`, folder, and artifact |
| Native Drive/MCP connector | Performs the provider operation with scoped credentials |
| Connector bridge | Persists outbox/inbox envelopes and provider receipts |
| Human approver | Approves non-dry-run upload or overwrite |
| GitHub/email modules | Consume a verified receipt; never infer one |

## Requirements

- **DR-001**: Every request MUST include `request_id`, `operation`, `folder_id`
  for writes, `mode`, and an idempotency key.
- **DR-002**: Upload MUST reject missing, unreadable, or symlinked source files
  unless a higher-tier policy explicitly permits them.
- **DR-003**: The connector MUST default to create-only behavior. Existing
  remote names MUST produce `DUPLICATE` unless the caller supplies an approved
  version operation.
- **DR-004**: The bridge MUST retain the request envelope until the provider
  result is recorded in an inbox receipt.
- **DR-005**: A remote file ID, content hash, byte count, folder ID, and
  provider timestamp MUST be recorded on success.
- **DR-006**: Logs MUST contain IDs and hashes, never file contents or tokens.
- **DR-007**: Retries MUST be bounded and safe after a network timeout; the
  connector MUST query by idempotency key or content hash before retrying.
- **DR-008**: External sharing, deletion, and overwrite are out of scope and
  MUST fail closed.

## Scenarios

### Stage a new artifact

**Given** a readable local artifact, an approved folder, and `mode=write`  
**When** the connector receives a new idempotency key  
**Then** it uploads once, records the remote file ID and hash, and returns a
receipt reference.

### Retry after ambiguous timeout

**Given** the provider may have accepted an upload but the response was lost  
**When** the same request is retried  
**Then** the connector searches the scoped folder by idempotency key or hash,
returns the existing file, and does not create a duplicate.

### Dry run

**Given** a valid artifact but no approval  
**When** `mode=dry_run` is requested  
**Then** the connector validates size, type, hash, and folder access without
performing a provider write.

### Unsafe overwrite

**Given** a remote file with the requested name already exists  
**When** a create-only request is submitted  
**Then** it returns `DUPLICATE`, leaves the remote file unchanged, and writes a
failure receipt.

## Proposed design

The flow is `validate → hash → enqueue → authorize → provider call → verify →
receipt`. The existing bridge outbox is the durable handoff. The inbox receipt
is the only authority downstream modules may use. Upload responses must be
verified with a metadata read when the provider supports it.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `stage` | `artifact_path`, `file_name`, `folder_id`, `idempotency_key` | remote file ID + receipt |
| `fetch` | `file_id` or scoped query | local path + hash + receipt |
| `metadata` | `file_id` | provider metadata + receipt |
| `receipt` | `request_id` | stored outcome |

Errors are stable classes: `INVALID_INPUT`, `NOT_FOUND`, `DUPLICATE`,
`PERMISSION_DENIED`, `QUOTA`, `PROVIDER_UNAVAILABLE`, and `AMBIGUOUS_RESULT`.

## Data model and invariants

The receipt records `request_id`, `operation`, `folder_id`, `file_id`,
`file_name`, `sha256`, `bytes`, `actor`, `mode`, `status`, `created_at`,
`completed_at`, and redacted `error`. Invariants: a success has a provider
reference; a failure has no claimed side effect; a hash is computed before
upload; and folder scope is never widened during retry.

## Security and privacy

Credentials remain in the native connector; Python code must not mint or store
OAuth tokens. Folder IDs are allowlisted per environment. Provider responses
and logs are redacted. Follow the least-privilege and receipt requirements in
[`BASIC_TIER`](../BASIC_TIER.md); no external share operation is permitted by
this spec.

## Reliability and failure modes

The bridge must survive process restart with pending outbox files. Quota,
permission, and validation failures are terminal until the input or grant
changes. Network failures may retry with exponential backoff, but ambiguous
uploads require lookup before retry. A missing receipt blocks downstream
publication.

## Observability

Emit structured events for `validated`, `enqueued`, `provider_started`,
`provider_succeeded`, `provider_failed`, and `receipt_written`. Metrics include
success rate, duplicate rate, provider latency, pending outbox count, and
receipt age. Never emit payload text.

## Testing and acceptance

- Unit-test hash, folder validation, create-only behavior, and redaction.
- Contract-test against a fake Drive provider for success, duplicate, timeout,
  quota, and revoked-access cases.
- Restart with a pending outbox and prove the receipt is eventually written.
- Acceptance requires all `DR-*` requirements, the dry-run scenario, and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Roll out read-only metadata and dry-run staging first. Enable writes only for
an allowlisted folder and explicit approval. Existing
`drive_connector_bridge.py` envelopes are compatible when they gain
`request_id`, `idempotency_key`, and content hash fields. Backout disables
provider writes while retaining receipts and pending envelopes.

## Open questions and decisions

- **Decision:** Drive is the data plane; email is not part of this connector.
- **Decision:** create-only is the BASIC_TIER default.
- **Open:** choose the authoritative native tool name for environments that do
  not expose `google_drive_upload_artifact`.
- **Open:** define retention for inbox receipts and downloaded local copies.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [`drive_connector_bridge.py`](../../../skill_tree/skills/skill-orchestrator/scripts/drive_connector_bridge.py)
- [Drive staging and GitHub conduit](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
- [Deterministic hop rules](../../../skill_tree/skills/system-roadmap/references/email-bridge-2026-08-17/03_DETERMINISTIC_HOP.md)
