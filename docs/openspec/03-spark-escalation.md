# OpenSpec: Gemini Spark Escalation

**Status:** Draft escalation and handoff specification
**Version:** 0.1.0
**Depends on:** [00-overview.md](./00-overview.md), [02-vultr-letta.md](./02-vultr-letta.md)

## Purpose

Define when and how the primary phone/Olivia surface delegates bounded work to
Gemini Spark, also called Vesper in the repository's bridge material. Spark is a
peer worker and complementary surface, not an unbounded fallback personality.
The escalation path exists for capability, availability, or routing reasons
that are explicit in the request.

The design makes the durable handoff more important than the wake mechanism:

```text
primary surface
  -> durable escalation payload
  -> queue record / current_handoff
  -> optional Gmail wake
  -> Spark reads durable payload
  -> bounded result + receipt
  -> primary surface resumes or asks human
```

This preserves the Thin Queue Sync rules: one shared queue, dated messages,
owner-prefixed artifacts, legal statuses, append preference, and a single
authoritative `current_handoff`. It also preserves the email-bridge rule that
email is wake only and Drive/local durable storage carries the payload.

## Actors

| Actor | Escalation role | May do |
|---|---|---|
| Primary surface | Detects need and submits bounded work | Create request, provide minimum context, cancel before execution |
| Human operator | Approves policy-gated work and resolves ambiguity | Approve, reject, reprioritize, or close |
| Escalation router | Validates eligibility, routes, retries, and reconciles result | Set queue state, wake Spark, enforce timeout |
| Spark/Vesper worker | Executes the declared task | Read referenced payload, use allowed tools, publish own result |
| Gmail wake path | Notifies Spark or a monitor of new work | Deliver a wake signal only |
| Drive/local store | Holds request, artifacts, and receipts | Preserve payload and evidence |
| Letta adapter | Supplies bounded memory context where authorized | Read/write according to tier policy |
| Olivia/Grok peer | Consumes Spark result or returns a follow-up | Verify receipt and resume work |
| Maintainer | Owns credentials, automation, and health | Change routing policy and investigate failures |

## Interfaces

### Escalation request

```yaml
schema: sovereign.escalation.request
schema_version: "0.1.0"
request_id: esc-20260917-000001
trace_id: trace-...
created_at: "2026-09-17T03:57:00Z"
requester: olivia | phone | system
target: spark
reason: capability | latency | complementary-search | outage | human-request
priority: routine | urgent | blocking
deadline: "2026-09-17T04:05:00Z"
approval:
  state: not_required | pending | approved | rejected
  approval_ref: null
payload_ref: durable://...
context_refs:
  - durable://...
allowed_tools:
  - memory.recall
  - artifact.read
  - artifact.write
expected_output:
  kind: answer | structured-report | artifact | decision-options
  schema_ref: ...
retention_class: session | receipt | archive
cancellation:
  allowed_until: "2026-09-17T04:00:00Z"
```

The durable payload may contain sensitive context, but the queue record should
contain only a minimal summary and references. The payload is written before the
wake signal.

### Queue and handoff

The queue record uses the TQS closed status vocabulary:

```json
{
  "id": "msg-20260917-035700-olivia",
  "sender": "olivia",
  "timestamp": "2026-09-17T03:57:00Z",
  "status": "AWAITING_VESPER",
  "in_reply_to": null,
  "payload_type": "artifact_ref",
  "summary": "Bounded research escalation for Spark",
  "file_ref": "2026-09-17_035700_olivia.md",
  "artifact_refs": ["esc-20260917-000001.json"]
}
```

The router sets `current_handoff` to `AWAITING_VESPER` only after the payload
and queue record are durable. Spark may set `ACKNOWLEDGED`, then
`READY_FOR_NEXT`, `AWAITING_OLIVIA`, or `CLOSED` through its own message and
surface. It must not edit Olivia's message in place.

Timeout and retry state may be represented by a new status record or a
versioned extension after review; inventing free-text statuses is prohibited.

### Spark result

