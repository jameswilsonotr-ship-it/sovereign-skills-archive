# T3 closeout ledger

## Requirements

### Requirement: identify the closeout slot

The ledger MUST identify the slot as `T3-31` and the change as
`third-salvo-31-closeout-ledger`.

#### Scenario: identity is present

- **WHEN** a reviewer opens the ledger
- **THEN** the slot and change ID are visible in the identity section

### Requirement: preserve Ultra-only inclusion

The ledger MUST mark the slot `INCLUDED / Ultra` and MUST state that
On-Demand is prohibited.

#### Scenario: classification is checked

- **WHEN** a reviewer evaluates the classification
- **THEN** the ledger has one unambiguous included mode
- **AND** no On-Demand path is offered

### Requirement: keep closeout evidence explicit

The ledger MUST provide separate fields for evidence, validation, disposition,
and unresolved items. Empty fields MUST remain visibly incomplete rather than
being implied complete.

#### Scenario: evidence is not yet available

- **WHEN** the skeleton is created before verification
- **THEN** evidence and validation fields remain unchecked or marked pending
- **AND** the record does not claim closeout completion

### Requirement: enforce the offline boundary

The change MUST be completable with repository-local text only. It MUST NOT
require network access, provider integration, credential material, or
deployment infrastructure.

#### Scenario: local review

- **WHEN** the change is reviewed offline
- **THEN** the identity, fence, and checklist structure can be inspected
- **AND** no remote operation is necessary
