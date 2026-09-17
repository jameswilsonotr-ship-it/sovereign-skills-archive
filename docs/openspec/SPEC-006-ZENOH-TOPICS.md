# SPEC-006 — Zenoh Topic Namespace and Envelope Contract

**Status:** proposed
**Version:** 0.1.0
**Owners:** burner-phone control-plane implementation
**Related work:** [Zenoh Android control-plane research](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/16), [SPEC-002 — Burner Phone MCP Intents](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/24)
**Document type:** OpenSpec acceptance specification
**Scope:** Zenoh key expressions, topic direction, message envelopes, authorization boundaries, lifecycle, and observability

## 1. Purpose

This specification defines the versioned Zenoh topic contract for a short-lived
burner-phone control plane. It is a protocol contract, not an implementation
plan. A conforming implementation MUST be able to prove the topic it used, the
envelope it accepted, the policy decision it made, and the lifecycle state in
which it made that decision.

The contract has four goals:

1. keep commands, results, events, presence, capabilities, telemetry, and
   companion handoffs in separate address spaces;
2. bind every device-scoped message to a non-permanent burner node identity;
3. prevent caller-controlled key expressions and payloads from becoming an
   authorization or dispatch escape hatch; and
4. make offline, simulated, native, failed, expired, and cancelled outcomes
   distinguishable without exposing secrets.

This document does not claim that the current `zenoh.apk` source already
implements these topics. The topics below are proposed interfaces and MUST be
treated as unavailable until an implementation passes this contract.

## 2. Boundary and non-goals

### 2.1 In scope

- the canonical `burner/v1/{node_id}/...` namespace;
- key-expression grammar and normalization;
- publisher/subscriber direction and per-node scope;
- command, result, event, presence, capabilities, telemetry, and companion
  envelope shapes;
- request correlation, expiry, nonce replay protection, and bounded payloads;
- separation of control traffic from telemetry and binary artifacts;
- lifecycle cancellation and topic retirement;
- transport truthfulness and audit-safe observability.

### 2.2 Out of scope

- selecting a Zenoh router, peer, client, or discovery topology;
- choosing a native Zenoh binding or Android ABI;
- defining MCP tool names or JSON-RPC transport;
- authorizing a real flashlight, SMS provider, microphone, camera, or shell;
- defining Android `Intent` actions, components, packages, or permissions;
- storing credentials, private keys, tokens, audio, exports, or other secrets;
- guaranteeing delivery, ordering, or persistence beyond what an implementation
  explicitly advertises;
- replacing the default-deny and zero-dispatch guarantees in SPEC-002.

The existing `swarm/bus/**` paths MAY remain as compatibility/demo traffic, but
they are not part of this privileged control contract and MUST NOT be used for
burner commands, results, or companion jobs.

## 3. Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, and **MAY** are normative.

Each requirement below is atomic: it has one primary contract obligation and
one observable acceptance scenario. A passing scenario MUST include both the
positive result and the stated negative assertion.

## 4. Canonical namespace

### 4.1 Topic inventory

The canonical root is:

```text
burner/v1/{node_id}
```

The following concrete topic families are defined:

| Topic family | Publisher | Subscriber | Purpose | Retention |
| --- | --- | --- | --- | --- |
| `burner/v1/{node_id}/command/{request_id}` | authorized host | matching node | one typed command | transient |
| `burner/v1/{node_id}/result/{request_id}` | matching node | authorized host | admission and terminal result | transient, bounded |
| `burner/v1/{node_id}/event/{event_id}` | matching node | authorized host | asynchronous state/event notice | transient, bounded |
| `burner/v1/{node_id}/presence` | matching node | authorized host | current liveness signal | latest-value or transient |
| `burner/v1/{node_id}/capabilities` | matching node | authorized host | effective capability/policy advertisement | latest-value |
| `burner/v1/{node_id}/telemetry` | matching node | authorized observer | redacted operational metrics | transient, bounded |
| `burner/v1/{node_id}/companion/{request_id}` | authorized host | matching node or approved companion adapter | bounded companion job handoff | transient, bounded |
| `burner/v1/{node_id}/audit/{event_id}` | trusted audit sink | authorized auditor | redacted decision evidence | policy-defined |

