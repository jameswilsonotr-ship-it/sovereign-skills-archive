# SPEC-002 — Burner Phone MCP Intents

**Status:** proposed
**Version:** 0.1.0
**Owners:** burner-phone control-plane implementation
**Related work:** [PR #16 — document zenoh.apk burner control plane and Android Intent MCP](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/16)
**Document type:** OpenSpec acceptance specification
**Scope:** health, typed Android Intent stubs, denied-by-default phone actions, and Tailscale-only binding

## 1. Purpose

This specification turns the control-plane architecture documented in PR #16
into executable acceptance tests for a burner-phone MCP surface.

The system under test (SUT) is a short-lived phone control plane with:

1. an MCP endpoint for named, schema-constrained tools;
2. a typed command core that does not accept arbitrary Android actions,
   components, or extras;
3. a local Android adapter that may eventually deliver explicit Intents;
4. a health surface that reports lifecycle, transport, policy, and bind state;
5. an optional Zenoh transport whose native, simulated, offline, and error
   states remain distinguishable; and
6. a network listener bound only to the Tailscale interface or explicitly
   configured loopback.

The first phone actions are intentionally **stubs**:

- `phone_flashlight` is registered but denied by policy;
- `phone_sms` is registered but denied by policy; and
- neither stub may dispatch an Android Intent while the default policy is in
  effect.

The acceptance bar is therefore not “the flashlight turns on” or “an SMS is
sent.” The acceptance bar is that the MCP contract is safe, observable,
deterministic, and fail-closed before hardware or messaging capability is
enabled.

## 2. Relationship to PR #16

PR #16 is the architectural source for this spec. It establishes the following
constraints that are tested here:

| PR #16 control-plane rule | SPEC-002 acceptance surface |
| --- | --- |
| Use named MCP tools instead of an `android_send_intent` escape hatch. | `I-001`, `I-002`, `I-003`, `I-004`, `I-008` |
| Android delivery must be explicit, permissioned, and allowlisted. | `I-005`, `I-006`, `I-009`, `I-010` |
| Simulation must never look like native or remote success. | `H-003`, `Z-001`, `Z-004`, `O-003` |
| A burner node is short-lived, scoped, revocable, and observable. | `H-004`, `H-006`, `Z-006`, `L-001`, `S-005` |
| Request IDs correlate acknowledgement and later results. | `H-005`, `I-011`, `Z-002`, `O-001` |
| Command, telemetry, and companion paths are separate. | `Z-003`, `S-004` |
| Tailscale is a private reachability lane, not a replacement for policy. | `T-001`, `T-002`, `T-006`, `S-001` |
| Large or sensitive material moves through bounded content URIs, not extras
  or telemetry. | `I-007`, `S-003`, `O-002` |

PR #16 also records an important implementation truth: the referenced
`zenoh.apk` repository had local Zenoh stubs and no existing MCP or custom
Intent endpoint at the time of research. This document is a proposed contract
and test plan; it does not claim that PR #16 already implements any of the
behaviors below.

## 3. Cross-links and document inventory

The source repository was searched while authoring this specification.

| Document | Result | Link policy |
| --- | --- | --- |
| `BASIC_TIER` | No file with this name or an equivalent `basic-tier` path is present in the current checkout. | Do not create a speculative link. Add a link here when the authoritative document lands. |
| `SPEC-001` | No file matching `SPEC-001` is present in the current checkout. | Do not infer its scope. Add a link here when the authoritative document lands. |
| PR #16 research brief | Present as the open pull request that motivates this spec. | Link to [PR #16](https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive/pull/16). |

If either missing document is added later, this section must be updated in the
same change that introduces the cross-reference. A dead relative link is worse
than an explicit inventory note because it falsely suggests that a prerequisite
policy has already been reviewed.

## 4. Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, and **MAY** are normative.

An acceptance test passes only when its observable behavior and its negative
assertions both hold. For example, returning `POLICY_DENIED` is not sufficient
for `I-004` if an Intent was emitted before that result was returned.

## 5. System boundary

### 5.1 Components

```text
MCP client
    |
    | JSON-RPC over Tailscale-bound listener
    v
MCP adapter
    |
    | typed command; fixed tool registry
    v
Policy engine
    |
    +--> health provider
    +--> Intent dispatcher (disabled for phone stubs by default)
    +--> Zenoh adapter (native / simulated / offline / error)
    +--> bounded event and audit sink
```

The Android operating system, the Tailscale daemon, the network namespace, and
any real SMS or flashlight hardware are outside the SUT but are observable
through test doubles, instrumentation, or OS inspection.

### 5.2 In scope

- MCP initialization and tool discovery relevant to this spec;
- a read-only `phone_health` tool;
- deterministic health states and response schema;
- fixed names and schemas for `phone_flashlight` and `phone_sms`;
- policy-denied responses for both phone stubs;
- proof that denied calls emit no Android Intent and cause no hardware or SMS
  side effect;
- explicit component/action/extra validation in the adapter;
- Tailscale-interface-only binding and fail-closed bind errors;
- request correlation, redaction, expiry, and audit behavior;
- distinction among native, simulated, offline, and error transport states;
- bounded lifecycle cleanup.

### 5.3 Out of scope

- actually enabling the flashlight;
- actually sending an SMS;
- carrier provisioning, SIM activation, or phone-number discovery;
- arbitrary Android automation;
- arbitrary Intent forwarding;
- a permanent identity or credential vault;
- general Zenoh query/storage access;
- voice, audio, Groxxporter, Kokoro, or other companion jobs;
- proving that Tailscale itself authenticates every MCP caller;
- production load or carrier reliability testing.

Any future feature that enables flashlight or SMS is a separate spec revision
and MUST preserve the negative tests in this document unless the policy change
is explicit, reviewed, audited, and versioned.

## 6. Contract under test

### 6.1 MCP tool registry

The initial registry is deliberately small:

| Tool | Read/write | Default result | Android dispatch allowed by this spec |
| --- | --- | --- | --- |
| `phone_health` | read-only | health document | never |
| `phone_flashlight` | write-shaped stub | `POLICY_DENIED` | never |
| `phone_sms` | write-shaped stub | `POLICY_DENIED` | never |

The tools MAY be implemented by an in-process MCP server or by a separate
trusted MCP-to-Intent bridge. The external shape and negative guarantees are
the same in either deployment.

There MUST NOT be a generic tool named `android_send_intent`,
`run_intent`, `start_component`, `send_sms_intent`, or an equivalent escape
hatch in the default registry.

### 6.2 Common request fields

Each tool MAY accept `request_id`. If omitted, the adapter MUST generate one
before invoking the command core.

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "request_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 96
    }
  }
}
```

Request IDs are opaque. They MUST NOT be interpreted as filesystem paths,
Android component names, Zenoh key expressions, or capability tokens.

### 6.3 Common result envelope

Every accepted or rejected command MUST return a structured envelope:

```json
{
  "protocol": "phone-mcp/v1",
  "request_id": "req-01JPHONE...",
  "operation": "phone_flashlight",
  "status": "denied",
  "code": "POLICY_DENIED",
  "transport": "offline",
  "policy_version": "phone-default-deny-v1",
  "created_at": "2026-09-17T04:00:00Z"
}
```

Required fields:

- `protocol`;
- `request_id`;
- `operation`;
- `status`;
- `code`;
- `policy_version`; and
- `created_at`.

`transport` is REQUIRED for operations that could otherwise be mistaken for
remote work. Valid values are:

- `native`;
- `simulated`;
- `offline`; or
- `error`.

For a denied phone stub, `transport` SHOULD be `offline` because no transport
was invoked. The implementation MAY use `error` only when the policy decision
itself could not be evaluated; it MUST NOT report `native` or `simulated` as
evidence of a phone side effect.

The result MAY contain `details`, but denied phone calls MUST NOT echo the SMS
recipient, SMS body, access tokens, phone number, or arbitrary Intent extras.

### 6.4 `phone_health`

`phone_health` accepts the common request fields and has no side effects.

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "request_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 96
    },
    "detail": {
      "type": "string",
      "enum": ["summary", "full"],
      "default": "summary"
    }
  }
}
```

