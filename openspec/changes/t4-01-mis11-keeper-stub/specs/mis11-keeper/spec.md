# MIS-11 keeper

## ADDED Requirements

### Requirement: MIS-11 has one canonical keeper

The T4-01 package SHALL identify exactly one atomic keeper for Linear `MIS-11`
using change ID `t4-01-mis11-keeper-stub`.

#### Scenario: Resolve the keeper

- **WHEN** a documentation consumer resolves the T4-01 keeper
- **THEN** it uses `MIS-11` as the target
- **AND** it uses `t4-01-mis11-keeper-stub` as the change ID
- **AND** it does not create a second alias or parallel keeper

### Requirement: The keeper is continuously included

The MIS-11 keeper SHALL be classified as `INCLUDED` with `CONTINUOUS` reload.

#### Scenario: Inspect keeper metadata

- **WHEN** the keeper metadata is read
- **THEN** `availability` is `INCLUDED`
- **AND** `reload` is `CONTINUOUS`
- **AND** the classification does not depend on a request-time switch

### Requirement: On-Demand is prohibited

The MIS-11 keeper SHALL set `on_demand` to `NEVER`. No alternate or inferred
On-Demand route may be added by this change.

#### Scenario: A consumer asks for a request-time route

- **WHEN** a consumer evaluates the keeper for request-time dispatch
- **THEN** it rejects the route
- **AND** the keeper remains `INCLUDED` with `CONTINUOUS` reload

### Requirement: Keeper paths are canonical

The proposal, specification, and receipt SHALL remain inside the exact
change-package root:

`openspec/changes/t4-01-mis11-keeper-stub/`

The keeper specification SHALL be at:

`openspec/changes/t4-01-mis11-keeper-stub/specs/mis11-keeper/spec.md`

#### Scenario: Check the package layout

- **WHEN** a reviewer resolves the T4-01 package
- **THEN** `proposal.md` is present at the package root
- **AND** the keeper delta is present at the canonical specification path
- **AND** `RECEIPT.md` is present at the package root
- **AND** no applied specification is required for this stub

### Requirement: The stub remains offline and inert

This change SHALL remain documentation-only and SHALL not call Linear or alter
runtime, connector, credential, infrastructure, skill, or conversation data.

#### Scenario: Validate the change boundary

- **WHEN** the package is reviewed offline
- **THEN** only the OpenSpec proposal, keeper delta, task list, and receipt are
  considered in scope
- **AND** no live API evidence is required
- **AND** no runtime behavior is inferred from the stub