`status` is represented by the `presence` and `capabilities` families. An
implementation MAY publish a compatibility alias under
`burner/v1/{node_id}/status`, but the alias MUST carry the same node identity,
policy version, and transport truth as the canonical status surfaces.

### 4.2 Topic direction

The host MAY publish only to `command` and, when the companion capability is
explicitly enabled, `companion`. The node MAY publish only to `result`,
`event`, `presence`, `capabilities`, `telemetry`, and `audit`. A subscriber
MUST NOT infer write authority from read access.

### 4.3 Key expression policy

The implementation MUST construct all key expressions from a fixed registry.
The caller may provide a request identifier, but MUST NOT provide a complete
Zenoh key expression, wildcard, root, node identifier, or topic family.

The following expressions are examples of valid concrete keys:

```text
burner/v1/burner-7f2e/command/req-01
burner/v1/burner-7f2e/result/req-01
burner/v1/burner-7f2e/event/evt-01
burner/v1/burner-7f2e/presence
burner/v1/burner-7f2e/capabilities
burner/v1/burner-7f2e/telemetry
burner/v1/burner-7f2e/companion/job-01
burner/v1/burner-7f2e/audit/evt-01
```

The examples are identifiers, not credentials. Implementations MUST generate
fresh node and request identifiers and MUST NOT embed a user name, phone
number, access token, private key, or other secret in a key.

## 5. Envelope contract

### 5.1 Common fields

Every control-plane envelope MUST be UTF-8 JSON or another versioned encoding
with an equivalent schema. JSON is the required interoperability fixture for
this specification.

The common control fields are:

```json
{
  "protocol": "zenoh-android-control/v1",
  "message_type": "command",
  "request_id": "req-01",
  "node_id": "burner-7f2e",
  "issued_at": "2026-09-17T04:00:00Z",
  "expires_at": "2026-09-17T04:00:30Z",
  "nonce": "opaque-single-use-value"
}
```

`request_id`, `node_id`, and `nonce` are opaque strings. They MUST be length
bounded, MUST be compared as data rather than interpreted as paths, and MUST
not contain control characters. `issued_at` and `expires_at` use UTC RFC 3339
timestamps with seconds precision or a more precise representation that
preserves their ordering.

### 5.2 Command envelope

A command adds the fixed logical operation, a bounded payload, and a fixed
reply topic:

```json
{
  "protocol": "zenoh-android-control/v1",
  "message_type": "command",
  "request_id": "req-01",
  "node_id": "burner-7f2e",
  "operation": "phone_health",
  "issued_at": "2026-09-17T04:00:00Z",
  "expires_at": "2026-09-17T04:00:30Z",
  "nonce": "opaque-single-use-value",
  "reply_to": "burner/v1/burner-7f2e/result/req-01",
  "payload": {}
}
```

`operation` MUST come from the fixed operation registry. `reply_to` is
computed by the receiver from the validated node and request identifiers; a
caller-supplied value MUST be equal to that computed key or the message MUST
be rejected.

### 5.3 Result envelope

A result acknowledges admission, rejection, failure, or completion:

```json
{
  "protocol": "zenoh-android-control/v1",
  "message_type": "result",
  "request_id": "req-01",
  "node_id": "burner-7f2e",
  "operation": "phone_health",
  "status": "accepted",
  "code": "OK",
  "transport": "offline",
  "policy_version": "phone-default-deny-v1",
  "created_at": "2026-09-17T04:00:01Z",
  "details": {}
}
```

`status`, `code`, and `transport` are machine-readable. A result MUST NOT
claim remote delivery, native transport, or a hardware/provider side effect
unless that fact is true for the operation and observable by the adapter.

### 5.4 Event envelope

