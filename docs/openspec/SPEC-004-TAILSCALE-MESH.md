# SPEC-004 — Tailscale Mesh

**Status:** Draft
**Type:** Atomic OpenSpec / architecture contract
**Scope:** Private, userspace Tailscale connectivity for approved peer-to-peer
workflows and their documented fallbacks.

## Context

The repository already describes a Tailscale-based ferry for reaching approved
peers, transferring artifacts, and optionally falling back to Drive. This
specification makes the boundary conditions explicit without implementing a
client, daemon, transfer worker, or credential store.

The current integration references are:

- [`tailnet-ferry`](../../skill_tree/skills/skill-orchestrator/references/integrations/tailnet-ferry/SKILL.md)
- [`heavy-olette-drive-pipe`](../../skill_tree/skills/skill-orchestrator/references/integrations/heavy-olette-drive-pipe/RUNBOOK.md)
- [`tool-shelf`](../../skill_tree/skills/system-roadmap/references/tool-shelf/README.md)

SPEC-001 and SPEC-002 are not present on the base branch at drafting time, so
there are no cross-links for them in this document.

## Goals

1. Define a private mesh boundary for approved nodes and approved workflows.
2. Separate mesh admission, peer identity, transport, and artifact
   authorization so one successful check cannot imply the others.
3. Support userspace networking where the host cannot or must not install a
   lasting TUN route.
4. Define deterministic interfaces for status, transfer intent, transfer
   result, and operator-visible receipts.
5. Prefer the least-powerful transport that satisfies the transfer:
   SFTP for structured exchange, Taildrop for one-off peer delivery, and an
   explicitly selected external fallback when the mesh is unavailable.
6. Make unsafe, ambiguous, stale, or unverifiable states fail closed.
7. Preserve auditability without retaining credentials or copying secret
   material into repository artifacts.

## Non-goals

- Implementing or packaging `tailscale`, `tailscaled`, SFTP, Taildrop, SOCKS,
  Drive, or any other transport.
- Creating, rotating, storing, displaying, or recovering Tailscale auth keys,
  SSH private keys, OAuth tokens, cookies, or other secrets.
- Designing a new control plane, ACL policy language, identity provider, or
  Headscale deployment.
- Treating Tailscale reachability as authorization to read, write, execute, or
  publish data on a peer.
- Providing a general-purpose VPN, exit-node policy, LAN bridge, subnet
  router, or inbound public service.
- Binding a service to an all-interface address or exposing a mesh service
  outside its approved peer and port scope.
- Guaranteeing direct connectivity; DERP relay use is an operational detail,
  not a reason to weaken identity or authorization checks.
- Silently switching to a fallback transport or reporting fallback success as
  mesh success.
- Defining implementation tasks, deployment manifests, CI jobs, or test code.

## Atomic boundary

This spec covers one decision unit: **may this approved workflow use this
transport to reach this approved peer for this declared artifact operation?**

Every decision has four independent dimensions:

| Dimension | Required question |
| --- | --- |
| Admission | Is the local node currently admitted to the intended tailnet? |
| Peer | Is the remote endpoint the expected node and identity? |
| Operation | Is this workflow allowed to perform the declared read/write action? |
| Evidence | Can the outcome be recorded without recording a secret? |

Failure of any dimension is a denial. A positive answer in one dimension must
not be cached or inferred as a positive answer in another.

## Interfaces

These are contracts, not implementation prescriptions.

### 1. Workflow intent

The caller supplies a structured intent containing:

| Field | Requirement |
| --- | --- |
| `request_id` | Unique, non-secret correlation identifier |
| `operation` | One of `read`, `write`, `list`, or `probe` |
| `peer_id` | Stable approved peer identity; hostname alone is insufficient |
| `endpoint` | Approved service and port for the selected operation |
| `artifact_scope` | Explicit path, object, or bounded transfer scope |
| `transport` | `sftp`, `taildrop`, or explicitly named fallback |
| `max_bytes` | Required for transfers; bounded and policy-approved |
| `allow_fallback` | Explicit boolean; default is false |
| `idempotency_key` | Required for writes and retryable transfers |

