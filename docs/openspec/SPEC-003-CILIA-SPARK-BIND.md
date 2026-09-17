# SPEC-003 — CILIA / SPARK BIND

**Title:** Vesper web Send + MCP bind  
**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** Liv HUB / Vesper integration  
**Audience:** Vesper web, Spark adapter, Cilia bus, MCP host/runtime, Keel Sentry, QA  
**Last updated:** 2026-09-17  
**Related surfaces:** `cilia-bus`, `mcp-surface`, Vesper web, Keel Sentry  

> This specification is intentionally large because the dangerous part of this
> change is not the button. It is proving that a visible web **Send** actually
> reaches the intended MCP bind, is attributed to the correct session, can be
> replayed safely, and leaves a durable receipt when any intermediary fails.

## 1. Executive decision

Build one explicit path:

```text
Vesper web composer
    │ user clicks visible Send
    ▼
Vesper web Send controller
    │ creates a signed, idempotent send intent
    ▼
Spark bind adapter
    │ validates the selected MCP binding and forwards the intent
    ▼
MCP host / selected tool
    │ executes exactly once or returns a classified failure
    ▼
Cilia receipt + high-water store
    │ durable outcome, correlation, and open-leg transition
    ▼
Keel Sentry
    │ traces, metrics, redacted events, alerts
    ▼
Vesper web result state
```

The contract is for **real UI Send**. A Gmail message, Gmail draft, email
automation, or mail-shaped test fixture is not a substitute for the Send
action and does not satisfy this specification.

The MCP bind is a web interaction binding, not a mail binding:

* the user sees which MCP server and tool are selected;
* the user invokes **Send** in the Vesper web UI;
* the browser submits a send intent to the Vesper/Spark path;
* the MCP host receives the intent and invokes the selected tool;
* the UI renders a result tied to that exact send;
* Cilia records a durable receipt without requiring email;
* Keel Sentry records the lifecycle with secrets and message content redacted.

Email may remain an optional wake or notification mechanism elsewhere in the
system. It MUST NOT be inserted into this path, and an email side effect MUST
NOT be used as evidence that the bind works.

## 2. Problem statement

The current Cilia contract is a high-water and receipt runner. Its historical
coordination pattern treats email as wake-only and Drive or another durable
receipt surface as the acknowledgement. The MCP surface is a domain feeder,
not a single implicit transport. That is useful for asynchronous coordination,
but it does not prove an interactive user flow.

Vesper needs a concrete, testable bridge from:

1. a human composing content in the web UI;
2. the human clicking the visible **Send** control;
3. a selected Spark/MCP binding;
4. an MCP invocation;
5. a typed result or failure visible in the same UI;
6. a durable Cilia receipt and high-water transition;
7. operational evidence in Keel Sentry.

Without this contract, the following false positives are possible:

* a mail draft exists, but no UI Send occurred;
* an email was sent, but no MCP tool was invoked;
* the MCP tool ran, but the UI displayed a stale or unrelated result;
* a retry invoked a non-idempotent tool twice;
* a bind disappeared after reload but was still treated as active;
* an error was shown to the user but no durable receipt recorded it;
* Sentry contains raw prompt or token data;
* a test passed using a mock function that bypassed the browser path.

This specification closes those gaps without inventing a new top-level skill.
Implementation belongs under the existing Vesper web/Spark integration and the
MCP/Cilia modules.

## 3. Goals

### 3.1 Primary goals

The implementation MUST:

1. expose a real Vesper web composer with a visible **Send** control;
2. make the selected MCP binding visible before Send;
3. bind a selected MCP server/tool to the current Vesper session;
4. send through that binding only after the user activates Send;
5. create a stable correlation ID and idempotency key before dispatch;
6. preserve the distinction between UI Send, bind, MCP invocation, and receipt;
7. return a typed success, partial-success, or failure state to the UI;
8. record a durable Cilia receipt for every terminal send outcome;
9. update Cilia high-water/open-leg state idempotently;
10. emit redacted Keel Sentry lifecycle hooks;
11. fail closed when the bind is ambiguous, unauthorized, stale, or unsafe;
12. support deterministic acceptance tests that exercise the browser path;
13. support safe retry after transport interruption;
14. make duplicate attempts visible without duplicating side effects;
15. preserve enough evidence to distinguish UI, adapter, MCP, receipt, and
    observability failures.

### 3.2 Secondary goals

The implementation SHOULD:

* restore a bind after a page reload when the session is still valid;
* make capability and health status understandable to a human;
* support a dry-run or preview mode that cannot invoke a side-effecting tool;
* allow a binding to be revoked independently of the Vesper session;
* make the smallest useful Cilia receipt available locally first;
* tolerate a temporary Keel Sentry outage without losing the user result;
* expose latency and duplicate-suppression metrics;
* allow a future non-web client to reuse the envelope without pretending it is
  a web UI Send.

### 3.3 Non-goals

This specification does not:

* implement Gmail, SMTP, mail drafts, mail watchers, or mail delivery;
* make email a second transport for the same send;
* define the internals of a particular MCP server;
* grant a tool capability the user did not select or authorize;
* replace MCP authentication, browser session authentication, or policy gates;
* define a new Cilia top-level skill;
* make all MCP tools safe for automatic retries;
* guarantee delivery when the selected downstream service is unavailable;
* store full prompt or tool-result bodies in Sentry;
* treat a browser network request made without a user click as a valid UI Send;
* turn a failed Sentry event into a failed business operation by default;
* solve long-term mailbox or conversation-lake indexing.

## 4. Normative language

The words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are normative.

An implementation is conformant only if it satisfies the MUST and MUST NOT
requirements in this document. An implementation may defer SHOULD items, but
the deferral MUST be recorded in the rollout checklist.

## 5. Terminology

| Term | Meaning |
|---|---|
| Vesper web | The browser-facing Vesper conversation/composer surface. |
| Spark | The adapter/runtime leg that connects Vesper web to the MCP host. It is not a mail provider. |
| Cilia | Durable coordination state: high-water, receipts, open legs, and correlation. |
| bind | An explicit association between a Vesper session and one allowed MCP server/tool capability. |
| binding | The persisted, versioned representation of a bind. |
| Send | The visible Vesper web user action that submits the current composer content. |
| send intent | The immutable request created by the Send controller before dispatch. |
| MCP host | The runtime that authenticates and invokes MCP tools. |
| selected tool | The exact tool name and server identity visible at Send time. |
| side effect | Any downstream action that changes external state or causes an externally observable action. |
| receipt | Durable Cilia record of a send outcome or classified failure. |
| high-water | Monotonic Cilia cursor/state used to avoid reprocessing. |
| open leg | A Cilia work item that has started but has not reached a terminal receipt. |
| Keel Sentry | Operational observability and safety hook surface for this flow. |
| attempt | One dispatch request identified by an attempt ID. |
| duplicate | A later request carrying an already-seen idempotency key or send ID. |
| stale bind | A binding whose TTL, version, session, auth, or capability no longer matches current policy. |
| mail | Email or email-like transport. Mail is explicitly out of this path. |

