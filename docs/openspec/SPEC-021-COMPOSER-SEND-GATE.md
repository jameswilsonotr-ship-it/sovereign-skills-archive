---
id: SPEC-021-COMPOSER-SEND-GATE
title: Composer send gate
status: proposed
owner: composer
priority: high
summary: Gate composer submission on valid content and a positively verified usage allowance.
tags: [composer, send-gate, usage, atomic-included-burn]
dependencies: [composer-input, usage-status]
---

# Composer send gate

## Scope

The send gate is the single decision boundary for whether the composer may
submit a message. It applies to pointer, keyboard, accessibility, and
programmatic submit paths.

The gate is **fail-closed**: a send is permitted only when every required
positive condition is known to be true. In particular, a missing, loading,
stale, malformed, or errored usage banner/status never counts as permission
to send.

## Definitions

- **Valid content** is at least one user-entered non-whitespace character.
- **Usage allowed** is an explicit, current, successfully parsed positive
  verdict from the usage banner/status source.
- **Sendable** means valid content and usage allowed are both true.
- **One-character proof** means entering one non-whitespace character is
  sufficient to make the send control clickable when usage is allowed; no
  minimum length greater than one is implied.

## Atomic acceptance criteria

- [ ] **CS-001** — With exactly one non-whitespace character in the composer
  and an explicit current `usage allowed` verdict, `send_clickable` is true.
- [ ] **CS-002** — With an empty composer, `send_clickable` is false even when
  usage is allowed.
- [ ] **CS-003** — With whitespace-only content, `send_clickable` is false.
- [ ] **CS-004** — With usage exhausted, denied, or otherwise explicitly not
  allowed, `send_clickable` is false regardless of composer content.
- [ ] **CS-005** — When the usage banner/status is missing, `send_clickable`
  is false.
- [ ] **CS-006** — While usage status is loading or indeterminate,
  `send_clickable` is false.
- [ ] **CS-007** — When usage status is stale, malformed, or has an error,
  `send_clickable` is false; no best-effort fallback may enable sending.
- [ ] **CS-008** — Adding the first valid character recomputes the gate and
  makes the send control clickable when usage is already allowed.
- [ ] **CS-009** — Removing the last valid character, or reducing the content
  to whitespace-only, recomputes the gate and makes the send control
  non-clickable.
- [ ] **CS-010** — A transition from usage allowed to loading, stale, denied,
  or errored immediately revokes clickability.
- [ ] **CS-011** — A disabled send control rejects pointer activation,
  keyboard submit, accessibility activation, and programmatic submit.
- [ ] **CS-012** — A send activation reads the same gate decision used to
  expose `send_clickable`; no alternate submit path can bypass it.
- [ ] **CS-013** — A successful send clears the composer and leaves the send
  control non-clickable until new valid content and a current allowed usage
  verdict are both present.
- [ ] **CS-014** — The composer exposes an accessible disabled state and a
  user-understandable reason whenever content or usage prevents sending.
- [ ] **CS-015** — The one-character proof and every fail-closed usage case
  are covered by deterministic acceptance tests without requiring a network
  request or a real send.

## Non-goals

This specification does not define usage accounting, quota calculation,
message delivery, retry behavior, or the visual design of the usage banner.