```yaml
schema: sovereign.escalation.result
schema_version: "0.1.0"
request_id: esc-...
trace_id: trace-...
worker: spark
started_at: "2026-09-17T03:58:00Z"
finished_at: "2026-09-17T03:59:30Z"
disposition: completed | needs-human | rejected | timed-out | failed | cancelled
summary: "Short result summary"
output_ref: durable://...
source_refs:
  - durable://...
limitations:
  - "Could not verify external source"
next_expected: olivia | operator | none
receipt_ref: rcpt-...
```

Spark must distinguish a useful partial result from a completed result. A
receipt proves what was written and verified, not that the answer is correct.

### Wake interface

The wake channel is pluggable. The current documented email-first policy is:

- permitted subject patterns are versioned and not invented per request;
- Gmail wake contains a short pointer, request ID, and durable payload reference;
- email body is not the canonical payload;
- an ACK is not ACKed;
- sending policy is explicit, with unattended external mail disabled by default;
- a Drive/local receipt is required regardless of email delivery.

The first implementation may use a manual or draft-only wake while send
permissions are unresolved. That is a valid staged state, not a successful
automated handoff.

### Normalized tool scope

Spark receives a task-specific capability set. The default read-oriented scope
may include:

- `artifact.read`
- `memory.recall`
- `queue.read`
- `capabilities.describe`

Writes require an explicit task allowance:

- `artifact.write` writes only Spark-owned artifacts;
- `receipt.write` writes the result receipt;
- `queue.ack` updates the shared handoff signal under protocol rules;
- `memory.archival.insert` is allowed only when the request permits it.

Core-memory mutation, external communication, deletion, publication, or
consequential actions are not inherited from “escalation” and require separate
approval.

### Routing decision

The router evaluates:

```text
eligible =
  target_available
  AND request_schema_valid
  AND payload_durable
  AND tool_scope_nonempty
  AND deadline_not_expired
  AND approval_satisfied
  AND no_duplicate_request
```

It records the decision and reason. “Spark is a better model” is not sufficient
without a declared capability or policy reason.

## Data flows

### Primary-to-Spark escalation

1. The primary surface identifies a bounded gap.
2. It writes a request payload to the durable store.
3. It calculates or records a content hash and parent refs.
4. It appends a queue record and sets `current_handoff`.
5. If allowed, it sends a wake signal.
6. Spark reads the durable request, validates request ID, expiry, and scope.
7. Spark acknowledges only after successful read/validation.
8. Spark executes within the allowed tool and retention scope.
9. Spark writes output and receipt under its ownership.
10. Spark publishes a result message and handoff state.
11. The router/primary verifies the receipt and resumes, asks the operator, or
    records a bounded failure.

### Human-gated escalation

For a request that may communicate externally, mutate Core, delete data, publish
an artifact, or take another consequential action:

1. Router writes `approval: pending`.
2. Phone or UI asks the operator for an exact action approval.
3. Approval binds to `request_id`, output scope, expiration, and actor.
4. The router rechecks the binding immediately before dispatch.
5. Rejection or expiry closes the request without invoking Spark.

An approval to research or summarize does not authorize publication or external
messaging.

### Search and provenance

Spark should search the designated strong surfaces first, then open a targeted
MCP request if the source is missing. Search terms and source IDs are preserved.
No invented source IDs or circular scout scores are allowed. If a source is an
empty stub, the worker records it as a stub/work item rather than silently
discarding it.

Results identify:

- which surfaces were searched;
- source IDs and timestamps;
- whether the result was direct, inferred, or unresolved;
- any score or confidence only when a real scoring method produced it;
- content hashes or durable references.

### Mobile/offline path

When the phone or primary web UI drops:

- the request can remain staged with a clear `AWAITING_*` state;
- Spark must not infer that a disconnected caller approved continuation;
- the operator can inspect the request later through the durable artifact;
- retry uses the same `request_id` and a new attempt ID;
- a completed result can be picked up on the next primary session.

### Failure and recovery matrix

