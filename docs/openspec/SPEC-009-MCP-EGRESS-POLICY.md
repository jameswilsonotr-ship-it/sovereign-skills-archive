# SPEC-009 — MCP Egress Policy

**Status:** Draft  
**Base:** `skill-tree-intake`  
**Owner:** Platform Security  
**Scope:** MCP clients, MCP hosts, MCP servers, and any sidecar or runtime that
executes an MCP tool  
**Classification:** Specification only; this document does not authorize an
implementation or deployment

## 1. Summary

This specification defines a deny-by-default, fail-closed egress boundary for
Model Context Protocol (MCP) tool execution. An MCP invocation may make an
outbound request only when the final destination, protocol, port, and network
path are explicitly authorized by a valid policy. Any missing, ambiguous,
unavailable, stale, or contradictory control MUST result in denial.

The policy is an enforcement boundary, not an allowlist for credentials.
Authentication, tool consent, prompt content, and MCP capability discovery
cannot grant network access.

## 2. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, and **MAY** in this document are to be interpreted
as normative requirements.

“Egress” means any connection or packet leaving the MCP execution boundary,
including HTTP(S), WebSocket, TCP, UDP, DNS, proxy tunneling, subprocess
traffic, and traffic created by a library or runtime on behalf of a tool.

“Fail closed” means that the requested operation is denied when the policy
decision cannot be established with complete and valid evidence. A timeout,
crash, partial response, stale cache, malformed input, or unavailable
dependency is not permission.

## 3. Goals

1. Prevent an MCP tool from reaching an unapproved destination.
2. Make every permitted destination and network path explicit and auditable.
3. Prevent DNS, redirect, proxy, parser, runtime, and error-path bypasses.
4. Keep policy evaluation deterministic for the same request and policy
   revision.
5. Avoid placing secrets, bearer material, or sensitive request data in policy
   records and decision logs.

## 4. Non-goals

- This specification does not define MCP authentication, authorization, or
  user-consent UX.
- This specification does not define a particular firewall, proxy, container
  runtime, programming language, or cloud provider.
- This specification does not permit arbitrary internet access for
  convenience, discovery, telemetry, package installation, or diagnostics.
- This specification does not treat a successful TLS handshake or valid
  credentials as evidence that a destination is approved.

## 5. Policy model

A policy is an immutable, versioned document containing:

- a unique policy revision;
- the applicable execution-boundary identity;
- explicit allow rules containing a protocol, canonical hostname or IP
  address, and port;
- optional path constraints for protocols that expose paths;
- optional DNS, proxy, byte, request-count, and time limits; and
- an expiry or renewal condition.

The empty allow set is valid and means “deny all egress.” A policy MAY contain
an explicit deny set for documentation and audit purposes, but an allow rule
MUST NOT be interpreted as overriding a higher-priority platform deny.

A destination is not approved merely because its parent domain, DNS answer,
redirect target, certificate subject, or authenticated principal appears
approved. Each network hop MUST be evaluated against the active policy.

### 5.1 Safe illustrative policy shape

The following is illustrative and contains no credentials:

```yaml
policy_revision: "spec-009-example-r1"
boundary: "mcp-runtime-example"
default: deny
allow:
  - protocol: https
    host: "api.example.invalid"
    port: 443
    path_prefix: "/v1/"
limits:
  max_requests: 100
  max_bytes: 1048576
  dns_ttl_seconds: 60
expiry: "2026-12-31T00:00:00Z"
```

An implementation MUST reject an equivalent document if any required field is
missing, duplicated, ambiguous, unsupported, or invalid.

## 6. Atomic requirements

Each requirement below is independently testable and intentionally atomic.

### EG-001 — Deny by default

The egress enforcer MUST deny every outbound connection when no active policy
exists, when the active policy contains no matching allow rule, or when the
requested destination is not explicitly listed.

### EG-002 — No implicit network capability

MCP discovery, tool registration, tool descriptions, prompt instructions,
resource metadata, environment variables, and user approval MUST NOT
implicitly enable egress.

### EG-003 — Explicit allow is required

The enforcer MUST permit a connection only after an active policy explicitly
allows the requested protocol, canonical destination, and port for the
requesting execution boundary.

### EG-004 — Canonicalize before evaluating

The enforcer MUST canonicalize the destination before policy matching,
including scheme, hostname case, trailing dot, Unicode representation,
authority delimiters, default ports, and IP address format. If canonicalization
is lossy, ambiguous, or unsupported, the enforcer MUST deny the request.

