# Phone Intent Safety — S2-21

```yaml
change_id: second-salvo-21-phone-intent-safety
slot: S2-21
status: proposed
scope: one-intent-contract
execution_tier: included-ultra
```

This document specifies one phone intent only: `phone.send_sms`. It is a
contract, not an enablement plan. The S2-21 slice must not contact a phone,
send a message, resolve a live contact, or call an external service.

## Hard fences

- **Included Ultra only.** The permitted execution tier is
  `included-ultra`; `od` is rejected before authorization.
- **No live phone.** The only permitted verification in this slice is
  offline validation against fixtures or static contract checks.
- **No secrets.** Do not put phone numbers, message bodies, tokens, API keys,
  credentials, cookies, or private URLs in source, receipts, test output, or
  audit events.
- **Source boundary.** This slice does not read, modify, or cite a Willow
  `SKILL.md`, and it does not use `CONV2_B`.
- **Infrastructure identity boundary.** `Vultr` and `Cold Steel` are distinct
  labels. A Vultr host is infrastructure, not a Cold Steel phone identity or
  authorization source. No host or provider label can authorize sending.

## Intent envelope

The policy evaluator receives a non-secret envelope with these fields:

| Field | Requirement |
| --- | --- |
| `intent` | Exactly `phone.send_sms`; anything else is out of scope |
| `actor_ref` | Opaque reference to the requesting principal |
| `session_ref` | Opaque reference for the current interaction |
| `target_ref` | Opaque, already-resolved recipient reference; no raw number |
| `body_ref` | Reference to the user-visible draft; the audit layer never stores the body |
| `confirmation_ref` | Reference to the confirmation event for this exact draft and target |
| `idempotency_key` | Non-secret key for this exact send attempt |
| `execution_tier` | Must equal `included-ultra` |

The transport may carry the draft and destination to an approved adapter only
after authorization. They must not be copied into logs or receipts.

## Authorization contract

`phone.send_sms` is authorized only when **all** gates pass:

1. The user explicitly requests an SMS in the current session.
2. The target is one exact, user-selected recipient. A display-name match,
   inferred contact, group expansion, or ambiguous lookup is a denial.
3. The exact message is rendered to the user before confirmation. A later
   edit, target change, or session change invalidates the confirmation.
4. The user gives a separate, affirmative confirmation for that rendered
   target and message. Prior consent, standing instructions, silence,
   model preference, or a health response is not confirmation.
5. `execution_tier` is `included-ultra`, the adapter is explicitly approved,
   and the live-phone feature is enabled by a separately reviewed deployment.
6. The `idempotency_key` has not already produced a terminal send decision.

The evaluator returns one of:

```text
allow       all gates pass; an approved adapter may be considered
deny        a gate fails; no adapter call is permitted
not_enabled this contract is being checked in the offline S2-21 slice
```

In this slice, the result must always be `not_enabled` or `deny`; an
`allow` result must not be reachable from the offline harness. An authorization
decision is not proof of delivery.

## Failure contract

The policy fails closed. It never guesses, silently edits, falls back to
another channel, or retries an unknown outcome with a new idempotency key.

| Condition | Result | Required behavior |
| --- | --- | --- |
| Missing or invalid confirmation | `deny / AUTH_MISSING` | Do not call an adapter |
| Ambiguous or unresolved target | `deny / TARGET_AMBIGUOUS` | Ask for a new exact target outside this slice |
| Body changed after confirmation | `deny / CONFIRMATION_STALE` | Discard the authorization |
| Tier is not `included-ultra` (including `od`) | `deny / TIER_REJECTED` | Stop before dispatch |
| Adapter, identity, or deployment is not approved | `deny / ADAPTER_UNAPPROVED` | Do not probe or discover alternatives |
| Live phone is disabled for this slice | `not_enabled / LIVE_PHONE_DISABLED` | Record a policy decision only |
| Timeout or transport interruption after handoff | `unknown / DELIVERY_UNKNOWN` | Do not claim delivery; reconcile using the same key |
| Repeated terminal key | `deny / DUPLICATE_INTENT` | Do not send again |
| Any unclassified exception | `deny / INTERNAL_FAIL_CLOSED` | Suppress sensitive details and stop |

The caller receives the stable result and reason code, not raw provider
errors. The user-facing response must distinguish `denied`, `not enabled`, and
`delivery unknown`; it must never say “sent” without a confirmed provider
receipt.

## Audit contract

Every request, authorization decision, and terminal outcome produces an
append-only audit event, including denied and offline-only attempts. Audit
events contain only:

```yaml
event_id: opaque
occurred_at: UTC timestamp
intent: phone.send_sms
actor_ref: opaque
session_ref: opaque
target_ref: opaque
execution_tier: included-ultra
confirmation_state: absent | valid | stale
decision: allow | deny | not_enabled | unknown
reason_code: stable code from this document
idempotency_key: non-secret
adapter_class: approved-reference-or-null
environment: offline-fixture | reviewed-deployment
```

Audit events must not contain the raw target, body, contact-book data,
provider payload, credentials, or secrets. `target_ref` and `body_ref` are
opaque references only; they must not be reversible encodings of phone
numbers or message text. A failed or unknown operation is never converted
into a success event.

The audit sink must be append-only, access-controlled, and separately
retained from conversational content. If the audit sink is unavailable, the
operation fails closed and no phone adapter call may start.

## S2-21 acceptance checks

- [ ] The document names exactly one intent: `phone.send_sms`.
- [ ] Authorization requires exact target, exact draft, fresh explicit
      confirmation, `included-ultra`, approved adapter, and idempotency.
- [ ] Missing, stale, ambiguous, unapproved, duplicate, and unknown outcomes
      fail closed with stable reason codes.
- [ ] Audit fields are sufficient to reconstruct a decision without storing
      phone numbers, message bodies, or secrets.
- [ ] Offline S2-21 verification performs no network request and no live-phone
      operation.
- [ ] The change is limited to this document; no other S2 slot is modified.

## Non-goals

This slice does not define contact discovery, message content policy,
provider selection, adapter implementation, delivery reconciliation, SMS
opt-in, phone health, or any other phone intent.
