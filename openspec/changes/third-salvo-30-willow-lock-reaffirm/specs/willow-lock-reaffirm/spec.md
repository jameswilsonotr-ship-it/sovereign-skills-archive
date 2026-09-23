# Willow lock reaffirmation

## Requirements

### Requirement: T3-30 is included for Ultra

The T3-30 Willow slot MUST be classified as `INCLUDED` for the `Ultra`
surface.

#### Scenario: Ultra evaluates T3-30

- **WHEN** the `Ultra` surface evaluates slot T3-30
- **THEN** T3-30 is eligible as an included slot

### Requirement: T3-30 is excluded from On-Demand

The T3-30 Willow slot MUST NOT be classified as `INCLUDED` for, or made
available through, the `On-Demand` surface.

#### Scenario: On-Demand evaluates T3-30

- **WHEN** the `On-Demand` surface evaluates slot T3-30
- **THEN** T3-30 is ineligible

### Requirement: This change is audit-only

The lock reaffirmation MUST be represented by documentation and MUST NOT
modify Willow implementation content.

#### Scenario: Review the change

- **WHEN** this change is reviewed
- **THEN** the diff contains only OpenSpec documentation and its audit receipt
- **AND** no Willow `SKILL.md` is modified
