# S2-30 receipt schema

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-30-receipt-schema` |
| Slot | `S2-30` |
| Operation | Atomic included burn |
| Inclusion profile | **Ultra only** |
| Deliverable | `docs/burn-wave/RECEIPT_SCHEMA.md` |
| Evidence boundary | Repository-local documentation and checks |

This schema defines the smallest receipt envelope for an Included Ultra
burn-wave slice. A receipt records what was evaluated and the local evidence
for that evaluation; it does not claim runtime, provider, or external-service
state.

## Envelope

A receipt MUST contain exactly one value for each required field below. Fields
not listed here are extensions and MUST NOT change the meaning of a required
field.

| Field | Type | Requirement |
| --- | --- | --- |
| `schema_version` | string | Contract version, currently `"1"`. |
| `change_id` | string | Exactly `second-salvo-30-receipt-schema`. |
| `slot` | string | Exactly `S2-30`. |
| `profile` | string | Exactly `ultra`. |
| `receipt_id` | string | Stable identifier for this receipt. |
| `status` | string | One of `pass`, `fail`, or `blocked`. |
| `recorded_at` | string | UTC RFC 3339 timestamp. |
| `artifacts` | array | Complete, ordered list of evaluated repository artifacts. |
| `verification` | array | Local checks and their results. |
| `scope` | object | Included and excluded boundaries for the slice. |

## Artifact record

Each `artifacts` entry MUST contain:

| Field | Type | Requirement |
| --- | --- | --- |
| `path` | string | Repository-relative POSIX path. |
| `sha256` | string | 64 lowercase hexadecimal characters. |
| `byte_len` | integer | Non-negative byte count. |

An artifact is complete only when its path, digest, and byte length are
present. A missing, malformed, or conflicting value makes the receipt
`fail`; an unavailable local check makes it `blocked`.

## Verification record

Each `verification` entry MUST contain:

| Field | Type | Requirement |
| --- | --- | --- |
| `check` | string | Short, stable name of the local check. |
| `result` | string | `pass`, `fail`, or `blocked`. |
| `evidence` | string | Reproducible command or repository-local reference. |

Verification evidence MUST be free of credentials, tokens, private keys,
cookies, signed URLs, and other secret values. PR state is optional
correlation data and is not a receipt result.

## Scope boundary

The receipt MUST declare the following boundary:

- **Included:** Ultra material required by this S2-30 documentation slice.
- **Excluded:** OD, all Willow `SKILL.md` content, and every other S2 slot.
- **Protected target:** `skill_tree/skills/willow/SKILL.md` is not added,
  reproduced, indexed, or modified.
- **Changed-path expectation:** this slice changes only
  `docs/burn-wave/RECEIPT_SCHEMA.md`.

## Example

```yaml
schema_version: "1"
change_id: second-salvo-30-receipt-schema
slot: S2-30
profile: ultra
receipt_id: s2-30-receipt-001
status: pass
recorded_at: "2026-09-17T00:00:00Z"
artifacts:
  - path: docs/burn-wave/RECEIPT_SCHEMA.md
    sha256: 0000000000000000000000000000000000000000000000000000000000000000
    byte_len: 0
verification:
  - check: diff-check
    result: pass
    evidence: git diff --check
scope:
  included: ultra
  excluded:
    - OD
    - Willow SKILL.md
    - other S2 slots
```

The example is illustrative; its digest and byte length are not evidence for
any particular checkout.