An event uses a new `event_id` but retains the originating `request_id` when
one exists:

```json
{
  "protocol": "zenoh-android-control/v1",
  "message_type": "event",
  "event_id": "evt-01",
  "request_id": "req-01",
  "node_id": "burner-7f2e",
  "event_type": "lifecycle.changed",
  "created_at": "2026-09-17T04:00:01Z",
  "transport": "simulated",
  "data": {}
}
```

Events MUST be bounded and MUST NOT be used as an untyped command channel.

### 5.5 Presence and capability envelopes

Presence reports current liveness without implying authorization:

```json
{
  "protocol": "zenoh-android-control/v1",
  "message_type": "presence",
  "node_id": "burner-7f2e",
  "lifecycle": "READY",
  "transport": "offline",
  "observed_at": "2026-09-17T04:00:00Z",
  "expires_at": "2026-09-17T04:00:15Z"
}
```

Capabilities report allowlisted operation names and policy metadata only. They
MUST NOT contain a private key, bearer token, raw Android package credential,
or an unredacted device secret.

## 6. Atomic requirements

### ZH-001 — Namespace is versioned

**Requirement:** Every privileged topic MUST begin with
`burner/v1/{node_id}/`. A message using an unversioned burner root or an
unsupported version MUST be rejected before dispatch.

**Acceptance scenario:**

```gherkin
Given a node configured for protocol version v1
When it receives one message under burner/v1/node-1/command/req-1
Then it may continue to schema and policy validation
When it receives one message under burner/node-1/command/req-2
Then it rejects the message with a version or namespace error
And it performs no publish, Intent, hardware, provider, or companion action
```

### ZH-002 — Node identity is scoped to the burner lifecycle

**Requirement:** Each active burner lifecycle MUST use one generated,
non-permanent `node_id`, and a closed lifecycle MUST NOT accept messages for
that identity.

**Acceptance scenario:**

```gherkin
Given a burner lifecycle with node_id node-a
When the lifecycle is closed and a command for node-a arrives
Then the command is rejected as closed
And a newly created lifecycle receives a different node_id
And the old node_id is not reused as the new lifecycle identity
```

### ZH-003 — Topic family is fixed

**Requirement:** Only the registered topic families `command`, `result`,
`event`, `presence`, `capabilities`, `telemetry`, `companion`, and `audit` MAY
be used below the canonical root.

**Acceptance scenario:**

```gherkin
Given a valid node_id and request_id
When a message targets burner/v1/node-1/shell/req-1
Then the key registry rejects the topic family
And no subscriber or dispatcher is created for that key
```

### ZH-004 — Request identifiers are key-safe and bounded

**Requirement:** A `request_id` used in a topic MUST satisfy the implementation's
published length limit, contain no `/`, `*`, `**`, control character, or
secret material, and remain opaque to routing logic.

**Acceptance scenario:**

```gherkin
Given a command request with request_id "../command/other"
When the adapter derives its command key
Then validation rejects the request
And the derived key cannot escape the request topic segment
And no normalized alternate request_id is silently substituted
```

### ZH-005 — Command and result paths are separate

**Requirement:** A command MUST publish only to `command/{request_id}`, and a
result MUST publish only to `result/{request_id}` for the same validated node.

**Acceptance scenario:**

```gherkin
Given an admitted command with node_id node-1 and request_id req-1
When the node emits its acknowledgement
Then the command spy records burner/v1/node-1/command/req-1
And the result spy records burner/v1/node-1/result/req-1
And neither message is published to the other message's family
```

### ZH-006 — Event identifiers do not replace request correlation

**Requirement:** An asynchronous event MUST use its own `event_id` topic
segment and MUST retain the originating `request_id` when the event is caused
by a command.

**Acceptance scenario:**

```gherkin
Given command req-1 produces event evt-1
When the event is published
Then its key is burner/v1/node-1/event/evt-1
And its envelope contains request_id req-1
And a consumer can distinguish event identity from request identity
```

