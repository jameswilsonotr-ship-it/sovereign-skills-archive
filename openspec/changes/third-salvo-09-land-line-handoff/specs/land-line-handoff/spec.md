# Specification: T3-09 land-line handoff

## Requirements

### Requirement: Preserve the reserved change identity

The change MUST use `third-salvo-09-land-line-handoff` as its change ID and
MUST identify itself as `THIRD_SALVO` slot `T3-09`.

#### Scenario: Change is reviewed

- **GIVEN** a reviewer opens the OpenSpec change
- **WHEN** the change identity is checked
- **THEN** the change ID is exactly `third-salvo-09-land-line-handoff`
- **AND** the slot is identified as `THIRD_SALVO` / `T3-09`

### Requirement: Enforce Included Ultra-only eligibility

The handoff MUST be scoped to Included Ultra. On-Demand MUST NOT be
supported, selected, implied, or used as a fallback for this slot.

#### Scenario: An execution mode is selected

- **GIVEN** a request is evaluated for T3-09
- **WHEN** eligibility is determined
- **THEN** Included Ultra is the only accepted mode
- **AND** an On-Demand request is rejected as out of scope

#### Scenario: The preferred mode is unavailable

- **GIVEN** Included Ultra cannot be used
- **WHEN** a fallback is considered
- **THEN** the slot remains unfulfilled
- **AND** the workflow MUST NOT switch to On-Demand

### Requirement: Keep the delivery offline and documentation-only

The change MUST contain only OpenSpec and handoff documentation. It MUST NOT
require an external/provider call, secret, live Vultr operation, or Linear
mint.

#### Scenario: The change is validated

- **GIVEN** the final diff is inspected
- **WHEN** changed paths and content are reviewed
- **THEN** only documentation paths are present
- **AND** no secret, credential, provider request, or live infrastructure
  action is introduced

### Requirement: Protect the hard-fenced surfaces

The change MUST NOT modify `Willow SKILL.md` and MUST NOT add, process, or
reference `CONV2_B` as an input or delivery surface.

#### Scenario: A forbidden surface appears in review

- **GIVEN** a proposed file or edit touches a hard-fenced surface
- **WHEN** the atomic diff is reviewed
- **THEN** the file or edit is removed before delivery
- **AND** the change remains documentation-only

### Requirement: Deliver one atomic pull request

The complete T3-09 delivery MUST be submitted as one pull request with the
exact title `salvo: T3-09 land-line-handoff`.

#### Scenario: The handoff is delivered

- **GIVEN** the OpenSpec change and handoff note are ready
- **WHEN** the delivery is submitted
- **THEN** both artifacts are included in the same pull request
- **AND** the pull request title is exactly `salvo: T3-09 land-line-handoff`
- **AND** no separate follow-up PR is required to satisfy this contract
