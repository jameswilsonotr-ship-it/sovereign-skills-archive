# Phone health contract

## Requirements

### Requirement: Health reports the local stub

The service MUST respond to `GET /health` with HTTP `200`, content type
`application/json`, and a JSON object containing:

- `status` equal to `"ok"`;
- `service` equal to `"atomic-phone"`;
- `schema_version` equal to `"1"`;
- `capabilities.sms` equal to `false`;
- `capabilities.flashlight` equal to `false`.

The endpoint MUST be served locally by the stub and MUST NOT require network
access to an external service.

#### Scenario: Offline health probe

- **WHEN** a local client requests `/health`
- **THEN** the client receives the contract payload with HTTP `200`

### Requirement: Sensitive capabilities are denied by default

The service MUST deny SMS and flashlight actions when the caller uses the
default policy. A denied action MUST raise `CapabilityDenied` before invoking
any provider or device integration.

#### Scenario: Default policy blocks SMS

- **WHEN** a caller invokes `send_sms` without an explicit enabled policy
- **THEN** the action is rejected with `CapabilityDenied`

#### Scenario: Default policy blocks flashlight

- **WHEN** a caller invokes `set_flashlight` without an explicit enabled policy
- **THEN** the action is rejected with `CapabilityDenied`

### Requirement: Explicit enablement does not imply implementation

The stub MUST NOT pretend to implement SMS or flashlight integration merely
because a caller constructs an explicitly enabled policy. Until a later change
adds an integration, the action MUST raise `NotImplementedError` after policy
authorization.

#### Scenario: Enabled policy reaches an unimplemented boundary

- **WHEN** a caller explicitly enables a capability
- **THEN** the stub raises `NotImplementedError` and performs no side effect
