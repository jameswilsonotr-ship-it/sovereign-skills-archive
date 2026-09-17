# Offline flashlight authorization

## Requirements

### Requirement: Deny by default

The offline flashlight contract MUST deny every supported action when no
capability is explicitly granted.

#### Scenario: No capability is configured

- **GIVEN** a newly constructed flashlight stub
- **WHEN** a caller requests `on`, `off`, or `status`
- **THEN** the decision is denied
- **AND** the decision reports that no operation was performed
- **AND** a denial audit event is emitted

### Requirement: Reject unknown input

The contract MUST deny unknown or malformed actions without copying the
untrusted action into an audit record.

#### Scenario: An unsupported action is requested

- **GIVEN** an action that is not in the supported action set
- **WHEN** the request is evaluated
- **THEN** the decision is denied
- **AND** the audit action is represented by a fixed placeholder
- **AND** the original input is absent from the audit record

### Requirement: Explicit authorization remains offline

An explicitly granted action MAY receive an allowed authorization decision,
but the contract MUST NOT perform or imply physical device I/O.

#### Scenario: Status is explicitly granted

- **GIVEN** `status` is in the configured capability allow-list
- **WHEN** `status` is requested
- **THEN** authorization is allowed
- **AND** the decision reports that no operation was performed
- **AND** no device, filesystem, process, or network adapter is consulted

### Requirement: Audit failure fails closed

If the audit sink cannot accept an event, the contract MUST return a denied
decision and MUST NOT authorize the request.

#### Scenario: Audit sink is unavailable

- **GIVEN** an explicitly allowed action
- **AND** an audit sink that raises while recording
- **WHEN** the action is requested
- **THEN** the decision is denied
- **AND** the reason is the fixed value `audit_unavailable`
- **AND** no sink exception text is returned

### Requirement: Bounded audit records

Each audit event MUST contain only the fields `event`, `action`, `outcome`,
and `reason`, with string values and no secret or request payload field.

#### Scenario: A decision is recorded

- **WHEN** any request is evaluated successfully by the sink
- **THEN** the event contains exactly the bounded contract fields
- **AND** no credential, token, environment value, or arbitrary payload is read

