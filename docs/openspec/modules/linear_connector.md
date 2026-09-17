# OpenSpec: `linear_connector`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `system-roadmap` / `olivia-dev-alpha`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define a bounded Linear connector for discovering, reading, and updating
work-tracking issues. It maps external issue state to local work-queue
receipts without making Linear the authority for repository truth or
autonomously changing priority, ownership, or workflow policy.

## Context

The repository uses Markdown work-queue items with explicit status vocabulary,
owners, and item-file presence. Linear can provide an external planning
surface, but synchronization must be additive and traceable. This spec
protects local queue discipline while allowing a scoped issue bridge.

## Problem statement

Issue synchronization becomes unsafe when titles are treated as stable IDs,
state changes are copied without authorization, or retries create duplicate
issues. The connector needs stable identifiers, team/project scope, explicit
field mapping, and human review for externally visible mutations.

## Goals

- Search and read issues, projects, teams, and workflow states in an
  allowlisted workspace.
- Create or update one issue with explicit field mapping and receipt.
- Link a Linear issue to a local work-queue item without copying secrets or
  whole histories.
- Suppress duplicate creates using a stable external idempotency key.
- Keep destructive operations disabled at BASIC_TIER.

## Non-goals

- Deleting issues, changing workspace settings, or modifying permissions.
- Autonomous priority, estimate, assignment, or SLA decisions.
- Mirroring every comment, attachment, or private team field.
- Replacing local Markdown work-queue files or GitHub review state.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Queue owner | Approves create/update intent and field mapping |
| Linear connector | Reads/writes scoped issue fields |
| Local work queue | Remains authoritative for local status and item presence |
| Receipt store | Records Linear issue ID and applied field set |
| Human reviewer | Resolves conflicting state or ownership |

## Requirements

- **LN-001**: Every request MUST include workspace/team scope, operation,
  actor, idempotency key, and explicit field allowlist.
- **LN-002**: Reads MUST use stable issue IDs when available; title search is
  discovery only and MUST NOT be used as a write target.
- **LN-003**: Create MUST require team and workflow state and MUST reject
  ambiguous matches.
- **LN-004**: Updates MUST use an expected version or last-seen timestamp and
  return `STALE_ISSUE` when the remote issue changed.
- **LN-005**: Only approved fields may be changed: title, description,
  assignee, project, labels, priority, and state as individually enabled.
- **LN-006**: Delete, archive, workspace-wide bulk updates, and comment posting
  are disabled in BASIC_TIER.
- **LN-007**: Receipts MUST include issue ID, applied fields, old/new values
  where safe, and provider revision.
- **LN-008**: Personal data and private descriptions MUST be redacted from
  logs; tokens MUST never be logged.

## Scenarios

### Discover an issue

**Given** a permitted team and a title or identifier  
**When** a read request is made  
**Then** the connector returns stable IDs and minimal metadata without
mutating Linear.

### Create a linked issue

**Given** an approved local work-queue item and an unambiguous team/state  
**When** the idempotency key has no prior result  
**Then** one issue is created, linked to the local item, and receipted.

### Concurrent update

**Given** a caller's last-seen issue revision is stale  
**When** an update is submitted  
**Then** no field changes are applied and `STALE_ISSUE` is returned for review.

### Duplicate create retry

**Given** a provider response was lost after issue creation  
**When** the same request is retried  
**Then** the connector finds the issue by idempotency marker and returns its
ID without creating a second issue.

## Proposed design

Use `scope → resolve ID → read revision → approval → mutate allowlisted fields
→ verify → receipt`. Store the local-to-Linear mapping in a small receipt
record, not in the issue body alone. A sync job may propose changes, but a
human or higher-tier policy must authorize them.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `search` | workspace/team, query | candidate issue IDs |
| `get` | issue ID | minimal issue projection + revision |
| `create` | team, title, state, idempotency key | issue ID + receipt |
| `update` | issue ID, expected revision, field patch | applied fields + receipt |
| `link` | local item ID, issue ID | durable mapping receipt |

Stable errors: `INVALID_SCOPE`, `AMBIGUOUS_MATCH`, `NOT_FOUND`,
`PERMISSION_DENIED`, `STALE_ISSUE`, `DUPLICATE`, `RATE_LIMITED`,
`PROVIDER_UNAVAILABLE`, and `UNSUPPORTED_MUTATION`.

## Data model and invariants

The mapping records `local_item_id`, `linear_issue_id`, workspace/team IDs,
source hash, last-seen provider revision, approved fields, actor, status, and
timestamps. Local status is not overwritten by a remote state without an
explicit mapping. Every mutation has one receipt and one idempotency key.

## Security and privacy

Use a workspace/team-scoped token with only issue read/write capability.
Allowlist teams and projects. Do not put credentials, private descriptions, or
full comment histories in prompts or logs. Apply the approval and receipt
requirements in [`BASIC_TIER`](../BASIC_TIER.md); no delete or archive call is
allowed.

## Reliability and failure modes

Rate limits use provider-directed backoff. A stale revision stops the write
instead of overwriting remote changes. Ambiguous creates resolve by
idempotency marker before retry. If the provider is unavailable, the local
item remains unchanged and the connector records a pending sync state.

## Observability

Emit `scope_checked`, `issue_resolved`, `mutation_approved`,
`mutation_applied`, `stale_rejected`, and `receipt_written`. Track duplicate
suppression, stale conflicts, latency, rate limits, and pending mappings.
Values in logs are IDs or redacted summaries only.

## Testing and acceptance

- Contract-test search, create, update, stale revision, duplicate retry, and
  permission failure against a fake Linear API.
- Verify disallowed fields and destructive operations fail closed.
- Verify local queue state is unchanged when a remote mutation is rejected.
- Acceptance requires all `LN-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Deploy read-only discovery first, then create-only linking for one team.
Enable updates field-by-field behind a feature flag. Backout disables writes
and leaves mapping receipts available for manual reconciliation. No bulk
backfill is implied by this spec.

## Open questions and decisions

- **Decision:** local Markdown work-queue files remain authoritative locally.
- **Decision:** issue title is never a write identifier.
- **Open:** map the repository's status vocabulary to each Linear team's
  workflow states.
- **Open:** choose whether links belong in a dedicated metadata store or a
  generated local sidecar.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [ICM / work-queue recon and status vocabulary](../../../skill_tree/skills/system-roadmap/references/research/icm-harness-recon-2026-09-10/ICM_HARNESS_RECON_2026-09-10.md)
- [Adding a connector](../../../skill_tree/skills/system-roadmap/connectors/add-connector.md)
- [System architecture target](../../../skill_tree/skills/system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md)