## 6. Invariants

These are the hard invariants for design, implementation, and review.

### 6.1 UI and intent invariants

1. A valid UI Send MUST originate from a trusted browser event tied to the
   current Vesper session.
2. The Send controller MUST create the `send_id`, `correlation_id`, and
   `idempotency_key` before network dispatch.
3. The `send_id` MUST remain stable across an automatic retry of the same user
   action.
4. A manually repeated click MAY create a new attempt, but it MUST NOT silently
   create a new semantic message unless the UI clearly allows it.
5. The UI MUST display the bound server and tool before Send.
6. The UI MUST display a pending state immediately after accepted Send.
7. A stale, missing, or ambiguous binding MUST disable Send or produce a
   deterministic bind error before MCP invocation.
8. A browser request without a current user gesture MUST NOT be labeled
   `ui_send.accepted`.

### 6.2 MCP invariants

1. The MCP host MUST receive the exact selected server ID, tool name, bind ID,
   session ID, and send ID.
2. The host MUST re-authorize the bind at dispatch time; browser state alone is
   insufficient.
3. The selected tool MUST be checked against the binding capability snapshot.
4. The host MUST NOT fall back to a different tool or server without explicit
   user-visible consent.
5. Tool arguments MUST be validated against the MCP schema before invocation.
6. Tool execution MUST carry an idempotency key when the tool supports one.
7. For non-idempotent tools, retry policy MUST be `manual` unless the adapter
   has a server-specific deduplication guarantee.
8. Tool output MUST be classified before it is rendered as success.
9. An MCP acknowledgement MUST NOT be called delivery unless the downstream
   tool contract says it represents delivery.

### 6.3 Cilia invariants

1. Cilia receipt writing MUST NOT require email.
2. Every accepted UI Send MUST produce exactly one terminal receipt keyed by
   `send_id`, even if the terminal state is failure or indeterminate.
3. Receipt writes MUST be idempotent.
4. High-water movement MUST be monotonic.
5. A receipt MUST include the selected binding identity, not merely a generic
   `mcp` label.
6. An open leg MUST remain open when the downstream outcome is unknown.
7. A duplicate dispatch MUST resolve from existing receipt or attempt state
   when possible.
8. The Cilia receipt MUST not contain access tokens, cookies, raw authorization
   headers, or unredacted secret-bearing arguments.

### 6.4 Keel Sentry invariants

1. Every lifecycle transition MUST have a Keel Sentry event or an explicitly
   counted telemetry drop.
2. Sentry payloads MUST be redacted before leaving the process boundary.
3. Sentry MUST receive identifiers and hashes needed for correlation, not raw
   message content by default.
4. A Sentry outage MUST NOT cause a second MCP invocation.
5. A Sentry outage MUST NOT turn an already completed downstream action into a
   user-visible failure.
6. Security, authorization, duplicate-side-effect, and unknown-outcome signals
   MUST remain alertable even when normal event delivery is degraded.

## 7. Reference architecture

### 7.1 Components

| Component | Responsibility | Must not do |
|---|---|---|
| Composer | Collect text/attachments/structured input and show bind state. | Choose a hidden fallback tool. |
| Send controller | Validate local state, create intent, submit once, render lifecycle. | Send mail or infer success from UI optimism. |
| Bind registry | Store bind ID, target identity, capabilities, version, expiry, revocation. | Grant broad server access by default. |
| Spark adapter | Translate Vesper intent to MCP-host request and map result. | Invent tool names or silently coerce arguments. |
| MCP host | Authenticate, authorize, validate, invoke, and classify tool result. | Trust browser claims without rechecking. |
| Cilia writer | Append durable receipt and advance high-water/open leg state. | Require Gmail or other mail transport. |
| Keel Sentry client | Emit redacted traces, events, metrics, and alerts. | Log secrets or raw prompt bodies. |
| Result reconciler | Resolve browser reconnect/retry against durable state. | Create a second send for an existing `send_id`. |

### 7.2 Trust boundaries

```text
[Browser DOM / browser storage]
            │ untrusted input
            ▼
[Vesper web session + Send controller]
            │ authenticated intent
            ▼
[Spark adapter boundary]
            │ server-side bind recheck
            ▼
[MCP host + policy/auth boundary]
            │ tool invocation
            ▼
[External MCP server/tool]

[All server-side stages] ──redacted telemetry──> [Keel Sentry]
[Terminal outcome] ────────durable receipt──────> [Cilia store]
```

The browser MAY display a cached binding, but only the server-side bind
registry and MCP host authorization are authoritative.

### 7.3 Required deployment shape

The first implementation MUST support a single authoritative Spark adapter per
Vesper environment. Multiple adapters MAY exist later, but the UI MUST expose
which adapter owns the bind and the backend MUST reject split-brain ownership.

The first implementation MUST use one Cilia receipt writer per logical
environment or a storage primitive that provides equivalent idempotent
conditional writes. Two writers must not race a terminal receipt into two
different outcomes.

## 8. Binding contract

### 8.1 What a bind means

A bind is a narrow capability grant:

```text
session S may invoke tool T on server M
using adapter A
under policy snapshot P
until expiry E or revocation R.
```

A bind is not:

* a login shortcut;
* a blanket grant to every tool on a server;
* a browser-only flag;
* a mail address;
* a permanent authorization;
* proof that the downstream tool is healthy;
* permission to retry a side effect forever.

### 8.2 Binding record

The canonical binding record MUST contain at least:

```json
{
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "session_id": "vesper_sess_01J...",
  "subject_id": "user_or_service_subject",
  "adapter_id": "spark-prod-us-east",
  "mcp_server_id": "server.example",
  "mcp_server_url_hash": "sha256:...",
  "tool_name": "example_tool",
  "tool_version": "2026-09-17",
  "capability_class": "read_only",
  "argument_schema_hash": "sha256:...",
  "side_effect_class": "none",
  "created_at": "2026-09-17T04:10:00Z",
  "expires_at": "2026-09-17T04:25:00Z",
  "revoked_at": null,
  "policy_snapshot_id": "policy_...",
  "status": "active"
}
```

The server URL MAY be retained in an access-controlled registry, but the
public UI and Sentry payload SHOULD use a stable hash or display-safe name.

### 8.3 Allowed binding states

```text
requested → pending_auth → active → rotating → expired
                         ├→ revoked
                         ├→ denied
                         └→ invalid
```

Only `active` bindings may accept Send. `rotating` MAY accept Send only if the
server has explicitly declared the old and new versions equivalent. Otherwise
the UI MUST show “Re-bind required”.

### 8.4 Bind creation

When the user chooses **Bind MCP**:

1. the UI MUST show server identity and tool identity;
2. the UI MUST show capability class and side-effect class;
3. the UI MUST show expiry or session scope;
4. the user MUST explicitly confirm the bind when the tool can cause an
   external side effect;
5. the server MUST create a bind record;
6. the server MUST return `bind_id`, `bind_version`, and an expiry;
7. the UI MUST render the active bind from the server response;
8. a bind success event MUST be distinguishable from a Send success event.