The response MUST expose enough information for an operator or test harness to
determine whether the node is safe to use:

```json
{
  "protocol": "phone-mcp/v1",
  "request_id": "req-health-1",
  "operation": "phone_health",
  "status": "ready",
  "code": "OK",
  "transport": "offline",
  "policy_version": "phone-default-deny-v1",
  "node": {
    "lifecycle": "READY",
    "node_id": "burner-7f2e",
    "session_expires_at": "2026-09-17T04:15:00Z"
  },
  "listener": {
    "bind_mode": "tailscale",
    "interface": "tailscale0",
    "addresses": ["100.101.102.103"],
    "port": 8787,
    "wildcard": false,
    "bound": true
  },
  "intents": {
    "registry_version": "phone-intents/v1",
    "flashlight": "denied_by_policy",
    "sms": "denied_by_policy"
  },
  "zenoh": {
    "availability": "unavailable",
    "transport": "offline",
    "simulation_enabled": false
  },
  "capabilities": {
    "health": true,
    "flashlight": false,
    "sms": false
  }
}
```

The implementation MAY omit fields from a summary response only if the full
response is available through `detail=full`. The listener bind mode, whether
the listener is wildcard-bound, and the policy state of flashlight and SMS are
never optional in a full health response.

### 6.5 `phone_flashlight`

