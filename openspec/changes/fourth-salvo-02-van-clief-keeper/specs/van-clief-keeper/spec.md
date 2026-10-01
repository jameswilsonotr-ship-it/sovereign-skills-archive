# Van Clief keeper specification

## Requirement: identify the CinC target

The change MUST identify T4-02 as the `CinC-TARGET` / `Van Clief keeper`
atomic slice.

### Scenario: target is recorded

- **GIVEN** the T4-02 OpenSpec change is reviewed
- **WHEN** its target is read
- **THEN** it names `CinC-TARGET`
- **AND** it names `Van Clief keeper`

## Requirement: continuous included reload

T4-02 MUST be classified as `CONTINUOUS` reload in the `INCLUDED` lane. It MUST
state that the lane is never On-Demand.

### Scenario: included reload is selected

- **GIVEN** a reader evaluates the T4-02 lane
- **WHEN** the reload mode and entitlement lane are read
- **THEN** the mode is `CONTINUOUS`
- **AND** the lane is `INCLUDED`
- **AND** the lane is explicitly never On-Demand

### Scenario: On-Demand is requested

- **GIVEN** a request names T4-02
- **WHEN** it selects the On-Demand lane
- **THEN** the request is rejected as outside this change
- **AND** no On-Demand receipt is emitted

## Requirement: atomic offline receipt

The deliverable MUST contain one independently reviewable OpenSpec change and
one receipt for T4-02. It MUST remain documentation-only and offline-only.

### Scenario: receipt is reviewed

- **GIVEN** the T4-02 change is checked
- **WHEN** its files are enumerated
- **THEN** the OpenSpec documents and receipt describe one atomic slice
- **AND** no runtime or integration behavior is introduced

## Requirement: hard scope fences

The change MUST NOT edit Willow `SKILL.md` or skill-tree locks, unpack
`CONV2_B`, use external/provider integrations, contain secrets, perform Vultr
work, or authorize On-Demand usage.

### Scenario: offline fence is audited

- **GIVEN** the T4-02 change is validated
- **WHEN** its scope is audited
- **THEN** only repository documentation is in scope
- **AND** the listed fences remain intact