### ZH-007 — Presence and capabilities are read-only surfaces

**Requirement:** `presence` and `capabilities` MUST contain state and policy
metadata only; they MUST NOT be accepted as command or companion input.

**Acceptance scenario:**

```gherkin
Given a message published to burner/v1/node-1/presence
When the node receives the message
Then it rejects the message as an invalid inbound direction
And it does not change lifecycle, policy, transport, or capability state
```

### ZH-008 — Telemetry is separated from control traffic

**Requirement:** Command, result, event, presence, and capability messages
MUST NOT be published under `telemetry`, and telemetry MUST NOT carry an
operation, reply topic, Intent action, or executable payload.

**Acceptance scenario:**

```gherkin
Given a telemetry publication containing a lifecycle metric
When the publication is serialized
Then it uses burner/v1/node-1/telemetry
And it contains no operation or reply_to field
And a control subscriber does not treat it as a command
```

### ZH-009 — Companion traffic has a separate boundary

**Requirement:** Companion handoffs MUST use
`companion/{request_id}` and MUST NOT be placed in command, event, or
telemetry topics.

**Acceptance scenario:**

```gherkin
Given an approved companion job with request_id job-1
When its bounded handoff is published
Then its key is burner/v1/node-1/companion/job-1
And no raw companion artifact is copied to command, event, or telemetry
And a node without companion policy rejects the handoff
```

### ZH-010 — Caller cannot supply a wildcard

**Requirement:** External callers MUST NOT be allowed to publish or subscribe
using `*`, `**`, a root-wide expression, or a caller-selected sibling node
expression for privileged traffic.

**Acceptance scenario:**

```gherkin
Given a caller requests subscription to burner/v1/**
When the subscription is authorized
Then authorization rejects the wildcard expression
And no broad subscription is opened
And an exact node-scoped subscription remains the only permitted form
```

### ZH-011 — ACLs are node-scoped

**Requirement:** A host or adapter credential authorized for node-a MUST NOT
publish to or consume privileged control topics for node-b.

**Acceptance scenario:**

```gherkin
Given a principal authorized for node-a
When it publishes a command for node-b
Then the ACL decision is denied
And no node-b subscriber receives the message
And the denial is auditable without logging credentials
```

### ZH-012 — Topic direction is enforced

**Requirement:** The host-to-node publisher set MUST be limited to `command`
and explicitly enabled `companion`; node-to-host publishers MUST be limited to
the remaining registered families.

**Acceptance scenario:**

```gherkin
Given a node attempts to publish to burner/v1/node-1/command/req-1
When the topic-direction policy evaluates the publication
Then it denies the publication
And it does not reinterpret the message as an event or telemetry record
```

### ZH-013 — Every control message declares its message type

**Requirement:** Every command, result, event, presence, capabilities,
companion, and audit envelope MUST contain a `message_type` matching its topic
family, and a mismatch MUST be rejected.

**Acceptance scenario:**

```gherkin
Given an envelope on burner/v1/node-1/result/req-1
When its message_type is command
Then schema validation rejects the envelope
And the result is not republished under a corrected topic
```

### ZH-014 — Request and result correlation is exact

**Requirement:** A result MUST preserve the command's `request_id`, `node_id`,
and logical `operation`; a missing or mismatched correlation tuple MUST be
treated as invalid.

**Acceptance scenario:**

```gherkin
Given a command tuple node-1, req-1, phone_health
When a result arrives with request_id req-2
Then the consumer rejects the result as uncorrelated
And it cannot complete or overwrite req-1
```

### ZH-015 — Expiry is enforced at admission

**Requirement:** A command or companion envelope with `expires_at` at or
before the receiver's trusted current time MUST be rejected before transport,
Intent, provider, or companion dispatch.

**Acceptance scenario:**

```gherkin
Given a command whose expires_at is earlier than the receiver clock
When the message is admitted
Then it returns a typed expiry decision
And the Zenoh adapter records no downstream publish
And no side effect is scheduled for later execution
```

