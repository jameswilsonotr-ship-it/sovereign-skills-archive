# Artifact hygiene specification

## Requirement: Keep the T3-26 eligibility boundary explicit

The pass MUST evaluate only artifacts explicitly included as Ultra for slot
T3-26.

### Scenario: An eligible artifact is reviewed

- **WHEN** an artifact is assigned to T3-26 as Ultra
- **THEN** it MAY be evaluated by the checks in the pass list
- **AND** its evidence MUST be recorded locally

### Scenario: An ineligible tier is encountered

- **WHEN** an artifact is identified as On-Demand
- **THEN** it MUST remain outside this change
- **AND** it MUST NOT be promoted, copied, or marked as passed

## Requirement: Keep the pass offline and non-invasive

The pass MUST use only the checkout and its local Git history. It MUST NOT
download, publish, unpack, or rewrite payload artifacts.

### Scenario: The checkout is evaluated

- **WHEN** the pass runs from a clean checkout
- **THEN** it checks documentation, paths, text format, and working-tree
  hygiene
- **AND** it records a deterministic result

### Scenario: A payload change would be required

- **WHEN** a check would require changing an artifact payload
- **THEN** the check is reported as blocked or not applicable
- **AND** the change does not perform that mutation

## Requirement: Make failures visible

Each checklist item MUST have one of these outcomes: `PASS`, `N/A`, or
`BLOCKED`. An item marked `N/A` or `BLOCKED` MUST include a reason.

### Scenario: The pass list is reviewed

- **WHEN** a reviewer opens `artifact-hygiene-pass.md`
- **THEN** the reviewer can identify the scope, check, evidence, and outcome
- **AND** the reviewer can reproduce every local check without network access
