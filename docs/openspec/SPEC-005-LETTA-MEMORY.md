---
id: SPEC-005
title: Letta Memory Contract
status: Draft
version: 0.1.0
owner: system-roadmap
base: skill-tree-intake
scope: Letta-compatible memory plane and its policy boundary
tags: [letta, memory, core, recall, archival, provenance, receipts]
---

# SPEC-005 — Letta Memory Contract

## Purpose

Define the smallest auditable contract for using a Letta-compatible memory
plane in the sovereign skill system. The contract preserves the distinction
between Core, Recall, and Archival memory while keeping source artifacts,
policy, approvals, and receipts outside any one model context.

This is an architecture specification. It does not deploy Letta, select a
provider, authorize credentials, or import existing conversations.

## Scope

This specification covers:

- memory-tier semantics and boundaries;
- session and agent isolation;
- retrieval, insertion, promotion, and revocation behavior;
- provenance, consent, retention, idempotency, and receipts;
- backup, restore, failure, observability, and test contracts.

The memory plane may be local, private-hosted, or exposed through a normalized
MCP boundary. Transport choice does not change the requirements in this file.

## Non-goals

- Choosing a Letta server version, model, embedding model, database, or host.
- Replacing the skill tree, durable artifact store, or work-queue protocol.
- Treating Core, Recall, and Archival as three personalities or agents.
- Making retrieved text authoritative merely because it was retrieved.
- Bulk-hydrating historical conversations into permanent memory.
- Performing live provider calls or storing credentials in this repository.

## Terms and invariants

| Term | Meaning |
|---|---|
| **Core** | Small, always-available memory blocks for identity, critical user facts, and active working state. |
| **Recall** | Searchable conversation or session history that may fall out of the active context. |
| **Archival** | Long-term, semantic storage for approved durable facts and references. |
| **Candidate** | Content proposed for a tier but not yet promoted into that tier. |
| **Source artifact** | The canonical document, event, or receipt from which a memory item was derived. |
| **Promotion** | An explicit, auditable move or copy from a lower-authority state into a more durable or sensitive tier. |
| **Memory revision** | An immutable version identifier for a Core block or other mutable memory record. |
| **Receipt** | Durable evidence of an attempted or completed mutation, including its outcome. |

The following invariants apply throughout the lifecycle:

1. Core is small and policy-controlled.
2. Recall and Archival are retrieval sources, not identity authorities.
3. A vector or search index is derived data; it is never the sole canonical
   copy of a source artifact.
4. Every durable mutation is attributable, replay-safe, and inspectable.
5. Unknown outcomes remain unknown until verified; a model assertion is not a
   receipt.

## Actors and authority

| Actor | Responsibility | Authority boundary |
|---|---|---|
| Primary agent | Reads allowed context and proposes or performs permitted operations | Cannot bypass tier policy or approval gates |
| Memory adapter | Enforces the typed memory interface | Cannot invent provenance or widen caller scope |
| Curator or sleeptime worker | Deduplicates, summarizes, and proposes changes | Cannot silently rewrite Core |
| Durable artifact store | Holds source material, manifests, and receipts | Is canonical only for artifacts in its declared namespace |
| Operator | Approves sensitive promotion, retention, recovery, and policy changes | Remains final authority for consequential changes |
| Runtime administrator | Operates the service and backups | Does not receive conversational authority by default |

## Requirements

Each requirement is intentionally atomic and has a corresponding acceptance
case below.