This is a typed stub, not an implementation promise.

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["action"],
  "properties": {
    "request_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 96
    },
    "action": {
      "type": "string",
      "enum": ["on", "off", "toggle"]
    }
  }
}
```

Default response:

```json
{
  "protocol": "phone-mcp/v1",
  "request_id": "req-light-1",
  "operation": "phone_flashlight",
  "status": "denied",
  "code": "POLICY_DENIED",
  "transport": "offline",
  "policy_version": "phone-default-deny-v1"
}
```

The default policy MUST deny all three actions. No Android action, component,
extra, camera/torch API, or hardware call may be attempted.

### 6.6 `phone_sms`

This is a typed stub, not an SMS transport.

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["recipient", "body"],
  "properties": {
    "request_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 96
    },
    "recipient": {
      "type": "string",
      "minLength": 1,
      "maxLength": 32
    },
    "body": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1600
    }
  }
}
```

The default policy MUST deny all SMS sends. The implementation MUST NOT:

- request or use `android.permission.SEND_SMS`;
- invoke `SmsManager`;
- launch an implicit `ACTION_SENDTO` or `ACTION_SEND` Intent;
- resolve a messaging application;
- display the recipient or body in a denial result;
- publish the recipient or body to Zenoh; or
- log the body, full recipient, or any authorization material.

Schema validation MAY reject malformed inputs before policy evaluation. Such a
validation error MUST still produce no external side effect. For a well-formed
request, `POLICY_DENIED` is the required default result.

### 6.7 Intent registry

The adapter MAY contain a registry for future explicit Android delivery. The
registry is data, not caller-controlled input:

| Logical operation | Action | Component/package | Default |
| --- | --- | --- | --- |
| `phone_health` | none | in-process handler | allowed |
| `phone_flashlight` | reserved `...FLASHLIGHT.v1` | fixed phone package | denied |
| `phone_sms` | reserved `...SMS.v1` | fixed phone package | denied |

The exact package name is deployment configuration and MUST be returned as a
non-secret policy identifier rather than accepted from MCP input. A caller MUST
NOT select an action, package, class, URI scheme, or extra key.

The default registry MUST reject unknown logical operations before any Android
API call. It MUST reject unknown extras in strict mode.

## 7. Acceptance criteria

The following criteria are the release gate for SPEC-002. The detailed
scenarios in Section 8 define the evidence required for each criterion.

| Criterion | Requirement | IDs |
| --- | --- | --- |
| AC-1 | Health is callable without a session and reports truthful bind, lifecycle, policy, and transport state. | `H-001`–`H-006` |
| AC-2 | Tool schemas are narrow and reject undeclared fields. | `I-001`, `I-002` |
| AC-3 | Flashlight is a named stub that is denied by default with no dispatch. | `I-003`–`I-005` |
| AC-4 | SMS is a named stub that is denied by default with no messaging API, Intent, or data leakage. | `I-006`–`I-008` |
| AC-5 | No caller can turn a named stub into arbitrary Intent execution. | `I-009`, `I-010` |
| AC-6 | Requests and delayed outcomes are correlated, bounded, and replay-aware. | `I-011`, `Z-002`, `Z-006` |
| AC-7 | The MCP listener binds to Tailscale without a wildcard/public listener. | `T-001`–`T-005` |
| AC-8 | Tailscale reachability is not treated as authorization. | `T-006`, `S-001` |
| AC-9 | Zenoh simulation/native/offline/error states cannot be confused. | `Z-001`, `Z-004` |
| AC-10 | Teardown revokes active work and leaves no unbounded operation. | `L-001`, `L-002`, `S-005` |
| AC-11 | Logs and audit records prove decisions without retaining sensitive payloads. | `O-001`–`O-003`, `S-003` |

## 8. Acceptance tests

The examples below use Gherkin-style notation. They are requirements, not
necessarily a demand for a particular test framework. A conforming
implementation SHOULD provide unit tests for the command core,
instrumentation tests for Android dispatch, and process/network tests for the
Tailscale listener.

### 8.1 Health and lifecycle

#### H-001 — Health is available before connect

**Tags:** `health`, `read-only`, `smoke`

```gherkin
Given a fresh burner node in lifecycle state READY
And no Zenoh session has been opened
When the MCP client calls phone_health with request_id "h-001"
Then the call succeeds with status "ready"
And the response request_id is "h-001"
And the response reports lifecycle "READY"
And the response reports the current policy version
And the response reports flashlight as "denied_by_policy"
And the response reports SMS as "denied_by_policy"
And the response reports whether the listener is bound
And no Android Intent is emitted
And no Zenoh session is opened
```

#### H-002 — Health is side-effect free

**Tags:** `health`, `negative`

```gherkin
Given a READY node with an empty Intent-dispatch spy
And an empty Zenoh-session spy
When the client calls phone_health three times with distinct request IDs
Then all three responses are deterministic except for timestamps and counters
And the Intent-dispatch spy remains empty
And the Zenoh-session spy remains empty
And no flashlight or SMS adapter is invoked
```

#### H-003 — Health distinguishes unavailable transport

**Tags:** `health`, `zenoh`, `truth-in-advertising`

