# Envelope & Cross-Skill Consistency

## Requirement: stable response envelope

Response-producing paths MUST expose the same envelope shape:

1. a top line identifying the active skill and mode;
2. the response body;
3. an optional structured front-matter note carrying `skill`, `mode`,
   `debug_outcome`, `heat`, and `clock`;
4. a bottom line identifying completion.

The envelope MUST remain usable when only one skill is active. It MUST NOT
require loading unrelated skills.

## Requirement: visible debug status

When debug information is available, the path MUST emit a compact
`DEBUG_STATUS` signal containing the active skill, mode, and outcome. The
signal MAY be harvested by an orchestrator, but the contract MUST remain
valid without an orchestrator.

## Requirement: single chrome owner

Menus and response paths MUST request the shared envelope rather than
inventing a second border or footer format.

## Requirement: lightweight implementation

This contract MUST be representable as Markdown or JSONL metadata. It MUST NOT
require a full telemetry stack or an integration-specific runtime.

## Scenarios

### Scenario: thin active load

- **WHEN** one skill produces a response
- **THEN** the response uses the stable envelope
- **AND** unrelated skills are not loaded solely to render the envelope

### Scenario: debug outcome exists

- **WHEN** a response path has a debug outcome
- **THEN** it emits `DEBUG_STATUS` with the active skill, mode, and outcome

### Scenario: no debug outcome exists

- **WHEN** a response path has no debug outcome
- **THEN** it may omit `DEBUG_STATUS`
- **AND** it still uses the stable envelope
