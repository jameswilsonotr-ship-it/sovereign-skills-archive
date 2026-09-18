# SPEC-011: Composio Account Bind

Status: **draft — specification only**

This specification defines the contract for binding a Composio-connected
account to an approved execution context. It does not implement a connector,
authorize a provider, or claim that a live Composio account is available.

No credential, token, cookie, API key, private endpoint, personal address, or
real account identifier belongs in this repository. Examples use placeholders
only.

## Scope

The bind is the controlled boundary between:

- an operator-approved principal and tenant;
- a Composio connection;
- an explicitly requested provider account; and
- the narrowly scoped tools that may run through that connection.

The bind covers discovery, authorization handoff, validation, use, expiry,
revocation, and secret-free receipts. Provider-specific consent screens and
Composio transport details remain implementation concerns.

## Terms

- **Principal**: the human or service identity requesting the bind.
- **Tenant**: the workspace or organizational boundary that owns the request.
- **Connection**: Composio's provider-account connection record.
- **Bind**: the short-lived authorization record that permits a declared set
  of actions through one connection.
- **Capability**: a named provider operation or tool action.
- **Receipt**: a secret-free record of the bind outcome.

## Normative requirements

### CB-001 — Require an execution identity

Every bind request MUST identify an authenticated principal and tenant in the
host system. An email address, access token, cookie, or provider credential
MUST NOT be used as a substitute for the host identity.

### CB-002 — Require explicit bind intent

A bind MUST be initiated by an explicit operator or an already authorized
workflow. A page visit, tool discovery result, failed request, or inferred
account match MUST NOT create a bind.

### CB-003 — Keep authorization at the Composio boundary

Provider authorization MUST be delegated to Composio's supported connection
flow. The caller MUST NOT collect, persist, echo, or forward provider
passwords, OAuth codes, refresh tokens, cookies, or API keys.

### CB-004 — Bind one declared account

A successful bind MUST resolve to exactly one declared provider and one
connection. If discovery returns zero or multiple candidates, the bind MUST
remain unbound and require explicit selection; it MUST NOT guess.

### CB-005 — Use an opaque bind identifier

Each bind MUST receive a unique, non-secret `bind_id`. The identifier MUST be
safe for logs and correlation, and MUST NOT encode a credential, token,
authorization code, or private account data.

### CB-006 — Minimize account identity disclosure

Responses and receipts MUST expose only the minimum account metadata needed for
operator confirmation and later correlation. Provider account names, email
addresses, phone numbers, and external identifiers MUST be redacted or
represented by an opaque display label unless disclosure is explicitly
required by the host policy.

### CB-007 — Match provider and environment exactly

The bind request MUST declare the expected provider and environment, such as
production or test. A connection for another provider, tenant, environment, or
region MUST fail closed with an actionable mismatch result.

### CB-008 — Require an allowlisted capability set

A bind MUST declare the capabilities it permits. An empty, wildcard, or
provider-wide capability set MUST NOT be treated as approval. Capability names
MUST be normalized before comparison, and unknown names MUST be rejected.

### CB-009 — Enforce tool and action scope at execution time

Every operation using a bind MUST be checked against the bind's capability
allowlist, principal, tenant, provider, and environment. A successful bind
MUST NOT grant permission to newly discovered tools without a new consent and
validation step.

### CB-010 — Bound lifetime MUST be explicit

A bind MUST include an explicit expiration time and issuance time. The runtime
MUST reject an expired bind before dispatching an operation. Renewal MUST
revalidate identity, connection state, provider, environment, and capabilities;
it MUST NOT silently extend an old authorization.

### CB-011 — Revocation MUST take effect before dispatch

The host MUST support revoking or unbinding a connection. Revocation MUST
prevent new operations from dispatching, even if a cached bind has not
expired. In-flight operation handling MUST follow the provider and host
shutdown policy and MUST never be reported as canceled unless cancellation was
verified.

### CB-012 — Bind requests MUST be idempotent

A caller MAY retry the same bind request using an idempotency key. Repeating a
request with the same key and unchanged security context MUST return the same
result or a stable in-progress status. Reusing a key with different principal,
tenant, provider, connection, environment, or capabilities MUST be rejected.

### CB-013 — Binding MUST be atomic

A bind is successful only when identity, tenant, connection, provider,
environment, capability, lifetime, and revocation checks all pass. The system
MUST NOT publish a partially valid bind, such as a bind with a connection but
without its capability set. On failure, no usable bind MUST remain.

### CB-014 — Do not confuse discovery with authorization

Listing providers, connections, or tools MUST NOT authorize their use.
Discovery results MUST be treated as untrusted metadata until the operator
selects the intended connection and the complete bind validation succeeds.

