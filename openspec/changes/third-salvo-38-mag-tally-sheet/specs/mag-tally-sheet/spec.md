# Mag Tally Sheet Specification

## Purpose

Define the manual tally record for `THIRD_SALVO` slot `T3-38`.

## Requirements

### Requirement: identify the slot

The sheet MUST identify the change ID, salvo, slot, and inclusion class in its
header.

#### Scenario: a new sheet is opened

- **WHEN** a reviewer opens a T3-38 sheet
- **THEN** the header shows `third-salvo-38-mag-tally-sheet`
- **AND** the header shows `THIRD_SALVO`
- **AND** the header shows `T3-38`
- **AND** the header shows `INCLUDED_ULTRA`

### Requirement: accept included Ultra rows only

The sheet MUST accept tally rows only for `INCLUDED Ultra`.

#### Scenario: an included Ultra count is recorded

- **WHEN** an operator records a whole-number count for an included Ultra item
- **THEN** the row may be added to the tally
- **AND** the count contributes to the total

#### Scenario: an On-Demand count is presented

- **WHEN** a count is identified as On-Demand
- **THEN** it MUST be excluded from the sheet total
- **AND** it MUST NOT be relabeled as included Ultra

### Requirement: reconcile the total

The sheet MUST expose a total that can be checked from the accepted rows.

#### Scenario: the sheet is reviewed

- **WHEN** a reviewer adds the accepted row counts
- **THEN** the result matches the stated total
- **AND** the reviewer can record initials and a review marker

### Requirement: remain offline

The sheet MUST work as a standalone Markdown document.

#### Scenario: the tally is used without connectivity

- **WHEN** the document is copied or edited offline
- **THEN** all required fields and rules remain available in the document
- **AND** no lookup outside this document is required to calculate or review
  the total
