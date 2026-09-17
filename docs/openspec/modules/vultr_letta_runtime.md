# OpenSpec: `vultr_letta_runtime`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `claim-runtime` / `system-roadmap`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define a small Vultr-hosted runtime boundary for a Letta-compatible agent
service. The runtime separates hot/core memory, searchable recall, and cold
archival references; exposes health and session operations; and treats Vultr
infrastructure as an execution host rather than the authority for identity,
policy, or long-term canon.

## Context

The repository's Letta notes distinguish Core (always in context), Recall
(searchable conversation history), and Archival (semantic long-term store).
They also warn that cold memory must not rewrite hot identity without a gate.
This spec captures a deployable runtime shape while keeping local skills and
Drive as external, receipted surfaces.

## Problem statement

A hosted agent runtime can lose state, overfill context, expose a management
port, or let retrieval rewrite identity. The deployment needs explicit
network boundaries, durable session semantics, backup/restore behavior, and
memory-tier invariants.

## Goals

- Run a Letta-compatible service on a scoped Vultr instance or equivalent.
- Keep Core memory small, explicit, and protected from archival auto-rewrites.
- Provide authenticated session, health, and controlled memory operations.
- Persist durable state with encrypted backups and tested restore.
- Make runtime changes observable and reversible.

## Non-goals

- Designing a new Letta memory algorithm or replacing provider semantics.
- Exposing the management plane to the public internet.
- Autonomous promotion of arbitrary retrieved text into Core memory.
- Treating a single Vultr instance as the only copy of canonical data.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Vultr host | Compute, firewall, volume, and lifecycle boundary |
| Letta-compatible service | Session and memory APIs |
| Secret store | Supplies runtime credentials without baking them into images |
| Backup store | Holds encrypted database and configuration backups |
| Connector layer | Provides receipted Drive/GitHub/Gmail access when enabled |

## Requirements

- **VL-001**: The service MUST bind behind a private network, firewall, or
  authenticated reverse proxy; management ports MUST not be public.
- **VL-002**: Deployment MUST be reproducible from a pinned image/config and
  MUST expose a health check that does not reveal secrets.
- **VL-003**: Core, Recall, and Archival stores MUST have distinct access
  policies and retention behavior.
- **VL-004**: Archival retrieval MUST be advisory; it MUST NOT rewrite Core
  identity or policy without explicit approval.
- **VL-005**: Session writes MUST be idempotent or carry a monotonic event
  sequence so reconnects cannot duplicate turns.
- **VL-006**: Backups MUST be encrypted, versioned, restorable, and tested
  without exposing message content in logs.
- **VL-007**: Runtime updates MUST use a staged rollout and retain a known-good
  image/config for backout.
- **VL-008**: Follow [`BASIC_TIER`](../BASIC_TIER.md); no provider credential,
  destructive infrastructure operation, or cross-tenant access is implied.

## Scenarios

### Start a session

**Given** an authenticated caller and a valid agent/session ID  
**When** the runtime receives a session-start request  
**Then** it returns a session handle and current Core revision without exposing
raw archival data.

### Recall without identity rewrite

**Given** a prompt requires historical context  
**When** Recall or Archival returns candidates  
**Then** the runtime labels them as retrieved context and leaves Core unchanged
unless an approved memory write is made.

### Instance replacement

**Given** the Vultr instance is lost  
**When** an operator provisions the pinned replacement  
**Then** the latest verified backup restores sessions and memory with a receipt,
or the runtime remains read-only if verification fails.

### Stale session retry

**Given** a client retries after a network disconnect  
**When** the event sequence was already committed  
**Then** the runtime returns the prior result and does not append a duplicate
event.

## Proposed design

Deploy the service in a private Vultr network with host firewall, encrypted
volume, secret injection, and an authenticated application ingress. Store
session/event state in the service database, Core separately guarded, and
Recall/Archival behind query interfaces. Export encrypted backups to a
different failure domain. Connector calls remain outside the runtime process
and use their own specs.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `health` | authenticated probe | service/version/dependency state |
| `session_start` | agent ID, session ID, client nonce | session handle + Core revision |
| `session_append` | session handle, sequence, event | committed event + receipt |
| `recall` | session, query, limit | labeled references |
| `core_propose` | session, proposed patch, approval | pending/committed Core revision |
| `backup_verify` | operator auth | backup ID, checksum, restore result |

Stable errors: `UNAUTHENTICATED`, `NOT_FOUND`, `STALE_SEQUENCE`,
`CORE_APPROVAL_REQUIRED`, `DEPENDENCY_UNAVAILABLE`, `BACKUP_INVALID`,
`QUOTA`, and `RUNTIME_UNAVAILABLE`.

## Data model and invariants

Session records contain agent/session IDs, event sequence, timestamps, and
references to memory revisions. Core records are small, versioned blocks with
explicit provenance. Recall records are searchable history; Archival records
are long-term references. A retrieved reference is never silently promoted to
Core. Each event is append-only and each backup has a checksum and schema
version.

## Security and privacy

Use private networking, host firewall rules, short-lived service credentials,
encrypted volumes, and encrypted off-host backups. Separate runtime,
management, and backup identities. Apply [`BASIC_TIER`](../BASIC_TIER.md)'s
least-privilege and receipt rules. Do not place provider keys in images,
source control, prompts, or diagnostic logs.

## Reliability and failure modes

Handle provider/network loss with bounded retries and sequence checks.
Degraded mode may serve health and verified read-only context but must not
accept unverified Core writes. Disk-full, checksum mismatch, schema mismatch,
or secret-store failure stops writes and raises an operator alert.

## Observability

Emit `deploy_verified`, `health_changed`, `session_started`,
`event_committed`, `recall_completed`, `core_write_proposed`,
`backup_created`, `backup_verified`, and `degraded_mode`. Track request
latency, error rate, event lag, memory sizes, backup age, and restore checks.
Use IDs and counts, not prompt or memory content.

## Testing and acceptance

- Test private ingress, invalid auth, sequence replay, Core approval, and
  retrieval labeling.
- Test backup creation, checksum failure, clean restore, and instance
  replacement using a disposable environment.
- Run a smoke session through health → start → append → recall → receipt.
- Acceptance requires all `VL-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Provision a non-production Vultr instance with read-only connectors and a
synthetic agent. Verify backup/restore before importing real sessions. Enable
session writes, then approved Core proposals. Backout restores the prior image
and disables writes; no automatic data deletion is performed.

## Open questions and decisions

- **Decision:** Letta memory tiers are separated by policy, not treated as
  three competing personalities.
- **Decision:** archival retrieval cannot rewrite Core without approval.
- **Open:** select the exact Letta-compatible service version and database
  topology.
- **Open:** choose Vultr region and backup failure domain after data-residency
  review.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [Letta memory tier mapping](../../../skill_tree/skills/smokeshow/notes/custom-agent-architecture-2026-08-17/analysis/11_LETTA_TIERS_AND_SLOTS.md)
- [MCP sovereign bridge security](../../../skill_tree/skills/mcp-surface/references/modules/sovereign-bridge/SKILL.md)
- [System architecture target](../../../skill_tree/skills/system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md)
