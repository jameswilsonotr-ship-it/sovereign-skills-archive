# Tube-2 spent-by-rule stamp

## Requirements

### Requirement: identify the reserved slot

The change MUST identify the stamp as slot `T3-08` in `THIRD_SALVO` and use
the reserved change ID `third-salvo-08-tube2-spent-stamp`.

#### Scenario: reviewer locates the allocation

- **WHEN** a reviewer opens the stamp artifact
- **THEN** the salvo, slot, and change ID are present as exact values

### Requirement: constrain inclusion and tier

The stamp MUST record `INCLUDED` as the inclusion mode and `Ultra` as the
only tier.

#### Scenario: reviewer checks the allowed lane

- **WHEN** a reviewer evaluates the stamped allocation
- **THEN** the allocation is visibly `INCLUDED` at `Ultra`
- **AND** no other tier is offered as an equivalent or fallback

### Requirement: mark Tube-2 spent by rule

The stamp MUST state that Tube-2 is `spent-by-rule` and MUST distinguish this
state from a live execution or provider-side action.

#### Scenario: the stamp is consumed as a record

- **WHEN** the artifact is read as an allocation record
- **THEN** Tube-2 is treated as spent by rule
- **AND** the artifact does not request, authorize, or perform execution

### Requirement: prohibit On-Demand use

The stamp MUST explicitly prohibit `On-Demand` use for this slot. The
prohibition applies to direct use, fallback, substitution, and later
reinterpretation of the stamp.

#### Scenario: an On-Demand path is considered

- **WHEN** a consumer evaluates whether the slot can enter an On-Demand path
- **THEN** the answer is no
- **AND** the artifact remains `INCLUDED` + `Ultra` only

### Requirement: remain offline and documentation-only

The change MUST be satisfiable from repository documentation alone and MUST
not require secrets, provider calls, live infrastructure, or external
tracking-system writes.

#### Scenario: receipt verification runs offline

- **WHEN** the change is reviewed or validated in the repository
- **THEN** verification uses only local files and text checks
- **AND** no external or live-system action is needed