For read-only or preview-only tools, the product MAY use a one-click bind if
the policy permits it, but the bind still requires server authorization.

### 8.5 Bind revocation

Revocation MUST take effect for new sends immediately after the authoritative
registry observes it. An in-flight call MAY complete, but it MUST be reconciled
against the revocation timestamp and classified according to policy.

The UI MUST not claim that revocation cancelled a downstream tool unless the
MCP server confirms cancellation.

## 9. Send contract

### 9.1 UI semantics

The composer MUST expose these states:

| UI state | Meaning | Send availability |
|---|---|---|
| `unbound` | No active MCP binding for this session. | Disabled. |
| `binding` | Bind request is in progress. | Disabled. |
| `bound` | Active bind is visible and current. | Enabled if input valid. |
| `submitting` | User Send accepted locally and dispatch is pending. | Disabled for same send. |
| `awaiting_mcp` | MCP host accepted the intent. | Disabled for same send; cancel only if supported. |
| `awaiting_receipt` | MCP outcome known; durable receipt pending. | Disabled for same send. |
| `succeeded` | Tool outcome and durable receipt are successful. | New Send allowed. |
| `failed` | Terminal failure with retry classification. | New or safe retry allowed. |
| `unknown` | Downstream outcome cannot be established. | Manual reconciliation required. |
| `rebind_required` | Bind stale, revoked, or capability changed. | Disabled until rebind. |

The visible primary control MUST be labeled **Send**. “Mail”, “Email”, “Draft”,
or “Compose email” MUST NOT be used as the action label for this feature.

The UI MUST show, at minimum, before the click:

* selected MCP server display name;
* selected tool name;
* side-effect classification;
* binding status;
* binding expiry or session scope;
* any approval/confirmation requirement.

The UI SHOULD show a compact correlation reference after dispatch. It MUST
provide a way for support or QA to obtain the full `send_id` without exposing
secrets.

### 9.2 Send intent

The Send controller MUST create an immutable intent with the following logical
fields:

```json
{
  "schema": "cilia.spark.send-intent.v1",
  "send_id": "send_01J...",
  "attempt_id": "attempt_01J...",
  "correlation_id": "corr_01J...",
  "idempotency_key": "sha256:...",
  "session_id": "vesper_sess_01J...",
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "adapter_id": "spark-prod-us-east",
  "mcp_server_id": "server.example",
  "tool_name": "example_tool",
  "input": {
    "content_ref": "content_01J...",
    "content_sha256": "sha256:...",
    "content_length": 42,
    "attachments": []
  },
  "client": {
    "ui_surface": "vesper-web",
    "ui_action": "send",
    "user_gesture": true,
    "client_request_id": "client_..."
  },
  "policy": {
    "side_effect_class": "none",
    "retry_class": "safe"
  },
  "created_at": "2026-09-17T04:10:00Z"
}
```

The actual content MAY be sent in a protected request body or referenced by a
short-lived content token. The receipt and Sentry event SHOULD store only the
content hash and length by default.

`user_gesture` is an assertion that MUST be established by trusted server-side
or browser security controls. It MUST NOT be accepted solely because the
browser posted `true`.

### 9.3 Idempotency

The system MUST deduplicate on `send_id` and `idempotency_key`. The preferred
key is derived from the immutable semantic send plus the active bind:

```text
idempotency_key =
  H(session_id || bind_id || bind_version || semantic_message_id)
```

The implementation MAY use a server-issued random idempotency key, but it
MUST persist the mapping from that key to `send_id` before dispatch.

Deduplication behavior:

| Condition | Required behavior |
|---|---|
| same `send_id`, same payload hash | Return existing state; do not invoke again. |
| same `send_id`, different payload hash | Reject as `send_payload_conflict`. |
| new `send_id`, same semantic message after user retry | Invoke only if retry policy allows; record link to predecessor. |
| same idempotency key, same bind | Return existing attempt/receipt. |
| same idempotency key, different bind | Reject and require new explicit Send. |
| same client request ID, no stored intent | Create exactly one intent transactionally. |

### 9.4 Request ordering

The server MUST persist the accepted intent before calling the MCP host.

The server MUST not:

1. invoke the MCP tool;
2. then attempt to invent the `send_id`;
3. then write a best-effort receipt.

If the process dies after persistence but before MCP invocation, reconciliation
MAY safely decide whether to dispatch based on attempt state and downstream
idempotency policy.

### 9.5 MCP request

The Spark adapter MUST forward:

```json
{
  "schema": "cilia.spark.mcp-dispatch.v1",
  "send_id": "send_01J...",
  "attempt_id": "attempt_01J...",
  "correlation_id": "corr_01J...",
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "session_id": "vesper_sess_01J...",
  "mcp_server_id": "server.example",
  "tool_name": "example_tool",
  "idempotency_key": "sha256:...",
  "arguments": {
    "content_ref": "content_01J..."
  },
  "deadline": "2026-09-17T04:10:30Z"
}
```

The adapter MUST reject a request if any target identity differs from the
authoritative binding. It MUST not use the browser’s selected tool name as the
sole authority.

### 9.6 Result classification

The Spark adapter MUST map downstream results into one of:

| Result class | Terminal? | Retry default | UI meaning |
|---|---:|---|---|
| `success` | yes | no | Tool completed according to its contract. |
| `rejected` | yes | no | Policy, auth, schema, or user approval denied it. |
| `transient_failure` | yes for attempt, no for send if safe | safe retry if declared | Service may recover. |
| `permanent_failure` | yes | no | Retry would repeat a known-invalid request. |
| `timeout_unknown` | no | manual reconcile | Tool may have run; do not duplicate blindly. |
| `transport_unknown` | no | manual reconcile | Response was lost after dispatch ambiguity. |
| `receipt_pending` | no | no MCP retry | Tool outcome known; Cilia write pending. |

The UI MUST NOT render `timeout_unknown` or `transport_unknown` as a clean
failure that invites an automatic duplicate side effect.

## 10. Cilia integration

### 10.1 Receipt model

Extend the conceptual Cilia receipt with bind-aware fields. Existing Cilia
fields (`msg_id`, `action`, optional `file_id`/`path`, timestamp, notes) remain
valid for older records. New receipts SHOULD use the following shape:

```json
{
  "receipt_version": "1.0",
  "msg_id": "send_01J...",
  "action": "vesper.web.send",
  "status": "succeeded",
  "send_id": "send_01J...",
  "attempt_id": "attempt_01J...",
  "correlation_id": "corr_01J...",
  "session_id": "vesper_sess_01J...",
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "adapter_id": "spark-prod-us-east",
  "mcp_server_id": "server.example",
  "tool_name": "example_tool",
  "tool_result_class": "success",
  "content_sha256": "sha256:...",
  "result_sha256": "sha256:...",
  "receipt_id": "receipt_01J...",
  "timestamp": "2026-09-17T04:10:02Z",
  "retryable": false,
  "notes": []
}
```

