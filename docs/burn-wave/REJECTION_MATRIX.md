---
id: second-salvo-15-rejection-matrix
title: Second salvo S2-15 rejection matrix
status: proposed
owner: burn-wave
priority: high
summary: Define deterministic offline rejection cases for malformed, unauthorized, and out-of-scope S2-15 inputs.
tags:
  - burn-wave
  - s2-15
  - rejection
  - offline
dependencies: none
---

# Second salvo S2-15 rejection matrix

This is the rejection contract for slot **S2-15**. It is a documentation-only,
offline matrix: a rejected input must stop before normalization, routing, or
any external call. This slot covers **included Ultra only**.

## Scope fence

The only admissible scope is:

- slot: `S2-15`
- mode: `included Ultra`
- execution: local/offline fixtures only
- output: a deterministic rejection receipt or an accepted handoff to the
  S2-15 consumer

The following are hard rejects, not aliases or fallbacks:

- `OD` is not included Ultra.
- `Willow SKILL.md` is not an S2-15 input.
- `CONV2_B` is not an S2-15 input.
- `Vultr ≠ Cold Steel`: they are distinct labels and must never be conflated.
- External calls, network lookups, and remote fetches are out of scope.
- Secrets and credential material are never accepted or echoed.
- Any other S2 slot is out of scope; S2-15 must not mutate or dispatch it.

## Rejection semantics

The validator evaluates the cases in this order:

1. Parse and shape checks.
2. Authorization checks.
3. Scope and hard-fence checks.

The first failing case wins. A rejection receipt contains only the case ID,
category, stable reason code, and a safe remediation hint. It must not contain
the raw input, credentials, tokens, or a network response. Rejections are
terminal for the input; they do not retry, downgrade to another mode, or call a
remote service.

## Matrix

| Case ID | Category | Trigger / input condition | Expected result | Safe remediation |
| --- | --- | --- | --- | --- |
| S2-15-M01 | malformed | Request is empty, not an object, or missing `slot`, `mode`, or `payload`. | Reject with `MALFORMED_INPUT`. | Supply the complete S2-15 envelope. |
| S2-15-M02 | malformed | Serialized input is invalid JSON, truncated, or contains duplicate keys that make the effective value ambiguous. | Reject with `MALFORMED_INPUT`. | Produce one valid, unambiguous offline fixture. |
| S2-15-M03 | malformed | `slot`, `mode`, or required payload fields have the wrong type, or a required value is blank. | Reject with `MALFORMED_INPUT`. | Match the declared field types and provide non-blank values. |
| S2-15-M04 | malformed | Payload includes an unrecognized operation, unsupported version, or fields that cannot be validated by the S2-15 schema. | Reject with `MALFORMED_INPUT`. | Use the pinned S2-15 schema and supported operation. |
| S2-15-U01 | unauthorized | Authorization context is absent, expired, unverifiable, or not bound to the requesting principal. | Reject with `UNAUTHORIZED`. | Establish authorization locally before submitting the fixture. |
| S2-15-U02 | unauthorized | Principal is not authorized for the `included Ultra` mode or for the referenced local fixture. | Reject with `UNAUTHORIZED`. | Use an authorized principal and an owned fixture. |
| S2-15-U03 | unauthorized | Input attempts to cross an owner, tenant, or resource boundary, even if the payload is otherwise well formed. | Reject with `UNAUTHORIZED`. | Submit only resources within the authorized boundary. |
| S2-15-O01 | out of scope | `mode` is `OD`, or the input asks for an OD fallback, conversion, or substitution. | Reject with `OUT_OF_SCOPE`. | Set the mode to `included Ultra`; do not translate OD. |
| S2-15-O02 | out of scope | Path, artifact, or instruction references `Willow SKILL.md`. | Reject with `OUT_OF_SCOPE`. | Remove the Willow skill reference and resubmit only S2-15 material. |
| S2-15-O03 | out of scope | Payload contains `CONV2_B` as a mode, source, route, dependency, or substitution. | Reject with `OUT_OF_SCOPE`. | Remove `CONV2_B`; it is not a valid S2-15 source or route. |
| S2-15-O04 | out of scope | Payload treats `Vultr` and `Cold Steel` as synonyms, aliases, or interchangeable environments. | Reject with `OUT_OF_SCOPE`. | Preserve the labels as distinct; do not map one to the other. |
| S2-15-O05 | out of scope | `slot` names an S2 slot other than `S2-15`, or a batch mixes S2-15 with another S2 slot. | Reject with `OUT_OF_SCOPE`. | Submit a single S2-15 input; do not touch other S2 slots. |
| S2-15-O06 | out of scope | Input requests HTTP, DNS, API, connector, Drive, GitHub, or any other external call. | Reject with `OUT_OF_SCOPE`. | Replace the request with a bounded local fixture. |
| S2-15-O07 | out of scope | Input contains a secret, token, private key, credential, authorization header, or asks the validator to reveal one. | Reject with `OUT_OF_SCOPE`. | Remove the secret material and use a non-secret placeholder. |

## Acceptance checks

- [ ] Every row above produces the stated stable reason code before any
  external call.
- [ ] `included Ultra` is the only accepted mode; `OD` is rejected.
- [ ] `Willow SKILL.md`, `CONV2_B`, and cross-slot inputs are rejected.
- [ ] `Vultr` and `Cold Steel` remain distinct in validation and receipts.
- [ ] No network, connector, or remote service is required to evaluate a case.
- [ ] Rejection receipts do not expose raw input or secret material.
- [ ] The implementation changes no slot other than S2-15.

## Receipt shape

The minimum safe receipt is:

```text
slot=S2-15
case_id=S2-15-O01
category=out_of_scope
reason=OUT_OF_SCOPE
action=reject_without_external_call
```

The receipt deliberately omits the submitted payload and any authorization
material.
