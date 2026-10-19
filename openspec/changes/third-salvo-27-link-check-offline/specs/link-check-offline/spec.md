# Capability: offline link checking

## Requirement: tier and execution boundary

The capability MUST be marked `INCLUDED` and `Ultra` and MUST NOT be available
to `On-Demand`.

The capability MUST inspect only files available in the local workspace. It
MUST NOT make network requests, resolve remote content, read credentials, or
depend on service configuration.

### Scenario: included Ultra validation

- **GIVEN** a workspace is being validated for the third salvo
- **WHEN** the capability is selected for the `Ultra` tier
- **THEN** the local Markdown link check is permitted
- **AND** the result identifies the workspace root and checked file count

### Scenario: On-Demand selection

- **GIVEN** a request is marked `On-Demand`
- **WHEN** the capability would be selected
- **THEN** the capability is rejected before any files are checked
- **AND** no fallback execution is attempted

## Requirement: local target resolution

The checker MUST inspect Markdown inline links, reference links, and images.
For a relative target, it MUST resolve the path from the Markdown file that
contains the link.

The checker MUST ignore the fragment while resolving a path. A target with a
missing local path MUST be reported as a failure containing the source file,
line, and target.

### Scenario: valid relative target

- **GIVEN** `guide/start.md` links to `../README.md`
- **AND** `README.md` exists inside the workspace
- **WHEN** the checker runs
- **THEN** the link passes

### Scenario: missing relative target

- **GIVEN** `guide/start.md` links to `../missing.md`
- **WHEN** the checker runs
- **THEN** the link fails
- **AND** the failure names `guide/start.md`, its line, and `../missing.md`

## Requirement: fragment validation

When a local target contains a fragment, the checker MUST verify that the
fragment matches a heading slug or an explicit HTML `id` in the target
Markdown/HTML document. Fragment matching MUST be deterministic and
case-insensitive for heading slugs.

### Scenario: existing heading fragment

- **GIVEN** `README.md` contains the heading `## Getting Started`
- **AND** another file links to `README.md#getting-started`
- **WHEN** the checker runs
- **THEN** the fragment passes

### Scenario: missing fragment

- **GIVEN** a link targets `README.md#unknown-section`
- **AND** no matching heading slug or HTML `id` exists
- **WHEN** the checker runs
- **THEN** the link fails with the missing fragment

## Requirement: deterministic reporting

The checker MUST sort findings by source path, line number, and target. It MUST
return exit status `0` when no local failures are found, `1` when one or more
local failures are found, and `2` for invalid usage.

Non-local targets MUST be reported as skipped rather than fetched. Skips MUST
not cause a failure.

### Scenario: clean workspace

- **GIVEN** every local target and checked fragment resolves
- **WHEN** the checker runs
- **THEN** it exits with status `0`

### Scenario: invalid root

- **GIVEN** the requested workspace root does not exist
- **WHEN** the checker starts
- **THEN** it exits with status `2`
- **AND** it does not inspect files outside the requested root