Secrets are not valid fields in the intent. Credentials are supplied only by
the runtime mechanism that owns them and are never echoed into an intent,
receipt, or log.

### 2. Mesh status

The mesh adapter exposes a read-only status result:

| Field | Meaning |
| --- | --- |
| `admitted` | Local node has an active, policy-approved mesh session |
| `local_peer_id` | Identity of the admitted local node |
| `tailnet_id` | Non-secret identifier of the intended tailnet |
| `daemon_reachable` | Required control socket/daemon health signal |
| `network_mode` | Must be `userspace` for this scope |
| `observed_at` | Freshness timestamp |
| `peers` | Approved peer identities, addresses, and observed state |
| `degraded_reason` | Redacted, operator-safe reason when not usable |

The adapter must distinguish “not admitted,” “daemon unavailable,” “peer
offline,” and “status stale.” A generic `false` without a reason is not an
adequate operational receipt.

### 3. Peer and endpoint authorization

Before a connection is attempted, policy evaluates:

1. the declared `peer_id` against the approved peer set;
2. the resolved endpoint against the peer's approved addresses;
3. the service and port against the operation's allowlist;
4. the requested artifact scope and byte bound against the workflow policy;
5. the freshness of the mesh status and peer identity observation.

DNS or a Tailscale IP is a locator, not an identity proof. Host-key or
equivalent service identity verification remains required for an application
protocol such as SFTP.

### 4. Transport contracts

#### SFTP

SFTP is the structured exchange interface. Its contract includes:

- an approved peer and service endpoint;
- an approved account identity;
- application-level host/service identity verification;
- an explicit read or write scope;
- bounded, resumable or idempotent transfer semantics;
- a result that identifies the remote scope and byte/hash evidence.

Mesh admission does not authorize an SFTP account, and an SFTP key does not
authorize mesh admission.

#### Taildrop

Taildrop is a peer-to-peer artifact delivery interface for bounded, one-off
transfers. It is not a login, shell, filesystem browsing, or remote execution
interface. The contract must state the receiving peer, artifact scope, byte
bound, and delivery result.

#### Explicit fallback

A fallback such as Drive is a separate trust and audit domain. It may be used
only when the caller explicitly set `allow_fallback` and policy allows that
fallback. Its receipt must identify the fallback transport and must not claim
that the artifact traversed the Tailscale mesh.

### 5. Result and receipt

Every accepted or denied intent returns a non-secret result with:

| Field | Requirement |
| --- | --- |
| `request_id` | Matches the intent |
| `decision` | `allow`, `deny`, `complete`, `partial`, or `error` |
| `transport_used` | Actual transport, including explicit fallback |
| `peer_id` | Approved identity or `unknown` on pre-admission denial |
| `scope` | Redacted only where necessary, never silently broadened |
| `bytes` | Transferred byte count when applicable |
| `content_evidence` | Hash, manifest, or equivalent when policy permits |
| `reason_code` | Stable, operator-safe denial or error category |
| `started_at` / `finished_at` | Timestamps |

Receipts must never contain credentials, private-key material, auth-key
material, bearer tokens, cookie contents, or secret-bearing command lines.

## Fail-closed rules

The following rules are normative:

1. **No admission, no mesh.** If local admission is absent, expired, revoked,
   or not verifiable, deny every mesh transport.
2. **No daemon, no mesh.** If the control socket or daemon health cannot be
   verified, do not infer that a prior process or cached state is still valid.
3. **No fresh status, no action.** Stale, partial, contradictory, or
   time-invalid peer status denies the operation.
4. **No approved peer, no connection.** A hostname, IP, or friendly name that
   cannot be mapped to an approved peer identity is denied.
5. **No approved endpoint, no connection.** Unlisted services, ports, or
   address families are denied, even if reachable.
6. **No application identity, no data.** Mesh reachability is insufficient;
   SFTP or another application protocol must verify its own service identity.
