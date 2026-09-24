# SMS default-deny and redaction stubs

## Why

The skill-tree intake contains no SMS runtime or provider adapter. An offline
contract is needed before any future integration can be exercised safely.

## What changes

- Add a provider-free `SmsSenderStub` with a default-deny policy.
- Keep the stub incapable of real delivery, including when explicitly enabled:
  opt-in only reports a local simulation.
- Record only redacted audit data; never retain recipient numbers or message
  bodies.
- Add pytest coverage that uses fake values and performs no network I/O.

## Out of scope

- Provider SDKs, credentials, phone-number verification, delivery, retries, or
  production transport behavior.
- Reading environment variables or making HTTP, socket, or messaging calls.