```gherkin
Given the native Zenoh binding is unavailable
And simulation mode has not been explicitly enabled
When the client calls phone_health with detail "full"
Then zenoh.availability is "unavailable"
And zenoh.transport is "offline"
And zenoh.simulation_enabled is false
And the response does not claim native connectivity
And the response does not claim a simulated remote side effect
```

#### H-004 — Health shows expired lifecycle

**Tags:** `health`, `lifecycle`, `expiry`

```gherkin
Given a burner node whose session expiry has passed
When the client calls phone_health
Then the response reports lifecycle "CLOSED" or the implementation's equivalent terminal state
And the response reports a non-ready status
And flashlight and SMS remain denied
And a subsequent write-shaped stub call is denied
And no new Android Intent or network operation is started
```

#### H-005 — Health preserves request correlation

**Tags:** `health`, `correlation`

```gherkin
Given two concurrent health requests with request IDs "h-a" and "h-b"
When both requests complete
Then each response contains its originating request ID
And no response contains the other request ID
And the audit records preserve the same mapping
```

#### H-006 — Health reports bind failure truthfully

**Tags:** `health`, `tailscale`, `failure`

```gherkin
Given Tailscale is configured as the required bind interface
And the interface is absent or has no eligible address
When the listener start operation is attempted
Then the listener does not bind to 0.0.0.0 or ::
And health reports bound false
And health reports a non-ready or degraded status
And the result code identifies the bind failure
And the process does not advertise a usable MCP endpoint
```

### 8.2 Tool registry and Intent boundary

#### I-001 — Only named tools are exposed

**Tags:** `mcp`, `registry`, `security`

```gherkin
Given the default phone MCP server
When the client requests the tool list
Then phone_health is present
And phone_flashlight is present as a policy-denied stub
And phone_sms is present as a policy-denied stub
And no generic android_send_intent tool is present
And no generic run_intent tool is present
And no tool accepts an arbitrary component or action field
```

If the implementation chooses not to expose denied stubs in `tools/list`, an
equivalent capabilities response MUST identify both logical operations as
registered and denied. A caller must receive a deterministic policy result
rather than discover a hidden generic escape hatch.

#### I-002 — Schemas reject undeclared fields

**Tags:** `mcp`, `schema`, `negative`

```gherkin
Given the phone_flashlight schema
When the client adds component "com.attacker.app"
Or adds action "android.intent.action.RUN"
Or adds an undeclared extra object
Then schema validation fails
And no policy or dispatch side effect occurs
```

```gherkin
Given the phone_sms schema
When the client adds package "com.attacker.messages"
Or adds intent_action "android.intent.action.SENDTO"
Or adds permission "android.permission.SEND_SMS"
Then schema validation fails
And the request is not transformed into an Android command
And no Android API is called
```

#### I-003 — Flashlight is denied by default

**Tags:** `flashlight`, `default-deny`, `stub`

```gherkin
Given the default policy phone-default-deny-v1
And a phone with a controllable flashlight
When the client calls phone_flashlight with action "on"
Then the response status is "denied"
And the response code is "POLICY_DENIED"
And the response transport is not "native"
And the flashlight state is unchanged
And no Android Intent is emitted
And no camera or torch API is called
```

#### I-004 — Every flashlight action is denied

**Tags:** `flashlight`, `default-deny`, `matrix`

```gherkin
Given the default policy
When the client calls phone_flashlight with action "on", "off", or "toggle"
Then each call returns "POLICY_DENIED"
And each call has a unique or caller-supplied correlated request_id
And no call reaches an Android component
And no call reaches hardware
```

This is a scenario outline over the action examples `on`, `off`, and `toggle`.

#### I-005 — Flashlight denial is fail-closed under dispatch failure

**Tags:** `flashlight`, `negative`, `fail-closed`

```gherkin
Given the Intent dispatcher is configured to fail if called
And the default flashlight policy is denied
When the client calls phone_flashlight with action "toggle"
Then the response is "POLICY_DENIED"
And the dispatcher failure spy records zero calls
And the result does not become "DISPATCH_FAILED"
And no retry is scheduled
```

The distinction matters: a denied command must stop before dispatch, not
attempt dispatch and then report that the dispatch failed.

#### I-006 — SMS is denied by default

**Tags:** `sms`, `default-deny`, `stub`

```gherkin
Given the default policy phone-default-deny-v1
And a valid recipient and body
When the client calls phone_sms
Then the response status is "denied"
And the response code is "POLICY_DENIED"
And no SMS provider is invoked
And no Android Intent is emitted
And no SMS leaves the device
```

#### I-007 — SMS payload is not retained or echoed

**Tags:** `sms`, `privacy`, `redaction`

```gherkin
Given recipient "+15550100123"
And body "burner-secret-should-not-appear"
When the client calls phone_sms
Then the response does not contain the full recipient
And the response does not contain the body
And the audit event does not contain the body
And the audit event does not contain a reversible recipient
And no Zenoh event contains either value
And the process log does not contain either value
```

