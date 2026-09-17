# S2-28 negative acceptance cases

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-28-negative-cases` |
| Slot | `S2-28` |
| Scope | Included **Ultra** only |
| Explicit exclusion | **OD** and every other S2 slot |
| Execution mode | Local, offline, fail-closed |

This document defines negative acceptance: the slice passes when each
prohibited input is rejected before it can be ingested, transformed, routed,
or published. A refusal is the expected result. No case below authorizes a
fallback, a best-effort interpretation, or an external lookup.

## Acceptance contract

An S2-28 run is acceptable only if all of the following are true:

1. The candidate is explicitly identified as an included Ultra item.
2. The candidate is not OD and is not assigned to another S2 slot.
3. No prohibited artifact, identifier, environment conflation, external call,
   or secret crosses the intake boundary.
4. The first failed fence produces a deterministic rejection and an immediate
   stop.
5. The rejected value is not copied into a receipt, generated artifact,
   network request, log, or PR text.

An unknown, missing, conflicting, or malformed classification is a rejection;
it is never inferred to be included Ultra.

## Negative acceptance cases

Each case is independently executable against the intake boundary. “Stop” is
part of the expected assertion, not an operator suggestion.

### S2-28-N01 — OD presented as included Ultra

- **Input:** A candidate is labeled `OD`, or its source metadata says OD while
  another field says Ultra.
- **Expected result:** Reject the candidate as out of scope.
- **Stop condition:** Stop before opening, parsing, copying, or publishing the
  candidate. Do not relabel OD as Ultra.
- **Pass evidence:** The receipt records a scoped rejection without the
  candidate contents; no output is produced.

### S2-28-N02 — Willow SKILL.md discovered

- **Input:** Any path, manifest entry, or content reference resolves to
  `Willow SKILL.md`.
- **Expected result:** Reject the candidate.
- **Stop condition:** Stop immediately; do not read, compare, summarize,
  modify, or include the file.
- **Pass evidence:** The run terminates with a scope-fence rejection and no
  Willow file bytes appear in output, logs, receipts, or PR text.

### S2-28-N03 — CONV2_B identifier appears

- **Input:** `CONV2_B` occurs in a path, identifier, manifest, payload, or
  generated name.
- **Expected result:** Reject the candidate and the run.
- **Stop condition:** Stop before any downstream processing. Do not treat the
  identifier as an alias, fixture, or recoverable warning.
- **Pass evidence:** The run has no generated artifact and no downstream call
  after the first occurrence.

### S2-28-N04 — Vultr and Cold Steel are conflated

- **Input:** A mapping, label, or instruction states or implies that Vultr is
  Cold Steel, or leaves the target ambiguous between them.
- **Expected result:** Reject the mapping.
- **Stop condition:** Stop before routing, deployment, environment selection,
  or publication. **Vultr ≠ Cold Steel**; do not normalize either name into
  the other.
- **Pass evidence:** The conflicting mapping is not emitted as a valid
  decision and no environment action is attempted.

### S2-28-N05 — External call is required or attempted

- **Input:** A case asks for network access, provider lookup, remote MCP/API
  invocation, webhook delivery, or any other external call.
- **Expected result:** Reject the operation as non-offline.
- **Stop condition:** Stop before DNS, socket, HTTP, MCP, provider, or
  webhook activity. Do not retry and do not substitute a live service.
- **Pass evidence:** An offline rejection is recorded and the network-call
  counter remains zero.

### S2-28-N06 — Secret or credential-like material is present

- **Input:** A token, API key, password, private key, session credential, or
  other secret is supplied, discovered, or requested.
- **Expected result:** Reject the input.
- **Stop condition:** Stop before displaying, parsing beyond detection,
  storing, redacting into a new artifact, transmitting, or copying the
  material. Never echo the value.
- **Pass evidence:** Only a generic secret-detected rejection is retained; no
  secret value occurs in logs, receipts, outputs, or PR text.

### S2-28-N07 — Another S2 slot is mixed into the slice

- **Input:** A request, path, artifact, or acceptance item names an S2 slot
  other than `S2-28`, or asks this change to implement adjacent slot work.
- **Expected result:** Reject the out-of-slice item.
- **Stop condition:** Stop that item at the scope boundary; do not modify,
  stage, or document another S2 slot.
- **Pass evidence:** The diff contains only the S2-28 negative-case document.

### S2-28-N08 — Ultra inclusion is missing or ambiguous

- **Input:** The candidate has no explicit Ultra inclusion marker, has
  conflicting inclusion metadata, or is described only by a nearby name.
- **Expected result:** Reject as unverified scope.
- **Stop condition:** Stop without guessing, searching externally, or
  promoting the candidate into the included set.
- **Pass evidence:** The candidate is absent from generated output and the
  rejection identifies missing or conflicting Ultra classification.

## Global stop conditions

Stop the entire S2-28 run immediately on the first occurrence of any of the
following:

- OD is encountered or Ultra inclusion cannot be proven.
- `Willow SKILL.md` or `CONV2_B` is encountered.
- Vultr/Cold Steel identity is merged, substituted, or left unresolved.
- Any external call is attempted, requested as a fallback, or required to
  continue.
- Any secret or credential-like material is detected.
- Any work outside S2-28 or any other S2 slot is requested.
- A required fence cannot be evaluated deterministically from local inputs.

After a global stop, do not retry with altered labels, continue with remaining
items, create a partial success receipt, or claim acceptance. Preserve only a
minimal generic stop reason; never preserve prohibited contents.

## Verification checklist

- [ ] Only explicitly included Ultra cases are eligible.
- [ ] OD is rejected and never treated as Ultra.
- [ ] `Willow SKILL.md` is rejected without being read or included.
- [ ] `CONV2_B` is rejected without downstream processing.
- [ ] Vultr and Cold Steel remain distinct.
- [ ] External-call count is zero.
- [ ] No secret value is emitted or persisted.
- [ ] No other S2 slot is changed.
- [ ] The first fence failure stops the run and prevents partial acceptance.
