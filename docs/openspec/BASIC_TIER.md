# BASIC_TIER

**OpenSpec profile:** `BASIC_TIER`  
**Version:** `0.1.0`  
**Status:** normative baseline for the connector and runtime module proposals  
**Owner:** `system-roadmap`  
**Last updated:** 2026-09-17

## Purpose

`BASIC_TIER` is the minimum contract every module in
[`docs/openspec/modules/`](./modules/) must satisfy before it can be
implemented or promoted. It is deliberately transport-neutral: a connector
may use MCP, a native API, a local bridge, or a host process, but callers must
see the same safety and receipt behavior.

## Required module contract

Every module specification MUST define:

1. **Identity and scope** — stable module name, version, status, owner, goals,
   non-goals, dependencies, and explicit assumptions.
2. **Typed boundary** — input and output fields, validation rules, idempotency
   behavior, timeout expectations, and error classes.
3. **Least privilege** — the smallest read/write capability set, credential
   location, account or tenant boundary, and human approval gate for
   irreversible or externally visible writes.
4. **Durable receipts** — a correlation ID, request hash, actor, target,
   outcome, timestamps, and redacted error details. A successful side effect
   without a receipt is not a successful operation.
5. **Retry safety** — bounded retries with backoff, duplicate suppression, and
   a clear rule for ambiguous outcomes.
6. **Observability** — structured logs and metrics that do not contain tokens,
   message bodies, private content, or unnecessary personal data.
7. **Testability** — deterministic unit tests, a contract test using a fake or
   sandboxed provider, failure-path coverage, and an acceptance checklist.
8. **Rollout discipline** — feature flag or dry-run path, migration/backout
   behavior, and a statement of what is not automated yet.

## Shared envelope

Modules SHOULD exchange this logical envelope, whether serialized as JSON,
MCP arguments, or a local file:

```json
{
  "request_id": "uuid",
  "module": "module_name",
  "operation": "verb",
  "actor": "principal",
  "account_id": "optional-provider-account",
  "idempotency_key": "stable-key",
  "mode": "read|write|dry_run",
  "payload": {},
  "created_at": "RFC-3339 timestamp"
}
```

The response MUST include `request_id`, `status`, `provider_reference` when
available, `receipt_reference`, and a machine-readable `error` object on
failure. Secrets and raw provider tokens MUST never appear in an envelope or
receipt.

## Tier boundary

`BASIC_TIER` covers one provider/account boundary, bounded operations, and
human-reviewable receipts. It does **not** authorize:

- unattended destructive actions;
- credential minting, storage, or distribution;
- broad tenant-wide synchronization;
- autonomous policy, legal, financial, or identity decisions;
- cross-provider fan-out without an explicit higher-tier specification.

## Cross-link rule

Each module spec MUST link back to this file in its metadata, security
section, and acceptance criteria. Changes to this baseline require reviewing
all module specs in the same pull request or recording an explicit
compatibility decision.

## Acceptance checklist

- [ ] All required OpenSpec sections are present.
- [ ] All external writes have dry-run and approval behavior.
- [ ] Account, tenant, and credential scope are explicit.
- [ ] Idempotency and ambiguous-outcome behavior are explicit.
- [ ] Receipts and redacted observability are explicit.
- [ ] Provider failure and revocation paths are tested.
- [ ] The module links to this baseline from at least three locations.
