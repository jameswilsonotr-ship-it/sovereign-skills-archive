# SPEC-015 — KEEL SENTRY WATCH

**Theme:** ATOMIC INCLUDED BURN
**Status:** Draft
**Date:** 2026-09-17
**Surface:** Auth-watch observation only
**Implementation state:** Specification only

## Abstract

KEEL SENTRY WATCH defines a bounded, read-only watcher for authentication
health. It observes whether an already-configured integration appears
available, degraded, expired, revoked, or in need of operator action. It does
not authenticate, renew credentials, change scopes, or store secrets.

The central accounting rule is **atomic included burn**: one watch cycle is
one declared unit of work. Its budget reservation, observation, redaction, and
receipt are treated as one unit. A cycle is either complete and accounted for,
or incomplete and surfaced for review; hidden retries and unreported work are
not allowed.

This document is a contract for a future implementation. It does not add a
watcher, provider adapter, scheduler, credential store, or notification
channel.

## Scope

In scope:

- Read-only observation of an operator-approved auth/integration reference.
- Normalization of provider-independent auth health states.
- Bounded polling or event consumption when a future adapter supports it.
- Secret-free receipts, deduplication, degradation, and escalation notes.
- An explicit per-cycle work/burn boundary.

Out of scope:

- Login, consent, token exchange, token refresh, or credential rotation.
- Persisting, indexing, echoing, or transmitting secrets.
- Reading message or file content behind an integration.
- Modifying provider configuration, permissions, scopes, or account state.
- Selecting a secret manager or implementing a provider adapter.
- Sending email, chat, SMS, webhooks, or other external notifications.

## Terms

- **Auth reference:** A non-secret identifier for the integration/account
  being watched. It may be a local label or an implementation-defined
  runtime handle; it is not a token, cookie, key, or session export.
- **Watch cycle:** One bounded observation attempt with one cycle identifier.
- **Auth health:** The normalized result of an observation.
- **Included burn:** The predeclared work allowance for one cycle. It may be
  represented as requests, time, or another implementation-defined unit, but
  must be visible in the receipt.
- **Atomic included burn:** The all-or-nothing accounting boundary covering
  reservation, observation, redaction, and receipt emission.
- **Secret-free receipt:** A result containing only approved metadata and
  redacted outcome fields.

## Normative requirements

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**
are normative.

### KS-001 — Declare the watch target

Each watch configuration MUST identify the target using a non-secret auth
reference and a provider/integration label. The configuration MUST NOT require
credential material as a document field, command argument, fixture, or
receipt field.

### KS-002 — Observe health, not content

An auth-watch cycle MUST inspect only the minimum signal needed to classify
authentication health. It MUST NOT fetch mailbox, drive, repository, message,
file, or other user content as part of an auth check.

### KS-003 — Never store secrets

The watcher MUST NOT persist, cache, index, log, export, or commit access
tokens, refresh tokens, API keys, passwords, cookies, private keys, session
exports, authorization codes, or bearer headers. This prohibition applies to
success, failure, debug, retry, and crash-recovery paths.

Runtime access, if eventually required by an adapter, MUST be supplied by an
external secret-aware runtime. The watcher may receive a success/failure
signal from that runtime, but the specification grants it no secret storage
responsibility.

### KS-004 — Do not acquire or repair credentials

The watcher MUST NOT initiate login, consent, token exchange, refresh,
rotation, scope expansion, or account linking. An expired, revoked, or
missing credential is an observed condition and MUST remain an operator-owned
repair action.

### KS-005 — Require explicit authorization

A watch MUST have an operator-approved configuration before it can run. The
approval record MUST identify the auth reference, permitted observation
surface, cadence or trigger, and included-burn limit. Absence, expiry, or
withdrawal of approval MUST stop new cycles.

Approval metadata MUST contain no credential material and MUST NOT be inferred
from a successful prior observation.

### KS-006 — Enforce read-only and least privilege

An implementation MUST request or use the least privilege needed for the
health signal. It MUST reject a proposed adapter that requires write access,
content access, or broader scopes solely for convenience. A health result MUST
not be treated as authorization to perform any follow-on action.

### KS-007 — Normalize health states

Every completed cycle MUST map its observation to exactly one normalized
health state:

| State | Meaning |
| --- | --- |
| `healthy` | The approved health signal was observed successfully. |
| `degraded` | The signal was reachable but incomplete, delayed, or outside a declared expectation. |
| `expired` | The provider reported an expired or otherwise time-invalid authorization. |
| `revoked` | The provider reported that authorization is no longer granted. |
| `consent_required` | An operator consent or re-approval step is required. |
| `scope_changed` | The observed authorization no longer matches the approved scope. |
| `unavailable` | The provider or auth surface could not be reached within bounds. |
| `unknown` | The result could not be safely classified without guessing. |

Provider-specific text MAY be retained only when it is demonstrably
secret-free and necessary for operator diagnosis.

### KS-008 — Make state transitions explicit

The watcher MUST model transitions between normalized states and MUST record
the previous state when one is known. It MUST NOT silently convert
`unknown`, `unavailable`, or `degraded` into `healthy`. A transition to
`expired`, `revoked`, `consent_required`, or `scope_changed` MUST be
actionable in the receipt without automatically attempting repair.

### KS-009 — Redact at the boundary

