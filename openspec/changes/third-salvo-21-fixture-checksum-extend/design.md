# Design: T3-21 fixture checksum extension

## Canonical fixture

The fixture is stored as UTF-8 JSON with sorted keys, two-space indentation,
and one trailing newline. These rules make the bytes reproducible across
machines and keep the SHA-256 value meaningful.

The fixture carries explicit policy fields:

- `salvo`: `THIRD_SALVO`
- `slot`: `T3-21`
- `availability`: `included`
- `tier`: `Ultra`
- `on_demand`: `false`

The fixture contains no credential material.

## Checksum manifest

`fixtures/third-salvo/checksums.sha256` uses the conventional
`<sha256><two spaces><relative path>` format. New fixtures can be appended
without rewriting existing records. Paths are relative to the repository root.

## Verification

`scripts/verify_t3_21_fixture.py` reads only the checked-in fixture and
checksum manifest. It:

1. verifies the recorded digest against the fixture bytes;
2. parses the JSON;
3. checks the T3-21 and Ultra-only policy fields; and
4. rejects an On-Demand interpretation.

The verifier uses only Python's standard library and performs no network or
environment-credential access.
