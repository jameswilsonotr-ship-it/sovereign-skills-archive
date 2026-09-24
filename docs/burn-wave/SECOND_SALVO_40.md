# SECOND_SALVO_40.md — next included-burn wave

**Status:** planning-only
**Activation:** after the first included-burn wave has landed on the target base
**Capacity:** exactly 40 included agents
**Mode:** one atomic change-id, one focused PR, one reviewable receipt per agent

This is the dispatch plan for the next forty included agents. It does not
authorize paid or on-demand capacity, provider calls, Vultr provisioning,
Linear posting, deployment, or live skill-tree writes. The second salvo starts
from the first-wave landing commit, not from a stale local checkout.

## Entry gate

Do not dispatch `S2-01` through `S2-40` until all of these are true:

- [ ] The first-wave PRs are merged into the declared base branch.
- [ ] The landed first-wave commit and changed paths are recorded in a receipt.
- [ ] The first-wave roster has been reconciled against the landed files.
- [ ] The burn-wave fence checklist is checked, or every unchecked item has
      been recorded as a stop condition.
- [ ] A second-salvo ledger assigns each slot below to exactly one agent,
      change-id, branch, and owner.
- [ ] No two slots own the same file, generated output, or OpenSpec change-id.
- [ ] The base branch is fetched after the first-wave landing and every agent
      branches from that exact commit.

If the gate cannot be proven from repository evidence, pause the salvo and
return the missing evidence for review. Do not infer that “landed” means
“approved” or that included capacity permits paid work.

## Atomic dispatch contract

Every slot is a separate, included-only unit:

1. Assign the reserved change-id to one agent.
2. Give that agent one narrow deliverable and an explicit file boundary.
3. Require one branch and one PR for that change-id.
4. Require a receipt containing the files changed, validation run, and
   side-effect statement.
5. Review and land the unit before reusing its paths or change-id.

Agents must not combine slots, opportunistically repair neighboring work, or
write shared indexes concurrently. A slot that discovers scope expansion
stops, records the conflict, and returns to intake.

## Dispatch matrix

The IDs below are reserved labels for the second-salvo ledger. They are not
permission to create all forty changes immediately; each becomes active only
when its atomic scope is assigned.