`msg_id` MUST equal `send_id` for this flow unless a legacy bridge requires
otherwise. If a legacy bridge uses another value, both IDs MUST be present.

### 10.2 Receipt lifecycle

```text
intent_persisted
    └─> dispatch_started
          ├─> mcp_succeeded
          │     └─> receipt_written ──> high_water_advanced
          ├─> mcp_rejected
          │     └─> failure_receipt_written ──> high_water_advanced
          ├─> mcp_transient_failure
          │     └─> retryable_receipt_written ──> high_water_advanced
          └─> outcome_unknown
                └─> open_leg_retained; no false ACK
```

The `outcome_unknown` branch is intentional. A missing response is not proof
that the tool did not run.

### 10.3 High-water requirements

The Cilia high-water record MUST:

* record the last accepted or terminal `send_id` in a durable way;
* retain receipt IDs or a queryable receipt index;
* retain open legs for unknown outcomes and receipt-pending work;
* reject backward movement;
* tolerate replay of the same terminal receipt;
* expose enough state for a reconnecting Vesper client to reconcile.

If an existing `last_inbox_msg_id` field cannot represent web sends cleanly,
add a namespaced cursor rather than overloading email semantics:

```json
{
  "cursors": {
    "cilia.web_send": {
      "last_send_id": "send_01J...",
      "last_receipt_id": "receipt_01J...",
      "updated_at": "2026-09-17T04:10:02Z"
    }
  }
}
```

### 10.4 No mail bridge

The Cilia web-send writer MUST be callable without:

* Gmail credentials;
* an email thread ID;
* a mail recipient;
* an email subject;
* a mail draft;
* an inbox poll.

Tests MUST prove this by running with mail connectors disabled or unavailable.

## 11. Keel Sentry hooks

### 11.1 Hook purpose

Keel Sentry is the operational spine for this flow. Hooks are not business
authorization, and a Sentry event is not a receipt. A Sentry event describes
what the system observed; a Cilia receipt records the durable business
outcome.

The implementation MUST emit hooks at the following boundaries:

| Hook | Emitted when |
|---|---|
| `keel.cilia_bind.requested` | User starts a bind request. |
| `keel.cilia_bind.authorized` | Server authorizes and persists a bind. |
| `keel.cilia_bind.denied` | Bind is refused. |
| `keel.cilia_bind.revoked` | Bind is revoked or expires. |
| `keel.ui_send.clicked` | Trusted user gesture reaches the Send controller. |
| `keel.ui_send.rejected` | Local or server validation rejects Send before intent acceptance. |
| `keel.ui_send.accepted` | Immutable send intent is persisted. |
| `keel.spark.dispatch.started` | Spark begins MCP dispatch. |
| `keel.spark.dispatch.rejected` | Dispatch is blocked before MCP invocation. |
| `keel.mcp.invoke.started` | MCP host begins tool invocation. |
| `keel.mcp.invoke.completed` | MCP host returns a classified result. |
| `keel.mcp.invoke.unknown` | Outcome cannot be established. |
| `keel.cilia.receipt.started` | Receipt writer begins durable write. |
| `keel.cilia.receipt.written` | Receipt is durably committed. |
| `keel.cilia.receipt.failed` | Receipt write fails or is deferred. |
| `keel.ui_send.rendered` | Browser renders terminal/reconciliation state. |
| `keel.ui_send.duplicate_suppressed` | Duplicate attempt returns prior state. |
| `keel.security.redaction_failed` | Payload could not be safely redacted. |

### 11.2 Common event envelope

Every hook MUST use a common envelope:

```json
{
  "event_name": "keel.mcp.invoke.completed",
  "event_version": 1,
  "event_id": "evt_01J...",
  "occurred_at": "2026-09-17T04:10:02.120Z",
  "environment": "staging",
  "service": "spark-adapter",
  "region": "us-east",
  "severity": "info",
  "correlation_id": "corr_01J...",
  "send_id": "send_01J...",
  "attempt_id": "attempt_01J...",
  "session_id_hash": "sha256:...",
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "mcp_server_id": "server.example",
  "tool_name": "example_tool",
  "outcome": "success",
  "duration_ms": 842,
  "payload": {
    "content_sha256": "sha256:...",
    "argument_keys": ["content_ref"],
    "result_class": "success"
  }
}
```

### 11.3 Redaction policy

The following MUST never appear in Keel Sentry:

* access tokens;
* refresh tokens;
* cookies;
* authorization headers;
* private keys;
* signed URLs;
* full user prompts;
* full MCP arguments by default;
* full tool results;
* email addresses unless separately approved as a display-safe identifier;
* attachment bytes;
* raw stack traces containing request bodies.

The following MAY appear:

* stable hashes;
* lengths;
* schema versions;
* key names;
* server/tool display-safe IDs;
* side-effect and capability classes;
* error code and category;
* latency;
* retry classification;
* environment and region;
* sampled, explicitly approved diagnostic fragments.

If redaction fails, the system MUST drop the unsafe event, emit
`keel.security.redaction_failed` with only a safe static code, and continue or
fail the business operation according to the underlying operation’s own
policy. It MUST NOT send the unredacted payload as a fallback.

### 11.4 Sentry failure policy

Keel Sentry is best-effort for normal events:

* UI Send MUST continue if the event sink is unavailable;
* MCP invocation MUST NOT be retried because a Sentry event failed;
* Cilia receipt writing MUST continue if the event sink is unavailable;
* event delivery failure MUST increment a local durable/drop counter;
* security and unknown-outcome events SHOULD use a local emergency buffer;
* a persistent event drop MUST create an alert when connectivity returns.

The only exception is a policy explicitly marked `telemetry_required`. That
policy MUST be declared before Send and MUST be visible to operators; it MUST
not be introduced accidentally by an adapter default.

### 11.5 Required metrics

Emit or derive:

* `cilia_bind_active_total`;
* `cilia_bind_denied_total`;
* `cilia_bind_stale_total`;
* `vesper_ui_send_clicked_total`;
* `vesper_ui_send_accepted_total`;
* `vesper_ui_send_rejected_total`;
* `spark_dispatch_started_total`;
* `mcp_invoke_started_total`;
* `mcp_invoke_completed_total`;
* `mcp_invoke_unknown_total`;
* `cilia_receipt_written_total`;
* `cilia_receipt_failed_total`;
* `cilia_duplicate_suppressed_total`;
* `keel_event_dropped_total`;
* `send_to_mcp_latency_ms`;
* `send_to_receipt_latency_ms`;
* `unknown_outcome_age_seconds`.

Metrics MUST be labeled by safe dimensions such as environment, adapter,
capability class, side-effect class, result class, and tool display-safe ID.
Do not label metrics with raw user text.

## 12. API surface

Names below are logical contracts, not a requirement to use a particular
framework or URL scheme.

### 12.1 Bind

```text
POST /vesper/sessions/{session_id}/bindings
```

Request:

```json
{
  "adapter_id": "spark-prod-us-east",
  "mcp_server_id": "server.example",
  "tool_name": "example_tool",
  "requested_mode": "interactive",
  "client_request_id": "client_bind_01J...",
  "approval": {
    "user_confirmed": true
  }
}
```

Response:

```json
{
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "status": "active",
  "expires_at": "2026-09-17T04:25:00Z",
  "server": {
    "id": "server.example",
    "display_name": "Example MCP"
  },
  "tool": {
    "name": "example_tool",
    "capability_class": "read_only",
    "side_effect_class": "none",
    "schema_hash": "sha256:..."
  }
}
```

### 12.2 Send

```text
POST /vesper/sessions/{session_id}/send
```

Request:

```json
{
  "send_id": "send_01J...",
  "client_request_id": "client_send_01J...",
  "bind_id": "bind_01J...",
  "bind_version": 3,
  "idempotency_key": "sha256:...",
  "content": {
    "text": "user content",
    "attachments": []
  },
  "ui_context": {
    "surface": "vesper-web",
    "action": "send",
    "user_gesture_token": "opaque-short-lived-token"
  }
}
```

Accepted response:

```json
{
  "send_id": "send_01J...",
  "attempt_id": "attempt_01J...",
  "correlation_id": "corr_01J...",
  "status": "accepted",
  "receipt_status": "pending"
}
```

The accepted response means intent persisted. It does not mean the MCP tool
completed.

### 12.3 Status/reconcile

```text
GET /vesper/sessions/{session_id}/send/{send_id}
```

Possible response states:

```json
{
  "send_id": "send_01J...",
  "status": "succeeded",
  "mcp": {
    "server_id": "server.example",
    "tool_name": "example_tool",
    "result_class": "success"
  },
  "receipt": {
    "status": "written",
    "receipt_id": "receipt_01J..."
  },
  "retry": {
    "allowed": false,
    "reason": "terminal_success"
  }
}
```

The status endpoint MUST be safe to poll/reload and MUST NOT invoke the tool.

### 12.4 Revoke

```text
DELETE /vesper/sessions/{session_id}/bindings/{bind_id}
```

The operation MUST be idempotent. Repeating revocation MUST return the current
revoked state and MUST NOT cause a new side effect.

## 13. State machines

### 13.1 Send state machine

```text
draft
  │ local validation + trusted click
  ▼
intent_persisted
  │ binding recheck
  ├───────────────► rejected_before_dispatch
  ▼
dispatch_started
  │
  ├───────────────► mcp_rejected
  ├───────────────► mcp_transient_failure
  ├───────────────► outcome_unknown
  ▼
mcp_completed
  │
  ├───────────────► receipt_failed (open leg retained)
  ▼
receipt_written
  │
  ▼
terminal_success | terminal_failure | retryable_failure
```

Illegal transitions MUST be rejected and logged as invariant violations. In
particular:

* `draft → mcp_completed` is illegal;
* `rejected_before_dispatch → mcp_completed` is illegal;
* `outcome_unknown → terminal_failure` is not automatic;
* `receipt_failed → terminal_success` is not allowed until the receipt is
  actually durable;
* a second `dispatch_started` for the same attempt is illegal.

### 13.2 Bind state machine

```text
unbound
  │ request
  ▼
pending_auth
  ├── denied ──► denied
  ├── invalid ─► invalid
  ▼
active
  ├── revoke ──► revoked
  ├── expiry ──► expired
  └── rotate ──► rotating ──► active | rebind_required
```

### 13.3 Receipt state machine

```text
not_started → writing → written
                    └→ deferred → writing
```

Receipt writing MUST be at-least-once with idempotent commit semantics. A
deferred receipt MUST remain visible as an open leg until written or explicitly
classified as a durable terminal failure.

## 14. Error taxonomy

Errors MUST have a stable machine code, human-safe summary, retry class, and
correlation ID. Suggested codes:

| Code | Layer | Retry |
|---|---|---|
| `bind_missing` | UI/bind | bind |
| `bind_expired` | bind | rebind |
| `bind_revoked` | bind | rebind |
| `bind_version_conflict` | bind | refresh/rebind |
| `bind_capability_mismatch` | bind/MCP | choose approved tool |
| `bind_server_unavailable` | bind | safe bind retry |
| `send_empty` | UI | edit input |
| `send_gesture_missing` | UI/security | user click |
| `send_payload_conflict` | idempotency | manual investigation |
| `send_duplicate` | idempotency | no retry |
| `dispatch_not_authorized` | Spark/MCP | rebind or approval |
| `mcp_schema_invalid` | MCP | fix input/tool |
| `mcp_tool_not_found` | MCP | rebind/refresh catalog |
| `mcp_tool_denied` | MCP | no automatic retry |
| `mcp_transient_unavailable` | MCP | safe retry if policy says so |
| `mcp_timeout_unknown` | MCP | reconcile manually |
| `mcp_transport_unknown` | Spark/MCP | reconcile manually |
| `receipt_conflict` | Cilia | investigate; no MCP retry |
| `receipt_unavailable` | Cilia | defer receipt only |
| `high_water_regression` | Cilia | fail closed |
| `sentry_redaction_failed` | Sentry/security | drop event; alert |
| `sentry_unavailable` | Sentry | buffer/drop telemetry |
| `session_expired` | Vesper | re-authenticate |

Human-facing copy MUST not leak the existence or value of secrets. It SHOULD
say what the user can do next, not expose stack traces.

## 15. Failure modes and required behavior