### EG-005 — Match protocol, host, and port together

An allow rule MUST match the effective protocol, canonical host or IP
address, and effective port as one tuple. Approval for `https` MUST NOT grant
`http`, approval for port `443` MUST NOT grant another port, and a hostname
rule MUST NOT silently grant an unrelated IP literal.

### EG-006 — Resolve DNS fail closed

If a hostname requires DNS resolution, the enforcer MUST deny the connection
when resolution fails, returns no usable answer, exceeds its freshness limit,
or cannot be evaluated against the active rule. DNS failure MUST NOT fall back
to a cached or previously approved answer without a valid freshness and
binding check.

### EG-007 — Re-authorize every redirect

The enforcer MUST evaluate every redirect target as a new destination before
following it. A redirect MUST NOT inherit approval from its source URL, even
when the source and target share a parent domain.

### EG-008 — Prevent IP-literal and DNS bypasses

The enforcer MUST evaluate IP literals, alternate numeric IP forms, IPv4
embedded in IPv6, and DNS-resolved addresses against the policy. A hostname
allow rule MUST NOT be bypassed by substituting an IP literal, and an IP allow
rule MUST NOT authorize an unrelated hostname.

### EG-009 — Re-authorize proxy tunnels

For an HTTP CONNECT, SOCKS tunnel, service-mesh route, or equivalent proxy
operation, the enforcer MUST authorize both the proxy endpoint and the final
target. A permitted proxy MUST NOT become a general-purpose tunnel to
otherwise denied destinations.

### EG-010 — Bind DNS answers to the connection

The enforcer MUST bind the address selected during policy evaluation to the
connection attempt and MUST deny when the connection resolves or connects to a
different address without a new policy decision. DNS rebinding, answer
rotation, and connection-pool reuse MUST NOT bypass this binding.

### EG-011 — Protect reserved and metadata networks

The enforcer MUST deny loopback, unspecified, link-local, multicast,
broadcast, private, carrier-grade NAT, and cloud or platform metadata
addresses by default. An implementation MAY support a separately governed
internal-network exception, but that exception MUST be explicit, exact,
boundary-scoped, time-bounded, and independently auditable; ordinary public
allow rules MUST NOT grant it.

### EG-012 — Reject ambiguous URL parsing

The enforcer MUST deny destinations containing userinfo, ambiguous authority
syntax, encoded delimiters, invalid percent encoding, control characters,
unsupported Unicode normalization, or parser disagreement between policy and
transport layers.

### EG-013 — Deny unsupported protocols

The enforcer MUST deny protocols that are not explicitly implemented and
listed as policy-matchable. Unknown schemes, protocol upgrades, raw sockets,
UDP, QUIC, WebRTC data channels, and alternate transports MUST NOT be treated
as equivalent to an approved protocol.

### EG-014 — Require secure transport validation

For a policy-approved secure protocol, the enforcer MUST require certificate
and hostname validation according to the platform trust policy. It MUST deny
expired, revoked-when-revocation-is-required, mismatched, untrusted, or
otherwise invalid peer identities, and MUST NOT provide an insecure fallback.

### EG-015 — Separate network approval from authentication

Credentials, API keys, cookies, client certificates, OAuth tokens, signed
requests, or a successful application login MUST NOT grant or broaden network
permission. Network policy evaluation MUST occur before credentials are sent.

### EG-016 — Treat tool-supplied destinations as untrusted

Any destination, URL, host, port, redirect preference, proxy selection, or
transport option supplied by an MCP tool, tool argument, resource, or model
output MUST be treated as untrusted input and MUST pass the same policy
evaluation as any other request.

### EG-017 — Reject invalid policy documents

The enforcer MUST reject a policy that is missing required fields, malformed,
expired, unsupported, internally contradictory, duplicated in a way that
changes meaning, or signed/versioned incorrectly. On rejection, the affected
boundary MUST have no active allow set.

### EG-018 — Apply policy revisions atomically

The enforcer MUST activate a policy revision atomically. It MUST use either
the previous known-valid revision or deny all while loading a new revision,
and MUST NOT expose a partially parsed or partially applied policy.

### EG-019 — Fail closed when enforcement is unavailable

If the policy evaluator, policy store, identity provider, DNS binding layer,
proxy integration, certificate verifier, or required kernel/runtime control
is unavailable, times out, crashes, or returns an indeterminate result, the
enforcer MUST deny the affected request.

### EG-020 — Constrain child processes and helpers