An implementation MAY store a keyed digest or a redacted shape for audit, but
the digest MUST NOT be presented as proof that a message was sent.

#### I-008 — SMS denial does not depend on a messaging application

**Tags:** `sms`, `android`, `negative`

```gherkin
Given no messaging application is installed
And the device has no SEND_SMS permission
When the client calls phone_sms with a valid request
Then the response is still deterministic POLICY_DENIED
And the adapter does not attempt package discovery
And the adapter does not construct ACTION_SEND or ACTION_SENDTO
And the response does not suggest that a message was queued
```

#### I-009 — Unknown Intent action is rejected

**Tags:** `intent`, `allowlist`, `negative`

```gherkin
Given the fixed Intent registry
When an adapter test submits action "android.intent.action.MAIN"
Then the command is rejected with "UNKNOWN_ACTION"
And no component resolution occurs
And no Intent is dispatched
And the rejection contains the registry version
And the rejection does not contain arbitrary caller extras
```

#### I-010 — Caller cannot select the destination component

**Tags:** `intent`, `allowlist`, `security`

```gherkin
Given a flashlight request with a caller-provided component
When the request reaches the command core
Then the component field is rejected by schema or policy
And the fixed registry is not overwritten
And no package-manager lookup is performed using the caller value
And no Intent is dispatched to the caller-provided component
```

#### I-011 — Replayed request IDs do not duplicate a side effect

**Tags:** `replay`, `idempotency`, `negative`

```gherkin
Given a denied phone_flashlight request with request_id "replay-1"
When the same request is submitted again before expiry
Then the response is deterministic
And no additional dispatch occurs
And the audit trail identifies the replay or duplicate
And the flashlight remains unchanged
```

For the current default-deny stubs, zero dispatches is the required outcome
both before and after replay. The replay cache is still required because the
same command core will later protect explicitly enabled operations.

### 8.3 Tailscale binding

#### T-001 — Listener binds to Tailscale address

**Tags:** `tailscale`, `network`, `smoke`

```gherkin
Given tailscale0 exists
And it has an eligible Tailscale address
And bind_mode is "tailscale"
When the MCP listener starts
Then it binds to the configured Tailscale address
And health reports interface "tailscale0"
And health reports wildcard false
And a local connection to the advertised Tailscale address reaches MCP
```

The test harness MAY substitute a deterministic interface name and address,
but it MUST preserve the non-wildcard assertion.

#### T-002 — No wildcard listener is created

**Tags:** `tailscale`, `network`, `security`, `negative`

```gherkin
Given bind_mode is "tailscale"
When the MCP listener starts
Then socket inspection finds no listener on 0.0.0.0:port
And socket inspection finds no listener on [::]:port
And health reports wildcard false
And an address on a non-Tailscale interface cannot reach MCP
```

Binding to `0.0.0.0` or `::` is a hard failure even if a firewall currently
blocks the port. A firewall is defense in depth, not a substitute for a
correct bind address.

#### T-003 — Missing Tailscale interface fails closed

**Tags:** `tailscale`, `failure`, `fail-closed`

```gherkin
Given tailscale0 is absent
And no explicit loopback-only test override is enabled
When the listener starts
Then startup fails with a typed bind error
And no wildcard fallback occurs
And no public-interface fallback occurs
And health reports the listener as unbound
And the process does not claim readiness
```

#### T-004 — Tailscale address changes are reconciled

**Tags:** `tailscale`, `lifecycle`, `resilience`

```gherkin
Given the listener is bound to a valid Tailscale address
When the address is removed or replaced
Then the listener is marked degraded or unbound
And it does not silently bind to a wildcard address
And health exposes the new bind state
And a newly advertised address is used only after policy validation
```

The implementation MAY reconnect or restart the listener, but the transition
must be observable and must not create a public exposure window.

#### T-005 — Health advertises the effective endpoint

**Tags:** `tailscale`, `health`, `observability`

```gherkin
Given the listener is bound to 100.101.102.103:8787
When the client calls phone_health with detail "full"
Then listener.addresses contains 100.101.102.103
And listener.port is 8787
And listener.interface is tailscale0
And listener.bound is true
And listener.wildcard is false
And the advertised endpoint is the endpoint that the socket actually serves
```

Health MUST NOT advertise a stale configuration value after a bind failure or
address change.

#### T-006 — Tailscale reachability is not authorization

**Tags:** `tailscale`, `authorization`, `security`

```gherkin
Given an MCP request arrives over a valid Tailscale connection
And the request has no valid capability or caller authorization
When the client calls a write-shaped phone stub
Then network reachability alone does not grant the operation
And the result remains POLICY_DENIED
And the denial is auditable
```

Tailscale supplies a private network path. It does not remove the need for
tool policy, capability expiry, request validation, or future caller identity
checks.

### 8.4 Zenoh and result truthfulness

#### Z-001 — Simulation is labelled

