# OpenSpec: Acceptance Tests

**Status:** Draft conformance plan  
**Version:** 0.1.0  
**Covers:** [00-overview.md](./00-overview.md), [01-phone-mcp.md](./01-phone-mcp.md), [02-vultr-letta.md](./02-vultr-letta.md), [03-spark-escalation.md](./03-spark-escalation.md)

## Purpose

Provide a provider-neutral acceptance suite for the sovereign phone-to-agent
bridge. The suite must prove the complete flow without requiring a live phone
carrier, public MCP endpoint, Gmail send permission, Vultr credentials, a
production Letta server, or a real model.

The tests are contract tests first and integration tests second. Fakes and local
fixtures must make the safety, ownership, provenance, idempotency, and failure
rules executable before external services are connected.

A test passes only when it proves both the positive behavior and the relevant
negative behavior. For example, “Spark completed” is not enough: the suite must
also prove that a missing receipt does not become success, that duplicate wakes
do not repeat work, and that a denied confirmation cannot mutate data.

## Actors

| Actor | Test double or fixture | What the suite verifies |
|---|---|---|
| Human caller | Scripted phone events | Consent, utterance, confirmation, interruption, disconnect |
| Phone provider | Signed fake callback server | Signature, replay, callback acknowledgment, deduplication |
| Phone adapter | System under test | Canonical envelopes and provider-neutral rendering |
| MCP proxy | In-process stdio/SSE bridge fake | Transport normalization and error preservation |
| MCP gateway | Policy-aware fake gateway | Scope, schemas, idempotency, side-effect controls |
| Primary agent | Deterministic scripted agent | Routing, memory lookup, confirmation, escalation |
| Letta | Tiered memory fake plus optional test server | Core/Recall/Archival semantics and receipts |
| Spark/Vesper | Deterministic worker fake | Bounded escalation and result lifecycle |
| Gmail | Wake-only fake | Pointer delivery, no payload dependency, retry behavior |
| Drive/local store | Hashing artifact store fake | Durable payloads, ownership, receipts, restore |
| Vultr edge | Container or VM test harness | Health, private routing, runtime manifest |
| Operator | Scripted approvals/rejections | Human gates and exact binding |
| Observer | Structured log/trace collector | Trace continuity and secret redaction |

## Interfaces

### Test harness contract

Every test creates an isolated `TestRun`:

```yaml
run_id: test-...
clock: frozen-or-controlled
trace_id: trace-test-...
session_id: ses-test-...
provider_event_ids: []
artifacts_root: test-artifacts/<run_id>/
queue_root: test-queue/<run_id>/
secrets:
  provider_token: synthetic-only
  mcp_token: synthetic-only
external_writes: disabled
```

The harness exposes:

```text
provider.send(event)
provider.replay(event)
phone.hear()
phone.say(text)
gateway.call(tool, args, context)
letta.read(tier, key)
letta.write(tier, value, source_refs)
spark.run(request_id)
gmail.wake(request_ref)
store.read(ref)
store.receipts()
queue.current_handoff()
trace.events(trace_id)
```

All clocks are controllable. Tests that cover deadline, retry, or expiry advance
the clock explicitly rather than sleeping.

### Required fixture payloads

The fixture set includes:

1. a valid signed `session_started` callback;
2. a final utterance requesting a read-only memory search;
3. a request that needs confirmation before mutation;
4. a partial transcript followed by a final transcript;
5. an escalation request with a bounded structured output;
6. a missing-source/stub artifact;
7. a result with a deliberate source conflict;
8. a secret-shaped string that must be redacted;
9. a duplicate provider callback and duplicate wake;
10. a Letta Core block, Recall messages, and Archival items with source refs.

### Evidence requirements

Each test records:

- test ID, run ID, and result;
- trace and session IDs;
- request/event IDs and sequence numbers;
- queue state before and after;
- artifact refs, hashes, and receipt refs;
- tool calls and typed failures;
- approval and confirmation records;
- redacted structured logs;
- final phone response;
- no raw production secrets or real personal content.

## Data flows

### Conformance path

```text
fixture phone callback
  -> fake provider verification
  -> phone adapter
  -> canonical event
  -> gateway policy check
  -> primary agent
  -> Letta/MCP read or write
  -> response plan
  -> fake phone renderer
  -> receipt + trace assertions
```

### Escalation path

