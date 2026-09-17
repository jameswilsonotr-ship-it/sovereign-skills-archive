# SPEC-007 — SMS Default-Deny, Audit, and Redaction

**Status:** Draft
**Type:** OpenSpec architecture specification
**Owner:** Messaging security
**Scope:** Outbound SMS authorization, decision audit, and sensitive-data redaction

## 1. Purpose

This specification defines a fail-closed boundary for outbound SMS. An SMS
provider may be called only after an explicit, current, and attributable
permit decision. Every decision is auditable without placing message content,
recipient data, credentials, or other secrets into logs.

This specification is intentionally implementation-neutral. It defines
observable behavior, data contracts, and security invariants; it does not
authorize a provider, prescribe a vendor, or contain operational credentials.

## 2. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative. A
missing, stale, malformed, contradictory, or unavailable input is treated as
unknown. Unknown inputs MUST resolve to **deny**.

## 3. Security invariants

1. **Default deny:** No outbound SMS is sent unless the policy engine returns
   an explicit `PERMIT`.
2. **Provider isolation:** The provider adapter is unreachable from callers
   until policy evaluation has completed.
3. **No side effect on deny:** A denied request MUST NOT create, queue, retry,
   or dispatch an outbound provider operation.
4. **Audit without disclosure:** A decision is recorded for every request,
   while raw destinations, bodies, credentials, access tokens, and provider
   payloads are excluded from audit and application logs.
5. **Fail closed:** Policy, audit, redaction, identity, consent, or provider
   uncertainty MUST NOT turn a denial into a permit.
6. **Human control:** Automated policy cannot override an explicit recipient
   opt-out or an administrative suspension.

## 4. Architectural boundary

The SMS path consists of these logical stages:

```text
request
  -> normalize and validate
  -> resolve actor, environment, consent, and policy context
  -> evaluate policy
  -> append redacted decision audit
  -> provider adapter (PERMIT only)
  -> append redacted delivery outcome
```

The policy decision is authoritative for the request. The provider adapter
MUST accept only a signed or otherwise integrity-protected internal permit
bound to the request identifier, actor, destination fingerprint, content
fingerprint, policy version, and expiry. A caller MUST NOT be able to supply
or alter that permit.

## 5. Policy inputs and outcomes

The policy engine evaluates, at minimum:

- request identifier and idempotency key;
- authenticated actor and actor authorization;
- execution environment and tenant or workspace boundary;
- normalized destination and destination classification;
- consent status, consent source, consent timestamp, and opt-out status;
- message purpose and approved template or template version;
- applicable allowlist, suspension, rate, and volume controls;
- policy version and current time.

The only successful outcome is `PERMIT`. Other outcomes are `DENY`, with a
stable reason code. A policy response MUST include:

```text
decision, reason_code, policy_version, request_id, expires_at,
destination_fingerprint, content_fingerprint
```

Permits are single-use, short-lived, and bound to the exact normalized
request. A permit is not reusable for another destination, body, actor,
environment, or request.

## 6. Audit contract

The audit stream is append-only and tamper-evident. Each decision event MUST
contain:

- event identifier and UTC timestamp;
- request identifier and, when present, parent operation identifier;
- actor reference in a non-secret, access-controlled form;
- environment and tenant references;
- action `sms.send`;
- decision and stable reason code;
- policy version and permit identifier when permitted;
- destination and content fingerprints;
- redaction profile/version;
- provider operation reference and outcome class, only after dispatch;
- schema version.

Audit records MUST NOT contain raw phone numbers, message bodies, opt-in
evidence contents, authorization headers, API keys, access tokens, cookies,
provider payloads, or unredacted exception text.

Audit availability is part of the safety boundary. If a decision cannot be
recorded durably before dispatch, the request MUST be denied. Delivery
outcomes MAY be recorded asynchronously only after the initial decision audit
has been committed.

## 7. Redaction contract

Redaction applies before data reaches application logs, audit records,
metrics labels, traces, queues, error reports, or support exports. It MUST be
recursive across structured values and MUST cover strings, maps, lists,
exceptions, headers, URLs, and provider responses.

