# OpenSpec: Sovereign Phone-to-Agent Bridge

**Status:** Draft architecture specification
**Version:** 0.1.0
**Scope:** Phone ingress, MCP normalization, Vultr/Letta memory, and Gemini Spark escalation
**Repository:** `sovereign-skills-archive`

## Purpose

This pack specifies a local-first, auditable path from a person using a phone to the
sovereign skill surface:

```text
phone session
    -> phone adapter
    -> canonical event/envelope
    -> MCP proxy + gateway
    -> Vultr edge services
    -> Letta memory and tools
    -> primary response or Spark escalation
    -> receipt, transcript, and next action
```

The design joins the repository's existing bridge decisions:

- MCP transports must be normalized across Grok/xAI SSE or Streamable HTTP and
  Gemini/Vesper local stdio.
- A compact gateway surface should prevent tool-registration and context bloat.
- Thin Queue Sync (TQS) provides durable handoff state between heterogeneous
  LLMs.
- Gmail may wake a worker, but Drive or another durable store carries the payload
  and receipt. Email is not the source of truth.
- Letta's Core, Recall, and Archival tiers are memory disciplines, not competing
  personas.
- Every substantive hop has provenance, source identifiers, content hashes where
  practical, and an inspectable receipt.

This is an implementation contract for a staged system. It does not claim that the
phone provider, production MCP gateway, inference provider, or escalation
automation already exists. Any interface marked **proposed** must be validated in
the acceptance suite before being called live.

## Actors

| Actor | Responsibility | Authority boundary |
|---|---|---|
| Human operator | Starts a call, gives consent, approves consequential actions, and remains final authority | Can stop a session and reject any proposed action |
| Phone adapter | Converts telephony-provider events and audio/transcript callbacks into canonical events | Must not decide agent actions or expose provider secrets |
| MCP proxy | Bridges local stdio servers to SSE/Streamable HTTP, and can reverse that direction | Owns transport adaptation, not business policy |
| MCP gateway | Presents a small, authenticated, rate-limited tool surface | May reject, scope, or route calls; must not silently mutate payloads |
| Vultr edge | Runs the reachable broker and, where selected, the Letta server or inference endpoint | Network boundary; not automatically a trusted memory writer |
| Letta server | Stores and retrieves Core, Recall, and Archival memory; executes configured agent operations | Core identity blocks require explicit policy; archival promotion is traceable |
| Primary agent | Answers the operator and uses allowed tools | Cannot bypass confirmation or retention policy |
| Gemini Spark / Vesper | Performs a defined escalation or complementary search task | Receives only the minimum routed context and returns a receipt |
| Olivia/Grok surface | Primary or peer surface for normalized skills and local archive work | Uses the same envelope and handoff vocabulary |
| Durable store | Drive, local disk, or equivalent store for transcripts, payloads, artifacts, and receipts | Must preserve immutable or append-preferred evidence |
| Gmail wake path | Optional delayed trigger for a queued work item | Wake signal only; never the payload or completion proof |
| Operator/ops maintainer | Rotates secrets, inspects health, and changes routing policy | Separate from ordinary conversational authority where possible |

## Interfaces

### Canonical event envelope

All boundaries use a versioned JSON envelope. Implementations may add fields, but
must not remove required fields without a version bump.

```json
{
  "schema": "sovereign.phone.event",
  "schema_version": "0.1.0",
  "event_id": "evt-20260917-000001",
  "session_id": "ses-...",
  "trace_id": "trace-...",
  "occurred_at": "2026-09-17T03:57:00Z",
  "source": {
    "kind": "phone",
    "provider": "provider-defined",
    "channel": "voice",
    "account_ref": "opaque-ref"
  },
  "actor": {
    "kind": "human",
    "consent": "granted | denied | unknown"
  },
  "payload": {
    "kind": "utterance | control | tool_result | escalation",
    "text": "redacted or transcript text",
    "content_ref": null
  },
  "policy": {
    "retention_class": "session | receipt | archive",
    "requires_confirmation": true
  },
  "provenance": {
    "parent_event_ids": [],
    "content_sha256": null
  }
}
```

