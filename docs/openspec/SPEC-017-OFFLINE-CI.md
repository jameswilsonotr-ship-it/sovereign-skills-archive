---
id: SPEC-017-OFFLINE-CI
title: Offline pytest CI
status: proposed
owner: quality-engineering
priority: high
summary: Make the required pytest burn deterministic and fail-closed when CI has no network.
tags: [ci, pytest, offline, reproducibility]
dependencies: [pytest, test-fixtures]
---

# Offline pytest CI

## Purpose

Define the contract for the required **offline burn**: the pytest execution
that proves the repository's tests can run from the checked-out source and
preinstalled CI environment without network access. This is a specification
only. It does not add a workflow, runner image, firewall rule, or test code.

The offline burn is an atomic CI gate. It is included in the required test
signal, runs as one bounded invocation, and cannot be made green by silently
skipping tests that need a network.

## Scope

This contract covers:

- pytest collection and execution;
- Python and pytest plugin discovery;
- test fixtures, snapshots, and generated local inputs;
- subprocesses started by tests; and
- the CI result and diagnostics produced by the burn.

This contract does not prohibit a separately named integration job from using
network access. Networked jobs must not be used to satisfy, replace, or weaken
the offline burn.

## Definitions

- **Networkless:** no DNS lookup, proxy use, outbound or inbound network
  connection, network service dependency, package index access, or cloud
  metadata access is available to the burn.
- **Local input:** a checked-in fixture or deterministic data generated from
  the checkout, with no remote fetch or ambient machine state.
- **Offline burn:** the single required pytest invocation governed by this
  specification.
- **Fail closed:** an attempted prohibited operation produces a failing test or
  CI job; it is never converted into a skip, xfail, pass, or retry.

## Requirements

1. **CI-001 — Required offline invocation.** CI MUST run the complete
   repository pytest suite through one explicitly named offline-burn job.
2. **CI-002 — Runner-level isolation.** The offline-burn job MUST enforce
   network isolation at the runner, container, namespace, or firewall boundary;
   an environment variable alone MUST NOT be treated as enforcement.
3. **CI-003 — No network dependency.** Collection and execution MUST succeed
   without DNS, HTTP(S), TCP, UDP, proxy, cloud-metadata, or remote-service
   access.
4. **CI-004 — Fail-closed network attempts.** A prohibited network attempt
   MUST fail the burn with a diagnostic result; it MUST NOT be silently
   skipped, marked xfail, retried until it passes, or treated as an optional
   capability.
5. **CI-005 — No install-time fetch.** The burn MUST NOT install packages or
   resolve dependencies from PyPI, a VCS host, an OS package mirror, or any
   other network package source while pytest is running.
6. **CI-006 — Predeclared environment.** Every runtime package and pytest
   plugin required by the burn MUST be available before isolation begins and
   MUST be declared by the repository's dependency metadata or CI image
   contract.
7. **CI-007 — Local-only fixtures.** Tests MUST use checked-in fixtures or
   deterministic local generators; they MUST NOT fetch fixtures, schemas,
   models, certificates, or test data at collection or execution time.
8. **CI-008 — Local service doubles.** Tests of HTTP, RPC, queue, storage, or
   provider integrations MUST use in-process fakes, deterministic stubs, or
   recorded fixtures and MUST NOT require a live service.
9. **CI-009 — Subprocess inheritance.** Any subprocess, worker, plugin, or
   child process launched by pytest MUST inherit the offline policy and MUST
   NOT regain network access through a separate runtime or shell.
10. **CI-010 — Proxy and credential hygiene.** The burn MUST neutralize proxy,
    cloud-credential, and service-discovery environment variables so that
    tests cannot route around isolation or depend on ambient credentials.
11. **CI-011 — Deterministic execution.** The same checkout and declared
    environment MUST produce the same test selection and result independent of
    wall-clock time, host locale, host timezone, process ordering, or random
    seed.
12. **CI-012 — Complete collection.** The burn MUST fail when pytest cannot
    collect a test module, plugin, or configured test path; collection errors
    MUST NOT be hidden by narrowing the test command or changing discovery
    rules for the offline job.
13. **CI-013 — Bounded execution.** The offline-burn job MUST have a finite
    timeout and MUST report a timeout as failure rather than retrying
    indefinitely or waiting for an unavailable service.
14. **CI-014 — Atomic required signal.** The offline burn MUST publish one
    required pass/fail status for the complete invocation; partial shards,
    optional markers, or a networked follow-up MUST NOT override a failure.
15. **CI-015 — Actionable receipt.** A failed burn MUST identify whether the
    failure occurred during setup, collection, isolation enforcement, or test
    execution and MUST preserve secret-free pytest output sufficient to
    reproduce the failure locally without network access.

## Offline burn contract

The implementation SHOULD expose a stable command equivalent to:

```text
python -m pytest
```

The exact runner mechanism is implementation-defined, but the job MUST
preserve the following properties:

1. isolation is active before Python or pytest starts;
2. dependency installation and fixture acquisition are complete before
   isolation begins;
3. the complete pytest suite is selected by the repository's normal discovery
   configuration; and
4. the resulting status is required by the repository's CI gate.

A test that needs a remote API belongs in a separately named integration
surface and MUST provide a local double for the offline burn. Marking the test
`skip` solely because the network is unavailable does not satisfy CI-004 or
CI-008.

## Acceptance

- [ ] **CI-001:** The required CI definition contains one explicitly named
  offline-burn job that runs the complete pytest suite.
- [ ] **CI-002:** The job demonstrates runner-level network isolation.
- [ ] **CI-003:** The suite passes with DNS and network services unavailable.
- [ ] **CI-004:** A deliberate prohibited network attempt makes the job fail.
- [ ] **CI-005:** The pytest phase performs no package or fixture download.
- [ ] **CI-006:** Required packages and plugins are present before isolation.
- [ ] **CI-007:** Removing network access does not remove required test inputs.
- [ ] **CI-008:** Integration tests use local doubles or recorded fixtures.
- [ ] **CI-009:** A child process cannot bypass the offline policy.
- [ ] **CI-010:** Proxy and ambient credential variables are neutralized.
- [ ] **CI-011:** Repeated runs use stable selection and deterministic results.
- [ ] **CI-012:** A collection error fails the complete offline burn.
- [ ] **CI-013:** A hung test reaches a finite failing timeout.
- [ ] **CI-014:** The complete burn produces one required CI status.
- [ ] **CI-015:** Failure output identifies the phase and contains no secrets.

## Non-goals

- Implementing or selecting a particular CI provider, runner image, or
  firewall technology.
- Replacing networked integration, end-to-end, or deployment tests.
- Disabling tests that are difficult to make deterministic.
- Committing credentials, service endpoints, network captures, or private
  fixtures.
