# SPEC-013 — Drive Receipt ACK

**Status:** Draft
**Scope:** `from-vesper/receipts` bus acknowledgement contract
**Type:** Specification only

## Purpose

Define the acknowledgement contract for a Vesper-originated receipt that
describes a Drive publication. The contract makes the Drive-side result
auditable, replay-safe, and independent from GitHub pull-request state.

The central invariant is:

> A GitHub pull request status is not a Drive ACK, and a Drive ACK is not a
> GitHub pull request status.

This document specifies the receipt and ACK semantics only. It does not
authorize an upload, merge, deletion, or any other external mutation.

## Terms

- **Receipt:** An immutable Vesper record describing one attempted publication
  of a bundle to Drive.
- **Bundle:** The complete set of artifacts declared by a receipt.
- **Drive ACK:** A receiver-produced result stating whether the declared Drive
  publication was accepted, rejected, or deferred.
- **PR:** A GitHub pull request and its lifecycle state. PR state is optional
  correlation metadata and is never proof of Drive state.
- **Atomic included burn:** The bundle is evaluated as one declared unit:
  an accepted ACK covers every required included artifact, not a silently
  successful subset.

## Contract

The producer publishes receipt envelopes to `from-vesper/receipts`. The
receiver evaluates the envelope against the Drive publication contract and
returns an ACK record through the configured bus response path. The response
path is a transport binding; it must not change the semantics below.

An ACK is authoritative only for the `receipt_id` and `bundle_id` it names.
A later receipt or ACK does not rewrite an earlier immutable record.

### Receipt envelope

The following fields are required:

| Field | Requirement |
| --- | --- |
| `schema` | Versioned contract name and version. |
| `receipt_id` | Globally unique, immutable receipt identifier. |
| `bundle_id` | Identifier for the atomic included bundle. |
| `event_id` | Unique identifier for this bus publication. |
| `source` | The logical producer; for this contract, `vesper`. |
| `created_at` | UTC creation timestamp. |
| `artifacts` | Complete, ordered list of required included artifacts. |
| `bundle_digest` | Digest over the canonical bundle manifest. |
| `attempt` | Positive publication attempt number. |

Each artifact declaration must include a stable logical path, byte length, and
content digest. Drive object identifiers and links may be included as opaque
references after publication, but are not credentials.

### ACK record

An ACK must include:

| Field | Requirement |
| --- | --- |
| `ack_schema` | Versioned ACK contract name and version. |
| `ack_id` | Globally unique ACK identifier. |
| `receipt_id` | Exact receipt being acknowledged. |
| `bundle_id` | Exact bundle being acknowledged. |
| `status` | `accepted`, `rejected`, or `deferred`. |
| `observed_at` | UTC time at which the receiver made the decision. |
| `artifact_count` | Number of required artifacts evaluated. |
| `bundle_digest` | Digest observed by the receiver. |
| `reason_code` | Required for `rejected` or `deferred`; absent for `accepted`. |

An ACK may include a PR reference for correlation. That reference is
non-authoritative and must never be used as the Drive result.

## Decision requirements

### DR-001 — Stable receipt identity

The producer MUST assign a globally unique `receipt_id`. It MUST remain
unchanged across retries of the same logical publication.

### DR-002 — Stable bundle identity

The producer MUST assign a `bundle_id` to the atomic included bundle. Every
receipt and ACK for that bundle MUST carry the same value.

### DR-003 — Source bus

Receipt envelopes governed by this specification MUST be published on
`from-vesper/receipts`. A message from another source or topic is not
implicitly covered by this contract.

### DR-004 — Explicit schema version

Every receipt and ACK MUST declare its schema version. Consumers MUST reject
unknown major versions and MUST preserve unknown extension fields for known
major versions.

### DR-005 — Complete manifest

The receipt MUST enumerate every artifact required for acceptance. An omitted
artifact is a contract violation; consumers MUST NOT infer missing members
from a Drive folder, PR, filename pattern, or prior receipt.

### DR-006 — Canonical bundle digest

`bundle_digest` MUST be computed from a canonical representation of the
ordered artifact manifest. Equivalent manifests MUST produce the same digest;
different membership, path, byte length, or content digest MUST produce a
different digest.

