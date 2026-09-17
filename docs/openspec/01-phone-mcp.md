# OpenSpec: Phone Ingress and MCP Boundary

**Status:** Draft component specification
**Version:** 0.1.0
**Depends on:** [00-overview.md](./00-overview.md)

## Purpose

Define the trust boundary between a phone interaction and the normalized MCP
surface. The phone adapter is a narrow translation layer: it authenticates
provider callbacks, tracks a session, captures consent and retention decisions,
normalizes utterances and control events, and renders approved responses back to
the phone channel.

The adapter must not become an agent, a memory curator, or a general-purpose
MCP proxy. Keeping those concerns separate is what makes the phone path
replaceable and testable.

The first implementation should use a provider-neutral contract. Provider
specific webhook names, signature algorithms, media URLs, and codec details
belong in an adapter module and must not leak into the agent-facing interface.

## Actors

| Actor | Role at this boundary | Trust level |
|---|---|---|
| Human caller | Supplies speech, consent, confirmations, and cancellation | Human authority |
| Telephony provider | Delivers signed callbacks/audio/transcripts and accepts rendered responses | External dependency |
| Phone adapter | Verifies callbacks, creates envelopes, and emits responses | Trusted translator, not policy owner |
| Session coordinator | Correlates events, manages turn and timeout state | Trusted control-plane service |
| MCP gateway | Authorizes normalized tool requests and applies side-effect policy | Policy enforcement point |
| Primary agent | Interprets the request and proposes or performs allowed tool calls | Constrained executor |
| Escalation router | Sends bounded work to Spark/Vesper when policy allows | Constrained dispatcher |
| Receipt store | Persists transcript/event/side-effect evidence | Durable evidence store |
| Operator | Can approve, cancel, or override configured actions | Final authority |

## Interfaces

### Provider adapter boundary

The provider adapter accepts external requests and returns a provider response:

```text
HTTP(S) callback + provider signature
  -> verify_callback(request) -> ProviderEvent | RejectedCallback
ProviderEvent + ResponsePlan
  -> render_response(plan) -> provider response
```

The adapter must:

- verify a signature, timestamp, nonce, or equivalent replay protection before
  reading sensitive payload content;
- reject unknown event types explicitly;
- preserve the provider event ID in opaque metadata;
- avoid logging raw authorization headers, media URLs, or full audio;
- handle duplicate callbacks idempotently;
- expose provider health separately from agent health.

The provider-facing endpoint must return a deterministic acknowledgment quickly.
Long-running work is asynchronous. The endpoint must not wait for Letta, Spark,
Drive, or an LLM completion.

### Session API

Proposed internal operations:

```text
session.open(provider_event, consent_input) -> SessionOpened
session.ingest(session_id, provider_event) -> EventAccepted
session.cancel(session_id, reason) -> SessionCancelled
session.close(session_id, close_reason) -> SessionClosed
session.status(session_id) -> SessionStatus
```

`SessionOpened` contains `session_id`, `trace_id`, `consent_state`,
`retention_class`, `capabilities`, and an expiration time. A session does not
grant permission to call every MCP tool.

### Canonical phone events

The adapter emits the envelope defined in the overview. Phone-specific payload
kinds are:

| Kind | Required payload | Side effect |
|---|---|---|
| `session_started` | provider call ref, channel, locale, consent state | Creates session state |
| `utterance` | text or content ref, sequence number, confidence if available | No external mutation |
| `confirmation` | target action ref, `yes/no/cancel/unclear`, source event | May authorize a pending action |
| `interrupt` | reason and sequence number | Cancels or pauses the current response |
| `media_available` | opaque media ref, MIME type, retention class | Makes media eligible for policy-controlled retrieval |
| `session_ended` | provider reason, final sequence number | Closes session and schedules receipt |

Every event has a monotonic per-session sequence number. The adapter rejects
conflicting reuse of a sequence number and treats an exact duplicate as an
idempotent replay.

### MCP call boundary

The adapter or session coordinator may call only normalized tools exposed by the
gateway. Each call includes:

```json
{
  "tool": "memory.recall",
  "arguments": {
    "query": "operator-approved query",
    "scope": "session"
  },
  "context": {
    "session_id": "ses-...",
    "trace_id": "trace-...",
    "caller": "phone-session-coordinator",
    "idempotency_key": "idem-...",
    "consent": "granted",
    "side_effect_class": "read"
  }
}
```

The gateway returns a typed result or typed rejection:

```json
{
  "ok": false,
  "error": {
    "code": "CONFIRMATION_REQUIRED",
    "retryable": false,
    "message": "Operator confirmation is required for this action."
  },
  "trace_id": "trace-...",
  "receipt_ref": null
}
```

No model-generated tool name is passed directly to an underlying server.
Unknown tools, unknown arguments, missing context, stale idempotency keys, and
scope violations are rejected before dispatch.

### Response API

The agent returns a `ResponsePlan`, not raw provider markup:

```json
{
  "session_id": "ses-...",
  "trace_id": "trace-...",
  "mode": "speak | ask_confirmation | wait | escalate | close",
  "text": "Short spoken response.",
  "pending_action": null,
  "next_deadline": "2026-09-17T04:00:00Z",
  "safety": {
    "redactions_applied": true,
    "requires_operator_confirmation": false
  }
}
```

The renderer applies channel constraints such as maximum utterance length,
interruptibility, SSML or codec rules, and fallback text. It must not change
the semantic action or turn an unanswered confirmation into approval.

### Authentication and secret handling

