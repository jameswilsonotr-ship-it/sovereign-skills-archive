# OpenSpec: Vultr Edge and Letta Memory Plane

**Status:** Draft deployment and memory specification  
**Version:** 0.1.0  
**Depends on:** [00-overview.md](./00-overview.md), [01-phone-mcp.md](./01-phone-mcp.md)

## Purpose

Define the deployment boundary and memory contract for the reachable sovereign
runtime. Vultr is the candidate edge location for the MCP proxy/gateway and,
subject to an explicit deployment decision, the Letta server and inference
services. Letta provides durable agent memory; it is not a replacement for the
archive, queue, receipt store, or operator approval layer.

The design preserves the repository's local-first posture:

- local stdio tools remain usable behind `mcp-proxy`;
- Grok/xAI can use an SSE or Streamable HTTP presentation;
- Gemini/Vesper can use a stdio or client presentation;
- a compact gateway can apply shared authentication, routing, and rate limits;
- the Letta server runs where its supported Python/runtime and model dependencies
  are available;
- Spark remains a client/worker boundary when its Debian 12 / CPython 3.11
  environment cannot safely host the Letta server's CPython 3.12 dependency set.

This document deliberately describes a topology and contracts, not a claim that
Vultr or Letta is already deployed.

## Actors

| Actor | Responsibility | Placement |
|---|---|---|
| Phone/session coordinator | Sends scoped requests and receives results | Phone ingress or control plane |
| MCP proxy | Converts stdio local servers to SSE/Streamable HTTP and reverse direction as needed | Vultr edge or local edge |
| MCP gateway | Authenticates, rate-limits, routes, and exposes compact tools | Public/private Vultr edge |
| Letta API/server | Manages Core, Recall, Archival, agents, and memory operations | Matching VM/runtime, candidate Vultr |
| Inference provider | Generates agent responses for Letta or a separate orchestrator | Separate service or same private network |
| Embedding provider | Produces vectors for Archival retrieval | API, ONNX host, or approved local model |
| Spark/Vesper client | Uses `letta-client` or normalized MCP tools for bounded work | Debian 12, CPython 3.11 |
| Local MCP servers | Git, SQLite, Drive helpers, archive tools | Local machine or private edge |
| Durable artifact store | Holds source documents, envelopes, and receipts | Drive/local/object store |
| Operator/maintainer | Approves topology, rotates keys, checks health | Human-controlled |

## Interfaces

### Deployment topology

The initial topology is:

```text
                         public/private network
phone / Olivia / Spark ----------------------------+
                                                   v
                                      [TLS + auth boundary]
                                             Vultr edge
                                      +--------------------+
                                      | MCP gateway        |
                                      | mcp-proxy          |
                                      | health/telemetry   |
                                      +---------+----------+
                                                |
                              private service network, no public Letta port
                         +----------------------+------------------+
                         v                                         v
                  [Letta server]                             [inference]
                         |                                         |
                         +----------------------+------------------+
                                                v
                                      [memory/vector storage]
                                                |
                                  [Drive/local artifact store]
```

The Letta API should not be directly exposed to the public internet unless a
separate review approves that exception. The gateway is the policy boundary and
the only service that should translate external caller identity into scoped
Letta operations.

### Runtime compatibility

The recovered package inventory establishes an important split:

- target edge baseline: Debian 12, x86_64, glibc 2.36;
- Spark baseline: CPython 3.11;
- the recorded Letta server bundle resolved native dependencies for CPython
  3.12;
- the safe immediate Spark role is `letta-client`, not the full Letta server;
- Spark is not the inference box;
- fastembed ONNX or an approved embedding API is the lightweight path;
- a local MRL/torch embedding path is a later VM decision and must not be
  dropped into the constrained Spark environment casually.

The deployment manifest must record Python version, architecture, package
source/hash, model provider, and whether a service is server, client, or worker.

### MCP proxy and gateway

`mcp-proxy` is the transport bridge. It may present local stdio servers to Grok
over SSE/Streamable HTTP or expose a remote MCP endpoint to a local client.
`mcp-gateway` is the optional aggregator and policy layer. It should collapse
large underlying surfaces to approximately 14–16 normalized operations where
that improves tool discoverability and token use.