| Failure mode | Detection | User-visible result | MCP retry | Cilia state | Sentry |
|---|---|---|---|---|---|
| No bind selected | local/server validation | Send disabled or “Bind an MCP tool first” | no | no send intent | `ui_send.rejected` |
| Bind expires while composer is open | dispatch-time recheck | “Binding expired; re-bind to Send” | no | no MCP receipt; optional rejection receipt if intent existed | bind stale + send rejected |
| Bind revoked after click | authoritative recheck | “Binding revoked before dispatch” | no | terminal rejected receipt | security/info |
| Tool changed after bind | schema/capability hash mismatch | “Tool changed; re-bind required” | no | rejected receipt | capability mismatch |
| Double click | idempotency store | one pending/result state | no second invocation | one receipt | duplicate suppressed |
| Browser retries after lost 202 | same send ID/key | reconcile existing state | no blind retry | existing state | duplicate suppressed |
| Adapter crashes before MCP call | attempt remains persisted | pending/retry state | safe only after recovery policy | open leg | dispatch interrupted |
| Adapter crashes after MCP call, before response | no definitive response | “Outcome unknown; reconcile” | no automatic side-effect retry | open leg | `mcp.invoke.unknown` |
| MCP returns explicit transient error | result class | retry control if safe | policy-defined | retryable receipt | completed/transient |
| MCP returns auth error | host auth | “MCP authorization failed” | no | terminal failure receipt | auth warning |
| MCP tool schema rejects args | preflight or host | “Input is not accepted by this tool” | no | terminal failure receipt | schema error |
| MCP server times out | deadline | unknown if call may have run | manual | open leg | unknown alert |
| MCP result malformed | result validator | “MCP returned invalid result” | no unless server contract says safe | terminal failure receipt | protocol error |
| Cilia receipt store down after tool success | receipt write failure | “Completed; receipt pending” | no MCP retry | open leg | receipt failed alert |
| Cilia receipt commit races | conditional write | reconcile winner | no | one terminal receipt | conflict |
| High-water would regress | monotonic check | operator-visible degraded state | no | fail closed | invariant alert |
| Keel Sentry down | sink timeout | no user impact if business path healthy | no | normal | durable telemetry drop |
| Redaction failure | sanitizer refusal | no raw diagnostic payload | no | business path per operation | security alert |
| Page reload during pending state | status fetch | reconstructed pending/result | no tool invocation | reconcile | rendered/reconciled |
| Session expires after intent persists | auth check | re-auth then reconcile | no blind retry | pending/open leg | auth event |
| Attachment upload incomplete | content ref validation | “Attachment still uploading” | no | no accepted intent | UI rejected |
| User navigates away | server continues | status available on return | policy-defined | durable state | lifecycle |
| Network partition after click | client timeout | “Checking status” | no blind retry | intent/open leg | transport unknown |
| Mail connector unavailable | not on path | no effect on UI Send | no | Cilia still works | no mail event |
| Mail connector accidentally invoked | integration guard | operation blocked and incident flagged | no | security failure receipt | policy violation |
| Wrong environment/server target | allowlist check | “Target is not allowed” | no | rejected | security alert |
| Clock skew affects expiry | server time authority | bind refresh/rebind | no | rejected if unsafe | clock skew metric |
| Receipt contains secret | schema/sanitizer | operation continues or stops per policy | no | safe redacted record only | security incident |

The implementation MUST include tests for every row marked “MUST” in the
acceptance matrix below. Operators MAY add failure modes without changing
existing error codes.

## 16. Acceptance criteria

The feature is accepted only when all P0 tests pass, no P0 security test is
waived, and each waiver has a named owner and explicit follow-up issue.

### 16.1 P0 acceptance matrix

| ID | Priority | Acceptance |
|---|---:|---|
| AT-001 | P0 | A browser test opens Vesper web, creates or selects an allowed bind, enters content, clicks visible **Send**, and observes a request with `ui_action=send`. |
| AT-002 | P0 | The test proves no mail API, Gmail draft, SMTP call, or email connector is needed for a successful send. |
| AT-003 | P0 | The selected MCP server and tool are visible before Send and match the backend bind. |
| AT-004 | P0 | An active bind is required; Send is unavailable or rejected deterministically when no bind exists. |
| AT-005 | P0 | A valid Send creates exactly one stable `send_id`, `attempt_id`, `correlation_id`, and idempotency key. |
| AT-006 | P0 | The send intent is durable before the MCP invocation begins. |
| AT-007 | P0 | The MCP host receives the exact bind ID/version, server ID, tool name, session ID, and send ID. |
| AT-008 | P0 | The host rechecks bind authorization and rejects a stale/revoked bind without invoking the tool. |
| AT-009 | P0 | A successful tool invocation produces a success result in the Vesper UI. |
| AT-010 | P0 | A successful tool invocation produces exactly one durable Cilia receipt. |
| AT-011 | P0 | A failure before dispatch produces a typed terminal receipt when an intent was accepted. |
| AT-012 | P0 | An unknown downstream outcome remains an open leg and is not rendered as safe-to-retry. |
| AT-013 | P0 | A lost browser response followed by reload reconciles by `send_id` without a second tool invocation. |
| AT-014 | P0 | A double click produces one invocation and one receipt. |
| AT-015 | P0 | Replaying the same `send_id` and payload returns existing state. |
| AT-016 | P0 | Replaying the same `send_id` with a different payload is rejected as a conflict. |
| AT-017 | P0 | Cilia receipt writing works with mail credentials and mail connectors disabled. |
| AT-018 | P0 | High-water movement is monotonic under duplicate, out-of-order, and concurrent receipt writes. |
| AT-019 | P0 | The UI distinguishes accepted, MCP-complete, receipt-written, failure, and unknown states. |
| AT-020 | P0 | Keel Sentry receives bind, UI Send, dispatch, MCP, receipt, and render lifecycle events. |
| AT-021 | P0 | Keel Sentry events contain correlation IDs but no raw prompt, token, cookie, or authorization header. |
| AT-022 | P0 | A Keel Sentry outage does not cause a second MCP invocation or lose the Cilia receipt. |
| AT-023 | P0 | A redaction failure never sends the original unsafe payload to Sentry. |
| AT-024 | P0 | The selected tool’s argument schema is validated before invocation. |
| AT-025 | P0 | The browser cannot change the target server/tool by mutating request JSON after binding. |
| AT-026 | P0 | The status/reconcile endpoint is side-effect free. |
| AT-027 | P0 | A page reload restores the active binding or clearly shows rebind required. |
| AT-028 | P0 | Revocation blocks a new Send immediately after authoritative revocation. |
| AT-029 | P0 | No implementation path labels an email draft or email delivery as UI Send success. |
| AT-030 | P0 | A production-like test uses the real rendered Send control, not only a direct API call. |

### 16.2 P1 acceptance matrix

| ID | Priority | Acceptance |
|---|---:|---|
| AT-031 | P1 | Read-only tools can use a policy-approved bind flow without unnecessary confirmation. |
| AT-032 | P1 | Side-effecting tools show side-effect classification and require explicit confirmation. |
| AT-033 | P1 | The UI exposes a support-safe correlation reference. |
| AT-034 | P1 | A retry button is shown only when the result class and tool policy allow retry. |
| AT-035 | P1 | The receipt contains content/result hashes, not full sensitive content. |
| AT-036 | P1 | An event sink outage is counted and later observable. |
| AT-037 | P1 | Concurrent bind rotation cannot silently route a send to a new tool. |
| AT-038 | P1 | Tool output validation rejects malformed success envelopes. |
| AT-039 | P1 | The adapter enforces environment and server allowlists. |
| AT-040 | P1 | Unknown outcomes can be reconciled by an operator using `send_id`. |
| AT-041 | P1 | Receipt-pending state survives process restart. |
| AT-042 | P1 | The test suite runs with deterministic fake time for bind expiry and deadlines. |
| AT-043 | P1 | Metrics distinguish duplicate suppression from ordinary failures. |
| AT-044 | P1 | The UI never exposes raw internal stack traces. |
| AT-045 | P1 | A cancelled bind cannot be reused from browser local storage. |

### 16.3 P2 acceptance matrix

| ID | Priority | Acceptance |
|---|---:|---|
| AT-046 | P2 | A preview/dry-run mode shows normalized arguments without side effects. |
| AT-047 | P2 | A future adapter can reuse the envelope without claiming it is a Vesper UI Send. |
| AT-048 | P2 | Operator dashboards show send-to-receipt latency percentiles. |
| AT-049 | P2 | Reconciliation tooling can list open legs older than the configured threshold. |
| AT-050 | P2 | The bind UI provides a clear expiry countdown or equivalent freshness signal. |

