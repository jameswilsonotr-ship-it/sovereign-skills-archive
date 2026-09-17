# SMS safety contract

## Requirements

### Requirement: SMS sending is denied by default
The offline sender MUST use a policy whose `allow_send` value defaults to
`False`.

#### Scenario: no policy is supplied
- **WHEN** a caller creates `SmsSenderStub()` and calls `send`
- **THEN** the result status is `denied`
- **AND** the result reason is `default_deny`
- **AND** the result has `sent=False`

### Requirement: the stub cannot deliver SMS
The offline sender MUST perform no provider, network, or transport I/O.
Explicit policy opt-in MAY change the result to `simulated`, but MUST NOT make
the result `sent=True`.

#### Scenario: explicit opt-in remains offline
- **WHEN** a caller creates `SmsSenderStub(policy=SmsPolicy(allow_send=True))`
  and calls `send`
- **THEN** the result status is `simulated`
- **AND** the result reason is `offline_stub`
- **AND** the result has `sent=False`

### Requirement: audit data is redacted
The sender MUST replace recipient numbers with a fixed phone placeholder and
message bodies with a fixed body placeholder. Sensitive metadata keys and
phone-like or secret-assignment values MUST be redacted recursively.

#### Scenario: a denied attempt is logged safely
- **WHEN** a caller attempts to send a message with recipient and metadata
- **THEN** the audit event contains no original recipient or body
- **AND** nested sensitive metadata is replaced with `[REDACTED]`
- **AND** the attempt remains denied by default.