Subprocesses, plugins, interpreters, native libraries, browser helpers,
sidecars, and other processes launched for an MCP operation MUST inherit an
egress boundary no broader than the parent operation. Failure to apply that
boundary MUST cause launch or network access to fail closed.

### EG-021 — Block bypass paths

The enforcement boundary MUST cover direct sockets, connection pools,
redirect handlers, DNS clients, proxy clients, file or URL handlers, and
runtime-specific networking APIs available to the MCP operation. An
unrecognized or uninstrumented network path MUST be denied.

### EG-022 — Enforce bounded use

When a policy specifies request-count, byte, concurrency, duration, DNS
freshness, or rate limits, the enforcer MUST deny the operation when the
limit is missing, invalid, exhausted, or cannot be measured reliably. A limit
check failure MUST NOT degrade into unlimited use.

### EG-023 — Record an auditable decision

For every allow or deny decision, the enforcer MUST record a tamper-evident
event containing policy revision, boundary identity, normalized destination
class, protocol, port, decision, reason code, and timestamp. The event MUST
not contain credentials or full request bodies.

### EG-024 — Protect decision and error telemetry

Logs, metrics, traces, denial messages, and policy diagnostics MUST redact
secrets and sensitive request material, including authorization headers,
cookies, tokens, query values classified as sensitive, and response bodies.
If safe redaction cannot be guaranteed, the telemetry operation MUST omit the
value and the network operation MUST still remain denied when the value is
needed for a decision.

### EG-025 — Make fail-closed conformance a release gate

An implementation MUST provide a conformance record covering every
requirement in EG-001 through EG-024, including positive authorization cases,
negative bypass cases, dependency failures, malformed policies, and
recovery-to-deny behavior. A release MUST be blocked when any requirement is
untested, indeterminate, or observed to fail open.

## 7. Decision flow

For each outbound operation, the enforcement sequence is:

1. Identify the MCP execution boundary and active policy revision.
2. Parse and canonicalize the requested destination.
3. Reject unsupported or ambiguous protocol and authority forms.
4. Resolve names and bind the resulting address when required.
5. Evaluate the complete protocol/host/port/path and network-scope tuple.
6. Validate proxy hops, transport security, and configured limits.
7. Record the decision without sensitive material.
8. Permit the operation only when every required check returns an affirmative
   result; otherwise deny it.
9. Re-evaluate every redirect, new connection, tunnel target, and changed
   destination.

No step may convert an indeterminate result into an allow result.

## 8. Reason codes

Implementations SHOULD use stable, machine-readable reason codes so that
denials can be acted on without exposing sensitive values. At minimum, the
following meanings MUST be distinguishable:

| Code | Meaning |
| --- | --- |
| `NO_ACTIVE_POLICY` | No valid policy is active |
| `NO_MATCHING_ALLOW` | No explicit rule authorizes the destination |
| `INVALID_DESTINATION` | Parsing or canonicalization failed |
| `DNS_UNAVAILABLE` | DNS resolution or freshness check failed |
| `REDIRECT_NOT_ALLOWED` | A redirect target was not authorized |
| `PROXY_TARGET_NOT_ALLOWED` | A proxy or final tunnel target was not authorized |
| `RESERVED_NETWORK` | The destination is in a protected address class |
| `UNSUPPORTED_PROTOCOL` | The transport is not policy-matchable |
| `TRANSPORT_NOT_TRUSTED` | Secure transport validation failed |
| `ENFORCER_UNAVAILABLE` | A required enforcement dependency failed |
| `LIMIT_EXCEEDED` | A configured bound was exhausted or unavailable |
| `POLICY_INVALID` | The policy was malformed, expired, or contradictory |

## 9. Security invariants

The following invariants are non-negotiable:

- No active valid policy means no egress.
- No explicit match means no egress.
- No complete destination identity means no egress.
- No trustworthy enforcement dependency means no egress.
- No safe audit record means no successful decision.
- A prior approval applies only to the exact operation and network path it
  authorized; it is not a blanket grant for future destinations.

## 10. Acceptance criteria

This specification is ready for implementation review only when:

1. A policy schema and precedence model define all fields referenced here.
2. The execution boundary identifies every process and helper covered by
   EG-020 and every network path covered by EG-021.
3. The conformance record maps one or more deterministic checks to each
   EG-001 through EG-025.
4. The audit event schema is finalized without secret-bearing fields.
5. Failure handling demonstrates deny behavior for policy, DNS, proxy, TLS,
   runtime, and telemetry failures.
6. No implementation claims success for a request that was denied or whose
   final destination was not evaluated.

