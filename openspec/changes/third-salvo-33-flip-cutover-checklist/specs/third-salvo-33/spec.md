# Specification: THIRD_SALVO T3-33 eligibility and flip cutover

## Requirements

### Requirement: T3-33 has one allowed class

T3-33 MUST be treated as eligible only when its class equals `INCLUDED Ultra`
exactly.

#### Scenario: Exact class is present

- **GIVEN** the reviewed slot is `T3-33`
- **AND** the reviewed class is `INCLUDED Ultra`
- **WHEN** the cutover gate is evaluated
- **THEN** the slot passes the eligibility gate
- **AND** the paper checklist may proceed to the flip decision

#### Scenario: On-Demand class is present

- **GIVEN** the reviewed slot is `T3-33`
- **AND** the reviewed class is `On-Demand`
- **WHEN** the cutover gate is evaluated
- **THEN** the slot fails the eligibility gate
- **AND** the flip MUST NOT proceed

#### Scenario: Class is ambiguous

- **GIVEN** the reviewed slot is `T3-33`
- **AND** its class is blank, unknown, aliased, or conflicting
- **WHEN** the cutover gate is evaluated
- **THEN** the slot fails closed
- **AND** the reviewer MUST record a stop condition

### Requirement: The cutover is explicitly bounded

The checklist MUST identify the change ID, workstream, slot, allowed class, and
offline-only boundary before any flip decision is recorded. The procedure MUST
not include adjacent slots or unrelated changes.

#### Scenario: Scope is complete

- **GIVEN** the paper checklist is opened
- **WHEN** the pre-flip gate is reviewed
- **THEN** it names `third-salvo-33-flip-cutover-checklist`, `THIRD_SALVO`,
  `T3-33`, and `INCLUDED Ultra`
- **AND** it records that the procedure is offline-only

#### Scenario: Scope is incomplete

- **GIVEN** any required identity or boundary is missing
- **WHEN** the pre-flip gate is reviewed
- **THEN** the checklist is not ready for sign-off
- **AND** no flip decision is recorded

### Requirement: The flip has readback evidence

The paper procedure MUST record the reviewed pre-flip state, the intended
target state, the post-flip readback, and reviewer sign-off. A written
intention alone MUST NOT count as a completed flip.

#### Scenario: Readback matches the allowed class

- **GIVEN** the eligibility gate passed
- **AND** the intended target is `INCLUDED Ultra`
- **WHEN** the post-flip readback is recorded
- **THEN** the readback MUST equal `INCLUDED Ultra`
- **AND** the reviewer may sign off the cutover

#### Scenario: Readback does not match

- **GIVEN** the post-flip readback is blank, unknown, `On-Demand`, or any
  other value
- **WHEN** the checklist is verified
- **THEN** the cutover is not accepted
- **AND** the reviewer records the stop condition and recovery decision

### Requirement: A receipt is produced

Completion MUST produce a local receipt that names the change ID, slot,
allowed class, artifact paths, validation result, and delivery state.

#### Scenario: Documentation-only delivery is complete

- **GIVEN** the proposal, specification, tasks, checklist, and receipt exist
- **AND** the documentation validation passes
- **WHEN** the delivery is closed
- **THEN** the receipt marks the change ready for review
- **AND** it makes no claim that a runtime flip was executed