### CB-015 — Record consent without sensitive content

The bind record MUST retain a timestamp, principal reference, tenant reference,
provider, opaque connection reference, capability set, policy/version
reference, and consent source sufficient for audit. It MUST NOT retain
credentials, authorization codes, raw provider responses, message bodies, file
contents, or unnecessary personal data.

### CB-016 — Return stable, secret-free outcomes

A bind response MUST identify a status and `bind_id` when one exists. It MAY
include redacted provider and capability summaries. It MUST NOT include
tokens, authorization headers, cookies, signed URLs, private endpoint details,
or raw Composio/provider error payloads.

The minimum status vocabulary is:

- `bound`: all checks passed and the bind may be used;
- `pending_consent`: operator authorization is required;
- `rejected`: authorization or policy denied the request;
- `mismatch`: the selected connection does not match the declaration;
- `expired`: a previously valid bind is no longer usable;
- `revoked`: the bind or connection was explicitly disabled;
- `unavailable`: Composio or the provider could not be reached; and
- `unknown`: the outcome could not be established safely.

### CB-017 — Fail closed on uncertainty

Timeouts, transport interruptions, malformed responses, provider account
changes, and unverifiable consent MUST NOT produce a `bound` result. The
caller MUST surface `unknown` or a more specific non-bound status and require
reconciliation before dispatching sensitive work.

### CB-018 — Limit retries and prevent replay

The implementation MUST NOT automatically retry authorization, revocation, or
an uncertain bind outcome without an idempotency key and policy approval.
Authorization codes and other one-time artifacts MUST be single-use and MUST
never be placed in logs, URLs, fixtures, or receipts.

### CB-019 — Keep fixtures and observability synthetic

Documentation, tests, logs, traces, screenshots, and examples MUST use
synthetic principals, tenants, connection references, capability names, and
provider data. Redaction MUST occur before persistence or export. A check that
detects a secret-like value MUST fail the operation rather than silently
publishing it.

### CB-020 — Make acceptance atomic and auditable

A Composio account-bind implementation is conformant only when it can
demonstrate, using synthetic data, that:

1. explicit intent and host identity are required;
2. one exact connection is selected without guessing;
3. provider, tenant, environment, and capability checks are enforced;
4. no credential crosses the host boundary or appears in output;
5. partial validation never produces a usable bind;
6. expiry and revocation block dispatch;
7. idempotent repeats do not create duplicate binds; and
8. every terminal result is represented by a secret-free receipt.

Passing individual checks MUST NOT be interpreted as a successful bind when
any other required check is missing or unresolved.

## Abstract bind record

The following fields define the shape of the contract without prescribing a
transport or storage system:

```text
BindRequest
  request_id: OPAQUE_REQUEST_ID
  idempotency_key: OPAQUE_IDEMPOTENCY_KEY
  principal_ref: SYNTHETIC_PRINCIPAL
  tenant_ref: SYNTHETIC_TENANT
  provider: PROVIDER_NAME
  environment: test | production
  connection_ref: SELECTED_CONNECTION_REF
  capabilities: [EXACT_ALLOWLIST]
  requested_expires_at: TIMESTAMP
  consent_source: operator | approved_workflow

BindReceipt
  status: bound | pending_consent | rejected | mismatch | expired
          | revoked | unavailable | unknown
  bind_id: OPAQUE_BIND_ID
  provider: PROVIDER_NAME
  capability_summary: REDACTED_ALLOWLIST_SUMMARY
  issued_at: TIMESTAMP
  expires_at: TIMESTAMP
  policy_ref: POLICY_VERSION
  reason_code: SECRET_FREE_REASON
```

`BindRequest` and `BindReceipt` are contract shapes, not executable schemas.
`connection_ref`, `principal_ref`, `tenant_ref`, and all opaque identifiers
above are placeholders and MUST be replaced only at runtime by the approved
secret-safe integration.

## State model

```text
unbound
  └─ explicit request ──> pending_consent
       ├─ rejected/mismatch ──> unbound
       ├─ consent + validation ──> bound
       └─ unavailable/uncertain ──> unknown

bound
  ├─ expiry ──> expired
  ├─ explicit revoke ──> revoked
  ├─ provider disconnect ──> revoked
  └─ approved renewal ──> bound
```

Only `bound` permits a new operation to be dispatched. `unknown` MUST be
reconciled before reuse; it MUST NOT be treated as either success or failure
by inference.

## Security boundary

The repository contains only this specification and synthetic examples. Live
Composio configuration belongs in the deployment's approved secret manager
and environment configuration. Any future implementation MUST document its
secret storage, redaction, audit retention, and operator-revocation behavior
before claiming conformance to SPEC-011.