### ZH-016 — Nonces prevent replay

**Requirement:** A nonce MUST be single-use within the active node and
capability lifetime; a repeated nonce/request pair MUST NOT produce a second
command or companion dispatch.

**Acceptance scenario:**

```gherkin
Given an accepted command with request_id req-1 and nonce nonce-1
When the same command is delivered again
Then the second delivery is rejected as replayed or duplicate
And the downstream dispatch count remains one
And the audit record identifies the replay without retaining the nonce value
```

### ZH-017 — Envelope size and fields are bounded

**Requirement:** Implementations MUST enforce declared limits for envelope
size, identifier length, operation name, and payload size, and MUST reject
unknown fields under the strict control schema.

**Acceptance scenario:**

```gherkin
Given a command containing an undeclared field named shell
When strict envelope validation runs
Then it rejects the command as an unknown field
And it does not forward shell to an Intent, process, Zenoh query, or log
```

### ZH-018 — Sensitive and binary data stay out of routine topics

**Requirement:** Raw credentials, bearer tokens, private keys, SMS content,
conversation exports, audio, voice profiles, and binary artifacts MUST NOT be
placed in command, result, event, telemetry, or audit payloads. A bounded
content reference MAY be used only when its capability and retention policy
are explicit.

**Acceptance scenario:**

```gherkin
Given a companion request referring to an audio artifact
When the request is serialized
Then it contains only an approved bounded content reference and digest
And it contains no audio bytes, credential, or bearer token
And ordinary telemetry and audit output contains neither raw content nor token
```

### ZH-019 — Lifecycle and transport state are truthful

**Requirement:** Presence, capabilities, results, and events MUST report the
effective lifecycle and transport state. `offline`, `simulated`, `native`, and
`error` MUST remain distinct, and a simulated or offline publication MUST NOT
claim native remote delivery.

**Acceptance scenario:**

```gherkin
Given native Zenoh is unavailable and simulation is not enabled
When a health result is published
Then transport is offline or error according to the actual failure
And the result does not claim native delivery
When simulation is explicitly enabled
Then transport is simulated
And the envelope makes simulation visible
```

### ZH-020 — Topic activity is bounded and auditable

**Requirement:** Every accepted, rejected, expired, replayed, cancelled, and
failed control decision MUST have a bounded audit record containing node,
request or event correlation, message type, outcome code, policy version, and
timestamp; subscriptions, queues, and retained events MUST be bounded by TTL
or count and cancelled at lifecycle close.

**Acceptance scenario:**

```gherkin
Given a node with an active subscription and one expired command
When the node lifecycle closes
Then the subscription and pending queue are cancelled
And the expired decision has an audit record with no secret payload
And no retained control event remains beyond its configured TTL or count bound
```

## 7. Failure codes

Failure codes are stable machine-readable values. Implementations MAY add
codes, but MUST NOT reuse a listed code for a different condition without a
protocol-version change.

| Code | Meaning |
| --- | --- |
| `OK` | Message was accepted or the read-only operation completed. |
| `NAMESPACE_INVALID` | Root, version, node segment, or family is invalid. |
| `TOPIC_DIRECTION_DENIED` | The principal or publisher direction is not allowed. |
| `NODE_SCOPE_DENIED` | The principal is not authorized for the node. |
| `SCHEMA_INVALID` | Required field, type, enum, or message-family validation failed. |
| `UNKNOWN_FIELD` | The strict envelope contains an undeclared field. |
| `REQUEST_INVALID` | An identifier or correlation field is malformed or mismatched. |
| `PAYLOAD_TOO_LARGE` | Envelope or payload exceeds its declared bound. |
| `CAPABILITY_EXPIRED` | The capability, node, or lifecycle is no longer valid. |
| `REQUEST_EXPIRED` | The message arrived after its expiry. |
| `REQUEST_REPLAYED` | The nonce or request was already accepted. |
| `TRANSPORT_UNAVAILABLE` | The requested transport is not configured. |
| `TRANSPORT_ERROR` | A configured transport failed unexpectedly. |
| `CLOSED` | The burner lifecycle is terminal. |

