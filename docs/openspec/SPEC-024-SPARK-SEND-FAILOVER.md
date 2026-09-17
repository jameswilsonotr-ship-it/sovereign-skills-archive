---
id: SPEC-024-SPARK-SEND-FAILOVER
title: Spark send failover
status: proposed
owner: spark
priority: high
summary: Route a blocked Spark send through olette-box while preserving the sticky Hi banner and preventing duplicate delivery.
tags: [spark, send, failover, olette-box, atomic-included-burn, salvo-s1]
dependencies: [spark-send, olette-box, hi-banner]
---

# Spark send failover

## Scope

This specification defines the failover boundary for a Spark send when the
sticky **Hi** banner is active and the primary send path cannot complete.
`olette-box` is the only permitted failover route in this contract.

Failover is a delivery-path decision, not a banner-dismissal decision. The
sticky Hi banner remains active throughout the attempt and must not be
silently replaced, hidden, or cleared to make the primary path appear
available.

## Definitions

- **Sticky Hi banner** is the active Hi banner state that remains present
  across the send attempt, including rerenders, retries, and failover.
- **Primary send** is the normal Spark delivery path.
- **olette-box failover** is the alternate delivery path selected only after
  the primary path is known to be unavailable, blocked, or unable to complete.
- **Send envelope** is the immutable payload plus its conversation,
  correlation, idempotency, and user-visible status metadata.
- **Failover eligible** means the envelope is valid, the Hi banner is sticky,
  and the primary path has returned a failover-eligible result; an
  indeterminate result is not eligible.

## Atomic acceptance criteria

- [ ] **SF-001** — When a valid Spark send encounters a sticky Hi banner and
  the primary path is failover-eligible, the send decision selects
  `olette-box` without requiring the user to resubmit.
- [ ] **SF-002** — The failover decision preserves the exact send envelope:
  message content, conversation target, attachments or references,
  correlation identifier, and idempotency key are unchanged.
- [ ] **SF-003** — The sticky Hi banner remains visible and active while the
  primary attempt, failover attempt, and resulting status are rendered; no
  failover step may dismiss, overwrite, or downgrade it.
- [ ] **SF-004** — A primary result that is loading, missing, malformed, or
  ambiguous does not trigger `olette-box` failover; the send remains
  fail-closed with an actionable pending or error status.
- [ ] **SF-005** — A primary result explicitly marked unavailable, blocked, or
  failover-eligible triggers at most one `olette-box` attempt for a given
  idempotency key.
- [ ] **SF-006** — Repeated pointer, keyboard, accessibility, or programmatic
  activation during the transition cannot create duplicate primary or
  `olette-box` deliveries.
- [ ] **SF-007** — `olette-box` receives the same authorization, target, and
  policy context required by the primary send; failover cannot broaden
  recipients, permissions, or content scope.
- [ ] **SF-008** — The send is reported successful only after `olette-box`
  returns an explicit accepted or delivered result tied to the same
  correlation and idempotency identifiers.
- [ ] **SF-009** — If `olette-box` is unavailable, denied, times out, or
  returns an indeterminate result, the system reports failure or
  needs-attention and does not claim delivery or silently retry.
- [ ] **SF-010** — A successful `olette-box` failover records the primary
  failure reason, failover route, correlation identifier, and final result
  without exposing secrets or changing the user-visible message content.
- [ ] **SF-011** — A later retry with the same idempotency key is deduplicated
  across both the primary path and `olette-box`; a retry may not produce a
  second delivery.
- [ ] **SF-012** — Deterministic acceptance tests cover sticky-banner
  persistence, eligible and ineligible primary outcomes, envelope
  preservation, one-attempt behavior, duplicate activation, policy parity,
  explicit success, and failover failure without requiring a live send.

## Non-goals

This specification does not define Spark message composition, Hi banner
visual design, primary transport implementation, olette-box provisioning,
retry policy beyond the idempotency boundary, or delivery accounting.