Redaction MUST happen before data reaches logs, durable state, metrics,
receipts, errors, or notification adapters. Redaction MUST cover both known
secret fields and provider error strings that may contain embedded
credentials, URLs with query secrets, personal addresses, or session data.

When safe redaction cannot be guaranteed, the cycle MUST return `unknown` or
`unavailable` with a generic reason and MUST discard the unsafe detail.

### KS-010 — Apply atomic included burn

Before a cycle begins, the implementation MUST reserve a declared included
burn. The cycle MUST then follow this sequence:

1. Reserve the cycle identifier and burn allowance.
2. Perform only the bounded observation work allowed by that allowance.
3. Normalize and redact the result.
4. Emit one secret-free receipt that accounts for the allowance and outcome.

If reservation fails, no observation work may begin. If observation,
normalization, redaction, or receipt emission fails, the cycle MUST be marked
incomplete or unknown and MUST NOT be reported as a successful completed
cycle. A cycle MUST NOT retry hidden work under the same identifier or burn
allowance.

### KS-011 — Bound cadence and work

Each watch MUST declare a maximum observation duration, maximum number of
provider operations, and cadence or event trigger. The implementation MUST
stop at the first limit and return `degraded` or `unavailable` as
appropriate. Backoff, if later implemented, MUST be bounded and visible in
the next scheduled cycle; it MUST NOT increase a cycle's included burn.

### KS-012 — Deduplicate and handle replay

Every cycle MUST have a unique cycle identifier and a stable fingerprint of
the secret-free observation input. Replayed events or duplicate triggers MUST
not create additional provider work when the same observation has already
been accounted for. Fingerprints MUST be derived only from approved
non-secret metadata and MUST NOT be a hash of a secret.

### KS-013 — Fail closed and preserve degraded truth

Missing configuration, withdrawn approval, unsupported provider signals,
redaction uncertainty, budget exhaustion, and ambiguous responses MUST fail
closed. The watcher MUST preserve the last known state separately from the
current failed observation so that a transient failure is not mistaken for a
healthy current state.

### KS-014 — Emit a secret-free receipt

Each attempted cycle MUST produce one receipt or an explicitly recorded
receipt failure. A receipt MAY contain:

- `spec_id` and `cycle_id`;
- auth reference and provider label, if non-secret;
- observation time and duration;
- previous and current normalized health state;
- declared and consumed included-burn units;
- bounded operation count;
- redacted failure class;
- whether operator review is required.

A receipt MUST NOT contain credential material, raw provider responses,
authorization URLs containing sensitive query data, content samples, or
personal data not required to identify the non-secret watch target.

### KS-015 — Surface operator action without side effects

Transitions requiring intervention MUST produce a clear next-action class,
such as `reapprove`, `inspect_provider`, `review_scope`, or
`contact_owner`. The watcher MUST stop at that boundary. It MUST NOT click,
send, approve, renew, delete, change, or otherwise mutate an external
system. Notification delivery is a separate future specification and is not
implied by this requirement.

## Reference cycle record

The following is illustrative schema only; it is not an implementation
mandate. Values are placeholders and MUST remain non-secret.

```yaml
spec_id: SPEC-015
cycle_id: CYCLE_PLACEHOLDER
auth_reference: AUTH_REF_PLACEHOLDER
provider: PROVIDER_LABEL
previous_state: degraded
current_state: consent_required
burn:
  unit: provider_operations
  declared: 1
  consumed: 1
observation:
  duration_ms: 0
  operation_count: 1
receipt:
  status: complete
  operator_review_required: true
  next_action: reapprove
```

Implementations MAY use another serialization format, but the same
secret-free and atomicity constraints apply.

## State and accounting notes

The minimum lifecycle is:

```text
approved
  -> reserved
  -> observing
  -> normalized
  -> redacted
  -> receipted
```

Any failure before `receipted` MUST produce an explicit incomplete/unknown
record where possible. No lifecycle state may imply that credentials were
valid merely because a runtime was reachable.

The included-burn ledger is per cycle. A future scheduler MAY aggregate
receipts, but aggregation MUST preserve cycle-level accounting and MUST NOT
hide discarded, replayed, or incomplete work.

## Security and privacy boundary

This spec intentionally leaves credential custody outside KEEL SENTRY WATCH.
Implementations MUST use placeholders in examples and tests. They MUST keep
live credentials in the operator's approved secret-management/runtime
boundary and MUST prevent them from appearing in:

- repository files or generated patches;
- environment dumps;
- debug logs, traces, metrics, or crash reports;
- fixtures, snapshots, or test snapshots;
- receipts, state files, or exported audit bundles.

The auth-watch surface is not an authorization decision-maker. It reports
health observations for human or separately specified automation review.

## Acceptance checklist

- [ ] KS-001 through KS-015 are individually testable in a future
      implementation.
- [ ] A watch target can be declared without a token, cookie, key, password,
      or session export.
- [ ] A health check cannot read protected content as part of auth watching.
- [ ] Expired, revoked, consent-required, scope-changed, unavailable, and
      unknown states remain distinct.
- [ ] Redaction occurs before logs, durable state, metrics, and receipts.
- [ ] Reservation, bounded observation, redaction, and receipt emission form
      one atomic included-burn unit.
- [ ] Duplicate triggers do not cause unaccounted provider work.
- [ ] Failures preserve degraded truth and never trigger credential repair.
- [ ] No implementation, provider adapter, scheduler, or secret store is
      included by this spec-only change.