- **LT-001**: The memory adapter MUST declare one stable agent and session scope for every operation.
- **LT-002**: The adapter MUST expose Core, Recall, and Archival as distinct memory tiers.
- **LT-003**: Core MUST enforce a configured size or item budget before accepting a write.
- **LT-004**: A Recall or Archival result MUST NOT rewrite a Core identity or policy block without an explicit approved mutation.
- **LT-005**: Recall MUST support append and bounded search without requiring every historical turn to be in active context.
- **LT-006**: Archival MUST support provenance-bearing insert and bounded semantic search as separate operations.
- **LT-007**: Every durable memory item MUST retain at least one source reference and its derivation actor.
- **LT-008**: A derived vector or search index MUST be rebuildable from canonical source artifacts and receipts.
- **LT-009**: The adapter MUST classify retention before writing content outside the current session.
- **LT-010**: When consent or retention policy denies persistence, the adapter MUST keep the content session-scoped and MUST NOT write it to Recall or Archival.
- **LT-011**: Every retrieval response MUST identify its tier and MUST enforce a caller-supplied or policy-supplied result bound.
- **LT-012**: Promotion into a more durable or authoritative state MUST create a distinct proposal or mutation event.
- **LT-013**: A promotion that changes identity, sensitive facts, or policy MUST require an operator approval reference.
- **LT-014**: Revocation of a promoted item MUST preserve a tombstone or equivalent audit record rather than erasing mutation history.
- **LT-015**: A memory operation MUST reject a caller whose agent or session scope does not match the target record.
- **LT-016**: Authorization MUST grant the smallest tier and operation set needed by the caller.
- **LT-017**: The adapter MUST return typed success and failure results for read, insert, search, propose, promote, and revoke operations.
- **LT-018**: A mutation MUST accept an idempotency key and MUST NOT apply the same logical mutation twice.
- **LT-019**: Concurrent Core updates MUST use a revision or equivalent compare-and-swap check.
- **LT-020**: Every attempted durable mutation MUST produce a receipt containing request, actor, target, outcome, and timestamps.
- **LT-021**: An ambiguous provider or storage response MUST remain pending or unknown until independently verified.
- **LT-022**: Backups MUST include the memory schema version, source references, integrity metadata, and an encrypted payload.
- **LT-023**: Restore MUST validate integrity and provenance before enabling memory writes.
- **LT-024**: Logs and metrics MUST use correlation identifiers without recording credentials, raw memory content, or unnecessary personal data.
- **LT-025**: The contract MUST be testable with deterministic fakes and a dry-run path before any live memory write is enabled.

## Typed boundary

The adapter exposes these logical operations:

| Operation | Required inputs | Result | Side effect |
|---|---|---|---|
| `core.read` | agent scope, block reference | block content or typed absence | none |
| `recall.search` | agent/session scope, query, result bound | labeled references | none |
| `archival.search` | agent scope, query, result bound | labeled references | none |
| `recall.append` | session scope, content, retention decision, idempotency key | record reference and receipt | append |
| `archival.insert` | agent scope, content, source references, idempotency key | record reference and receipt | insert |
| `core.propose` | agent scope, block revision, patch, source references | proposal reference | staged |
| `core.promote` | proposal reference, approval reference when required | new revision and receipt | mutate |
| `memory.revoke` | record reference, reason, idempotency key | tombstone and receipt | mutate |

All operations carry a correlation ID, schema version, actor, and deadline.
Errors are machine-readable and distinguish at least `UNAUTHENTICATED`,
`FORBIDDEN`, `NOT_FOUND`, `INVALID_INPUT`, `SCOPE_MISMATCH`,
`REVISION_CONFLICT`, `DUPLICATE`, `POLICY_DENIED`, `PENDING_VERIFICATION`,
`DEPENDENCY_UNAVAILABLE`, `INTEGRITY_FAILURE`, and `QUOTA_EXCEEDED`.

## Memory lifecycle

```text
session content
  -> consent and retention classification
  -> session-only, Recall append, or Archival candidate
  -> source reference + derivation record
  -> bounded retrieval or curator review
  -> explicit promotion proposal
  -> approval when required
  -> versioned Core or durable record
  -> receipt and later revocation if policy changes
```

Summaries and embeddings are derived representations. They may improve
retrieval, but they do not replace the source artifact, its provenance, or its
retention decision.

## Security and privacy

The implementation MUST follow least privilege and keep provider credentials
outside prompts, memory content, source control, receipts, and diagnostic
output. A memory token, API key, cookie, private signing material, or live
credential MUST NOT appear in this specification or in test fixtures.

Raw transcript, derived summary, embedding, and Core content MUST have
separately reviewable retention classes. Access to an Archival result MUST NOT
implicitly grant access to its source artifact or to another agent's memory.
Sensitive promotion and policy changes require a human-reviewable approval
reference.

## Failure and recovery semantics

The adapter fails closed for authorization, scope, integrity, and revision
errors. It may serve verified read-only data during a write dependency outage,
but it MUST surface the degraded state and MUST NOT report an unverified write
as successful.