**Tags:** `zenoh`, `simulation`, `truth-in-advertising`

```gherkin
Given the SUT is running with simulation explicitly enabled
When the client calls phone_health
Then zenoh.transport is "simulated"
And zenoh.simulation_enabled is true
And every Zenoh-shaped result contains transport "simulated"
And no result claims delivery to a remote router
```

#### Z-002 — Request ID correlates delayed events

**Tags:** `zenoh`, `correlation`, `events`

```gherkin
Given a command produces an immediate acknowledgement and a later event
When the command is submitted with request_id "z-001"
Then the acknowledgement contains "z-001"
And the later event contains "z-001"
And the event operation matches the original operation
And an unrelated request cannot consume the event
```

This scenario applies to future enabled commands even though the phone stubs
currently stop at policy evaluation.

#### Z-003 — Control and telemetry namespaces are separate

**Tags:** `zenoh`, `namespace`, `security`

```gherkin
Given the configured control namespace is burner/v1/{node_id}/command
When a test command or event is serialized
Then it is not published under a telemetry-only key
And a caller cannot replace the control namespace with an arbitrary key expression
And health reports the effective policy or namespace version
```

#### Z-004 — Offline and error are distinct

**Tags:** `zenoh`, `failure`, `truth-in-advertising`

```gherkin
Given Zenoh is not configured
When a phone stub is denied by policy
Then the result transport is "offline"
And the result code is "POLICY_DENIED"
```

```gherkin
Given Zenoh is configured but its adapter fails unexpectedly
When a command reaches the adapter
Then the result transport is "error"
And the error does not get rewritten as "simulated"
And the result does not claim a remote side effect
```

#### Z-005 — Denied phone commands never enter Zenoh

**Tags:** `zenoh`, `phone`, `negative`

```gherkin
Given a Zenoh publish spy
When the client calls phone_flashlight or phone_sms under default policy
Then the publish spy records zero calls
And no phone payload appears in a Zenoh key
And the response is decided by policy before transport selection
```

#### Z-006 — Subscriptions and background work are bounded

**Tags:** `zenoh`, `lifecycle`, `resource`

```gherkin
Given a future command or diagnostic subscription with a configured TTL
When the TTL expires or the MCP connection closes
Then the subscription is cancelled
And the event buffer is bounded
And no unbounded task remains owned by the burner node
And health reports the cancellation or terminal state
```

This is a release criterion for the shared control core even if the initial
phone stubs do not create subscriptions.

### 8.5 Security and teardown

#### S-001 — Capability expiry still applies over Tailscale

**Tags:** `security`, `capability`, `tailscale`

```gherkin
Given a capability that expires at time E
And a Tailscale connection remains open after E
When a write-shaped command arrives after E
Then the command is denied
And the response identifies capability expiry
And the open network connection does not extend the capability
```

#### S-002 — Sensitive values are absent from ordinary logs

**Tags:** `security`, `logging`, `privacy`

```gherkin
Given a phone_sms call with a unique recipient and body marker
When the call is denied
Then ordinary logs contain neither marker
And ordinary logs contain no bearer credential
And the audit record contains only the request ID, operation, decision,
    policy version, and an allowed redacted digest or shape
```

#### S-003 — Oversized values are rejected before dispatch

**Tags:** `security`, `bounds`, `negative`

```gherkin
Given a request body or extra larger than its declared limit
When the client submits the request
Then validation returns a typed size error
And no Android Intent is created
And no Zenoh publication occurs
And no retry is scheduled
```

#### S-004 — Unknown extras are not forwarded

**Tags:** `security`, `intent`, `negative`

```gherkin
Given a valid logical operation plus an unknown extra named "shell"
When the command is adapted for Android
Then strict validation rejects the request
And "shell" is not present in any constructed Intent
And no component is started
```

#### S-005 — Disconnect closes the burner boundary

**Tags:** `security`, `lifecycle`, `teardown`

```gherkin
Given a burner node with an active MCP connection and pending bounded work
When the node disconnects or its expiry is reached
Then the listener is closed or no longer accepts the capability
And subscriptions are cancelled
And heartbeat work is cancelled
And pending companion or command work owned by the node is cancelled
And later write-shaped calls are rejected
And health reports the terminal or degraded state
```

### 8.6 Evidence and audit

#### O-001 — Every decision is auditable

**Tags:** `observability`, `audit`

```gherkin
Given a health call, a denied flashlight call, and a denied SMS call
When the test finishes
Then each operation has an audit record
And each record includes request_id, operation, status, code, policy_version,
    and timestamp
And the records can be correlated without logging sensitive payloads
```

#### O-002 — Dispatch spy proves the negative boundary

**Tags:** `observability`, `intent`, `negative`

```gherkin
Given an instrumented Android adapter with an Intent-dispatch spy
When all default phone stub actions are exercised
Then the spy count remains zero
And the test report includes the zero-dispatch assertion
And the result codes remain POLICY_DENIED
```