```text
phone request
  -> primary creates bounded escalation
  -> store payload + hash
  -> queue record + current_handoff
  -> fake Gmail wake
  -> Spark validates request
  -> Spark writes result + receipt
  -> primary verifies and resumes
```

### Failure path

Every injected failure must prove:

1. no unauthorized side effect occurred;
2. the request/event remains inspectable;
3. the user-facing response does not claim completion;
4. retryability or terminal disposition is explicit;
5. the trace links the failure to its cause.

## Test cases

### Contract and schema tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| CT-001 | Valid phone event normalization | Send a signed `session_started` and `utterance` | Envelopes contain schema version, event/session/trace IDs, source, consent, sequence, and provenance |
| CT-002 | Provider event deduplication | Send the same provider event twice | One logical event and one downstream effect; second response is deterministic |
| CT-003 | Conflicting sequence number | Send two different payloads with one sequence number | Second event rejected and security/audit event recorded |
| CT-004 | Unknown event type | Send an unsupported provider event | Explicit typed rejection; no agent call |
| CT-005 | Invalid signature | Alter the signed body or timestamp | Callback rejected; payload not logged; no session event |
| CT-006 | Schema version mismatch | Send unsupported envelope version | Typed incompatibility response; no silent downgrade |
| CT-007 | OpenAI/Gemini schema parity | Render one normalized tool in both declaration formats | Required arguments, optional arguments, result semantics, and side-effect class match |
| CT-008 | Missing MCP context | Omit trace, caller, or idempotency key | Gateway rejects before downstream dispatch |
| CT-009 | Unknown normalized tool | Request a tool not in the allowlist | Deterministic `UNKNOWN_TOOL`; no server call |
| CT-010 | Receipt schema | Complete a fake artifact write | Receipt has ref, hash, writer, time, parent refs, and status |

### Phone/session safety tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| PH-001 | Consent granted | Open session with affirmative consent, send a harmless utterance | Session records consent and permits only configured retention |
| PH-002 | Consent denied | Open session with denied consent and end call | Raw content remains session-only; no Recall/Archival write |
| PH-003 | Consent unknown | Omit consent, request a memory write | System asks or stages; it does not archive |
| PH-004 | Partial transcript | Send partial utterance containing a destructive instruction | No irreversible tool call until final event and confirmation |
| PH-005 | Exact confirmation | Propose one pending action and answer `yes` before expiry | Only the exact pending action executes once |
| PH-006 | Ambiguous confirmation | Answer `maybe`, unrelated “yes,” or silence | No action; caller receives clarification request |
| PH-007 | Stale confirmation | Advance past confirmation expiry and answer `yes` | Action rejected as stale; no side effect |
| PH-008 | Cancellation | Propose action, caller says `cancel` | Pending action closes; no tool call |
| PH-009 | Barge-in | Start a long spoken response and interrupt | Response stops or is marked interrupted; no duplicate turn |
| PH-010 | Disconnect during read | End session while a read-only tool is pending | Result is staged or cancelled per policy; no false spoken completion |
| PH-011 | Disconnect before mutation | End session before confirmation | Mutation never runs |
| PH-012 | Provider timeout | Delay downstream response past provider deadline | Provider gets deterministic acknowledgment/fallback; work has inspectable state |
| PH-013 | Secret redaction | Include synthetic provider and MCP secrets in all payload paths | Secrets absent from prompts, memory, artifacts, ordinary logs, and receipts |
| PH-014 | Session close | End a successful session | Close receipt references child events and final disposition |

### MCP, proxy, and gateway tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| MCP-001 | stdio to remote bridge | Start fake local MCP server and call through remote presentation | Tool result and error semantics survive translation |
| MCP-002 | Remote to stdio bridge | Call fake remote endpoint from local client | Same normalized schema and trace continuity |
| MCP-003 | Capability discovery | Query gateway capabilities as each actor | Caller sees only scoped tools and versioned descriptions |
| MCP-004 | Read scope | Spark requests `memory.recall` | Read succeeds when scoped; no mutation capability appears |
| MCP-005 | Write scope | Spark requests unlisted external write | Gateway rejects before downstream call |
| MCP-006 | Idempotent tool call | Repeat same idempotency key and args | One side effect; second response references original receipt |
| MCP-007 | Conflicting idempotency key | Reuse key with different args | Request rejected as conflict |
| MCP-008 | Downstream timeout | Make fake MCP server timeout | Typed retryable failure; no success receipt |
| MCP-009 | Downstream malformed response | Return invalid tool result | Gateway rejects/contains the result; no invented value |
| MCP-010 | Rate limit | Exceed per-caller request budget | Further calls rejected with retry metadata |
| MCP-011 | Credential rotation | Rotate synthetic gateway credential during traffic | New requests use new credential; allowed in-flight request behavior is documented |
| MCP-012 | Health endpoints | Toggle gateway, proxy, Letta, and storage states | Live/ready responses distinguish process and dependency readiness |