| Slot | Reserved change-id | Atomic deliverable |
|---|---|---|
| S2-01 | `second-salvo-01-intake-receipt` | Record the first-wave landing commit, merged PRs, and source/base refs. |
| S2-02 | `second-salvo-02-path-ledger` | Produce a machine-checkable changed-path ledger for the landed wave. |
| S2-03 | `second-salvo-03-roster-reconcile` | Reconcile the first-wave roster with actual PR owners and files. |
| S2-04 | `second-salvo-04-provenance-audit` | Audit dates, source claims, and stale-snapshot labels in burn-wave docs. |
| S2-05 | `second-salvo-05-collision-scan` | Scan the second-salvo plan for duplicate ownership and reserved-path collisions. |
| S2-06 | `second-salvo-06-shelf-index` | Add or refresh the burn-wave shelf index without rewriting historical docs. |
| S2-07 | `second-salvo-07-status-delta` | Record a point-in-time delta from the first-wave status board. |
| S2-08 | `second-salvo-08-pr-brief-template` | Define the minimal evidence-backed PR brief for second-salvo work. |
| S2-09 | `second-salvo-09-decision-log` | Capture unresolved decisions and their required human approvers. |
| S2-10 | `second-salvo-10-terminology-audit` | Check burn, included, atomic, and fence terminology for consistent use. |
| S2-11 | `second-salvo-11-fixture-inventory` | Inventory existing offline fixtures and identify one bounded gap. |
| S2-12 | `second-salvo-12-connector-fixture` | Add one deterministic connector fixture with no provider access. |
| S2-13 | `second-salvo-13-phone-fixture` | Add one deterministic phone-MCP fixture with default-deny behavior. |
| S2-14 | `second-salvo-14-corpus-manifest` | Document hashes, provenance, and local-only boundaries for one corpus set. |
| S2-15 | `second-salvo-15-rejection-matrix` | Add rejection cases for malformed, unauthorized, or out-of-scope inputs. |
| S2-16 | `second-salvo-16-drive-contract` | Document one Drive connector contract and its offline acceptance cases. |
| S2-17 | `second-salvo-17-github-contract` | Document one GitHub connector contract and its read/write boundary. |
| S2-18 | `second-salvo-18-linear-draft` | Add a paste-ready Linear update draft; do not post it. |
| S2-19 | `second-salvo-19-gmail-contract` | Document one Gmail connector contract and redaction expectations. |
| S2-20 | `second-salvo-20-calendar-contract` | Document one calendar connector contract and conflict behavior. |
| S2-21 | `second-salvo-21-phone-intent-safety` | Specify one phone intent’s authorization, failure, and audit contract. |
| S2-22 | `second-salvo-22-sms-default-deny` | Add offline cases proving SMS remains default-deny without consent. |
| S2-23 | `second-salvo-23-imessage-onboarding` | Document iMessage onboarding state transitions without sending a message. |
| S2-24 | `second-salvo-24-call-fixture` | Add a non-live call-history or transcript fixture with redacted content. |
| S2-25 | `second-salvo-25-redaction-check` | Define and exercise one secret/PII redaction check over local fixtures. |
| S2-26 | `second-salvo-26-openspec-matrix` | Add one deterministic OpenSpec-to-file traceability matrix. |
| S2-27 | `second-salvo-27-acceptance-cases` | Write acceptance cases for one already-scoped change-id. |
| S2-28 | `second-salvo-28-negative-cases` | Write negative acceptance cases and explicit stop conditions. |
| S2-29 | `second-salvo-29-offline-test-plan` | Define the offline test command, fixtures, and expected evidence. |
| S2-30 | `second-salvo-30-receipt-schema` | Define the smallest receipt schema that proves an atomic unit landed. |
| S2-31 | `second-salvo-31-packager-contract` | Document one packaging boundary and its deterministic validation. |
| S2-32 | `second-salvo-32-skill-path-inventory` | Inventory one skill-tree path without modifying live `SKILL.md` files. |
| S2-33 | `second-salvo-33-skill-lock-audit` | Verify the Willow `SKILL.md` lock and record evidence only. |
| S2-34 | `second-salvo-34-dependency-inventory` | Record one dependency/license boundary; do not install or upgrade packages. |
| S2-35 | `second-salvo-35-artifact-hygiene` | Check generated artifacts for accidental payloads, secrets, or oversized files. |
| S2-36 | `second-salvo-36-link-check` | Check repository-relative links within the second-salvo documentation shelf. |
| S2-37 | `second-salvo-37-diff-hygiene` | Run and record whitespace, path, and accidental-file checks. |
| S2-38 | `second-salvo-38-independent-review` | Perform a focused review of one landed second-salvo unit. |
| S2-39 | `second-salvo-39-evidence-bundle` | Assemble links to receipts and validation output without duplicating content. |
| S2-40 | `second-salvo-40-closeout` | Publish the closeout ledger: landed, deferred, blocked, and next human decisions. |

## Sequencing

- **Intake (S2-01–S2-05)** is sequential and establishes the second-salvo
  ledger.
- **Documentation (S2-06–S2-10)** may start after the ledger and must not
  rewrite the intake receipt.
- **Fixtures and connectors (S2-11–S2-20)** may run in parallel only when
  their paths and fixture namespaces are disjoint.
- **Safety and acceptance (S2-21–S2-30)** require the relevant fixture or
  contract owner to be named in the ledger.
- **Packaging and hygiene (S2-31–S2-35)** remain inventory/validation work;
  they do not authorize live skill-tree edits or dependency installation.
- **Review and closeout (S2-36–S2-40)** run after their referenced units
  produce receipts. S2-40 is the only slot that may mark the salvo complete.

## Hard stops

Stop the affected slot immediately if it would:

- add, copy, generate, install, or modify a Willow `SKILL.md`;
- create, enable, or assume a `CONV2_B` surface;
- conflate Vultr with Cold Steel;
- incur Vultr or any other provider spend without explicit current approval;
- contact a phone, connector, provider, Linear, GitHub, or external service;
- add credentials, tokens, private keys, model weights, or unredacted payloads;
- take ownership of a file already assigned to another slot; or
- require a second change-id to finish the first.

Record the stop reason in the slot receipt. A blocked slot is not silently
reassigned and does not consume another slot’s scope.

## Definition of done

The second salvo is complete only when all forty slots have one of these
explicit states: **landed**, **deferred**, or **blocked**, with no blank
receipts; all landed work passes its declared offline validation; the
changed-path ledger is reconciled; and the closeout records the human
decisions still required. “Agent dispatched” is not an acceptance state.