#### O-003 — Socket inspection proves the network boundary

**Tags:** `observability`, `tailscale`, `network`

```gherkin
Given the listener is started in tailscale bind mode
When the test captures socket bindings and the full health result
Then both evidence sources agree on the non-wildcard Tailscale endpoint
And no public or wildcard listener is present
And a bind failure is reflected in health rather than hidden by stale metadata
```

## 9. Test harness requirements

### 9.1 Required test doubles

The implementation test harness MUST make these boundaries observable:

| Double or probe | Required observation |
| --- | --- |
| MCP client | tool list, schema errors, response envelopes, connection close |
| Policy engine | decision, policy version, capability expiry |
| Intent dispatcher | constructed Intent count and complete typed metadata |
| Android package resolver | whether caller-controlled package lookup occurred |
| Flashlight adapter | invocation count and state |
| SMS adapter | invocation count and payload access |
| Zenoh adapter | session open, publish, subscribe, close, transport label |
| Audit sink | structured decision event with redaction |
| Log sink | absence of payload markers and secrets |
| Socket inspector | bound addresses, wildcard state, port |
| Tailscale provider | interface presence, eligible addresses, address changes |
| Clock | deterministic expiry and replay-cache behavior |

Tests that only assert the returned JSON are insufficient for the negative
requirements. The dispatch, hardware, transport, logging, and socket probes
must also be checked.

### 9.2 Fixture matrix

At minimum, run the acceptance suite against:

| Fixture | Purpose |
| --- | --- |
| `fresh-offline` | no Zenoh binding, no Tailscale interface, default deny |
| `tailscale-ready` | valid Tailscale address, no wildcard bind |
| `tailscale-missing` | required interface absent, fail-closed startup |
| `zenoh-simulated` | explicit simulation and visible `simulated` labeling |
| `zenoh-error` | adapter failure remains `error`, not simulated |
| `expired-burner` | capability and lifecycle expiry |
| `malformed-input` | unknown fields, invalid enums, oversized values |
| `instrumented-android` | Intent, package, flashlight, and SMS spies |

### 9.3 Test ordering

The suite SHOULD run in this order:

1. schema and registry tests;
2. health and lifecycle tests;
3. default-deny flashlight and SMS tests;
4. Intent negative-boundary tests;
5. Tailscale socket tests;
6. Zenoh labeling and correlation tests;
7. expiry, teardown, logging, and audit tests.

No later test may rely on a side effect from an earlier test. Each fixture must
start with a fresh request replay cache and a fresh burner identity.

## 10. Failure codes

Failure codes are stable machine-readable values, not prose.

| Code | Meaning | Expected default status |
| --- | --- | --- |
| `OK` | Read-only health succeeded. | `ready` |
| `POLICY_DENIED` | Named operation is denied by the active policy. | `denied` |
| `SCHEMA_INVALID` | Input contains an invalid type, enum, or required-field violation. | `rejected` |
| `UNKNOWN_FIELD` | Strict schema or adapter found an undeclared field. | `rejected` |
| `UNKNOWN_ACTION` | Action is not in the fixed Intent registry. | `rejected` |
| `UNKNOWN_OPERATION` | Logical operation is not registered. | `rejected` |
| `CAPABILITY_EXPIRED` | Capability or burner session is no longer valid. | `denied` |
| `REQUEST_REPLAYED` | Request ID is outside the allowed replay/idempotency rule. | `rejected` |
| `PAYLOAD_TOO_LARGE` | Input exceeds the contract limit. | `rejected` |
| `TAILSCALE_UNAVAILABLE` | Required Tailscale interface/address is unavailable. | `not_ready` |
| `BIND_FAILED` | Listener could not bind to the effective Tailscale address. | `not_ready` |
| `TRANSPORT_UNAVAILABLE` | A requested transport is not configured. | `rejected` |
| `TRANSPORT_ERROR` | A configured transport failed unexpectedly. | `failed` |
| `CLOSED` | Burner lifecycle is terminal. | `rejected` |

Implementations MAY add codes, but MUST NOT reuse these codes for a different
condition without a protocol-version change.

## 11. Security invariants

The following invariants are release-blocking:

1. **No arbitrary Intent invariant:** MCP input cannot select an Android
   component, action, package, URI scheme, permission, or extra key.
2. **Default-deny invariant:** flashlight and SMS both remain denied unless a
   separately approved policy version changes the capability.
3. **Zero-dispatch invariant:** denied phone calls create zero Android Intents
   and zero hardware/provider calls.
4. **No-SMS invariant:** the default build does not use `SEND_SMS`,
   `SmsManager`, `ACTION_SEND`, or `ACTION_SENDTO` for `phone_sms`.
5. **No-wildcard invariant:** Tailscale mode never binds `0.0.0.0` or `::`.
6. **No-fallback invariant:** loss of Tailscale does not fall back to a public
   interface.
