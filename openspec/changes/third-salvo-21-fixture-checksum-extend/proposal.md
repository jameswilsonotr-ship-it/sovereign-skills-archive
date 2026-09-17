# Change: Extend the T3-21 offline fixture checksum

## Why

The THIRD_SALVO T3-21 fixture needs a stable, offline integrity check before it
can be included in the Ultra surface. Without a checked-in checksum, fixture
drift can silently change the tested entitlement boundary.

## What changes

- Add a canonical T3-21 fixture for the included Ultra surface.
- Record its SHA-256 digest in an extendable checksum manifest.
- Add an offline verifier that checks both the digest and the entitlement
  boundary.
- Document that T3-21 is included in Ultra only and is never On-Demand.

## Scope

This change is offline-only. It does not make network calls, read environment
credentials, or alter any runtime integration.

## Success criteria

- The fixture is valid canonical JSON with a deterministic trailing newline.
- The checksum manifest matches the fixture bytes exactly.
- The offline verifier exits successfully without network access.
- The fixture cannot be interpreted as On-Demand.
