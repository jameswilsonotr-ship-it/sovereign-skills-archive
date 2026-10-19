# Landing reconcile index

## Requirements

### Requirement: Index SECOND_SALVO Tube-2 landing state

The change MUST provide a focused index of SECOND_SALVO (Tube-2) pull
requests, with each evidenced row classified as `OPEN` or `MERGED`.

#### Scenario: A locally evidenced Tube-2 PR exists

- **GIVEN** a Tube-2 PR identifier and repository-local landing evidence
- **WHEN** the receipt is updated
- **THEN** the row records the PR identifier, state, and evidence pointer
- **AND** the state is either `OPEN` or `MERGED`

#### Scenario: No local Tube-2 evidence exists

- **GIVEN** the checkout contains no Tube-2 PR manifest, ref, or checked-in
  receipt
- **WHEN** the offline receipt is produced
- **THEN** it MUST report the evidence gap explicitly
- **AND** it MUST NOT invent a PR identifier or infer provider state

### Requirement: Keep the change atomic

The change MUST remain a docs-only landing reconciliation index.

#### Scenario: Scope is reviewed

- **THEN** the change contains no `SKILL.md` edit
- **AND** contains no `CONV2_B` material
- **AND** contains no On-Demand material
- **AND** performs no provider, secret, Vultr, or Linear operation
