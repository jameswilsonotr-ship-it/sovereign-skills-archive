# SPEC-016 — MCP Tool Allowlist

Status: **Draft**

This specification defines the security boundary for Model Context Protocol
(MCP) tool invocation. It is a policy contract only; it does not implement an
MCP client, server, registry, or enforcement middleware.

## 1. Decision

MCP tools are **default-deny**. A tool may run only when its fully qualified
identifier is present in an explicit, active grant for the current principal,
session, and scope. Discovery, advertisement, successful connection, or
historical use does not constitute a grant.

The allowlist is evaluated per invocation. A request that contains multiple
tools is not partially authorized: every tool must pass independently, and a
failed decision denies the failed invocation without creating an implicit
grant for subsequent calls.

## 2. Terminology

- **Tool identifier** — the canonical, fully qualified MCP identifier
  `<server-id>/<tool-name>`. Aliases, display names, and descriptions are not
  authorization identifiers.
- **Grant** — an explicit policy record allowing one canonical tool identifier
  for a named principal, bounded scope, and stated lifetime.
- **Default-deny** — absence of a matching grant produces a denial.
- **Sensitive tool** — any tool covered by AL-003 through AL-020.
- **Policy owner** — the human or control-plane authority permitted to issue or
  revoke grants. An MCP server cannot grant access to its own tools.

## 3. Authorization invariants

1. No wildcard, prefix, server-wide, or “all tools” grant is valid for the
   controls in this specification.
2. Every grant names a canonical server and tool, principal, resource scope,
   expiration, and approving policy owner.
3. The evaluator fails closed when the tool identifier, server identity,
   principal, scope, grant, or policy state cannot be resolved.
4. Tool arguments are evaluated against the grant scope before execution.
   Arguments must not expand the granted scope.
5. A tool rename, server identity change, schema change, or capability change
   invalidates the affected grant until it is reviewed and reissued.
6. Denials are side-effect free. A denied request must not execute the tool,
   enqueue deferred work, or trigger a fallback tool.
7. Every decision records the canonical identifier, principal, decision,
   policy version, grant reference or denial reason, and timestamp. Arguments
   and results are recorded only under a separate data-minimization policy.
8. Revocation takes effect before the next invocation and does not depend on
   the MCP server acknowledging the revocation.

## 4. Default-deny controls

The following controls are normative. Each `AL-*` entry identifies a tool
family that is denied unless explicitly granted under this specification.

| ID | Default-deny tool family | Required policy boundary |
| --- | --- | --- |
| **AL-001** | Unknown, unregistered, or unresolvable tools | Deny before schema fetch or execution; do not infer identity from a description. |
| **AL-002** | Tools served by an untrusted, unverified, or changed MCP server | Require a verified server identity and reviewed capability manifest. |
| **AL-003** | Filesystem reads outside the declared workspace or resource scope | Require an approved path scope; deny traversal, symlink escape, and path re-resolution outside it. |
| **AL-004** | Filesystem creation or modification, including writes and patches | Require an exact writable path scope and an explicit mutation grant. |
| **AL-005** | File or directory deletion, move, overwrite, or permission change | Require an explicit destructive-action grant; confirmation is not implied by a write grant. |
| **AL-006** | Shell, command, process, script, or interpreter execution | Require an approved executable, argument policy, working directory, and resource limits. |
| **AL-007** | Package installation, dependency resolution, build hooks, or toolchain mutation | Require an approved package source, package set, lockfile policy, and execution scope. |
| **AL-008** | Outbound network requests, URL fetches, webhooks, and remote API calls | Require an approved destination, method, data class, and egress scope. |
| **AL-009** | Listening sockets, port binding, tunneling, proxying, or inbound network exposure | Require an approved bind address, port, duration, and exposure policy. |
| **AL-010** | Access to secrets, credentials, tokens, cookies, private keys, or key stores | Deny by default even when a tool can read the containing file or environment. |
| **AL-011** | Environment, runtime, host, or deployment configuration reads | Require an explicit named-variable or named-resource scope; blanket environment dumps are denied. |
| **AL-012** | Browser control, authenticated sessions, screen capture, or UI automation | Require an approved origin, session, action class, and handling policy for visible data. |
| **AL-013** | Sending, replying to, forwarding, or publishing external communications | Require an approved channel, recipient scope, content class, and send confirmation policy. |
| **AL-014** | Uploading, sharing, exporting, or changing permissions in external storage | Require an approved destination, audience, data class, and sharing lifetime. |
| **AL-015** | Source-control mutation, including commit, push, branch deletion, merge, or tag changes | Require an approved repository, branch/ref scope, and operation-specific grant. |
| **AL-016** | CI/CD, deployment, release, rollback, or production-environment operations | Require an approved project, environment, change window, and rollback authority. |
| **AL-017** | Database writes, schema changes, migrations, bulk exports, or queue mutations | Require an approved data store, operation class, transaction scope, and row/data boundary. |
| **AL-018** | Payments, purchases, refunds, transfers, billing, or other financial actions | Require an approved account, transaction limit, beneficiary scope, and human approval where applicable. |
| **AL-019** | Identity, access-control, organization, tenant, or administrator operations | Require an approved target, role/permission delta, duration, and elevated approval. |
| **AL-020** | Tool registration, capability expansion, policy mutation, or allowlist changes | Deny to runtime tools; changes must be made by the policy owner through a separately protected control plane. |

