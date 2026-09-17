---
name: atomic-openspec-engineer
description: Build and verify a local-first phone surface from small OpenSpec changes. Provides a JSON /health stub and keeps SMS and flashlight capabilities denied by default.
---

# ATOMIC OpenSpec Engineer

This skill is a deliberately small, offline-safe phone surface for contract-first
engineering. The current change adds only:

- `GET /health`, a deterministic JSON health response.
- A capability policy whose SMS and flashlight permissions are `False` by
  default.
- An offline pytest harness that exercises the HTTP response and the denial
  boundary.

No network client, credential, SMS provider, flashlight driver, or secret is
required. A future implementation must opt into a capability explicitly and
add a separate OpenSpec change before wiring a real device or provider.

## Run the harness

From the repository root:

```bash
python -m pytest -q skill_tree/skills/atomic-openspec-engineer/harness
```

The tests use only the Python standard library at runtime. Pytest is the test
runner, not an application dependency.

## Contract

The health endpoint returns HTTP `200` and JSON with:

```json
{
  "status": "ok",
  "service": "atomic-phone",
  "schema_version": "1",
  "capabilities": {
    "sms": false,
    "flashlight": false
  }
}
```

The capability policy is deny-by-default. Calling either action without an
explicitly enabled policy raises `CapabilityDenied` before any side effect can
occur.