## 17. Test plan

### 17.1 Test layers

| Layer | What it proves | Required |
|---|---|---:|
| Pure unit | State transitions, redaction, hashes, error mapping. | yes |
| Contract | Envelope/schema compatibility between web, Spark, MCP, Cilia. | yes |
| Adapter integration | Bind/auth/schema/dispatch behavior with a fake MCP server. | yes |
| Cilia integration | Idempotent receipts, high-water, open legs, restart recovery. | yes |
| Sentry integration | Event names, redaction, drop behavior, metrics. | yes |
| Browser E2E | Real rendered Vesper Send control through a test MCP server. | yes |
| Failure injection | Timeouts, crash points, revoked bind, store outage, Sentry outage. | yes |
| Production smoke | One safe read-only tool in a controlled environment. | before rollout |

### 17.2 Required fake MCP server

The test harness MUST include a fake MCP server with these behaviors:

1. deterministic read-only success;
2. deterministic explicit rejection;
3. schema rejection;
4. transient failure on first call then success;
5. response delay beyond client timeout;
6. accept-and-drop-response behavior;
7. duplicate-observation counter keyed by idempotency key;
8. revocation or authorization check;
9. malformed success response;
10. side-effect counter that proves duplicate suppression.

The fake server MUST expose an invocation ledger to the test runner. The ledger
MUST record server ID, tool name, bind ID, send ID, idempotency key, call count,
and whether the test tool’s side effect occurred.

### 17.3 Browser E2E outline

```text
1. Start Vesper web in test mode.
2. Start Spark adapter with a test binding registry.
3. Start fake MCP server.
4. Disable all mail connectors and remove mail credentials.
5. Open a fresh browser context.
6. Authenticate as a test subject.
7. Bind the approved fake read-only tool.
8. Assert server/tool/capability are visible.
9. Enter a unique test payload.
10. Click the rendered Send control.
11. Assert pending state appears.
12. Assert fake MCP ledger has one invocation.
13. Assert result state appears in Vesper.
14. Assert Cilia has one receipt for the same send_id.
15. Assert high-water advanced once.
16. Assert Sentry has the expected lifecycle events.
17. Assert no mail invocation occurred.
```

### 17.4 Double-click test

The test MUST fire two clicks as close together as the browser allows. It MUST
prove:

* one semantic send;
* one MCP side effect;
* one terminal receipt;
* duplicate suppression event;
* no user-visible false failure caused by the second click.

### 17.5 Lost-response test

The fake MCP server MUST execute the side effect and then drop the response.
The browser/client MUST time out into `unknown` or a reconciliation state. A
reload or status request MUST find the existing outcome by `send_id` or
idempotency key. The test MUST prove there was no second side effect.

If the fake server does not support querying an outcome by idempotency key, the
test MUST remain `unknown` and require manual reconciliation; it MUST not
pretend the send failed safely.

### 17.6 Mail exclusion test

Run the full P0 browser test with:

* no Gmail credentials;
* no SMTP credentials;
* mail connector module unavailable or explicitly denied;
* no email route registered.

The test passes only if Vesper Send still invokes the fake MCP server and
writes the Cilia receipt. Any attempt to call mail is a failure, even if MCP
eventually succeeds.

### 17.7 Security tests

Security tests MUST include:

* tampered tool name;
* tampered bind ID;
* tampered bind version;
* replayed expired user-gesture token;
* cross-session send ID;
* cross-user binding use;
* revoked bind from stale browser tab;
* oversized input;
* malformed attachment reference;
* secret in prompt and secret in tool result;
* Sentry sanitizer failure;
* unauthorized server target;
* status endpoint attempting to cause invocation.

Each test MUST verify both user-visible behavior and absence of unauthorized
downstream invocation.

## 18. Operational runbook

### 18.1 Investigate a reported Send failure

Start with the support-safe correlation reference, then:

1. retrieve `send_id` and `correlation_id`;
2. inspect `keel.ui_send.clicked`;
3. inspect `keel.ui_send.accepted` or `rejected`;
4. inspect Spark dispatch state;
5. inspect MCP invocation state;
6. inspect Cilia receipt state;
7. inspect open-leg age;
8. determine whether the outcome is terminal or unknown;
9. never re-run a side effecting tool solely because the UI showed a timeout;
10. reconcile by `send_id`/idempotency key before authorizing retry.

### 18.2 Receipt pending

If MCP completed but the receipt is pending:

* show “Completed; receipt pending” rather than “Failed”;
* keep the open leg;
* retry the receipt writer with the same receipt ID;
* do not retry MCP;
* alert when pending age exceeds the configured threshold;
* close the leg only after durable receipt commit.

### 18.3 Unknown outcome

If the downstream result is unknown:

* preserve the open leg;
* classify as `timeout_unknown` or `transport_unknown`;
* query any server-supported outcome endpoint;
* inspect the MCP invocation ledger or downstream audit record;
* use idempotency-key lookup if supported;
* require explicit operator decision before retrying a side-effecting tool;
* write the eventual reconciliation receipt;
* retain the original attempt in the audit trail.

### 18.4 Keel Sentry outage

If Keel Sentry is unavailable:

* continue the business path if Cilia and MCP policy permit;
* buffer only redacted events;
* increment a local drop counter;
* do not retry MCP due to telemetry failure;
* surface telemetry degradation to operators;
* flush buffered events when safe;
* alert if the outage crosses the configured threshold.

### 18.5 Bind drift

If a bind’s tool schema or server capability changes:

* mark the bind stale;
* reject new Sends using the stale version;
* display rebind-required state;
* do not silently update the tool target;
* retain historical receipts against the old bind version.

## 19. Security and privacy

### 19.1 Authorization

Authorization MUST be checked at three points:

1. bind creation;
2. Send acceptance;
3. MCP dispatch.

The checks MAY share a policy engine, but the dispatch check MUST exist
independently of cached browser state.

### 19.2 Least privilege

Bindings MUST identify one tool or an explicitly enumerated small capability
set. A generic “all tools on server” bind is not allowed for this first version.

Side-effecting tools MUST declare:

* side-effect class;
* retry class;
* approval requirement;
* cancellation semantics;
* result/delivery semantics.

### 19.3 Content handling

Content SHOULD be passed by protected reference when possible. If raw content
must cross the adapter boundary, transport MUST be authenticated and
encrypted. Content MUST be excluded from ordinary Sentry events and Cilia
receipts unless a separate retention policy explicitly permits it.

### 19.4 Browser storage

Browser local storage MAY cache display state but MUST NOT be authoritative for:

* access tokens;
* bind authorization;
* tool capability;
* receipt status;
* retry safety.

Stale local state MUST be invalidated on session change, bind revocation,
expiry, or server version change.

### 19.5 Abuse controls

The server SHOULD enforce:

* per-session send rate limits;
* per-subject bind creation limits;
* content size limits;
* attachment count/size limits;
* downstream deadline limits;
* duplicate/replay detection;
* audit retention for security events.