7. **Transport-truth invariant:** simulated, offline, and error results cannot
   be reported as native success.
8. **Correlation invariant:** a result or event cannot be attributed to a
   different request ID.
9. **Expiry invariant:** network connection lifetime does not extend capability
   or burner lifetime.
10. **Redaction invariant:** SMS content, credentials, and sensitive artifacts
    are absent from ordinary logs, Zenoh telemetry, and denial responses.
11. **Teardown invariant:** disconnect and expiry cancel bounded background work
    and prevent new write-shaped operations.
12. **Evidence invariant:** each negative result has enough structured metadata
    to prove which policy decision was made without retaining the secret input.

## 12. Implementation checklist

This checklist is intentionally ordered so the safe boundary exists before any
future hardware integration.

### Phase 0 — Contract and policy

- [ ] Add `phone-mcp/v1` result-envelope types.
- [ ] Add a fixed logical operation registry.
- [ ] Add `phone-default-deny-v1`.
- [ ] Add schema validation with `additionalProperties: false`.
- [ ] Add stable failure codes.
- [ ] Add deterministic clock and request-ID interfaces.
- [ ] Add the redaction policy before adding payload logging.

### Phase 1 — Health and lifecycle

- [ ] Implement `phone_health` without opening Zenoh or dispatching Intents.
- [ ] Implement READY, degraded, and CLOSED state reporting.
- [ ] Report the effective policy version and stub states.
- [ ] Report native, simulated, offline, and error transport distinctly.
- [ ] Add session expiry and teardown hooks.

### Phase 2 — Tailscale bind

- [ ] Resolve eligible addresses from the configured Tailscale interface.
- [ ] Bind the listener to an explicit address, never a wildcard.
- [ ] Fail closed when the interface or address is absent.
- [ ] Reconcile address changes without public fallback.
- [ ] Make socket inspection part of the integration test.
- [ ] Keep authorization separate from network reachability.

### Phase 3 — Intent stubs

- [ ] Register `phone_flashlight` as a named, denied stub.
- [ ] Register `phone_sms` as a named, denied stub.
- [ ] Assert zero Intent dispatches for all default actions.
- [ ] Assert zero flashlight-provider calls.
- [ ] Assert zero SMS-provider calls.
- [ ] Assert no `SEND_SMS`, `SmsManager`, `ACTION_SEND`, or `ACTION_SENDTO`
      path is reached.
- [ ] Reject caller-selected components, packages, actions, and extras.

### Phase 4 — Zenoh and observability

- [ ] Add the adapter interface without making it the policy authority.
- [ ] Label simulation explicitly.
- [ ] Keep control and telemetry namespaces separate.
- [ ] Add request-correlated events and bounded TTLs.
- [ ] Add audit records and sensitive-value redaction.
- [ ] Verify teardown cancels subscriptions and background work.

### Phase 5 — Future capability change

- [ ] Write a new spec or revision before enabling flashlight.
- [ ] Write a new spec or revision before enabling SMS.
- [ ] Require an explicit policy version and approval record.
- [ ] Preserve all schema, component, capability, expiry, and audit tests.
- [ ] Add hardware/provider tests before changing the default status.

## 13. Definition of done

SPEC-002 is accepted when:

- every mandatory acceptance test passes in the fixture matrix;
- the default registry has no generic Intent escape hatch;
- `phone_health` is truthful before, during, and after bind/lifecycle changes;
- flashlight and SMS return deterministic `POLICY_DENIED` results;
- instrumentation proves those calls dispatch zero Intents and perform zero
  hardware/provider side effects;
- SMS content and credentials are absent from results, logs, and Zenoh;
- the MCP listener is demonstrably Tailscale-only and non-wildcard;
- loss of Tailscale fails closed;
- native, simulated, offline, and error transport states are distinguishable;
- replay, expiry, disconnect, and teardown behavior is tested;
- the audit and socket evidence is attached to the implementation change; and
- any later link to `BASIC_TIER` or `SPEC-001` points to an authoritative file,
  not a guessed path.

Passing a mocked tool call alone is not sufficient. The implementation must
prove both the positive contract (health and structured results) and the
negative boundary (no dispatch, no public listener, no secret retention).

## 14. Open decisions for a future revision

These questions are deliberately not resolved by this spec:

1. Which Android package owns the future explicit flashlight and SMS actions?
2. Which capability issuer, if any, authorizes a future non-denied action?
3. Will the MCP endpoint run in-process on Android or in a workstation bridge?
4. Which Tailscale peer identity claims are available to the MCP layer?
5. Which native Zenoh Kotlin binding and ABI set will replace the research
   stubs?
6. What user-visible confirmation is required before enabling a physical
   flashlight or sending a message?
7. What retention period applies to audit digests and burner node IDs?

Resolving any of these questions does not automatically authorize hardware or
messaging capability. The default-deny and no-arbitrary-Intent invariants
remain in force until a reviewed policy change and corresponding acceptance
tests are merged.
