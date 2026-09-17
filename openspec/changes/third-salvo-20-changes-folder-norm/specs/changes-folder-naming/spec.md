# Changes-folder naming

## ADDED Requirements

### Requirement: Change directories use canonical IDs

Every directory directly under `openspec/changes/` MUST be named with a
unique lowercase kebab-case change ID.

#### Scenario: A new change is created

- **WHEN** an author creates an OpenSpec change
- **THEN** the change is placed at
  `openspec/changes/<change-id>/`
- **AND** `<change-id>` matches
  `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`
- **AND** the ID is not already used by another change directory

### Requirement: Directory and proposal IDs stay aligned

The directory name MUST exactly match the `Change ID` declared in that
change's `proposal.md`.

#### Scenario: A change is reviewed

- **WHEN** a reviewer compares a change directory with its proposal
- **THEN** the two change IDs are identical
- **AND** no alias directory is used as an alternate path

### Requirement: Change contents follow the canonical shape

Each change directory MUST contain `proposal.md`, `tasks.md`, and a `specs/`
directory. Each capability directory under `specs/` MUST use lowercase
kebab-case and contain its `spec.md`.

#### Scenario: A change is discoverable

- **WHEN** tooling resolves a change by its canonical ID
- **THEN** it can find the proposal, task list, and capability specification
  beneath the same change directory
