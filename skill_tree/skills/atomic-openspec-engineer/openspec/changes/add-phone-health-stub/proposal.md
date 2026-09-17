# Add an offline phone health stub

## Why

The phone surface needs a probeable contract before any provider or device
integration is introduced. A local-only health endpoint gives the harness a
stable seam while keeping sensitive capabilities unavailable.

## What changes

- Add `GET /health` with a versioned JSON response.
- Expose SMS and flashlight state as `false` in the default policy.
- Guard both action boundaries with a deny-by-default policy.
- Add an offline pytest harness using only loopback and the Python standard
  library at runtime.

## Non-goals

- Sending SMS.
- Controlling a flashlight or any other device.
- Network calls, credentials, provider SDKs, persistence, or secrets.
