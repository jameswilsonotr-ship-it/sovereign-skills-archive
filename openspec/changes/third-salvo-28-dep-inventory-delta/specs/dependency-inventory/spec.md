# Dependency inventory delta specification

## Requirement: record an auditable delta

The change MUST identify the inventory evidence used as its baseline and MUST
separate baseline observations from changes introduced by T3-28.

### Scenario: baseline and delta are distinguishable

- **Given** the latest dated local export reports 27 scanned skills
- **And** the historical library ledger reports 32 entries
- **When** a consumer reads the T3-28 delta
- **Then** both counts are preserved as evidence
- **And** the T3-28 change is not represented as a rewrite of either source

## Requirement: include Ultra only

The T3-28 artifact MUST be classified as included in `Ultra`.

### Scenario: included artifact is selected

- **Given** a consumer resolves the T3-28 inclusion tier
- **When** the consumer reads the delta
- **Then** the result is `Ultra`
- **And** the artifact is available as part of the included surface

## Requirement: never classify as On-Demand

The T3-28 artifact MUST NOT have an On-Demand entry, loader, fallback, or
deferred dependency.

### Scenario: On-Demand lookup is attempted

- **Given** a consumer asks for an On-Demand T3-28 dependency
- **When** the consumer reads the delta
- **Then** the result is an explicit exclusion
- **And** no install or remote resolution is implied

## Requirement: document zero dependency change

The delta MUST record zero runtime, build, provider, secret, and installation
dependencies for this documentation-only change.

### Scenario: dependency inventory is computed

- **Given** the change contains only Markdown artifacts
- **When** the dependency inventory is computed locally
- **Then** added dependencies equal zero
- **And** removed dependencies equal zero
- **And** installation actions equal zero

## Requirement: preserve fences

The change MUST avoid introducing forbidden files, integrations, or data
sources, including Willow `SKILL.md`, `CONV2_B`, external/provider inputs,
secrets, Vultr, and Linear.

### Scenario: fence audit passes

- **Given** the change file set is inspected from the repository checkout
- **When** the fence audit runs
- **Then** no forbidden path or input is present
- **And** the audit remains offline
