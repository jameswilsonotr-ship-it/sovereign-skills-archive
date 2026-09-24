# SPEC-019 — Phone Intent Default Deny

**Status:** Draft
**Scope:** Phone-originated intent handling
**Change type:** Specification only
**Atomicity:** This file is the atomic contract for the default-deny phone
intent boundary. It does not authorize implementation, rollout, or external
side effects.

## 1. Purpose

Phone input is convenient but ambiguous, interruptible, and easy to misroute.
This specification defines the safety boundary for interpreting a phone
request as an intent. A request MUST NOT produce an action merely because it
resembles a known command.

The governing invariant is:

> No recognized, authorized, and explicitly permitted intent means no action.

“Phone” includes voice, speech-to-text, mobile UI, and other phone-originated
input surfaces. An **intent** is a proposed operation plus its target, scope,
parameters, and requested side effects. A **burn** is any bounded resource
consumption attributable to one intent, including model/tool calls, retries,
latency, money, quota, or external actions.

## 2. Decision outcomes

Every request MUST resolve to exactly one of these outcomes:

- **ALLOW:** perform the bounded, pre-authorized operation.
- **CONFIRM:** pause before a side effect and request an explicit,
  request-specific confirmation.
- **DENY:** perform no operation and return a safe explanation.
- **ESCALATE:** perform no operation and route the request for an authorized
  human or higher-assurance flow.

`CONFIRM` is not success. A confirmation that is absent, stale, ambiguous, or
invalid resolves to `DENY`.

## 3. Normative requirements

### Intake and classification

**PI-001 — Initial deny state.** Every phone-originated request MUST enter the
decision pipeline in `DENY` state. An `ALLOW` or `CONFIRM` outcome MUST be
earned by all applicable checks; it MUST NOT be the fallback.

**PI-002 — Unknown input.** Missing, empty, malformed, unintelligible, or
unclassifiable input MUST be denied without invoking a side-effecting tool.
The system MAY ask the caller to restate the request, but the restatement is a
new request.

**PI-003 — Versioned allowlist.** Only intents in an active, versioned
allowlist MAY proceed beyond classification. Similar wording, fuzzy matching,
historical behavior, or a successful prior request MUST NOT expand the
allowlist.

**PI-004 — Non-widening normalization.** Transcription, locale, unit, and
format normalization MUST preserve the raw request and MUST NOT add entities,
targets, permissions, or side effects. If normalization changes the candidate
intent or its risk class, the request MUST be denied or re-confirmed.

**PI-005 — Complete intent shape.** A candidate MUST contain a recognized
intent name, target, scope, parameters, and requested side effects. Missing,
conflicting, or ambiguous fields MUST result in `DENY` or `CONFIRM` before
any tool call.

**PI-006 — Confidence is not authorization.** Classification confidence MAY
inform review, but it MUST NOT substitute for authorization or confirmation.
Candidates below the configured confidence threshold MUST be denied or
re-asked without side effects.

### Authorization and confirmation

**PI-007 — Current authorization context.** An intent MUST have a current
authorization context bound to the caller, phone session, policy version, and
intended target. Missing, expired, revoked, or mismatched context MUST deny
the request.

**PI-008 — Explicit side-effect confirmation.** Any intent that sends,
publishes, calls, purchases, changes state, shares data, or deletes data MUST
require an explicit confirmation tied to a canonical summary of the exact
operation, target, and material parameters.

**PI-009 — No inferred consent.** Silence, interruption, a wake word, an
earlier confirmation, conversation history, sentiment, urgency, or a
preference inferred from prior behavior MUST NOT count as confirmation.

**PI-010 — Confirmation freshness and binding.** Confirmation MUST expire
after the configured session boundary or timeout and MUST be invalidated if
the target, scope, parameters, risk class, or policy version changes. A
confirmation for one intent MUST NOT authorize another intent.

**PI-011 — High-risk step-up.** Credentials, authentication changes, secrets,
financial actions, external sharing, destructive actions, physical-device
controls, and access-policy changes MUST require an approved step-up flow.
Phone intent classification alone MUST never authorize these operations.

### Execution and burn boundaries

**PI-012 — One intent, one bounded transaction.** An accepted intent MUST
execute as one bounded transaction. It MUST NOT silently fan out, delegate,
chain unrelated intents, or turn a response into a new command.

**PI-013 — Re-authorization across tools.** Every side-effecting tool or
delegated capability MUST receive the canonical intent identity and pass its
own authorization check. Tool success, tool availability, or a prior
read-only result MUST NOT grant transitive permission.

**PI-014 — Atomic commit.** A multi-step operation MUST commit all required
side effects or none. On a pre-commit failure, the system MUST leave no
partial effect. If rollback is impossible after a failure, the system MUST
stop further work, mark the outcome uncertain, and escalate rather than
guessing success.

**PI-015 — Included burn budget.** Each intent MUST have a finite,
policy-controlled burn budget covering tool calls, retries, elapsed time,
monetary or quota use, and external side effects. Budget exhaustion MUST
deny remaining work and MUST NOT trigger an unbounded retry, fallback chain,
or broader authorization.

**PI-016 — Uncertain-result handling.** A timeout, disconnect, interrupted
call, duplicate response, or unknown post-action state MUST be reported as
`ESCALATE` or an equivalent uncertain state. The system MUST NOT
automatically retry a potentially side-effecting operation without an
idempotency check and fresh authorization.

### Privacy, refusal, and audit

**PI-017 — Secret and content minimization.** Decision logs and receipts MUST
exclude credentials, tokens, full message bodies, private transcripts, and
unnecessary personal data. The raw request MUST be access-controlled and
retained only under the applicable retention policy.

**PI-018 — Fail closed.** Policy-store failures, authorization-service
failures, missing policy versions, stale cached decisions, classifier
failures, audit failures, and unavailable dependencies MUST resolve to
`DENY` or `ESCALATE`. They MUST NOT fall back to permissive behavior.

**PI-019 — Safe refusal and receipt.** A denial MUST identify a
non-sensitive reason category and a safe next step without revealing policy
internals or guessing the caller’s intended target. Each attempted intent
MUST produce a secret-free receipt containing the intent identifier, policy
version, decision, confirmation status, outcome, and consumed burn counters.

**PI-020 — Conformance gate.** A release claiming SPEC-019 conformance MUST
demonstrate all requirements in this document, including tests for unknown
input, ambiguity, replayed confirmation, policy outage, prompt injection,
partial failure, timeout, budget exhaustion, duplicate delivery, and each
high-risk class. Any unmet or untestable requirement keeps the implementation
at `DENY` for the affected intent and prevents a conformance claim.

## 4. Required decision order

The implementation of this contract, when authorized separately, MUST apply
the checks in this order:

1. Preserve and classify the request.
2. Normalize without widening it.
3. Validate the complete intent shape.
4. Load the current policy and authorization context.
5. Apply allowlist and risk checks.
6. Require fresh confirmation or step-up authentication when applicable.
7. Reserve and enforce the burn budget.
8. Execute one atomic transaction.
9. Emit a secret-free receipt and surface any uncertainty.

Failure at any step MUST stop subsequent steps and resolve to `DENY` or
`ESCALATE`. This document intentionally defines no APIs, storage schema,
runtime, vendor, or deployment procedure.
