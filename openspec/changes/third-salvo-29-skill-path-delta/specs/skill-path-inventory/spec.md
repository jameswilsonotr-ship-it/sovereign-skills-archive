# Skill-path inventory

## Requirements

### Requirement: Emit canonical skill paths

The change MUST emit one row for every tracked source path below
`skill_tree/skills/` whose basename is exactly `SKILL.md` and which is absent
from the recorded baseline.

#### Scenario: Nested entrypoints are retained

- **GIVEN** a valid `SKILL.md` occurs below a skill's nested reference/module
  directory
- **WHEN** the source and baseline are compared
- **THEN** the relative path is retained as its own inventory row

#### Scenario: Non-entrypoint files are excluded

- **GIVEN** a tracked file below `skill_tree/skills/` has a different basename
- **WHEN** the inventory is generated
- **THEN** it does not appear in the inventory

### Requirement: Use the fixed inclusion class

Every row MUST use the exact inclusion class `INCLUDED_ULTRA`. No row MAY use
`ON_DEMAND` or an empty class.

#### Scenario: Consumer receives a T3-29 row

- **GIVEN** a row from this change
- **WHEN** a consumer reads its class column
- **THEN** it receives `INCLUDED_ULTRA`

### Requirement: Keep the manifest deterministic

The inventory MUST contain repository-relative paths, be lexicographically
sorted, and contain no duplicate path.

#### Scenario: Repeated generation

- **GIVEN** the same baseline and source revisions
- **WHEN** the inventory is generated again
- **THEN** the path and class columns are byte-for-byte identical

### Requirement: Remain offline

Validation MUST use only the checkout and its local Git object database. The
change MUST NOT add runtime calls, credentials, or network configuration.

#### Scenario: Offline validation

- **GIVEN** the checkout contains the recorded revisions
- **WHEN** the validation runs without network access
- **THEN** it verifies the manifest and produces a receipt
