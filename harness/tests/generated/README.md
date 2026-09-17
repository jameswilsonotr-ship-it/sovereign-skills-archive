# Generated OpenSpec scenario stubs

This directory contains a deterministic corpus of **1,000 offline synthetic
scenario stubs** covering all 80 cases listed in
[`docs/openspec/04-acceptance-tests.md`](../../../docs/openspec/04-acceptance-tests.md).
The records are contract-shaped data. They do not claim that a production
adapter or service is implemented.

## Files

- `scenarios.jsonl` — exactly 1,000 canonical JSONL records, distributed across
  the documented CT, PH, MCP, LT, ES, and OP cases.
- `manifest.json` — fixed seed, generator version, case catalog, count, and
  corpus SHA-256.
- `templates.py` — the 80-case catalog and scenario template.
- `generate.py` — deterministic generator and stale-output checker.
- `scenario_schema.py` — standard-library schema and canonical JSON helpers.
- `runner.py` — dependency-free offline verifier.
- `test_generated_scenarios.py` — `unittest` checks for determinism and corpus
  validity.

Every record has `status: "stub"`, synthetic-only credentials, controlled time,
and an explicit `external_io: "disabled"` setup. Its forbidden effects include
network access, subprocesses, real credentials, model calls, and unapproved
writes.

## Commands

Run from the repository root without installing anything:

```sh
python3 -m harness.tests.generated.runner
python3 -m harness.tests.generated.generate --check
python3 -m unittest discover -s harness/tests/generated -p 'test_*.py'
```

To regenerate the committed corpus after changing templates:

```sh
python3 -m harness.tests.generated.generate
```

The generator uses no current time, UUIDs, environment values, randomness, or
network input. CI only runs the verifier and standard-library tests; it does
not install packages or contact providers.
