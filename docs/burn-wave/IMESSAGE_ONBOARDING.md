# iMessage onboarding state transitions

Status: **documentation-only; no live messaging performed**

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-23-imessage-onboarding` |
| Slot | `S2-23` |
| Included surface | `Ultra` only |
| Change type | State-transition documentation |

## Purpose

This document defines the iMessage onboarding lifecycle without initiating
onboarding, sending a message, or asserting that a contact is currently
bound. It is a contract for describing state; it is not an integration
implementation or a connectivity check.

The shared iMessage flow is recipient-first: the person receives onboarding
instructions, uses the supplied connection action to reach the shared router,
opens the returned contact card, and starts the iMessage conversation from
that card. The connection action is a user-controlled step. This change does
not perform it.

## Scope fences

- Included: the `Ultra` onboarding state model for slot `S2-23`.
- Excluded: `OD`, `Willow SKILL.md`, `CONV2_B`, and every other S2 slot.
- `Vultr` and `Cold Steel` are distinct labels and must not be treated as
  equivalent environments, providers, or states.
- No live messaging, onboarding lookup, QR-code retrieval, contact-card
  retrieval, account inspection, or secret handling is part of this change.

## State vocabulary

| State | Meaning | Evidence required to enter |
| --- | --- | --- |
| `UNINITIALIZED` | No onboarding context has been presented or recorded. | None. This is the safe initial state. |
| `ONBOARDING_PRESENTED` | A user-facing onboarding instruction is available for the selected identity. | A read-only onboarding presentation exists; it does not prove a connection. |
| `USER_ACTION_PENDING` | The person still needs to complete the connection flow shown by onboarding. | The presentation was acknowledged or handed off; no programmatic send is implied. |
| `CONTACT_CARD_RETURNED` | The shared router has returned the contact card needed to start the conversation. | A user or an authorized read-only status source confirms the card return. |
| `BOUND` | The person has opened the returned card and completed the iMessage-side connection. | Explicit confirmation of the completed bind; never infer this from an onboarding screen alone. |
| `RELEASED` | A previous assignment is no longer connected. | An authoritative release or disconnect result. |
| `BLOCKED` | Policy or missing setup prevents the next transition. | A specific, non-secret reason suitable for an operator. |
| `UNKNOWN` | The result of a transition cannot be established. | Interruption, timeout, or contradictory evidence. |

`BOUND` is not a default or optimistic state. In particular, this document
does not move the slot into `BOUND`.

## Allowed transitions

```text
UNINITIALIZED
    -> ONBOARDING_PRESENTED
    -> USER_ACTION_PENDING
    -> CONTACT_CARD_RETURNED
    -> BOUND

BOUND
    -> RELEASED
    -> UNKNOWN

RELEASED
    -> ONBOARDING_PRESENTED

Any state
    -> BLOCKED
    -> UNKNOWN
```

The linear path is conceptual: each arrow describes the evidence that a
future implementation must obtain, not an action performed by this change.

| From | To | Transition condition | Guard |
| --- | --- | --- | --- |
| `UNINITIALIZED` | `ONBOARDING_PRESENTED` | The approved onboarding instructions are made available. | Presentation is read-only and contains no credentials or private identifiers. |
| `ONBOARDING_PRESENTED` | `USER_ACTION_PENDING` | The instructions are handed to the person who must complete the connection flow. | Do not send on the person's behalf. |
| `USER_ACTION_PENDING` | `CONTACT_CARD_RETURNED` | The shared router returns the contact card after the person completes the connection step. | Do not claim this state without an external confirmation. |
| `CONTACT_CARD_RETURNED` | `BOUND` | The person opens the returned card and completes the iMessage-side bind. | Do not infer a bind from a QR scan, a displayed card, or a prepared compose view. |
| `BOUND` | `RELEASED` | The prior assignment is released. | A released assignment requires onboarding again. |
| `RELEASED` | `ONBOARDING_PRESENTED` | A new onboarding presentation is requested. | Treat the old bind as unusable. |
| `Any` | `BLOCKED` | A required setup or policy condition is absent. | Report only a safe, actionable reason. |
| `Any` | `UNKNOWN` | The system cannot establish whether the transition completed. | Do not retry automatically or report success. |

## Operational invariants

1. **No send in this slice.** No user message, `connect` action, contact-card
   interaction, or outbound iMessage is initiated by this document.
2. **Onboarding is not binding.** `ONBOARDING_PRESENTED` and
   `USER_ACTION_PENDING` do not establish a connected person.
3. **Release requires re-onboarding.** A released assignment must follow the
   onboarding path again; it must not silently return to `BOUND`.
4. **Unknown is conservative.** An interrupted or contradictory result remains
   `UNKNOWN` until an authorized status source resolves it.
5. **The iMessage route is identity-scoped.** The state belongs to the
   selected identity and recipient binding, not to an unrelated phone,
   provider, host, or environment label.
6. **Receipts are secret-free.** A future receipt may include state, outcome,
   and a redacted operation reference, but never message text, phone numbers,
   contact-card contents, credentials, cookies, tokens, or private URLs.

## Offline acceptance checklist

- [ ] The state names and transitions above are documented without invoking a
      messaging or onboarding operation.
- [ ] `BOUND` requires explicit external confirmation and is not claimed here.
- [ ] `UNKNOWN`, `BLOCKED`, and `RELEASED` have conservative recovery rules.
- [ ] The scope fences exclude `OD`, `Willow SKILL.md`, `CONV2_B`, other S2
      slots, and any Vultr/Cold Steel conflation.
- [ ] No secrets, personal identifiers, live endpoints, or message contents
      are present.
