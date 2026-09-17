# OpenSpec: `github_connector`

**Status:** Proposed  
**Version:** 0.1.0  
**Owner:** `system-roadmap` / `olivia-dev-alpha`  
**Tier:** [`BASIC_TIER`](../BASIC_TIER.md)  
**Last updated:** 2026-09-17

## Summary

Define a scoped GitHub connector for reading repository context and publishing
reviewable Markdown or CSV changes. The connector treats GitHub as the
versioned system of record for committed specs and receipts, not as an
unbounded automation target.

## Context

The repository's current conduit design stages pure Markdown/CSV in Drive and
publishes an atomic commit through a GitHub pusher or native git. The first
touch rule in `olivia-dev-alpha` requires reading a repository landing page and
README before deeper work. This module formalizes those boundaries and keeps
writes reviewable.

## Problem statement

A GitHub write can be technically successful but operationally unsafe if it
targets the wrong repository, skips human-readable context, overwrites a
branch, or loses the commit reference. Callers need explicit repository,
branch, path, and approval scope plus a receipt that can be traced to the
source artifact.

## Goals

- Read repository metadata, landing-page context, README, and file contents.
- Create a branch and atomic commit for allowlisted text artifacts.
- Return commit, branch, and pull-request references where applicable.
- Enforce first-touch discovery before publication.
- Make retries idempotent and prevent accidental force pushes.

## Non-goals

- Merging pull requests, changing repository settings, or managing users.
- Force-pushing, deleting branches, or rewriting history in BASIC_TIER.
- Executing arbitrary Actions, webhooks, or code from repository contents.
- Treating a PR as merged or deployed based only on API acceptance.

## Actors and dependencies

| Actor/dependency | Responsibility |
|---|---|
| Calling agent | Provides repository, branch, paths, intent, and approval |
| GitHub connector | Performs scoped reads/writes with least-privilege token |
| Drive connector | Supplies staged artifact and verified hash when used |
| Reviewer | Reviews the commit/PR before merge |
| Receipt store | Persists API outcome and immutable refs |

## Requirements

- **GH-001**: Every write MUST identify owner, repository, base branch, target
  path, expected current revision, and idempotency key.
- **GH-002**: A new repository MUST pass the first-touch read of landing page and
  README, or record that either is unavailable.
- **GH-003**: BASIC_TIER writes MUST be branch-scoped and create-only for files;
  an existing path with a changed hash MUST fail unless explicit update
  approval is present.
- **GH-004**: The connector MUST reject force pushes, history rewrites, branch
  deletion, merges, settings changes, and Actions dispatch.
- **GH-005**: A successful write MUST return commit SHA, branch, paths, and
  receipt reference.
- **GH-006**: Retries MUST use the idempotency key and expected revision to
  prevent duplicate commits or lost updates.
- **GH-007**: Tokens, file contents, and private repository data MUST be absent
  from logs and receipts unless a redacted digest is sufficient.
- **GH-008**: A publication MUST NOT claim review, merge, or deployment.

## Scenarios

### First-touch read

**Given** a repository not present in the connector cache  
**When** a caller requests publication  
**Then** the connector reads the landing metadata and README first, records
their revisions, and only then permits a write plan.

### Atomic staged commit

**Given** an approved Markdown artifact and an allowlisted branch/path  
**When** the expected base revision matches  
**Then** the connector creates one commit, returns its SHA, and writes a receipt
containing the source hash.

### Stale branch

**Given** the remote base revision differs from the request  
**When** a write is submitted  
**Then** it returns `STALE_REVISION`, creates no commit, and requires a fresh
read/review.

### Retry after lost response

**Given** a commit may have been accepted but the response was lost  
**When** the same idempotency key is retried  
**Then** the connector finds the existing commit or branch result and returns
it without creating a second commit.

## Proposed design

The flow is `first_touch → plan → approval → branch/write → verify → receipt`.
The write adapter may use the GitHub API or native git, but the contract is
identical. Verification reads the target ref and commit after the write. PR
creation is a separate explicitly approved operation and never implies merge.

## Interface contract

### Operations

| Operation | Required input | Result |
|---|---|---|
| `first_touch` | `owner`, `repo` | metadata, landing revision, README revision |
| `read` | `owner`, `repo`, `ref`, `path` | content or metadata, redacted receipt |
| `commit` | repo, base ref, target branch, files, expected revision | commit SHA + receipt |
| `open_review` | commit/branch, base branch, title, body | PR reference + receipt |

Stable errors: `INVALID_TARGET`, `FIRST_TOUCH_REQUIRED`, `NOT_FOUND`,
`PERMISSION_DENIED`, `STALE_REVISION`, `DUPLICATE`, `RATE_LIMITED`,
`PROVIDER_UNAVAILABLE`, and `AMBIGUOUS_RESULT`.

## Data model and invariants

The publication receipt contains `request_id`, repository, base and target
refs, expected revision, commit SHA, changed paths, source hashes, actor,
approval reference, status, timestamps, and redacted error. Invariants: all
paths are normalized and allowlisted; one request has at most one commit; the
expected revision is checked; and a receipt never says merged unless a
separate approved merge operation exists.

## Security and privacy

Use a repository-scoped token with contents read/write only; keep it outside
prompts, files, and logs. Reject path traversal and hidden credential files
unless explicitly allowlisted. Apply [`BASIC_TIER`](../BASIC_TIER.md)'s least
privilege, approval, and receipt rules. Private content is returned only to
the authorized caller.

## Reliability and failure modes

Rate limits are retried only when the provider supplies a safe retry window.
Permission and stale-revision errors are terminal for the request. Ambiguous
commit outcomes require lookup by idempotency key, branch, and source hash.
Partial multi-file updates are not acceptable: use one tree/commit operation or
fail before writing.

## Observability

Emit `first_touch_completed`, `write_planned`, `approval_received`,
`commit_created`, `review_opened`, and failure events. Metrics include API
latency, stale-revision rate, duplicate suppression, rate-limit responses, and
receipt age. Log repository and commit identifiers, never token values or raw
file bodies.

## Testing and acceptance

- Test first-touch success and missing README/landing-page behavior.
- Test path traversal, disallowed operations, stale revisions, rate limits,
  duplicate retry, and ambiguous commit recovery with a fake GitHub API.
- Verify that a multi-file publication is one atomic commit.
- Acceptance requires all `GH-*` requirements and the
  [`BASIC_TIER`](../BASIC_TIER.md) checklist.

## Rollout and migration

Start with read-only first-touch and file reads. Enable branch commits for one
allowlisted repository and a non-protected branch. Add PR creation only after
receipt verification is stable. Disable writes to back out; existing commits
remain reviewable and are never reverted automatically.

## Open questions and decisions

- **Decision:** no force push or merge in BASIC_TIER.
- **Decision:** repository landing page and README are mandatory first-touch
  context, with an explicit unavailable result when absent.
- **Open:** select one canonical implementation between the native API adapter
  and `github_tree_pusher.py` when that adapter is introduced.
- **Open:** define the repository/path allowlist for production use.

## References

- [`BASIC_TIER`](../BASIC_TIER.md)
- [GitHub first-touch work item](../../../skill_tree/skills/olivia-dev-alpha/references/work-queue/items/ODA-WQ-036_github_first_touch.md)
- [Drive staging + GitHub conduit](../../../skill_tree/skills/system-roadmap/references/io-normalization-recon-2026-08-16/03_Drive_Staging_GitHub_Conduit.md)
- [GitHub mirror deferred work](../../../skill_tree/skills/olivia-dev-alpha/references/work-queue/items/ODA-WQ-056_github_mirror_later.md)
