# Specification: next-40 prep gate

## Requirements

### Requirement: T3-39 must be landed first

The gate MUST require local evidence that the THIRD_SALVO T3-39 change has
landed before it can return a passing result.

#### Scenario: T3-39 land evidence is absent

- **GIVEN** no local commit, tag, or receipt identifies the landed T3-39 result
- **WHEN** the next-40 prep gate is evaluated
- **THEN** the result is `BLOCKED_T3_NOT_LANDED`
- **AND** next-40 preparation is not authorized

#### Scenario: T3-39 land evidence is present

- **GIVEN** a local commit, tag, or receipt identifies the landed T3-39 result
- **WHEN** all remaining gate checks pass
- **THEN** the T3-39 prerequisite is satisfied
- **AND** the gate may return `READY_FOR_NEXT40_PREP`

### Requirement: Ultra is the only accepted mode

The gate MUST accept `Ultra` and MUST reject every other mode.

#### Scenario: Ultra is requested

- **GIVEN** `execution_mode` is exactly `Ultra`
- **WHEN** the mode check runs
- **THEN** the mode check passes

#### Scenario: On-Demand is requested

- **GIVEN** `execution_mode` is `On-Demand`
- **WHEN** the mode check runs
- **THEN** the result is `REJECTED_MODE`
- **AND** the gate does not fall back to or enable Ultra

### Requirement: Evaluation is offline

The gate MUST evaluate from local evidence only and MUST require
`network_access: false`.

#### Scenario: Offline evidence is supplied

- **GIVEN** all required fields are present
- **AND** `network_access` is `false`
- **WHEN** the gate is evaluated
- **THEN** no network or service call is needed

#### Scenario: Network access is enabled or unknown

- **GIVEN** `network_access` is `true` or cannot be verified
- **WHEN** the gate is evaluated
- **THEN** the result is `REJECTED_OFFLINE`

### Requirement: A receipt records the decision

The gate MUST emit a receipt containing the change ID, slot, execution mode,
T3-39 land reference, offline flag, result, and next action.

#### Scenario: Gate result is emitted

- **GIVEN** the gate has evaluated all required checks
- **WHEN** the result is written
- **THEN** the receipt contains all required evidence fields
- **AND** the receipt does not imply authorization for next-40 execution
