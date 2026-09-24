# OpenSpec: `spark_escalation`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `system-roadmap` / `mcp-surface`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define a controlled escalation path from a lightweight Spark execution surface
to a heavier or more capable worker. Escalation carries a bounded task
envelope and references to approved artifacts; it does not copy an entire
conversation, grant ambient credentials, or silently change the authority
chain.

## Context

The repository distinguishes light Expert-mode work from explicit Heavy
overrides and uses Gmail/Drive receipts for cross-surface handoff. Spark is
treated as a capable execution surface, not as a universal source of truth.
This module provides the missing decision and handoff contract.

## Problem statement

Escalation can amplify cost, permissions, and data exposure. A vague “send to
heavy” operation may leak unrelated context, repeat work, or claim completion
before the downstream worker returns a verified receipt.

## Goals

- Detect explicit, policy-defined escalation conditions.
- Package only the minimum task context and artifact pointers.
- Require approval for costly, external, or high-impact escalation.
- Track lifecycle from proposed through accepted, completed, failed, or expired.
- Return a receipt that preserves provenance and does not overclaim success.

## Non-goals

- Automatic model selection based on unreviewed prompt content.
- Copying private conversation history or credentials into the task.
- Letting the escalated worker rewrite local policy or identity state.
- Treating a timeout as successful completion or retrying without deduplication.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Spark/light worker | Detects need and proposes a bounded escalation |
| Policy gate | Evaluates threshold, budget, data class, and approval |
| Heavy worker | Accepts and executes the approved task |
| Drive/Gmail connectors | Carry artifacts, wake signals, and receipts |
| Human operator | Approves escalations outside standing policy |

## Requirements

- **SP-001**: A proposal MUST identify reason, task ID, origin, destination
  capability, data classification, budget, deadline, and artifact references.
- **SP-002**: Escalation MUST be triggered only by explicit rules such as
  context limit, required tool capability, confidence threshold, or human
  instruction; the rule ID is part of the receipt.
- **SP-003**: Payloads MUST be minimal and pointer-based for large artifacts;
  credentials, unrelated history, and hidden system prompts MUST be excluded.
- **SP-004**: Costly, externally visible, destructive, or policy-sensitive
  tasks MUST require approval before dispatch.
- **SP-005**: The destination MUST acknowledge acceptance before the origin
  claims handoff; completion requires a verified result receipt.
- **SP-006**: Repeated proposals with the same task and rule MUST collapse to
  one idempotent escalation.
- **SP-007**: Deadlines and budgets MUST be enforced; expired tasks must not
  execute without reapproval.
- **SP-008**: The module MUST follow [`BASIC_TIER`](../BASIC_TIER.md) and may
  not grant the destination broader permissions than the approved envelope.

## Scenarios

### Context-limit escalation

**Given** a task exceeds the light worker's declared context budget  
**When** rule `CONTEXT_LIMIT` evaluates true  
**Then** a minimal proposal is created with a task ID, artifact pointers, and
budget; no dispatch occurs until policy allows it.

### Capability escalation

**Given** the light worker lacks a required approved tool  
**When** rule `MISSING_CAPABILITY` evaluates true  
**Then** the proposal names that capability, excludes unrelated context, and
requests approval or returns `BLOCKED`.

### Accepted handoff

**Given** an approved proposal and reachable destination  
**When** the destination acknowledges it  
**Then** the origin records `accepted`, waits for the result receipt, and
reports only the accepted state until completion.

### Expired or duplicate proposal

**Given** a proposal is expired or already dispatched with the same key  
**When** a dispatch is attempted  
**Then** it is rejected as `EXPIRED` or returns the existing lifecycle record;
the downstream worker is not invoked twice.

## Proposed design

Use `evaluate → propose → approve → dispatch → acknowledge → execute →
verify → receipt`. The proposal is a signed/hashed envelope with references
to Drive artifacts where possible. Gmail may wake the destination but cannot
substitute for acceptance or completion receipts.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `evaluate` | task metrics, rule set | decision + rule ID |
| `propose` | bounded task envelope | proposal ID + receipt |
| `approve` | proposal ID, approval scope | approval receipt |
| `dispatch` | approved proposal | destination request ID |
| `acknowledge` | destination request ID | accepted/rejected state |
| `complete` | result, provenance, usage | verified completion receipt |
| `cancel` | proposal/request ID | cancellation state |

Stable errors: `NO_RULE_MATCH`, `APPROVAL_REQUIRED`, `INVALID_PAYLOAD`,
`DESTINATION_UNAVAILABLE`, `DUPLICATE`, `EXPIRED`, `BUDGET_EXCEEDED`,
`REJECTED`, and `AMBIGUOUS_RESULT`.

## Data model and invariants

The envelope contains `task_id`, `proposal_id`, origin, destination,
rule ID, objective, allowed tools, data classification, artifact refs,
budget, deadline, idempotency key, and approval ref. Lifecycle states are
`proposed → approved → dispatched → accepted → completed`, with terminal
`rejected`, `failed`, `expired`, or `cancelled`. A state transition is
append-only and receipted.

## Security and privacy

Classify data before dispatch and use allowlisted artifact references. Scope
destination credentials to the task. Never include tokens, unrelated
conversation history, or hidden prompts. Apply [`BASIC_TIER`](../BASIC_TIER.md)
for approval, retry, redaction, and receipt behavior. Human approval is
mandatory for external side effects unless a written standing policy says
otherwise.

## Reliability and failure modes

An unreachable destination leaves the proposal pending until deadline; it does
not silently downgrade or reroute. A dispatch timeout is ambiguous and
requires lookup by task/proposal key. Partial results are marked incomplete.
Budget, deadline, or receipt verification failure blocks completion claims.

## Observability

Emit `rule_evaluated`, `proposal_created`, `approval_recorded`,
`dispatch_started`, `accepted`, `completed`, `expired`, `cancelled`, and
`receipt_verified`. Track escalation rate by rule, approval latency, duplicate
suppression, budget use, destination latency, and incomplete results. Log
envelope IDs and classifications, not payload contents.

## Testing and acceptance

- Test every rule path, missing capability, approval denial, minimal payload,
  duplicate proposal, timeout recovery, deadline expiry, and budget limit.
- Verify that acceptance and completion are distinct states.
- Contract-test a fake Spark/light worker and heavy destination.
- Acceptance requires all `SP-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Start in observe-only mode, recording would-escalate decisions without
dispatch. Enable proposals, then approved dispatch for synthetic tasks, then
one low-risk production class. Backout disables dispatch while retaining
proposal history and receipts. Existing tasks are not auto-rerouted.

## Open questions and decisions

- **Decision:** escalation is a handoff protocol, not an implicit model switch.
- **Decision:** Gmail can wake a destination but cannot prove acceptance.
- **Open:** define the canonical Spark capability and budget registry.
- **Open:** decide whether approval tokens are human-issued or supplied by a
  policy service.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [Gmail fake-MCP bus recon](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/01_Gmail_Fake_MCP_Bus.md)
- [Drive staging + GitHub conduit](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
- [System architecture target](../../../skill_tree/skills/system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md)
