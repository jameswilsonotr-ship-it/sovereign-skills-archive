# Proposal: S2-25 redaction check

## Change ID

`second-salvo-25-redaction-check`

## Intent

Add one deterministic, offline check that detects high-confidence secret or PII
patterns in the included Ultra fixture set before fixture content is committed.

## Scope

In scope:

- local JSON fixtures under `harness/src/sovereign_harness/fixtures/`;
- a small scanner that reports rule names and locations without matched values;
- a smoke test covering both the clean fixture set and synthetic canaries; and
- operator documentation in `docs/burn-wave/REDACTION_CHECK.md`.

Out of scope:

- live services, network calls, or provider infrastructure;
- live skill files;
- adjacent S2 slots; and
- storing, transforming, or redacting real secrets.
