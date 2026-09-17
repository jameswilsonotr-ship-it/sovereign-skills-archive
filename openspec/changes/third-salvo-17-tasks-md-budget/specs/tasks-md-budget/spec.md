# Tasks Markdown Budget

## ADDED Requirements

### Requirement: Limit the task-list artifact

The change MUST keep its `tasks.md` at or below 1,024 UTF-8 bytes and 24
non-empty lines. The file MUST contain a size-budget note and remain readable
without relying on generated content.

#### Scenario: Budget is checked locally

- **GIVEN** the change is validated offline
- **WHEN** the byte and non-empty-line counts for `tasks.md` are measured
- **THEN** both counts are within the stated limits

### Requirement: Restrict eligibility to Included Ultra

The change MUST apply only to the `INCLUDED` mode at the `Ultra` tier.

#### Scenario: Included Ultra is eligible

- **GIVEN** mode is `INCLUDED`
- **AND** tier is `Ultra`
- **THEN** the change's task list and budget rule apply

#### Scenario: On-Demand is excluded

- **GIVEN** mode is `On-Demand`, regardless of tier
- **THEN** this change MUST NOT apply
- **AND** no fallback or automatic enrollment is permitted
