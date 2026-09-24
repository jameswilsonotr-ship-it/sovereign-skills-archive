# SPEC-014 — RAWV Frame: Atomic Included Burn

**Status:** Draft
**Type:** Normative specification
**Scope:** One bounded raw-artifact validation frame
**Requirements:** RV-001 through RV-015

## 1. Purpose

RAWV defines the smallest auditable unit for taking a set of raw artifacts
through validation without silently changing, omitting, or partially
consuming the set. The frame is designed for local-first processing,
replayable review, and handoff between tools.

“Atomic included burn” is the name of the commit boundary in this
specification:

- **Atomic** means the frame is accepted as one unit, not as an independently
  successful collection of items.
- **Included** means membership is fixed by the frame manifest before
  processing starts.
- **Burn** means logical consumption of the accepted frame after a durable
  receipt is written. It does **not** authorize deleting, overwriting, or
  shredding the source artifacts.

RAWV is a validation and accounting contract. It is not a storage system,
workflow scheduler, redaction policy, or authorization grant.

## 2. Terminology

| Term | Meaning |
| --- | --- |
| **frame** | One versioned RAWV input envelope and its resulting receipt |
| **raw artifact** | An input byte stream plus its declared identity and provenance |
| **manifest** | The ordered, closed list of artifacts included in a frame |
| **included burn** | The single logical transition from accepted to consumed |
| **receipt** | Durable evidence of validation, outcome, and consumption state |
| **source** | The original artifact location or provider; it remains authoritative |
| **replay** | Re-running validation against the same frame identity and bytes |

All timestamps in a frame or receipt MUST use UTC and an unambiguous
machine-readable representation.

## 3. Invariants and non-goals

The following invariants apply to every conforming implementation:

1. The source is never mutated by RAWV.
2. A frame has one immutable membership decision.
3. A frame has at most one successful included burn.
4. A failed or incomplete frame is not reported as consumed.
5. Every result can be traced back to a manifest entry and its source.

RAWV does not prescribe a transport, programming language, database, hash
algorithm beyond the requirements below, or user-interface presentation.

## 4. Requirements

### RV-001 — Frame identity

Every frame MUST have a globally unique `frame_id`, a `spec_id` set to
`SPEC-014`, and a schema/version identifier. A retry of the same frame MUST
reuse its `frame_id`; a materially different input MUST receive a new one.

### RV-002 — Explicit boundary

The producer MUST declare the frame boundary before validation begins. The
boundary MUST identify the source scope, inclusion rule, creation time, and
the operator or process that assembled the frame. Undeclared discovery during
validation MUST NOT silently expand membership.

### RV-003 — Closed manifest

The manifest MUST contain one entry for every included artifact and MUST
contain no artifact outside the declared boundary. Each entry MUST include a
stable `artifact_id`, source reference, byte length, media/content type when
known, and source modification marker when available.

### RV-004 — Deterministic ordering

Manifest entries MUST have a deterministic order. The ordering rule MUST be
recorded in the frame metadata, and two producers given the same eligible
inputs MUST produce the same ordered membership after normalization.

### RV-005 — Byte-level integrity

The producer MUST record a cryptographic digest of each raw artifact and a
digest of the canonical manifest. Validation MUST compare the observed bytes
with the manifest digest before an artifact can pass.

### RV-006 — Raw preservation

RAWV MUST validate a read-only view of the source bytes. It MUST NOT rewrite,
normalize in place, truncate, rename, move, or delete the source. Any
canonical representation MUST be emitted as a separate derived value linked
to the original digest.

### RV-007 — Provenance

Each artifact result MUST identify where the artifact came from, how it
entered the frame, and which validator version produced the result. Missing
provenance MUST be an explicit validation failure or an explicit
`unknown` outcome; it MUST NOT be inferred and presented as fact.

### RV-008 — Validation states

An artifact MUST resolve to exactly one terminal state:
`valid`, `invalid`, `unavailable`, or `unknown`. A frame MUST additionally
record whether validation completed. Informational warnings MAY accompany a
terminal state but MUST NOT create a second state.

### RV-009 — Inclusion accounting

The receipt MUST account for every manifest entry exactly once, including
entries that could not be read or validated. Counts for valid, invalid,
unavailable, unknown, and excluded items MUST be derivable from the manifest;
an implementation MUST NOT hide omissions in aggregate counts.

### RV-010 — Validation isolation

Validators MUST be side-effect free with respect to the source and the frame
manifest. Network access, external tools, or derived writes MUST be declared
in validator metadata and MUST NOT alter the inclusion decision after the
frame is closed.

### RV-011 — Atomic acceptance

A frame MAY be accepted only when its manifest, integrity checks, validation
results, and receipt pass the conformance checks together. If any required
component is missing or contradictory, the frame MUST remain
`rejected` or `incomplete`; it MUST NOT be partially accepted.

### RV-012 — Included-burn commit

The included burn MUST be a single durable state transition recorded after
atomic acceptance. It MUST bind the `frame_id`, manifest digest, receipt
digest, validator version, and commit time. Before that transition, the frame
is not consumed; after it, the frame is consumed exactly once.

### RV-013 — Idempotent replay

Replaying a consumed frame MUST be safe and MUST NOT create a second burn,
duplicate a receipt, or mutate the source. A replay MUST report the existing
commit and MUST flag any changed bytes or metadata as a conflict requiring a
new frame.

### RV-014 — Failure, recovery, and audit trail

Failures MUST preserve enough durable information to distinguish
`not_started`, `in_progress`, `rejected`, `incomplete`, and `consumed`.
Recovery MUST resume or restart from the same immutable manifest, and every
state transition MUST include a timestamp, actor/process identity, and reason.

### RV-015 — Conformance and handoff

A conforming implementation MUST be able to export the frame manifest, raw
digests, per-artifact outcomes, validator metadata, state history, and final
receipt without requiring access to private process memory. A handoff is
conforming only when the receiving party can independently verify the
manifest digest and determine whether the included burn has occurred.

## 5. Reference state model

```text
assembled
   |
   v
closed ──> incomplete
   |
   v
validated ──> rejected
   |
   v
accepted
   |
   v
consumed
```

`consumed` is the only state that means the included burn occurred. A source
artifact may remain available, unchanged, and reusable in a later frame.

## 6. Minimum receipt shape

The field names below are descriptive and may be represented in JSON, YAML,
or another documented interchange format:

```yaml
spec_id: SPEC-014
frame_id: <globally-unique-id>
state: consumed
manifest_digest: <digest>
validator:
  name: <validator-name>
  version: <validator-version>
artifacts:
  - artifact_id: <stable-id>
    source: <source-reference>
    byte_length: <integer>
    raw_digest: <digest>
    outcome: valid|invalid|unavailable|unknown
receipt:
  digest: <digest>
  committed_at: <utc-timestamp>
  committed_by: <actor-or-process>
```

## 7. Draft acceptance checklist

- [ ] A producer can close membership before validation.
- [ ] A reviewer can account for every manifest entry.
- [ ] A validator cannot mutate the source through the RAWV interface.
- [ ] A failed frame cannot be mistaken for a consumed frame.
- [ ] A replay is idempotent and exposes conflicts.
- [ ] A recipient can verify the handoff from the exported receipt alone.

## 8. Open questions for review

1. Should the final profile mandate SHA-256, or permit a stronger
   implementation-declared digest algorithm?
2. Should `unknown` be permitted in an accepted frame, or only in a complete
   frame that is rejected from burn?
3. Which external receipt store, if any, should be standardized separately
   from this frame contract?