The gateway interface includes:

```text
POST /mcp/capabilities
POST /mcp/tools/{normalized_tool}
GET  /health/live
GET  /health/ready
GET  /metrics (authenticated or private only)
```

Exact paths are provisional. Each request requires:

- short-lived service or session credential;
- caller and capability scope;
- `trace_id`, request ID, and idempotency key;
- schema version;
- side-effect class: `read`, `stage`, `mutate`, or `external`;
- timeout and deadline.

The gateway validates the normalized request, then dispatches to the concrete
MCP server or Letta adapter. It returns the concrete server result plus a
normalized receipt reference. It must preserve source errors instead of
converting them to a generic success.

### Letta adapter

The adapter exposes a small semantic interface:

```text
memory.core.read(agent_ref, block_ref)
memory.core.propose_update(agent_ref, block_ref, patch, source_refs)
memory.recall.search(agent_ref, query, filters)
memory.archival.insert(agent_ref, item, source_refs)
memory.archival.search(agent_ref, query, filters)
memory.promote(candidate_ref, destination, approval_ref)
memory.receipt.read(receipt_ref)
```

Every mutation includes an explicit `source_refs` list, a content hash when
available, actor identity, policy decision, and idempotency key.

### Memory tier contract

| Tier | Letta role | Allowed content | Mutation rule |
|---|---|---|---|
| Core | Always in-context memory blocks | Small identity, critical user facts, active working state | Never bulk-replace; sensitive changes require policy/approval |
| Recall | Searchable message history | Recent dialogue and recoverable session context | Append/search; retention applies |
| Archival | Long-term semantic store | Durable facts, extracted atoms, package references | Insert/search with provenance; promotion is explicit |

“Hot/warm/cold” are operator shorthand only. They must not become an
untracked fourth memory model. A curator or sleeptime agent may compact Recall
or propose Archival promotion, but cannot silently rewrite Core identity.

### Storage and backup

The server's memory database, vector index, and source artifact store are
separate logical assets, even if initially co-located. Backups must identify:

- Letta agent and memory IDs;
- source artifact and receipt IDs;
- schema and embedding model/version;
- encryption and key version;
- backup timestamp and verification result.

A vector index is a derived representation. Loss of the index must not destroy
the canonical source or receipts.

### Secret and network controls

- Public ingress terminates at a TLS-capable boundary.
- Letta's admin and database ports stay private.
- MCP downstream credentials are stored separately from model API keys.
- Drive/Gmail credentials are not passed through model prompts.
- Service-to-service calls use least privilege and rotation.
- Health endpoints reveal readiness, not secrets, prompts, memory contents, or
  infrastructure credentials.
- Logs use trace IDs and opaque references; payloads are redacted by policy.

## Data flows

### Request and memory read

1. Phone or peer agent sends a canonical event to the gateway.
2. Gateway authenticates the caller and checks the allowed capability scope.
3. Agent reads the minimum Core block needed for continuity.
4. If context is missing, the agent performs a Recall search.
5. If a durable fact is needed, it searches Archival with a bounded query.
6. Results are tagged with tier, record ID, source references, and trace.
7. The response returns through the gateway and phone renderer.

The default query order is Core, then Recall, then Archival. A caller must not
receive an unbounded dump of all three tiers.

### New material and promotion

```text
phone utterance
  -> session record
  -> policy classification
  -> Recall or Archival candidate
  -> provenance + hash + receipt
  -> optional curator/deduplication
  -> explicit promotion proposal
  -> approval policy
  -> Core patch (if approved)
```

Raw content can remain session-only. The adapter must not treat every helpful
sentence as a permanent fact. A promotion proposal states what changed, why,
which sources support it, and whether an operator approved it.

### Tool execution

1. Agent requests a normalized tool.
2. Gateway checks capability, side-effect class, and confirmation.
3. Proxy translates the call to the target MCP server.
4. Result is normalized and stored with parent request/trace references.
5. Letta receives a summary only when retention and memory policy permit.
6. The agent receives the result or a typed failure.

