# Change: Add an offline, default-deny flashlight contract

## Why

The flashlight capability needs a reviewable safety boundary before any
platform adapter is considered.  The current intake tree has no device
integration, so the first increment should prove authorization and audit
behavior entirely in memory.

## Scope

- Add pytest contracts under `harness/tests`.
- Add test-only in-memory flashlight and audit stubs.
- Deny every action unless a capability is explicitly granted.
- Fail closed when audit delivery is unavailable.
- Keep the harness free of device, file, process, network, and secret access.

## Non-goals

- No platform flashlight adapter or device discovery.
- No subprocess, socket, filesystem, camera, sensor, or USB integration.
- No credentials, tokens, environment-secret reads, or external service calls.
- No claim that an allowed request changed physical hardware.

## Acceptance criteria

1. A default-constructed stub denies supported actions.
2. Unknown and malformed actions are denied without echoing untrusted input.
3. An explicit capability only authorizes an offline simulation.
4. Every decision has bounded, non-sensitive audit fields.
5. An audit sink failure results in denial.
6. The pytest suite passes with device/process I/O patched to fail.