- Destinations are replaced with a keyed, access-controlled fingerprint; a
  display form, if required by an authorized support view, is generated
  separately and is never emitted to general logs.
- Bodies and opt-in evidence are not retained in the decision audit. A
  keyed content fingerprint MAY be retained for exact-request correlation.
- Credentials and bearer material are replaced with a constant redaction
  marker before formatting or serialization.
- Known sensitive fields are redacted by field name and by value-pattern
  detection. Pattern detection is defense in depth, not permission to retain
  raw values.
- Fingerprints MUST be stable only within their approved correlation scope
  and MUST NOT reveal the source value through reversible encoding.
- Redaction failures MUST discard the affected record or replace the entire
  sensitive field; they MUST NOT emit the unredacted value.

Keyed-fingerprint keys are supplied by the approved secret-management system
at runtime. This document contains no key material, credentials, or example
secrets.

## 8. Acceptance criteria

### SMS-001 — Absent policy defaults to deny

**Given** no applicable SMS policy exists, **when** an outbound request is
evaluated, **then** the decision is `DENY` with a stable missing-policy reason
code.

### SMS-002 — Explicit permit is required

**Given** a request has no explicit `PERMIT` result, **when** dispatch is
attempted, **then** the provider adapter rejects it before any provider call.

### SMS-003 — Policy precedes provider access

**Given** a new outbound request, **when** the request enters the SMS path,
**then** actor, environment, destination, consent, purpose, and policy are
resolved before provider credentials or provider methods are accessed.

### SMS-004 — Unknown inputs fail closed

**Given** any required policy input is absent, malformed, stale, contradictory,
or unavailable, **when** policy evaluation completes, **then** the result is
`DENY` and identifies the unknown or invalid input class.

### SMS-005 — Denial has no external side effect

**Given** a request is denied, **when** the request lifecycle completes,
**then** it is not dispatched, queued for dispatch, retried as a send, or
submitted to a provider.

### SMS-006 — Current consent is mandatory

**Given** a destination has no current, attributable, purpose-compatible
consent, **when** an outbound request is evaluated, **then** it is denied.

### SMS-007 — Opt-out always wins

**Given** a destination has an active opt-out or administrative suppression,
**when** any outbound request is evaluated, **then** it is denied regardless of
consent, allowlist membership, template, or actor role.

### SMS-008 — Destination authorization is bounded

**Given** a destination is not authorized by the applicable tenant or
workspace boundary, **when** an outbound request is evaluated, **then** it is
denied without exposing the destination to the caller.

### SMS-009 — Actor authorization is attributable

**Given** the actor is unauthenticated, suspended, or lacks the required SMS
permission, **when** an outbound request is evaluated, **then** it is denied
and the audit event records a non-secret actor reference when available.

### SMS-010 — Environment separation is enforced

**Given** the request environment does not match the policy, consent, and
provider configuration environment, **when** it is evaluated, **then** it is
denied and cannot use credentials or allowlists from another environment.

### SMS-011 — Purpose and template are constrained

**Given** the requested purpose or template is absent, unapproved, expired, or
incompatible with consent, **when** the request is evaluated, **then** it is
denied before message rendering or dispatch.

### SMS-012 — Content constraints are enforced

**Given** normalized content violates an approved policy constraint, **when**
the request is evaluated, **then** it is denied and raw content is absent from
the decision, error, and audit records.

### SMS-013 — Rate and volume limits are fail closed

**Given** a destination, actor, tenant, or system limit is exceeded or its
counter cannot be read reliably, **when** a request is evaluated, **then** it
is denied without attempting provider dispatch.

### SMS-014 — Replay is prevented

**Given** a request identifier or idempotency key has already produced a
terminal decision, **when** the same request is submitted again, **then** it
does not create a second provider operation.

### SMS-015 — Permits are exact and single-use

**Given** a permit was issued for one normalized request, **when** any bound
field changes or the permit is reused or expired, **then** the provider
adapter rejects it and no SMS is sent.