Tool output is not automatically Core memory. Large outputs should be artifacts
with a compact pointer in memory.

### Spark client access

Spark uses the same gateway or `letta-client` against a private, authenticated
Letta endpoint. If Spark is given direct client access, the token must be scoped
to the agent, memory operation, and task. Spark does not get administrator
rights merely because it is an escalation worker.

The package inventory's `letta-client` and `letta` server split is a deployment
constraint, not a semantic split: both paths must preserve the same envelope,
receipt, and memory-tier rules.

### Restart, backup, and restore

On restart, the edge reports `live` only when the process is running and
`ready` only when credentials, Letta dependency, storage, and required model
connectivity are verified. A restored vector index must be checked against
source hashes. In-flight requests are recovered from durable idempotency state
or marked explicitly as unknown/pending; they are never replayed blindly.

## Non-goals

- Declaring Vultr as the final host without a capacity, network, and cost review.
- Installing the full Letta server on Spark when runtime compatibility says to
  use `letta-client`.
- Putting inference, embeddings, MCP, and durable storage into one unbounded
  process.
- Treating a vector database as the source of truth.
- Making Core a transcript cache or bulk-importing the entire archive.
- Exposing Letta admin APIs or databases publicly.
- Choosing an embedding model solely by dimension count.
- Guaranteeing high availability, multi-region failover, or zero-downtime
  upgrades in version 0.1.0.
- Replacing TQS with an implicit model-to-model conversation.
- Allowing a worker to mutate another actor's queue or surface file.

## Acceptance criteria

### Topology and runtime

1. A deployment manifest identifies each service's host, runtime, package source,
   version/hash, network exposure, and secret class.
2. The reference environment runs the gateway and proxy on Debian 12-compatible
   infrastructure.
3. Spark can perform an authenticated client request without requiring the
   CPython 3.12 Letta server bundle.
4. The Letta server is reachable only through the approved private route.
5. Liveness and readiness distinguish process-up from dependency-ready.

### Gateway and proxy

6. A local stdio test server can be reached through the normalized remote
   presentation.
7. OpenAI-style and Gemini-style schemas describe the same required arguments,
   result shape, and side-effect class.
8. Missing scope, stale credentials, malformed arguments, and duplicate
   idempotency keys are rejected deterministically.
9. A downstream MCP failure is preserved as a typed failure and produces no
   false receipt.
10. Gateway logs contain correlation identifiers without raw secrets or
    unrestricted payloads.

### Letta memory

11. Core, Recall, and Archival operations are separately observable in tests.
12. A Recall or Archival write includes source refs and a mutation receipt.
13. A curator cannot silently overwrite a Core identity block.
14. A failed vector-index restore leaves canonical artifacts and receipts intact.
15. Memory search results are bounded and identify their tier and provenance.
16. Session-only data remains out of long-term memory under denied consent.

### Operational recovery

17. A restart does not replay a completed side effect.
18. A timeout or dependency outage is visible through health state and a typed
    request failure.
19. Backup/restore verification checks source hashes and embedding metadata.
20. The cases in `04-acceptance-tests.md` pass with fake Letta and fake storage
    before production credentials are introduced.

## Open questions

1. Does the first Vultr node host only edge services or also Letta?
2. What Vultr size, disk type, backup policy, and region are approved?
3. Which database/storage backend does the selected Letta version require?
4. Which inference provider is connected to Letta, and what are its data-use
   constraints?
5. Is a private network/VPC available between gateway, Letta, and storage?
6. Which gateway implementation is selected: a packaged gateway, custom thin
   service, or a combination?
7. How are service identities issued and rotated?
8. What is the maximum Core block size and the approved Core schema?
9. Which retention classes map to raw transcript, summary, Recall, and Archival?
10. Are embeddings generated locally with fastembed ONNX, remotely by API, or
    by a later MRL-capable model?
11. What is the restore point objective for memory and receipts?
12. How are Letta agent IDs and archive package IDs cross-referenced?
13. Does direct `letta-client` access from Spark remain necessary after gateway
    stabilization?
14. Which metrics define acceptable search quality, latency, and token savings?
15. What maintenance window and migration procedure apply to a Letta version
    change?