## 8. Security invariants

The following are release-blocking:

1. **Version invariant:** privileged traffic uses the versioned burner root.
2. **Fixed-registry invariant:** callers cannot choose arbitrary key
   expressions, topic families, wildcards, or sibling node identifiers.
3. **Separation invariant:** commands, results, events, telemetry, and
   companion handoffs cannot be substituted for one another.
4. **Scope invariant:** ACL reachability is node-scoped and is not itself
   sufficient to authorize an operation.
5. **Correlation invariant:** a result or event cannot be attributed to a
   different request or node.
6. **Expiry invariant:** a live network connection does not extend a message,
   capability, or burner lifecycle.
7. **Replay invariant:** a repeated nonce/request cannot duplicate a side
   effect.
8. **Redaction invariant:** secrets and sensitive artifacts are absent from
   routine topic payloads, logs, denials, and audit records.
9. **Truth invariant:** simulated, offline, and failed transport states cannot
   be represented as native success.
10. **Teardown invariant:** lifecycle close cancels subscriptions, queues,
    heartbeats, and retained control work.

## 9. Implementation checklist

### Phase 0 — Registry and schema

- [ ] Register the canonical root and fixed topic families.
- [ ] Implement strict key-expression construction.
- [ ] Implement common, command, result, event, presence, capability,
      telemetry, companion, and audit schemas.
- [ ] Publish all identifier and payload bounds.
- [ ] Reject unknown fields and caller-supplied complete keys.

### Phase 1 — Policy and transport

- [ ] Enforce node-scoped ACLs and publisher direction.
- [ ] Enforce expiry and single-use nonce state before downstream dispatch.
- [ ] Keep control and telemetry policy separate.
- [ ] Label native, simulated, offline, and error transport states.
- [ ] Keep binary and sensitive data on approved out-of-band references.

### Phase 2 — Lifecycle and evidence

- [ ] Generate a fresh node identity for each burner lifecycle.
- [ ] Bound event retention, queues, subscriptions, and companion handoffs.
- [ ] Cancel all node-owned work at expiry or close.
- [ ] Emit redacted audit evidence for every decision.
- [ ] Add negative tests for wildcards, sibling nodes, topic confusion,
      expired messages, replays, oversized payloads, and secret leakage.

## 10. Definition of done

SPEC-006 is accepted when:

- all 20 atomic requirements pass against the implementation;
- every privileged key is produced by the fixed registry;
- node scope and topic direction are enforced by observable ACL decisions;
- command/result/event correlation is exact and replay-safe;
- expired, oversized, malformed, and secret-bearing messages fail before
  downstream dispatch;
- telemetry and companion traffic cannot become a control escape hatch;
- transport and lifecycle metadata are truthful;
- lifecycle close cancels bounded work and retires the node identity; and
- audit evidence proves the decisions without retaining sensitive content.

Passing a mock publish call is not sufficient. Acceptance requires both
positive contract evidence and negative-boundary evidence for unauthorized
topics, wildcard expressions, sibling nodes, stale messages, replayed
messages, topic confusion, and secret retention.

## 11. Open decisions for a future revision

This proposal intentionally leaves these deployment choices unresolved:

1. Which Zenoh router or peer topology will serve the control plane?
2. Which authenticated identity and ACL mechanism will bind a principal to a
   burner node?
3. Which native Zenoh binding will provide the production transport?
4. Which persistence or durability policy, if any, applies to audit topics?
5. Which exact upper bounds are appropriate for each deployed payload class?
6. Which approved content-reference service owns companion artifacts?
7. Which user-visible confirmation is required before any real phone
   capability is enabled?

Resolving an open decision does not authorize arbitrary Android Intents,
hardware access, SMS delivery, shell execution, or secret transport. Such
changes require a separately reviewed specification revision.