### Letta memory tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| LT-001 | Core read | Seed a small identity block and read it | Core is returned as in-context memory with block ID |
| LT-002 | Recall search | Seed searchable conversation history and query it | Results identify Recall tier, IDs, and source refs |
| LT-003 | Archival search | Seed long-term facts and query semantically | Results identify Archival tier, source, and embedding metadata |
| LT-004 | Core protection | Have curator propose a bulk Core replacement | Proposal is recorded; Core remains unchanged without approval |
| LT-005 | Approved Core patch | Approve one exact patch with source refs | Only requested block fields change; receipt records approval |
| LT-006 | Provenance-required write | Attempt write without source refs | Adapter rejects or stages as non-promotable per policy |
| LT-007 | Sensitive fact | Attempt to persist a sensitive phone detail | Policy selects retention/approval; no silent Archival insert |
| LT-008 | Deduplicated Archival item | Insert same content hash twice | One logical item or explicit duplicate receipt; no silent overwrite |
| LT-009 | Index loss | Delete derived vector index and restore source store | Source/receipts survive; rebuild is explicit and verifiable |
| LT-010 | Embedding mismatch | Search with a different embedding model/version | System rejects or marks migration required; no false comparable result |
| LT-011 | Spark client runtime | Run client fixture under CPython 3.11 profile | Client works without installing server-only CPython 3.12 bundle |
| LT-012 | Bounded results | Seed many matches and query | Response is bounded, ordered by declared policy, and traceable |

### Escalation and TQS tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| ES-001 | Durable-before-wake ordering | Instrument store and fake Gmail | Payload, hash, queue record, and handoff exist before wake |
| ES-002 | Valid Spark request | Submit bounded research request | Spark reads durable payload and acknowledges after validation |
| ES-003 | Completed result | Spark writes output and receipt | Primary verifies receipt and resumes with correct result |
| ES-004 | Partial result | Spark returns incomplete output with limitation | Disposition is partial/needs-human, never completed without qualification |
| ES-005 | Missing payload | Delete or hide payload before Spark reads | Spark rejects; no invented context or success |
| ES-006 | Duplicate wake | Deliver same wake twice | One attempt or idempotent continuation; no duplicate external side effect |
| ES-007 | Wake unavailable | Make Gmail fake fail | Durable request remains discoverable; no completion claim |
| ES-008 | Spark unavailable | Make worker unavailable | Queue/handoff remains waiting or staged under approved status policy |
| ES-009 | Expired deadline | Advance clock beyond deadline | Request is not dispatched; terminal or human-review state is explicit |
| ES-010 | Approval pending | Submit a Core/publication request without approval | Router holds request and does not invoke Spark |
| ES-011 | Approval rejected | Reject exact request | Request closes/cancels with rejection receipt; no action |
| ES-012 | Approval mismatch | Approve request A and dispatch request B | Router rejects mismatch |
| ES-013 | Worker ownership | Spark attempts to write Olivia-owned artifact | Write rejected/audited; Spark-owned output remains possible |
| ES-014 | TQS status | Exercise post, ack, ready, awaiting, close | Only legal statuses are used and `current_handoff` is authoritative |
| ES-015 | No ACK-of-ACK | Have Spark acknowledge a primary ACK | No pointless ACK loop is created |
| ES-016 | Stub source | Include an empty source stub in request | Result preserves stub as unresolved work; no fabricated evidence |
| ES-017 | Source conflict | Seed two contradictory source artifacts | Spark returns conflict and refs; primary does not silently choose |
| ES-018 | Retry attempt | Fail first attempt, retry with same request and new attempt ID | Trace links attempts; completed side effect remains once |
| ES-019 | Caller disconnect | End phone session after durable submission | Continuation follows policy; no implicit approval |
| ES-020 | Receipt failure | Make receipt store fail after Spark output | System reports not verified and preserves local staging |

