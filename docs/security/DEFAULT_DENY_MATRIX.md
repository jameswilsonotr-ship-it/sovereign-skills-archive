# Default-Deny Matrix

**Status:** normative
**Scope:** offline execution only

This policy governs SMS, flashlight, and MCP capability surfaces. Every
operation is denied unless an exact, local policy entry permits it. A missing,
unknown, stale, malformed, or unavailable policy is a denial.

## Non-negotiable invariants

1. **Default deny:** absence of an explicit allow is not permission.
2. **Fail closed:** uncertainty, errors, timeouts, partial state, and
   unavailable dependencies produce no side effect.
3. **Offline only:** live network transports, remote services, modem access,
   credential lookup, and secret injection are out of scope and denied.
4. **Atomic gate:** policy evaluation and the side effect are one decision.
   Nothing may happen before the decision is explicitly allowed, and a
   partially completed decision is treated as denied.
5. **No inference:** do not widen scope from a similar surface, tool, target,
   or prior request.

## Matrix

| Surface | Default | Only permitted when | Fail-closed response |
| --- | --- | --- | --- |
| **SMS — send** | Deny | A local test fixture is named by an explicit allow entry with an exact recipient, exact message class, and bounded lifetime. | Do not queue, transmit, retry, or fall back to another transport. |
| **SMS — receive or poll** | Deny | A local, pre-recorded fixture is explicitly selected for offline parsing. | Do not open a modem, network connection, inbox, or webhook. Return no live-message result. |
| **Flashlight — hardware control** | Deny | A local policy explicitly names the device, operation, and duration; the request is local and within the stated bound. | Leave hardware unchanged. Do not retry or substitute another device. |
| **Flashlight — fixture/simulation** | Deny | A named local fixture is explicitly allowed for a test. | Keep the fixture unchanged and report the denial locally. |
| **MCP — discovery or connection** | Deny | A named local fixture/server is explicitly allowlisted and the transport is local-only. | Do not discover, connect, reconnect, or fall back to a remote server. |
| **MCP — tool call** | Deny | The server, tool, operation, input schema, and scope exactly match a local allow entry. | Do not invoke, retry, substitute, or interpret an incomplete response as success. |

An allow entry must identify, at minimum: `surface`, `operation`, `target`,
`scope`, `input constraints`, `expiry`, and `offline-only: true`. An allow entry
that omits any of these fields is invalid and therefore denied.

## Decision procedure

For every request:

1. Parse the request without executing any capability.
2. Load the local policy without fetching or resolving anything remotely.
3. Match the complete request against one valid, unexpired allow entry.
4. Verify that all dependencies remain local and that inputs satisfy the
   entry's constraints.
5. Execute only after the allow decision is committed for that request.
6. On any error before or during execution, stop and return a local denial or
   failure result. Never convert an error into permission.

Unknown fields, unknown operations, wildcard targets, implicit recipients,
missing expiry, and policy parse errors must not be normalized into an allow.

## Local audit requirements

Record denied decisions locally with the surface, operation, target class,
decision (`deny`), and reason. Do not record message bodies, credentials,
tokens, API keys, or other secret material. Audit logging must not require a
network connection; if local logging is unavailable, the capability remains
denied.

## Minimum offline checks

The following cases must remain denied:

- an SMS request with no matching fixture or with a live recipient;
- a flashlight request with an unknown device or unbounded duration;
- an MCP request for an unknown server, tool, schema, or remote transport;
- any request after policy expiry, parse failure, timeout, or dependency loss;
- any request that would require a secret, network access, retry fallback, or
  partial side effect.