Rate limiting MUST not be implemented as a hidden mail queue.

## 20. Compatibility and migration

### 20.1 Existing Cilia records

Older receipt records without bind fields remain readable. New records MUST
use a namespaced action such as `vesper.web.send`. Do not reinterpret an old
email receipt as a web-send receipt.

### 20.2 Existing email bus

The email bus remains a separate coordination surface:

```text
email wake → Cilia/email workflow
Vesper UI Send → Spark/MCP workflow
```

The two surfaces MAY share correlation conventions, but they MUST have
different action names and receipt types. A mail wake may request work; it does
not impersonate a user clicking Send.

### 20.3 Existing MCP surface

The implementation should live under the current MCP surface and Cilia
modules. It MUST NOT create another top-level skill merely to house this
adapter. If a new package is needed, record it as a module or integration
under the existing architecture and update the relevant registry.

### 20.4 Rollout modes

| Mode | Behavior |
|---|---|
| `observe` | Render bind and collect telemetry; no external MCP side effect. |
| `dry_run` | Validate and show normalized dispatch; no invocation. |
| `shadow` | Send to a non-side-effect fake/test MCP server only. |
| `canary` | One approved read-only production-like tool and allowlisted users. |
| `active` | Normal conformant behavior. |
| `kill_switch` | Disable new Sends; allow reconciliation and receipt drain. |

The kill switch MUST fail closed for new side-effecting dispatches and MUST
remain usable for status/reconciliation.

## 21. Implementation checklist

### 21.1 Contract

- [ ] Define versioned bind, send-intent, dispatch, result, and receipt schemas.
- [ ] Define stable error codes and retry classes.
- [ ] Define side-effect and tool capability registry fields.
- [ ] Define authoritative server/tool allowlist.
- [ ] Define expiry and revocation semantics.

### 21.2 Vesper web

- [ ] Render active bind identity before Send.
- [ ] Use visible **Send** label.
- [ ] Disable Send when unbound or stale.
- [ ] Create stable IDs before request.
- [ ] Prevent duplicate same-send clicks.
- [ ] Render accepted/pending/unknown/receipt-pending states.
- [ ] Reconcile on reload.
- [ ] Never route to mail.

### 21.3 Spark adapter

- [ ] Persist intent before dispatch.
- [ ] Re-authorize bind at dispatch.
- [ ] Validate tool schema.
- [ ] Forward exact target identity and IDs.
- [ ] Attach idempotency key.
- [ ] Classify results.
- [ ] Avoid unsafe retry.
- [ ] Map all terminal/unknown states.

### 21.4 Cilia

- [ ] Add web-send action namespace.
- [ ] Add bind-aware receipt fields.
- [ ] Make receipt commit idempotent.
- [ ] Preserve open legs for unknown/pending outcomes.
- [ ] Add namespaced high-water cursor if needed.
- [ ] Prove operation without mail connectors.

### 21.5 Keel Sentry

- [ ] Implement all P0 lifecycle hooks.
- [ ] Implement redaction before emission.
- [ ] Add event-drop counter/buffer.
- [ ] Add required metrics.
- [ ] Add alerts for unknown outcomes, receipt lag, auth failures, and redaction failures.
- [ ] Add correlation lookup/runbook.

### 21.6 QA and operations

- [ ] Build fake MCP server and invocation ledger.
- [ ] Add browser E2E using rendered Send.
- [ ] Add duplicate, crash, timeout, revocation, and reload tests.
- [ ] Add mail exclusion test.
- [ ] Add security tampering tests.
- [ ] Run staging smoke with a read-only tool.
- [ ] Record test evidence with send IDs and receipt IDs.

## 22. Definition of done

SPEC-003 is implemented when:

1. a human can bind an approved MCP tool in Vesper web;
2. the human can click visible **Send**;
3. the selected MCP tool is invoked through Spark;
4. the tool result is shown in the same Vesper session;
5. the exact send has a durable Cilia receipt;
6. a reload/retry cannot duplicate the side effect;
7. unknown outcomes are not falsely labeled failed or successful;
8. the full lifecycle is visible in Keel Sentry without secrets;
9. the path works with mail disabled;
10. all P0 acceptance tests pass;
11. the architecture remains within existing MCP/Cilia surfaces;
12. rollback and reconciliation are documented and exercised.

## 23. Evidence requirements for review

The implementation PR MUST attach or link:

* a browser test recording or screenshot showing the visible **Send** action;
* the sanitized send-intent fixture;
* fake MCP invocation ledger for a success;
* fake MCP invocation ledger for duplicate suppression;
* Cilia receipt fixture for success;
* Cilia receipt fixture for unknown outcome/open leg;
* Sentry event fixture with redaction proof;
* mail-disabled test output;
* bind revocation test output;
* high-water monotonicity test output;
* a short operator reconciliation example.

Evidence MUST use synthetic content and test identities. Do not attach
production prompts, tokens, cookies, email contents, or private MCP results.

## 24. Open decisions

These decisions are intentionally left for the implementation owner, but each
must be resolved before active rollout:

1. Which authoritative Vesper session store owns `send_id` persistence?
2. Which exact MCP host API carries idempotency metadata?
3. Does the selected MCP server support outcome lookup after timeout?
4. What is the maximum bind TTL for read-only and side-effecting tools?
5. Which Cilia durable store is authoritative for web-send receipts?
6. Is receipt storage local-first with later promotion, or directly remote?
7. What is the Keel Sentry event retention period?
8. Which display-safe server/tool identifiers may be exposed to users?
9. Which side-effect classes require per-send confirmation?
10. What is the operator escalation threshold for unknown outcomes?
11. Which test runner provides the real browser E2E environment?
12. What is the kill-switch ownership and audit path?

An unresolved decision MUST NOT be hidden behind a default that changes the
meaning of UI Send.

## 25. Explicit anti-requirements

The following are prohibited as “completion”:

* sending an email and calling that a Vesper Send;
* creating a Gmail draft and calling that a successful bind;
* invoking an MCP tool directly from a unit test and skipping the browser;
* using a fake Send button that does not create a trusted UI intent;
* silently switching from the selected MCP tool to another tool;
* retrying an unknown side effect without reconciliation;
* writing a receipt only after a best-effort, non-idempotent action;
* using a Sentry event as the durable Cilia receipt;
* logging raw prompts or credentials for debugging;
* relying on browser local storage as authorization;
* advancing high-water backward;
* closing an unknown open leg merely because the HTTP request timed out;
* introducing a new top-level skill for this integration;
* hiding bind identity, expiry, or side-effect classification from the user;
* claiming “real UI Send” when only an API endpoint was tested.

## 26. Short conformance statement

An implementation may claim:

> “Cilia Spark Bind conformant”

only if it demonstrates a real Vesper web Send to an authorized MCP bind,
durable idempotent Cilia receipt behavior, safe unknown-outcome handling,
mail-independent operation, and redacted Keel Sentry lifecycle evidence as
defined by all P0 acceptance tests.