Required correlation fields are `event_id`, `session_id`, and `trace_id`.
Provider call IDs, message IDs, and tool-call IDs are retained under an opaque
provider metadata field, never used as the only internal identifier.

### Normalized MCP interface

The public gateway should expose domain operations rather than every underlying
server method. The initial target is approximately 14–16 tools, grouped into:

1. `session.read` / `session.write`
2. `memory.recall` / `memory.archive` / `memory.promote`
3. `artifact.read` / `artifact.write` / `receipt.write`
4. `queue.post` / `queue.read` / `queue.ack`
5. `escalation.request` / `escalation.result`
6. `health.check` / `capabilities.describe`

Exact names are provisional. Tool schemas must be generated or checked for both
OpenAI-style JSON parameters and Gemini Function Declarations. A tool call must
carry `trace_id`, an idempotency key, the caller identity, and its requested
side-effect class.

### Handoff and queue interface

TQS uses one shared queue, dated message files, and optional owner surface files.
The legal statuses are:

`DRAFT`, `POSTED`, `ACKNOWLEDGED`, `READY_FOR_NEXT`, `AWAITING_OLIVIA`,
`AWAITING_VESPER`, and `CLOSED`.

`current_handoff` is the authoritative answer to “who is waiting on whom.” New
records are preferred over rewriting history. Ownership is per side: a worker may
write its own message, surface, and artifacts, not the peer's.

### Memory interface

The Letta-facing adapter must make tiers explicit:

- **Core:** small, always-in-context identity and active working state.
- **Recall:** searchable conversation history.
- **Archival:** long-term semantic storage and durable facts.

The adapter must return a memory tier, record ID, source reference, and mutation
receipt for every write. A curator may propose a Core rewrite, but promotion into
Core requires the configured policy and, for identity or sensitive facts, human
approval.

### Durable artifact and receipt interface

An artifact write produces:

```json
{
  "receipt_id": "rcpt-...",
  "trace_id": "trace-...",
  "artifact_ref": "drive-or-local-ref",
  "content_sha256": "...",
  "written_by": "phone-adapter | letta | spark | olivia",
  "written_at": "ISO8601",
  "parent_refs": [],
  "status": "STAGED | PUBLISHED | VERIFIED | REJECTED"
}
```

The receipt is the completion proof. A UI identifier, email delivery, or model
claim alone is not a receipt.

## Data flows

### A. Normal phone request

1. The adapter authenticates the provider callback and creates a session.
2. Consent and retention policy are recorded before sensitive transcript handling.
3. Audio or provider transcript becomes an event envelope.
4. The gateway validates the envelope, checks authorization and idempotency, and
   routes only the allowed normalized tools.
5. The primary agent reads the smallest useful Core context and searches Recall
   or Archival only when needed.
6. Tool results and decisions inherit `trace_id` and parent references.
7. The response is rendered to the phone channel.
8. A transcript summary, event log, and receipt are written according to policy.

### B. Escalation

1. The primary agent emits an `escalation.request` with reason, urgency,
   requested capability, deadline, and a redacted context reference.
2. The router decides whether Spark is eligible, whether the operator must
   approve, and whether the request is immediate or queued.
3. The payload is stored durably before an optional Gmail wake.
4. Spark reads the payload from the durable store, performs the bounded task, and
   posts a result plus receipt under its own ownership.
5. The router verifies the result, updates the queue, and either resumes the
   phone session or asks the operator for a decision.
6. Failure, timeout, or malformed output becomes an explicit failed state; it
   does not become a false ACK.

### C. Memory promotion

1. Conversation material is kept in session scope unless policy says otherwise.
2. A candidate fact is classified as Recall or Archival with provenance.
3. A curator may summarize or deduplicate it without replacing Core.
4. Promotion to Core is a separate, auditable mutation.
5. A later retrieval can show the source event and the promotion receipt.

