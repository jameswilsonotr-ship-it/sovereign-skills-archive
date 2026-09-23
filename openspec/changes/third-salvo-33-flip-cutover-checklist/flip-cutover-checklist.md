# Paper checklist — T3-33 flip cutover

**Change ID:** `third-salvo-33-flip-cutover-checklist`
**Workstream:** `THIRD_SALVO`
**Slot:** `T3-33`
**Allowed class:** `INCLUDED Ultra`
**Procedure boundary:** offline-only; paper record, not an execution claim

> Every box is a gate. If a value is unknown, blank, aliased, or conflicting,
> stop and record the reason. `On-Demand` is never acceptable for T3-33.

## 1. Pre-flip identity gate

- [ ] Change ID matches `third-salvo-33-flip-cutover-checklist`.
- [ ] Workstream matches `THIRD_SALVO`.
- [ ] Slot matches `T3-33`.
- [ ] Reviewed class equals `INCLUDED Ultra` exactly.
- [ ] Reviewed class is not `On-Demand`.
- [ ] The work remains offline-only.
- [ ] No adjacent slot or unrelated change is included.

**Identity notes:**
`______________________________________________________________________________`

## 2. State record

Record values before making or approving any flip decision.

- **Pre-flip class:** `____________________________________________`
- **Pre-flip evidence / local reference:** `________________________`
- **Intended target class:** `INCLUDED Ultra`
- **Decision:** [ ] proceed  [ ] stop
- **Decision reason:** `_______________________________________________________`

The intended target is not evidence that a flip occurred. Do not sign this
section if the pre-flip class is not exactly `INCLUDED Ultra`.

## 3. Flip gate

- [ ] Eligibility gate in section 1 is complete.
- [ ] State record in section 2 is complete.
- [ ] The target remains `INCLUDED Ultra`.
- [ ] No fallback to `On-Demand` is permitted.
- [ ] The reviewer has confirmed this is the T3-33 change only.

**Reviewer initials:** `____________`  **UTC:** `________________`

## 4. Post-flip readback

Record the observed state after the authorized cutover step. If no cutover was
performed, write `NOT EXECUTED` and leave the completion box unchecked.

- **Observed post-flip class:** `____________________________________________`
- **Readback reference / notes:** `___________________________________________`
- [ ] Observed class equals `INCLUDED Ultra` exactly.
- [ ] Observed class is not `On-Demand`.
- [ ] No unexpected scope change was observed.

**Verification result:** [ ] accepted  [ ] stopped  [ ] recovery required
**Verifier initials:** `____________`  **UTC:** `________________`

## 5. Stop and recovery record

Complete this section for any failed gate, ambiguous value, or mismatched
readback. Do not convert a stop into an acceptance.

- **Stop condition:** `________________________________________________________`
- **Affected state:** `_______________________________________________________`
- **Recovery decision:** [ ] hold  [ ] restore recorded pre-flip state
  [ ] escalate for review
- **Recovery notes:** `_______________________________________________________`

## 6. Receipt and handoff

- [ ] Change ID is present in the local receipt.
- [ ] T3-33 and `INCLUDED Ultra` are present in the local receipt.
- [ ] Validation result is recorded.
- [ ] The receipt does not claim an unperformed runtime flip.
- [ ] Reviewer sign-off is complete.

**Operator:** `____________________________`
**Reviewer:** `____________________________`
**Final UTC:** `___________________________`
**Receipt path:** `snapshots/2026-09-17/T3-33_FLIP_CUTOVER_RECEIPT.md`

**Final disposition:** [ ] ready for review  [ ] stopped  [ ] recovery pending