### DR-007 — Immutable receipt

After publication, the receipt body and its declared artifact set MUST be
immutable. Corrections MUST use a new receipt linked to the prior
`receipt_id`; an ACK MUST NOT mutate the original receipt.

### DR-008 — Content integrity

The receiver MUST compare each available Drive artifact with its declared
logical path, byte length, and content digest. A mismatch MUST prevent an
`accepted` ACK.

### DR-009 — Drive durability gate

The receiver MUST issue `accepted` only after every required artifact is
durably committed in Drive and the receiver can observe the committed state.
An upload request, client-side success, or eventual-write assumption is not
an accepted result.

### DR-010 — Atomic included burn

Acceptance MUST be all-or-nothing for the declared bundle. If any required
artifact is missing, partial, inaccessible, mismatched, or not durably
observable, the receiver MUST NOT issue an `accepted` ACK for the bundle.

### DR-011 — Bounded status vocabulary

The ACK status MUST be exactly one of:

- `accepted`: all requirements passed;
- `rejected`: the receiver determined that the bundle violates a requirement;
- `deferred`: the receiver could not make a durable determination yet.

`pending`, `uploaded`, `merged`, and `passed` are not ACK statuses.

### DR-012 — Actionable negative results

`rejected` and `deferred` ACKs MUST include a stable `reason_code` and a
human-readable diagnostic that identifies the affected receipt or artifact
without exposing credentials or secret values.

### DR-013 — ACK correlation

An ACK MUST name the exact `receipt_id`, `bundle_id`, and `bundle_digest` it
evaluated. A consumer MUST treat an ACK with an unknown or conflicting
correlation tuple as invalid.

### DR-014 — Idempotent replay

Reprocessing the same receipt and unchanged Drive state MUST yield the same
logical result. Duplicate bus delivery MUST NOT create a second publication
or imply a different outcome solely because the delivery was repeated.

### DR-015 — Attempt accounting

Retries of one logical publication MUST retain `receipt_id` and increment
`attempt` monotonically. A new `receipt_id` MUST be used only when the
producer intentionally begins a new logical publication or changes the
declared bundle.

### DR-016 — Ordering and late delivery

Consumers MUST tolerate out-of-order and late delivery. A late ACK MUST NOT
overwrite a newer result unless its correlation tuple and attempt policy
explicitly permit that transition. The final state must remain auditable as
an ordered event history.

### DR-017 — PR independence

PR creation, review, approval, closure, or merge MUST NOT generate an
`accepted` Drive ACK. An `accepted` Drive ACK MUST NOT imply that a PR exists,
is approved, is mergeable, or is merged.

### DR-018 — Correlation is informational

If a receipt contains a PR reference, it MUST be treated as informational
correlation only. Systems MUST store and display PR state and Drive ACK state
as separate fields and MUST not collapse them into one status.

### DR-019 — Secret-free payloads

Receipts, ACKs, diagnostics, and logs MUST NOT contain access tokens,
refresh tokens, private keys, cookies, signed URLs, credentials, or copied
secret configuration. Redaction MUST occur before bus publication and before
diagnostics are persisted.

### DR-020 — Conformance and change control

A producer or receiver conforms to this specification only if it can
demonstrate all of the following:

1. a complete receipt is published on `from-vesper/receipts`;
2. the bundle digest and per-artifact digests are reproducible;
3. partial, missing, mismatched, and non-durable Drive state cannot receive
   `accepted`;
4. duplicate and out-of-order delivery is handled without false success;
5. PR state and Drive ACK state remain independently observable; and
6. the resulting fixtures and diagnostics contain no secrets.

Changes to required fields, status meanings, atomicity, or the PR/Drive
separation require a new major schema version and an updated specification.

## Non-goals

This specification does not define:

- a Drive folder, file, permission, or retention policy;
- a GitHub branch, PR workflow, merge policy, or CI implementation;
- a particular bus vendor, serialization format, or response topic;
- credentials, secret storage, or access provisioning;
- code, deployment configuration, or a real Drive publication.
