# Offline test harness

## Requirements

### Requirement: enforce the T3-23 slot boundary
The harness MUST accept only slot `T3-23` with `included` availability and
`ultra` tier. It MUST reject a policy that enables on-demand fallback.

#### Scenario: default policy
- **WHEN** the harness is constructed without a policy
- **THEN** it uses T3-23, Included, Ultra, with fallback disabled

#### Scenario: widened policy
- **WHEN** a policy changes the slot, availability, tier, or fallback flag
- **THEN** construction fails with `HarnessConfigurationError`

### Requirement: resolve cases from local fixtures
The harness MUST resolve requests only from explicitly registered fixture
responses.

#### Scenario: registered fixture
- **WHEN** a case matches a registered endpoint and payload
- **THEN** the fixture response is returned and the case passes when expected

#### Scenario: missing fixture
- **WHEN** a case has no matching fixture
- **THEN** the case fails and no alternate request path is attempted

### Requirement: preserve deterministic evidence
The harness MUST record each request and expose a JSON-friendly result.

#### Scenario: result serialization
- **WHEN** a case has been run
- **THEN** its result includes the case ID, pass/fail state, response or reason,
  and recorded request payloads