## 5. Grant requirements

An implementation conforming to this specification MUST:

- match grants on the canonical server identity and exact tool name;
- bind each grant to a principal and a minimum necessary resource scope;
- require an expiration or explicit revocation mechanism;
- distinguish read, write, destructive, communication, and administrative
  operation classes;
- validate argument scope before invoking the MCP tool;
- expose a deterministic denial reason without exposing secrets; and
- retain an auditable decision receipt for both allow and deny outcomes.

An implementation MUST NOT:

- treat a tool's `readOnly`, `safe`, or descriptive metadata as permission;
- inherit permission from a different server, principal, session, or tool;
- convert a denied call into a different tool call;
- permit a server to self-approve, self-register, or broaden its grant; or
- persist credentials or authorization tokens in tool arguments, logs, or
  receipts.

## 6. Decision order

The evaluator MUST apply these checks in order:

1. Resolve the caller principal and canonical MCP server identity.
2. Resolve the exact tool identifier and its current capability/schema version.
3. Classify the tool against AL-001 through AL-020.
4. Load the current policy and matching grant.
5. Validate grant lifetime, principal, server identity, operation class, and
   argument/resource scope.
6. Emit the decision receipt.
7. Invoke the tool only after an allow decision.

Any unresolved check is a denial. Enforcement must not rely on a post-call
audit to compensate for a pre-call authorization failure.

## 7. Denial and review behavior

The denial response SHOULD identify the failed `AL-*` control, canonical tool
identifier, and missing or invalid grant reference. It MUST NOT disclose
secret values, hidden policy data, or inaccessible resource names.

Policy owners may review a denial and issue a narrower grant. A denial must not
be retried automatically with broader permissions, a different server, or a
different tool.

## 8. Non-goals

This specification does not define:

- an MCP transport or authentication protocol;
- a particular policy file, database, SDK, or deployment topology;
- the user-interface wording for confirmations;
- data-retention periods beyond requiring auditable decisions; or
- an implementation-time exception for emergency or “trusted” tools.

## 9. Acceptance criteria

- [ ] A tool absent from the active grant set is denied.
- [ ] All 20 controls, AL-001 through AL-020, are represented in policy
      classification and review documentation.
- [ ] Exact tool identity is required; aliases and wildcards do not authorize.
- [ ] Scope, arguments, principal, lifetime, and server identity are checked
      before execution.
- [ ] Unknown, stale, unavailable, or conflicting policy state fails closed.
- [ ] Denied calls have no tool side effect and produce a secret-free reason.
- [ ] Allow and deny decisions produce auditable, secret-minimized receipts.
- [ ] AL-020 changes cannot be made by an ordinary runtime tool invocation.