- Provider secrets live in the adapter's secret store or runtime environment,
  never in a transcript, prompt, Letta memory block, or queue message.
- MCP credentials are held by the gateway or a short-lived sidecar. The phone
  process receives capability-scoped handles, not bearer tokens.
- Internal calls use service identity plus `trace_id`; user identity and service
  identity are recorded separately.
- Logs use opaque references and structured redaction.
- Secret rotation must allow overlap so an in-flight callback can complete
  without disabling the new credential.

## Data flows

### Inbound call

```text
provider callback
  -> signature/replay verification
  -> provider event deduplication
  -> session correlation
  -> consent + retention decision
  -> canonical event
  -> coordinator queue
  -> gateway validation
  -> agent / memory / tool
```

The provider acknowledgment is returned after verification and enqueueing, not
after agent processing. This prevents provider retries from being mistaken for
new user turns.

### Transcript and media

Raw audio is never copied into Core. If retained, it is stored under a
policy-controlled media reference with encryption and an expiry. A transcript
may be kept in session scope, promoted to Recall, or summarized into Archival
only when its retention class permits. Every derived transcript or summary links
to its source event and hash.

If transcription is provider-side, the provider confidence and final/partial
state are retained. Partial utterances may drive interruption handling but may
not trigger irreversible tools without a final event and required confirmation.

### Confirmation-gated action

1. Agent proposes an action with `pending_action_id`.
2. Session coordinator renders a concise confirmation request.
3. Caller responds with a normalized confirmation event.
4. Coordinator checks that the confirmation is recent, targets the exact pending
   action, and is not ambiguous.
5. Gateway rechecks authorization and dispatches with a one-time idempotency key.
6. Result and confirmation receipt are written before the spoken completion claim.

“Yes” to a broad question must not authorize a different or newly modified
action.

### Escalation request

The phone path emits a bounded request containing:

- the reason and requested capability;
- urgency and deadline;
- a minimal context summary;
- references to durable source material;
- whether caller approval is present;
- allowed output shape;
- cancellation and timeout policy.

The request is durable before Spark is woken. If the phone call ends, the work
may continue only if the retention and authorization policy explicitly permits
it; otherwise the request is cancelled or returned as pending operator work.

### Failure and recovery

| Failure | Adapter behavior |
|---|---|
| Invalid signature | Reject; record security event without payload |
| Duplicate callback | Return the original acknowledgment/result |
| Missing consent | Keep in session-only mode or ask; do not archive |
| Provider timeout | Queue once, then use a bounded retry policy |
| Gateway unavailable | Speak a short retry/fallback message and stage an event |
| Tool timeout | Return “not completed”; preserve retryable receipt |
| Ambiguous confirmation | Ask again; do not execute |
| Session disconnect | Close or pause according to policy; preserve trace |
| Audio/transcript failure | Ask caller to repeat; never invent transcript text |

## Non-goals

- Building a telephony provider integration in this specification.
- Performing transcription, sentiment analysis, or identity verification as an
  implicit side effect.
- Using caller voiceprint as authentication unless a separate, reviewed
  biometric design exists.
- Allowing raw MCP access from a phone client.
- Treating “caller stayed on the line” as consent for data retention or action.
- Performing money movement, account changes, deletion, publication, or external
  communication without the appropriate confirmation class.
- Storing secrets in prompts, Letta memory, TQS messages, or Drive artifacts.
- Guaranteeing real-time response latency while an escalation is running.

## Acceptance criteria

### Contract

1. A fake provider event can be converted into a valid canonical envelope with
   stable `event_id`, `session_id`, `trace_id`, sequence number, and provenance.
2. The provider callback receives a fast deterministic acknowledgment before
   downstream work completes.
3. The same callback delivered twice produces one logical event and one side
   effect.
4. An invalid signature is rejected without exposing payload contents in logs.
5. Unknown event types, malformed schemas, and conflicting sequence numbers are
   explicit failures.

### Consent and safety

6. A session without consent cannot promote raw content to Recall or Archival.
7. A pending action cannot execute on `unclear`, stale, or mismatched
   confirmation.
8. Provider credentials never appear in generated envelopes, prompts, memories,
   receipts, or ordinary logs.
9. Partial transcripts cannot independently authorize an irreversible action.

### MCP behavior

10. The adapter calls only allowlisted normalized tools.
11. Every tool request carries caller, session, trace, side-effect class, and
    idempotency key.
12. The adapter can render a typed gateway error into a safe spoken response.
13. A gateway outage leaves an inspectable staged event and does not claim tool
    success.

### Recovery

14. A disconnect preserves enough state to resume or close a session without
    replaying completed side effects.
15. A phone-to-Spark escalation is durable before any wake signal is sent.
16. The close receipt names all child events and the final disposition.

## Open questions

1. Which provider callback signature and replay window will be required?
2. Where does transcription happen, and are partial transcripts available?
3. What is the approved operator authentication mechanism for inbound calls?
4. Which confirmation phrases are acceptable in the selected language/locale?
5. How should barge-in interact with a tool call already in flight?
6. Is provider media retained at all, and who may retrieve it?
7. What spoken fallback should be used when a request is queued for Spark?
8. What hard limits apply to turn length, silence, session duration, and retries?
9. Is an explicit “end retention” command required during a call?
10. Which tool classes may run without a spoken confirmation?
11. How does the adapter notify a caller that an async result is ready after the
    original session has ended?
12. Do local and remote phone adapters need identical codec and transcript
    fixtures for conformance testing?
