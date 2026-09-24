# OpenSpec: `gmail_connector(account_id)`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `system-roadmap` / `skill-orchestrator`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define an account-scoped Gmail connector for reading messages, creating drafts,
and sending approved control-plane signals. Gmail is a trigger and lightweight
structured transport; large payloads remain in Drive or another data plane.
`account_id` is mandatory so one mailbox can never be inferred from ambient
session state.

## Context

The repository's Gmail recon defines a reflective fake-MCP bus with subject
tags such as `[MCP-REQ]`, `[MCP-ACK]`, `[MCP-EVENT]`, and bridge-specific
tags. The deterministic-hop rules state that email is wake-only, payloads live
on Drive, every hop has a receipt, and unattended mail is restricted. This
spec makes those rules enforceable at the connector boundary.

## Problem statement

Email is easy to duplicate, misroute, or expose accidentally. A connector
that omits account identity can send from the wrong mailbox; a connector that
puts payloads in the body can leak large or sensitive data; and a connector
that retries blindly can send duplicate control signals.

## Goals

- Read and search messages within an explicit `account_id`.
- Create drafts and send only approved, typed control messages.
- Validate subject tags, recipients, payload pointers, and correlation IDs.
- Support idempotent send recovery and durable receipts.
- Keep body content small, redacted in logs, and free of credentials.

## Non-goals

- Bulk mailbox export, automatic deletion, spam handling, or label policy.
- Sending arbitrary unattended email to third parties.
- Storing large artifacts or conversation histories in Gmail.
- Inferring an account from a default mailbox or sender address.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Calling runtime | Supplies `account_id`, intent, recipient, and correlation ID |
| Gmail provider | Reads, drafts, or sends within that account |
| Drive connector | Hosts heavy payloads referenced by pointer |
| Approval gate | Authorizes external send |
| Receipt store | Records message ID, thread ID, and outcome |

## Requirements

- **GM-001**: `account_id` MUST be required on every operation and MUST be
  resolved to an allowlisted mailbox before provider access.
- **GM-002**: Search and read MUST be account-scoped; thread IDs from another
  account MUST be rejected.
- **GM-003**: Send MUST validate an approved subject grammar and recipient
  policy. Drafting is the default when approval is absent.
- **GM-004**: Control bodies MUST carry `msg_id`, `from`, `to`, `type`,
  `action`, `reply_to_subject` where applicable, and a Drive pointer for
  large payloads.
- **GM-005**: The connector MUST prevent ACK-of-ACK loops and duplicate sends
  for the same `(account_id, msg_id)`.
- **GM-006**: Raw message bodies, attachments, tokens, and personal mailbox
  data MUST be excluded from logs and receipts.
- **GM-007**: Every send or draft MUST return a message/thread reference and a
  durable receipt, including ambiguous outcomes.
- **GM-008**: Unattended external sending, deletion, and bulk operations are
  disabled in BASIC_TIER.

## Scenarios

### Read an account-scoped request

**Given** a valid `account_id` and a known message ID in that account  
**When** the connector reads the message  
**Then** it returns the minimal structured fields and a receipt without
cross-account lookup.

### Create a safe draft

**Given** a valid `[MCP-ACK]` body and no send approval  
**When** a response is requested  
**Then** the connector creates a draft, returns its ID, and does not send.

### Approved send

**Given** a permitted recipient, approved subject tag, and explicit approval  
**When** the send operation runs  
**Then** exactly one message is sent and its provider IDs are receipted.

### Duplicate or ACK-of-ACK

**Given** the same `msg_id` was already processed or the incoming type is
`MCP-ACK` and the proposed response is another ACK  
**When** send is requested  
**Then** it returns `DUPLICATE` or `ACK_LOOP`, sends nothing, and records why.

## Proposed design

Use `resolve_account → parse/validate → approval/draft → provider call →
verify → receipt`. The subject tag and `msg_id` are the routing contract.
Gmail contains the wake signal and pointer; Drive contains heavy artifacts.
Inbound processing is read-only until a separate send approval exists.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `search` | `account_id`, scoped query | message/thread summaries |
| `read` | `account_id`, message ID | minimal normalized message |
| `draft` | `account_id`, typed envelope | draft ID + receipt |
| `send` | account, approved envelope, approval ref | message/thread IDs + receipt |
| `receipt` | `account_id`, `msg_id` | prior outcome |

Stable errors: `INVALID_ACCOUNT`, `INVALID_SUBJECT`, `INVALID_ENVELOPE`,
`RECIPIENT_BLOCKED`, `DUPLICATE`, `ACK_LOOP`, `PERMISSION_DENIED`,
`RATE_LIMITED`, `PROVIDER_UNAVAILABLE`, and `AMBIGUOUS_RESULT`.

## Data model and invariants

The normalized envelope contains `account_id`, `msg_id`, `subject_tag`,
`from`, `to`, `type`, `action`, `payload_ref`, `reply_to_subject`, and
`created_at`. The receipt adds provider message/thread IDs, approval ref,
status, hashes, and timestamps. A `msg_id` is processed once per account;
payload refs are pointers, not inline bulk data.

## Security and privacy

Use account-scoped OAuth with only the required Gmail capabilities. Never put
tokens in prompts, envelopes, or logs. Restrict unattended sending as stated
in the deterministic-hop policy. Apply [`BASIC_TIER`](../BASIC_TIER.md)'s
least-privilege, approval, retry, and receipt rules. Treat mailbox content as
private data and minimize retention.

## Reliability and failure modes

Provider timeouts produce an ambiguous receipt and trigger lookup by
`account_id` + `msg_id` before retry. Rate limits use bounded backoff.
Malformed messages remain unread or quarantined for review; they are not
interpreted by inference. A missing Drive payload blocks downstream work but
does not cause an email resend.

## Observability

Emit `account_resolved`, `message_validated`, `draft_created`, `send_started`,
`send_succeeded`, `send_blocked`, and `receipt_written`. Metrics include
duplicate/ACK-loop suppression, draft-to-send conversion, provider latency,
and pending receipt age. Do not log subjects if they contain user data beyond
the approved tag.

## Testing and acceptance

- Test account isolation, subject parsing, body schema, draft-only mode,
  approved send, duplicate suppression, ACK-loop prevention, timeout
  recovery, and recipient blocking.
- Test that payload bodies never accept oversized artifacts or credentials.
- Acceptance requires all `GM-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Enable read-only search/read first. Enable drafts next, then restrict approved
sends to the designated internal mailbox. Add external recipients only through
a separately reviewed policy. Backout forces draft-only mode; it does not
delete queued drafts or messages.

## Open questions and decisions

- **Decision:** `account_id` is mandatory and never inferred.
- **Decision:** Gmail is wake/receipt transport, not the artifact data plane.
- **Decision:** draft is the safe default when send approval is absent.
- **Open:** finalize the allowlisted subject-tag registry and recipient
  policy for each deployment.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [Gmail fake-MCP bus recon](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/01_Gmail_Fake_MCP_Bus.md)
- [Deterministic hop rules](../../../skill_tree/skills/system-roadmap/references/email-bridge-2026-08-17/03_DETERMINISTIC_HOP.md)
- [Drive staging + GitHub conduit](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