Retries are bounded and keyed by the original idempotency key. If the outcome
of a write is ambiguous, recovery first queries the receipt or provider by
that key before attempting another mutation. Restore failure leaves the memory
plane read-only until integrity and provenance checks pass.

## Observability

Implementations SHOULD emit structured events for:

`memory_read`, `recall_searched`, `archival_inserted`, `promotion_proposed`,
`promotion_approved`, `core_revision_written`, `memory_revoked`,
`receipt_verified`, `backup_created`, `restore_verified`, `degraded_mode`,
and `policy_denied`.

Events SHOULD contain correlation ID, agent/session scope hash, tier,
operation, outcome, latency, and opaque record references. Events MUST NOT
contain prompt bodies, raw memory content, credentials, or unrestricted
personal data.

## Acceptance

- **LT-001**: A request without an agent or session scope is rejected, and a valid request records exactly one scope.
- **LT-002**: The capability description lists Core, Recall, and Archival separately, with no fourth implicit tier.
- **LT-003**: A Core write over the configured budget is rejected without changing the prior Core revision.
- **LT-004**: A retrieval result presented to the agent leaves the Core identity block unchanged.
- **LT-005**: A historical session event can be appended and later found by a bounded Recall query.
- **LT-006**: An Archival insert and an Archival search return a source reference and tier label.
- **LT-007**: A durable item missing a source reference or derivation actor is rejected.
- **LT-008**: Deleting a derived index and rebuilding it from canonical fixtures reproduces the same record references.
- **LT-009**: A write without a retention classification is rejected before persistence.
- **LT-010**: A denied-consent fixture is absent from Recall and Archival after the session ends.
- **LT-011**: A query requesting more than its policy bound receives no more than the bound and labels every result.
- **LT-012**: A promotion produces a proposal or mutation event distinct from the original retrieval event.
- **LT-013**: An identity-changing promotion without an approval reference is denied and leaves Core unchanged.
- **LT-014**: Revoking a promoted item hides it from normal retrieval while preserving a verifiable tombstone.
- **LT-015**: A session from agent A cannot read or mutate agent B's record.
- **LT-016**: A read-only caller cannot invoke insert, promote, or revoke.
- **LT-017**: Invalid input, denied policy, missing record, and successful read each return distinct typed outcomes.
- **LT-018**: Repeating one mutation with the same idempotency key returns the original receipt without a second write.
- **LT-019**: Two writes against one stale Core revision result in one commit and one revision conflict.
- **LT-020**: A successful, denied, failed, and pending mutation each has a receipt with the required fields.
- **LT-021**: A simulated timeout produces `PENDING_VERIFICATION` and no success receipt until the outcome is checked.
- **LT-022**: A backup fixture contains encrypted payload metadata, schema version, source references, and integrity metadata without credentials.
- **LT-023**: A checksum or provenance mismatch prevents writes after restore and reports an integrity failure.
- **LT-024**: Captured logs contain correlation and outcome fields but no fixture prompt, credential, or raw memory body.
- **LT-025**: The full contract suite passes against deterministic fakes in dry-run mode without network access or live credentials.

## Rollout and open decisions

The first implementation should remain dry-run or read-only until the contract
suite passes. Enable session-scoped writes before long-term persistence, then
enable Recall and Archival, and enable Core promotion only after approval UX,
retention review, backup verification, and revocation behavior are accepted.
Each rollout stage needs a reversible flag and a known-good receipt format.

The following decisions remain open and MUST be resolved by a later change:

- selected Letta-compatible service and supported runtime;
- canonical artifact store and backup failure domain;
- approved Core schema and size budget;
- retention periods for raw transcript, Recall, Archival, and embeddings;
- embedding generation and deletion behavior;
- operator approval channel for sensitive promotion;
- recovery point and recovery time objectives.

## References

- [Letta memory tiers and slots](../../skill_tree/skills/smokeshow/notes/custom-agent-architecture-2026-08-17/analysis/11_LETTA_TIERS_AND_SLOTS.md)
- [System architecture target](../../skill_tree/skills/system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md)
- [Sovereign bridge skill](../../skill_tree/skills/mcp-surface/references/modules/sovereign-bridge/SKILL.md)
- [Multi-LLM sync protocol](../../skill_tree/skills/system-roadmap/references/multi-llm-sync/PROTOCOL.md)