### Recovery, security, and operations tests

| ID | Scenario | Procedure | Pass criteria |
|---|---|---|---|
| OP-001 | Process restart | Restart coordinator with pending request | Pending request is recovered or explicitly marked unknown; no blind replay |
| OP-002 | Store unavailable | Disable artifact store temporarily | Health becomes not-ready where required; calls fail safely |
| OP-003 | Restore from backup | Restore memory/source fixture | Hashes, tier metadata, and receipt links verify |
| OP-004 | TLS/auth boundary | Attempt direct public Letta/admin access | Connection is refused or requires approved private route |
| OP-005 | Least privilege | Use phone, Spark, and maintainer credentials against all tools | Each identity can perform only its declared operations |
| OP-006 | Log scan | Run all fixtures and scan structured logs | No synthetic secret, raw auth header, or unredacted sensitive text |
| OP-007 | Trace continuity | Follow one normal and one escalated request | Every child event/tool/artifact shares or links to root trace |
| OP-008 | Artifact hash | Modify stored payload after receipt | Verification detects content hash mismatch |
| OP-009 | Backup index rebuild | Recreate vector index from canonical records | Result count/source hashes meet declared tolerance |
| OP-010 | Configuration drift | Remove required runtime field | Readiness/config validation fails with actionable error |
| OP-011 | Rate/timeout budget | Saturate phone, gateway, and Spark queues | Backpressure is explicit; system does not create unbounded work |
| OP-012 | Manual wake mode | Disable automated Gmail send | Request remains staged and discoverable; automated completion test does not pass |

## Non-goals

- Proving carrier audio quality or model answer quality with synthetic tests.
- Testing a real personal phone number, production Gmail account, or production
  Drive folder.
- Testing provider-specific UI behavior not represented by the adapter contract.
- Measuring final cloud cost, high availability, or regional failover.
- Treating green health checks as proof of semantic correctness.
- Replacing human review with a test fixture that always approves.
- Accepting a test that passes only because logs or receipts were deleted.
- Using a real secret merely to prove redaction.

## Acceptance criteria

The OpenSpec implementation is acceptance-ready when:

1. All contract tests `CT-001` through `CT-010` pass.
2. All phone safety tests `PH-001` through `PH-014` pass.
3. MCP tests `MCP-001` through `MCP-012` pass for the chosen bridge path.
4. Letta tests `LT-001` through `LT-012` pass against a fake and, when
   available, a version-pinned integration server.
5. Escalation tests `ES-001` through `ES-020` pass with external mail disabled.
6. Operations tests `OP-001` through `OP-012` pass in an isolated environment.
7. Each test emits the evidence fields listed in this document.
8. Negative tests prove no unauthorized side effect, no false completion, and no
   secret leakage.
9. A failed external dependency produces a visible typed failure and durable
   recovery state.
10. Test fixtures are deterministic, isolated per run, and safe to rerun.
11. The test report names any skipped integration test and the missing external
    dependency; skipped is not passed.
12. The test suite can be executed without hydrating the complete skill archive
    into Letta.

## Open questions

1. Which language and test runner will own the executable harness?
2. Will the conformance suite run in CI, on Vultr, on Spark, or all three?
3. Which OpenAPI/JSON Schema validator is approved for envelope/tool parity?
4. What latency budgets should be asserted for provider acknowledgment, local
   tool calls, memory reads, and escalation?
5. What exact status extension will represent timeout, retry, and cancellation
   while preserving TQS compatibility?
6. Which redaction patterns are required beyond provider and MCP credentials?
7. What hash algorithm and canonical serialization are normative for artifacts?
8. How much retrieval variance is acceptable when embeddings are provider-backed?
9. What is the minimum evidence needed to call a remote receipt `VERIFIED`?
10. Which integration tests may send a real Gmail draft, if any?
11. What approval UI or phone control is used for human-gated tests?
12. Which runtime matrix must be tested for Debian/CPython versions and package
    wheels?
13. How are test artifacts retained and cleaned without deleting production
    receipts?
14. Which scenarios require a manual review sign-off even when automated checks
    pass?
15. When top-level `bridges/` and `docs/` sources are restored, which additional
    fixtures or invariants must be added to this suite?

