# SPEC-010 — Connector Fixtures

**Status:** Draft
**Scope:** Deterministic, offline fixtures for connector behavior
**Normative language:** `MUST`, `MUST NOT`, `SHOULD`, and `MAY` are normative.

## Purpose

This specification defines the contract for connector fixtures used by tests,
examples, and local development. Fixtures model connector inputs, outputs, and
failure cases without contacting a provider or depending on runtime secrets.

## Scope and non-goals

In scope:

- checked-in or in-memory fixture data;
- deterministic connector request and response shapes;
- account-scoped isolation;
- representative success, empty, pagination, and error cases.

Out of scope:

- provider API integration;
- credential acquisition or refresh;
- production connector behavior;
- real customer, organization, or provider data.

## Terms

- **Fixture:** Synthetic data and metadata that represents a connector scenario.
- **Fixture set:** A named, versioned collection of related fixtures for one
  connector and account.
- **Account:** The tenant or external account boundary identified by
  `account_id`.
- **Live I/O:** Any runtime interaction with a network, provider SDK, external
  process, secret store, database, or service outside the fixture package.

## Requirements

### CF-001 — Offline availability

Every fixture set MUST be usable with network access disabled and without
provider availability.

### CF-002 — Required account identifier

Every account-scoped fixture input, record, request, response, and error
context MUST contain a non-empty `account_id` string. A missing, null, empty, or
whitespace-only `account_id` MUST be rejected.

### CF-003 — Explicit account selection

Fixture factories and loaders MUST require `account_id` as an explicit input.
They MUST NOT silently select a default account or infer an account from global
state.

### CF-004 — Synthetic account namespace

Fixture `account_id` values MUST be synthetic, stable, and clearly test-only
(for example, `acct_fixture_alpha`). They MUST NOT contain real customer,
provider, or production identifiers.

### CF-005 — Account-scoped ownership

Every fixture record that represents account-owned data MUST carry the same
`account_id` as its fixture set. Records from another account MUST NOT be
included in that set.

### CF-006 — Account isolation

Loading a fixture set for account A MUST NOT return, mutate, or expose records
belonging to account B. Tests MUST be able to load at least two accounts and
verify this boundary.

### CF-007 — No network I/O

Fixture execution MUST NOT open sockets, make HTTP requests, perform DNS
resolution, or contact a provider endpoint, including through a transitive
connector client.

### CF-008 — No external service I/O

Fixture execution MUST NOT access databases, queues, object stores, secret
stores, subprocesses, or other external services. Repository-local fixture
resources MAY be read when they are part of the fixture package and are
available offline.

### CF-009 — No credential dependency

Fixtures MUST NOT require, read, generate, or validate API keys, access tokens,
refresh tokens, cookies, private keys, passwords, or other secrets.

### CF-010 — No environment dependency

Fixture results MUST NOT depend on environment variables, local user
configuration, machine identity, current working directory, or ambient cloud
credentials. Missing or unrelated environment configuration MUST NOT make a
fixture unusable.

### CF-011 — Deterministic selection

Given the same connector name, fixture-set version, `account_id`, scenario, and
request parameters, a fixture loader MUST return the same result and outcome
across runs and machines.

### CF-012 — Stable ordering

Collections returned by fixtures MUST have an explicitly defined, stable
ordering. Ordering MUST NOT depend on hash iteration order, filesystem order,
wall-clock time, or provider response order.

### CF-013 — Stable identifiers and timestamps

Fixture entity identifiers, cursors, timestamps, and version values MUST be
declared constants or deterministic derivations. Fixtures MUST NOT use random
UUIDs, current time, process state, or nondeterministic counters.

### CF-014 — Request-shape coverage

Each connector fixture set MUST define representative request inputs for the
supported operations, including the required `account_id`, scenario name, and
any operation-specific parameters.

### CF-015 — Success-shape coverage

Each connector fixture set MUST include at least one internally consistent
successful response whose records, metadata, identifiers, and `account_id`
agree with the selected fixture set.

### CF-016 — Empty-result coverage

Each connector fixture set MUST include an explicit empty-result scenario for a
valid `account_id`. The empty result MUST be distinguishable from a missing or
invalid account.

### CF-017 — Pagination coverage

When a connector exposes pagination, its fixture set MUST include a
deterministic multi-page scenario with stable page boundaries and cursors. A
terminal page MUST represent the absence of a next cursor explicitly.

### CF-018 — Error coverage

Each connector fixture set MUST include deterministic fixtures for invalid
`account_id` input and at least one connector-level failure. Error fixtures MUST
not contain real provider error payloads, credentials, or unredacted secret
material.

### CF-019 — Fixture metadata

Every fixture set MUST declare a stable fixture-set name, schema version,
connector identifier, supported scenarios, and the selected `account_id`.
Metadata MUST be sufficient to identify the fixture without contacting any
external system.

### CF-020 — Conformance and enforcement

A fixture implementation conforms to this specification only when all
requirements CF-001 through CF-019 are satisfied and automated tests verify
offline execution, required `account_id`, deterministic results, account
isolation, and absence of live I/O. A conformance failure MUST fail the test
run rather than silently falling back to a live connector.

## Canonical synthetic example

The following is illustrative only and contains no credential material:

```json
{
  "fixture_set": "connector-example",
  "schema_version": "1",
  "connector_id": "example",
  "account_id": "acct_fixture_alpha",
  "scenario": "list_success"
}
```