### D. Offline or mobile degradation

When live sockets or the web UI are unavailable, a queue item can be staged
locally and later published. Gmail may wake a worker, but the worker must retrieve
the durable payload and write a Drive/local receipt. No component should claim
completion solely because a wake message was sent.

## Non-goals

- Selecting a phone vendor, carrier, voice model, or inference provider.
- Treating a phone transcript as automatically authoritative memory.
- Making Gmail a bidirectional real-time bus or storing the only copy of a payload
  in an email body.
- Deploying a production gateway, Letta server, or public endpoint as part of this
  documentation change.
- Replacing the existing skill tree with a new top-level runtime.
- Letting three “slots” become three autonomous personalities; the Letta mapping is
  about memory tiers.
- Automatic unattended external communication or consequential action.
- Bulk hydration of the archive into Letta.
- Erasing or rewriting historical receipts to make a test pass.

## Acceptance criteria

The pack is accepted when:

1. A reviewer can trace a request from phone event through MCP, memory/tool use,
   optional Spark escalation, and response using one `trace_id`.
2. All interfaces name an owner, input contract, output contract, side effects,
   and failure behavior.
3. The same normalized tool description can be rendered as OpenAI-style JSON and
   Gemini Function Declarations without semantic drift.
4. A queued handoff has one authoritative status and an inspectable durable
   receipt.
5. The system preserves the distinction between Letta Core, Recall, and Archival.
6. A failed or timed-out escalation is visible and recoverable, never reported as
   success.
7. Consent, secret isolation, idempotency, redaction, and retention behavior are
   testable.
8. The detailed cases in `04-acceptance-tests.md` pass against a fake provider and
   fake durable store without requiring production credentials.
9. Every remaining provider or deployment decision is listed in Open Questions
   rather than hidden as an implementation assumption.

## Open questions

1. Which phone provider and callback/signature scheme will be the first adapter?
2. Is the first phone interaction voice-only, or does it include SMS control
   messages and media?
3. Which service terminates TLS and authenticates the public MCP endpoint?
4. Does Vultr host the Letta server, only the edge broker, or both in separate
   network zones?
5. Which model supplies inference for the Letta server, and where are its keys
   stored?
6. What is the canonical durable store for production receipts: Drive, an object
   store, local disk replicated later, or a combination?
7. What exact escalation classes require human confirmation before Spark runs?
8. What retention and deletion policy applies to raw audio, transcript text,
   summaries, and embeddings?
9. Which gateway implementation is selected, and how will the 14–16 tool target
   be measured for latency and context reduction?
10. Which agent owns a session when both Olivia/Grok and Spark are available?
11. Are the existing TQS status values sufficient for timeout, retry, and
   cancellation, or is a versioned extension needed?
12. What constitutes a “verified” receipt when a remote store is temporarily
   unavailable?
13. Which embeddings are approved for Archival: Spark-safe fastembed ONNX,
   provider API embeddings, or a later local MRL model?
14. What is the operator experience for approving a Core-memory promotion while
   on a phone call?
15. Which observability backend receives health, latency, tool-call, and
   redaction audit events?

## Source reconciliation

This pack consolidates the available repository material under the hydrated
`skill_tree/` mirror, especially:

- `system-roadmap/references/third-party-skills-eval-2026-08-17/`
- `system-roadmap/references/multi-llm-sync/`
- `system-roadmap/references/email-bridge-2026-08-17/`
- `system-roadmap/references/plans/VESPER_PKG_PROXY_INVENTORY_2026-08-26.md`
- `system-roadmap/references/python-libs-for-circular-system-2026-08-16/`
- `system-roadmap/references/research/icm-harness-recon-2026-09-10/`
- `system-roadmap/references/skills/vesper-alignment/`

The checkout did not contain top-level `bridges/` or `docs/` directories at
authoring time. No claims above depend on an unverified file in those paths.
When those trees are restored, their contracts should be reconciled against this
pack before version 0.2.0.
