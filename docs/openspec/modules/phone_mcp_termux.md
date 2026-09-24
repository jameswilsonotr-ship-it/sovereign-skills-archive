# OpenSpec: `phone_mcp_termux`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `mcp-surface` / `system-roadmap`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define a local MCP boundary for Android Termux phone capabilities. The module
exposes explicit, auditable operations such as device health, notification
read, and approved SMS intent handoff without turning a phone into an
unbounded remote shell or unattended communications agent.

## Context

The architecture favors local-first, least-privilege MCP surfaces, phone-off
capability, and explicit human gates for high-impact actions. A Termux
endpoint is intermittently connected and may be on cellular data, so requests
must be queued safely and receipts must distinguish accepted, delivered, and
unknown states.

## Problem statement

Phone automation mixes sensitive data, unreliable connectivity, and
irreversible side effects. Without a narrow command set and device-bound
authentication, an MCP client could execute arbitrary shell commands or send
messages from the wrong device.

## Goals

- Provide a device-bound MCP transport over a local or explicitly tunneled
  endpoint.
- Expose health and read-only capabilities first.
- Gate SMS or other external actions with explicit approval and idempotency.
- Queue safely across disconnects without claiming delivery.
- Record redacted, durable receipts for every request.

## Non-goals

- Arbitrary shell, package installation, filesystem browsing, or root access.
- Silent phone calls, SMS, purchases, or account changes.
- Bypassing Android permissions, lock state, carrier controls, or user consent.
- Treating queued as sent or sent as delivered.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| MCP client | Calls the allowlisted tool surface |
| Termux adapter | Validates and executes approved local operations |
| Android permission layer | Grants or denies device capability |
| Human approver | Authorizes external communication |
| Receipt queue | Persists outcome across disconnects |

## Requirements

- **PT-001**: The server MUST bind to loopback by default; any tunnel or LAN
  exposure MUST use device-bound authentication and explicit configuration.
- **PT-002**: The tool list MUST be an allowlist. No generic shell or eval tool
  may be exposed.
- **PT-003**: Every request MUST include device ID, request ID, operation,
  expiry, and idempotency key.
- **PT-004**: Read operations MUST be available without write permissions;
  outbound messaging MUST require explicit approval.
- **PT-005**: Queue state MUST distinguish `accepted`, `queued`, `sent`,
  `delivered`, `failed`, and `unknown`.
- **PT-006**: The adapter MUST fail closed when Android permissions, device
  identity, or transport authentication is missing.
- **PT-007**: Logs MUST omit message bodies, contact books, tokens, and
  notification contents unless a redacted diagnostic is explicitly requested.
- **PT-008**: The server MUST provide a stop/disable control that prevents new
  side effects and leaves receipts intact.

## Scenarios

### Device health

**Given** a device-authenticated MCP client  
**When** it requests health  
**Then** the server returns connectivity, permission, queue, and software
version status without exposing arbitrary device data.

### Disconnected SMS request

**Given** an approved SMS intent and an offline phone  
**When** the request arrives  
**Then** it is queued with `queued` status and is not reported as sent.

### Reconnected send

**Given** a queued request with an unexpired idempotency key  
**When** the phone reconnects  
**Then** it sends at most once, records provider/device acknowledgment, and
reports delivery only if the phone explicitly confirms it.

### Unauthorized command

**Given** an MCP call naming an operation outside the allowlist  
**When** the adapter receives it  
**Then** it returns `UNSUPPORTED_OPERATION` and executes nothing.

## Proposed design

The adapter has four layers: authenticated transport, typed tool router,
Android capability wrapper, and append-only receipt queue. Termux APIs are
implementation details behind typed operations. A watchdog can disable writes
on repeated auth or permission failures.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `health` | device auth | capability and queue status |
| `permissions` | device auth | allowlisted permission state |
| `notifications_read` | scope, limit | redacted notification records |
| `sms_prepare` | recipient, body, expiry | preview + approval token |
| `sms_send` | approval token, idempotency key | queue/send receipt |
| `queue_status` | request or device ID | current delivery state |
| `disable_writes` | operator approval | disabled state + receipt |

Stable errors: `UNAUTHENTICATED`, `WRONG_DEVICE`, `UNSUPPORTED_OPERATION`,
`PERMISSION_DENIED`, `EXPIRED`, `DUPLICATE`, `OFFLINE`, `CARRIER_FAILURE`,
and `UNKNOWN_OUTCOME`.

## Data model and invariants

Requests include device ID, operation, expiry, approval reference, and
idempotency key. Receipts include queue ID, operation, recipient hash,
state, timestamps, and redacted provider response. Message bodies are held
only in the protected adapter queue for the minimum required retention.
`queued` never implies `sent`; `sent` never implies `delivered`.

## Security and privacy

Use device-bound keys, short-lived session credentials, and loopback binding
by default. Store secrets in Termux/Android protected storage, not repository
files or prompts. Apply [`BASIC_TIER`](../BASIC_TIER.md)'s approval, retry,
receipt, and logging requirements. Never expose a shell escape or broad
filesystem tool.

## Reliability and failure modes

The phone may disappear, reboot, lose carrier service, or revoke permissions.
Requests expire rather than sending late. Ambiguous provider responses are
`unknown` and require device-side lookup before retry. Queue corruption
disables writes and preserves the last verified receipt.

## Observability

Emit `authenticated`, `capability_checked`, `request_queued`,
`request_sent`, `delivery_confirmed`, `request_failed`, and `writes_disabled`.
Track uptime, reconnects, queue depth, expired requests, and unknown outcomes.
All event fields are IDs, states, and timings; content is excluded.

## Testing and acceptance

- Test loopback auth, wrong-device rejection, allowlist enforcement, permission
  denial, offline queueing, expiry, duplicate retry, and unknown outcomes.
- Run an Android/Termux integration test with a fake carrier or SMS adapter.
- Prove `disable_writes` prevents side effects while reads remain available.
- Acceptance requires all `PT-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Ship a read-only health/permission server first. Add notification reads,
then prepare-only SMS, and finally approved sends. Keep the endpoint local
until device-bound auth and queue recovery are verified. Backout disables
write tools and drains no existing queue automatically.

## Open questions and decisions

- **Decision:** no arbitrary Termux shell tool.
- **Decision:** delivery state is reported only from explicit device/provider
  acknowledgment.
- **Open:** choose the transport (loopback HTTP, Unix socket bridge, or
  explicitly authenticated tunnel).
- **Open:** finalize protected queue retention and Android notification scopes.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [MCP surface policy](../../../skill_tree/skills/mcp-surface/SKILL.md)
- [Sovereign bridge security rules](../../../skill_tree/skills/mcp-surface/references/modules/sovereign-bridge/SKILL.md)
- [Adding a connector](../../../skill_tree/skills/system-roadmap/connectors/add-connector.md)