| Failure | Required behavior |
|---|---|
| Spark unavailable | Keep durable request, set waiting state, do not claim escalation ran |
| Wake delivery fails | Request remains discoverable; retry boundedly or require operator |
| Payload missing | Spark rejects with `PAYLOAD_NOT_FOUND`; no invented context |
| Duplicate wake | Same request/attempt is idempotent |
| Deadline expires | Mark expired/needs-human using an approved status extension |
| Tool scope mismatch | Reject before tool call |
| Partial output | Publish as partial with limitations, not completed |
| Receipt write fails | Do not report completion; preserve local staging |
| Spark writes peer-owned file | Reject/audit and isolate the artifact |
| Result contradicts source | Return to primary with conflict and source refs |
| Human rejects | Cancel and retain rejection receipt |

## Non-goals

- Keeping a continuous, unattended Spark conversation alive.
- Making Gmail a full message bus, payload database, or completion oracle.
- Treating Spark as a replacement for the primary agent or human operator.
- Giving Spark unrestricted access to the archive, Letta Core, or external tools.
- Inventing a new folder hierarchy for each escalation.
- Sending unattended mail to arbitrary recipients.
- Treating an ACK, a model answer, or a UI artifact as a durable receipt.
- Creating a second “heavy” automation by modifying the regular Olivia path
  without an explicit routing decision.
- Solving every multi-surface recovery problem inside this component.
- Removing human approval from consequential actions because an escalation was
  requested from a phone.

## Acceptance criteria

### Request lifecycle

1. A valid request produces a durable payload, queue record, and handoff state in
   that order.
2. A wake signal contains a pointer and request ID, not the only copy of the
   payload.
3. Spark can acknowledge, complete, partially complete, reject, time out, and
   cancel a request with distinct dispositions.
4. Every result links to request ID, trace ID, source refs, and a receipt.
5. Exact duplicate wakes do not cause duplicate work or duplicate external
   side effects.

### Ownership and policy

6. Spark writes only its own message, surface, and artifact names.
7. A task-specific tool allowlist is enforced at the gateway.
8. Core-memory mutation, publication, deletion, and external communication are
   blocked without their required approval class.
9. An expired or rejected approval cannot be reused.
10. The primary path never claims success when Spark has not written a verified
    receipt.

### Provenance and recovery

11. A result records searched surfaces, source IDs, limitations, and unresolved
    questions.
12. Empty stubs and missing sources remain visible as work, not fabricated
    evidence.
13. A failed wake leaves a durable, inspectable request.
14. A disconnected phone session does not turn into implicit approval.
15. A result can be resumed by a later primary session using durable references.
16. The TQS legal status vocabulary and `current_handoff` rule are honored.

### Operational proof

17. The scenarios in `04-acceptance-tests.md` pass with a fake Gmail wake,
    fake Drive store, fake Spark worker, and no external mail send.
18. Draft-only or manual-wake operation is represented as staged and does not
    pass the automated completion test.
19. Retry count, attempt IDs, deadline, and final disposition are observable.
20. The operator can inspect the request, approval, result, and receipt without
    reading model logs.

## Open questions

1. Which Spark account/runtime is the authoritative worker?
2. Is Spark reached through the normalized MCP gateway, `letta-client`, Gmail,
   or a staged combination?
3. Which wake subjects are currently approved and versioned?
4. Who may send automated mail, and which recipients are allowlisted?
5. What exact capabilities cause an escalation instead of a local retry?
6. Which work is allowed to continue after the caller hangs up?
7. What is the retry budget and backoff for an unavailable Spark?
8. How should timeout and cancellation be represented without violating the
   closed TQS status vocabulary?
9. Does Spark need an owner surface file in every deployment?
10. Which Drive/local folder is the canonical escalation root?
11. Are human approvals captured in the phone transcript, a UI, or a signed
    control record?
12. What does the primary do when Spark returns a conflict with a local source?
13. Should a partial result be eligible for Archival insertion?
14. How are “regular Olivia” and “Grok Heavy” routes isolated operationally?
15. What monitoring schedule is allowed, given that MCP invocation is not itself
    a background monitor?
