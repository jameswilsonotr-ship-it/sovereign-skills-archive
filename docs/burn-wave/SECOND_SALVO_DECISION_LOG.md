# Second Salvo Decision Log

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-09-decision-log` |
| Slot | `S2-09` |
| Status | Draft; decisions below remain unresolved |
| Base | `skill-tree-intake` |
| Artifact | `docs/burn-wave/SECOND_SALVO_DECISION_LOG.md` |

## Purpose

This is the decision register for the S2-09 second-salvo work. It records what
still needs a human decision, who must approve it, and what evidence is
required before the decision can be treated as closed. It is not an approval
record and it does not authorize work in another slot.

## Fixed hard fences

These are constraints for S2-09, not decisions to be inferred or relaxed:

- **Included Ultra only.** `OD` is excluded; no OD item may be promoted by
  implication, alias, or fallback.
- **No `Willow SKILL.md`.** It is not a source, dependency, input, or
  deliverable for this slot.
- **No `CONV2_B`.** It is outside the S2-09 evidence and output boundary.
- **`Vultr` ≠ `Cold Steel`.** They are distinct labels and environments; a
  reference to one must not be silently classified as the other.
- **No external calls.** Resolution must use repository-local, already
  available evidence. Do not call external services, connectors, runtimes, or
  remote research sources to fill a gap.
- **No secrets.** Do not collect, paste, generate, or commit credentials,
  tokens, cookies, private URLs, personal addresses, or unredacted private
  payloads.
- **S2-09 only.** Do not edit, close, infer, or bundle any other S2 slot.

If a proposed action conflicts with a fence, stop and route it to the
appropriate human approver; do not resolve the conflict by assumption.

## Unresolved decision register

| ID | Decision still required | Why it is unresolved | Required human approver | Closure evidence |
| --- | --- | --- | --- | --- |
| S2-09-D01 | Define the exact admission rule for **Included Ultra** items. | “Included Ultra” is a scope label, not yet a complete item-level manifest or acceptance rule in this log. | S2-09 scope owner | An approved item list or manifest, with each item mapped to the Included Ultra rule. |
| S2-09-D02 | Decide how ambiguous or dual-labelled candidates are handled. | A candidate cannot be admitted merely because it is adjacent to Ultra; the tie-break rule is not recorded. | S2-09 scope owner and content custodian | Written tie-break rule and disposition for every ambiguous candidate. |
| S2-09-D03 | Confirm the disposition of all OD candidates. | The fence says no OD, but the candidate inventory and final reject/park action are not recorded here. | S2-09 scope owner | A reviewed OD exclusion list; no OD item appears in the Included Ultra output. |
| S2-09-D04 | Confirm the source boundary and treatment of references to excluded material. | The log names `Willow SKILL.md` and `CONV2_B` as excluded, but a human must decide whether any indirect mention is rejected, redacted, or merely noted. | Skill-tree/content custodian | Reviewed source inventory showing neither excluded surface is used as input or output. |
| S2-09-D05 | Approve the environment taxonomy and ownership boundary for `Vultr` versus `Cold Steel`. | The labels are explicitly non-equivalent, but the operational owner and allowed classification for each are not recorded. | Infrastructure owner | A two-column classification/ownership note with no cross-labeling. |
| S2-09-D06 | Confirm what counts as acceptable offline evidence. | The no-external-calls fence requires local evidence, but the minimum review artifact and reproducibility check are not specified. | Release or security reviewer | Reproducible local receipt naming inputs, checks, and outputs without network-dependent evidence. |
| S2-09-D07 | Approve the secret-safety review gate. | “No secrets” is mandatory, but the human sign-off and redaction/check method are not assigned. | Security/privacy owner | Human sign-off after reviewing the diff, receipt, and generated artifacts for secret material. |
| S2-09-D08 | Confirm the slot lock and deferment of adjacent S2 work. | This log is for S2-09 only; no owner has yet recorded the boundary for neighboring S2 requests. | S2 coordinator or program owner | Scope sign-off stating that only S2-09 changes are included and all other S2 slots are deferred. |

## Required approver record

Approver names are intentionally unassigned in this draft. A machine check,
agent assertion, or silence is not a human approval. Before a decision is
closed, record the human approver, date, decision ID, and a link or repository
path to the evidence:

| Role | Required responsibility | Name | Status |
| --- | --- | --- | --- |
| S2-09 scope owner | Included Ultra boundary, ambiguity rule, and OD exclusion | `UNASSIGNED` | Pending |
| Content custodian | Excluded-source boundary for `Willow SKILL.md` and `CONV2_B` | `UNASSIGNED` | Pending |
| Infrastructure owner | Separate `Vultr` and `Cold Steel` classification | `UNASSIGNED` | Pending |
| Release/security reviewer | Offline evidence and no-external-calls gate | `UNASSIGNED` | Pending |
| Security/privacy owner | No-secrets review | `UNASSIGNED` | Pending |
| S2 coordinator/program owner | S2-09-only scope lock | `UNASSIGNED` | Pending |

One human may fill more than one role only when that person explicitly accepts
each responsibility. Do not replace a required human approver with an
automated green check.

## Closure protocol

1. The responsible approver answers one register row at a time; do not mark
   unrelated rows closed by association.
2. Record the decision and evidence without adding excluded source content.
3. Re-check the final diff and artifact list for secrets, external-call
   claims, and edits outside S2-09.
4. Leave a row **Pending** when its approver, evidence, or scope is unclear.
   Pending decisions block treating this log as final.

## Draft receipt

- **Change:** `second-salvo-09-decision-log`
- **Slot:** `S2-09`
- **Included surface:** Included Ultra only; OD excluded
- **Excluded surfaces:** `Willow SKILL.md`, `CONV2_B`, and all other S2 slots
- **Environment distinction:** `Vultr` and `Cold Steel` remain separate
- **Evidence policy:** repository-local and secret-free; no external calls
- **Decision state:** eight decisions pending human approvers