### SMS-016 — Provider failure cannot grant permission

**Given** the provider, credential lookup, network, or adapter is unavailable,
**when** a request is processed, **then** no new permit is granted and the
request fails closed with a redacted outcome.

### SMS-017 — Every decision is audited

**Given** any valid, invalid, permitted, denied, duplicate, or failed
outbound request, **when** processing reaches a terminal decision, **then**
exactly one primary decision audit event is written for that request.

### SMS-018 — Audit is committed before dispatch

**Given** policy returns `PERMIT`, **when** the primary audit event cannot be
committed durably, **then** dispatch is blocked and the request is denied or
held in a non-dispatchable state.

### SMS-019 — Audit records use a stable schema

**Given** a decision audit event is written, **when** it is consumed by an
auditor, **then** all required fields and the schema version are present and
the decision and reason code use documented enumerations.

### SMS-020 — Audit events are tamper evident

**Given** a decision audit event has been committed, **when** it is read or
verified, **then** unauthorized modification, deletion, reordering, or
duplication is detectable.

### SMS-021 — Correlation is possible without raw data

**Given** a request generates policy, audit, trace, or delivery records,
**when** an authorized auditor correlates them, **then** request identifiers
and scoped fingerprints link the records without exposing the destination or
body.

### SMS-022 — Raw destinations are excluded

**Given** a destination appears in input, normalization, an exception, a
provider response, or a log field, **when** the value is recorded, **then** it
is replaced by the approved fingerprint or redaction marker.

### SMS-023 — Raw message bodies are excluded

**Given** message content appears in rendering, validation, tracing, an
exception, or a provider response, **when** the value is recorded, **then**
the body is absent and only an approved content fingerprint or safe reason
code remains.

### SMS-024 — Sensitive fields are recursively redacted

**Given** sensitive data is nested in a map, list, exception, header, URL,
metric label, or serialized provider object, **when** redaction runs, **then**
all matching values are removed before output.

### SMS-025 — Secrets never reach telemetry

**Given** credentials, access tokens, authorization headers, cookies, signing
material, or runtime secret references are present, **when** logs, traces,
metrics, audits, or errors are produced, **then** the values are replaced with
a constant marker and are not partially emitted.

### SMS-026 — Fingerprints are non-reversible and scoped

**Given** the same authorized correlation scope receives the same normalized
destination or content, **when** fingerprints are generated, **then** they
are deterministic for correlation, non-reversible, and different scopes
cannot use them to correlate records.

### SMS-027 — Redaction failure fails closed

**Given** a redaction operation cannot prove that a record is safe, **when**
the record would be emitted, **then** the record is suppressed or replaced by
a safe failure record and no raw value is emitted.

### SMS-028 — Access is least privilege

**Given** an audit, fingerprint, or support record is requested, **when**
access is authorized, **then** the requester receives only the minimum
redacted fields needed for the approved role and purpose.

### SMS-029 — Retention and deletion are controlled

**Given** an audit or delivery record reaches its approved retention boundary,
**when** retention processing runs, **then** it is deleted or irreversibly
anonymized according to the retention policy, with the action itself audited
without restoring sensitive values.

### SMS-030 — Conformance is observable

**Given** the SMS boundary is deployed or changed, **when** its conformance
suite runs, **then** it proves default-deny, no-side-effect denial, consent
and opt-out precedence, audit-before-dispatch, replay prevention, recursive
redaction, secret exclusion, and fail-closed behavior for each required
failure mode.

## 9. Open decisions for implementation review

The implementation review MUST select and document:

- the stable reason-code registry and policy versioning scheme;
- the approved consent and opt-out authorities;
- the keyed-fingerprint algorithm, key scope, rotation, and access policy;
- the audit storage, tamper-evidence mechanism, retention schedule, and
  authorized roles;
- the exact rate limits, template registry, and provider adapter contract;
- the conformance test harness and deployment gate.

These choices MUST preserve every invariant and acceptance criterion in this
specification. They MUST NOT introduce credentials, tokens, personal data, or
provider secrets into source control or documentation.
