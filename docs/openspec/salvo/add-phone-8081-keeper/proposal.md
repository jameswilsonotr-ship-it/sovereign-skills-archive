# Proposal: add-phone-8081-keeper

## Why

T4-04 needs a durable note for the CinC target `phone:8081/keeper`.
The reload lane is continuous and included-only; this change must not turn
that note into a live service binding or an On-Demand path.

## What Changes

- Add the `phone-8081-keeper` capability note for the CinC target.
- Define continuous reload as an included-only operating contract.
- Record the `/keeper` path at phone port `8081` without selecting a
  transport or opening a socket.
- Keep the change offline and documentation-only.

## Capabilities

| Capability | Mode |
|------------|------|
| `phone-8081-keeper` | ADDED |

## Impact

- Provides a reviewable T4-04 target note for CinC.
- Makes included-only reload and the prohibition on On-Demand explicit.
- Adds no runtime code, live bind, provider integration, credentials, or
  infrastructure provisioning.