7. **No declared scope, no transfer.** Empty, wildcard, traversal-like, or
   otherwise ambiguous artifact scopes are denied.
8. **No bound, no transfer.** Missing, non-positive, or excessive byte limits
   deny a transfer.
9. **No explicit fallback, no fallback.** A mesh failure never silently
   becomes a Drive, public URL, or other external transfer.
10. **No explicit transport, no selection.** The system must not choose a
    higher-power transport because the caller omitted one.
11. **No secret provenance, no use.** Credentials with unknown source,
    unexpected format, unsafe permissions, or ambiguous ownership are denied
    and must not be printed for diagnosis.
12. **No all-interface exposure.** Services must not bind to `0.0.0.0`,
    `::`, or an equivalent unrestricted interface for this workflow.
13. **No remote execution.** SFTP and Taildrop operations must not be
    upgraded into shell, command execution, or arbitrary port forwarding.
14. **No duplicate write.** A retry without a matching idempotency key and
    prior-result check must not repeat a write.
15. **No unverifiable completion.** A transfer with unknown completion,
    mismatched evidence, or interrupted receipt is `partial` or `error`, never
    `complete`.
16. **No secret-bearing observability.** Logs, metrics, receipts, and error
    messages redact secret values and secret-derived command arguments.

## Acceptance criteria

Each criterion is independently reviewable. “Pass” means the document or
event demonstrates the stated property without requiring an implementation in
this change.

- **TS-001 — Atomic scope:** The change defines one Tailscale mesh decision
  unit and does not claim to implement it.
- **TS-002 — Goals:** Mesh privacy, separation of concerns, userspace support,
  least-powerful transport, auditability, and fail-closed behavior are stated
  as goals.
- **TS-003 — Non-goals:** VPN expansion, credential lifecycle, implementation,
  public exposure, and silent fallback are explicitly excluded.
- **TS-004 — Admission interface:** The workflow intent and mesh status
  interfaces identify the information needed to decide admission.
- **TS-005 — Peer identity:** Peer identity is evaluated separately from
  hostname, IP address, or general reachability.
- **TS-006 — Endpoint allowlist:** Service, port, address, operation, and
  artifact scope are all authorization inputs.
- **TS-007 — Userspace mode:** The contract requires userspace networking for
  this scope and does not assume a kernel TUN route.
- **TS-008 — Freshness:** Status includes an observation time and stale or
  contradictory status is denied.
- **TS-009 — SFTP boundary:** SFTP requires both approved mesh peer identity
  and application-level service identity.
- **TS-010 — Taildrop boundary:** Taildrop is defined as bounded delivery only
  and cannot imply shell, login, browsing, or execution.
- **TS-011 — Fallback disclosure:** Fallback requires explicit caller
  consent, separate policy, and a receipt naming the actual transport.
- **TS-012 — Secret exclusion:** No auth key, private key, token, cookie, or
  secret-bearing command line is a valid intent or receipt field.
- **TS-013 — Scope bounds:** Every transfer has an explicit artifact scope and
  a positive, policy-approved byte bound.
- **TS-014 — Interface exposure:** All-interface binds and unrestricted
  listeners are prohibited.
- **TS-015 — Credential separation:** Mesh admission credentials and
  application credentials are treated as independent authorities.
- **TS-016 — Denial semantics:** The spec defines stable, operator-safe
  denial reasons for missing admission, daemon health, peer, endpoint,
  freshness, scope, and byte-bound evidence.
- **TS-017 — Retry safety:** Writes require idempotency and retries cannot
  repeat an unknown or unverified write.
- **TS-018 — Completion evidence:** A result distinguishes complete, partial,
  denied, and error outcomes and does not claim completion without evidence.
- **TS-019 — Audit receipt:** Results correlate to the request, identify the
  actual transport and peer, and include timestamps without secrets.
- **TS-020 — Repository boundary:** This specification is the only requested
  file change; no implementation, credentials, generated artifact, or
  unrelated cleanup is included.
