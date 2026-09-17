---
id: SPEC-022-LETTA-DOCKER-HEALTH
title: Letta/Ollama Docker healthcheck contract
status: proposed
owner: infrastructure
priority: high
summary: Define fail-closed Compose health and dependency semantics for a Letta service backed by Ollama.
tags: [letta, ollama, docker-compose, healthcheck, atomic-included-burn]
dependencies: [docker-compose, letta, ollama]
---

# Letta/Ollama Docker healthcheck contract

## Scope

This specification defines the health, readiness, and dependency contract for
a Docker Compose stack containing Letta and Ollama. It applies to local
development, the approved `bridges/vultr` deployment shape, and any other
Compose environment that uses the same service boundary.

The contract is **fail-closed**: a container being started, running, or
reachable at the TCP layer is not sufficient evidence that the service is
healthy. A dependent service may be considered ready only after its
service-specific readiness check succeeds.

The exact Compose service names, image references, ports, health endpoints,
and database implementation remain owned by the bridge. They must be supplied
by the rendered Compose configuration and must not be inferred by a consumer
of this specification.

## Definitions

- **Started** means Docker has created and launched the container process.
- **Healthy** means the service's configured Docker healthcheck is passing.
- **Ready** means the service can perform the operation its dependents need,
  not merely that its process is alive.
- **Unavailable** includes missing, starting, unhealthy, exited, timed-out,
  malformed, or otherwise indeterminate health state.
- **Internal health request** means a request issued from inside the Compose
  network to the service's documented local interface; it does not require a
  host-published or public port.
- **Controlled inference** means one explicitly approved, bounded model
  request used as an end-to-end smoke check after service readiness. It is not
  part of the recurring container healthcheck.

## Requirements

- Healthchecks must measure service readiness at the Compose boundary.
- Letta must not be marked ready while a required Ollama or database
  dependency is unavailable.
- Ollama health must not imply that a particular model is loaded or suitable
  for the host; model availability is a separate deployment check.
- Healthchecks must be safe to run repeatedly, bounded in time, and free of
  credentials and model-generation side effects.
- The stack must preserve evidence of dependency failure instead of masking it
  with a permanently passing process-level check.

## Acceptance

- [ ] **LD-001** — The rendered Compose configuration declares a Docker
  healthcheck for both the Letta service and the Ollama service; a missing
  healthcheck is a contract failure.
- [ ] **LD-002** — Each healthcheck invokes the service's documented local
  readiness interface from within the container or Compose network and does
  not depend on a host-published, public, Tailscale, or external network
  address.
- [ ] **LD-003** — The Ollama healthcheck passes only when the Ollama API
  process is accepting its documented readiness request with a successful
  response; a running PID or open TCP socket alone cannot produce `healthy`.
- [ ] **LD-004** — The Letta healthcheck passes only when the Letta API
  readiness request succeeds according to the bridge's documented endpoint
  and response contract; a running web process alone cannot produce
  `healthy`.
- [ ] **LD-005** — Every healthcheck has an explicit finite timeout,
  retry count, interval, and startup grace period appropriate to the service;
  no check may wait indefinitely or use an unbounded shell command.
- [ ] **LD-006** — Healthchecks are read-only and repeatable: they do not
  create agents, mutate Letta state, pull or load an Ollama model, send a
  generation request, run migrations, or alter persistent volumes.
- [ ] **LD-007** — Letta startup ordering declares every required dependency
  through Compose health-aware dependency semantics or an equivalent
  documented gate; Letta cannot be reported ready while required Ollama or
  database dependencies are unavailable.
- [ ] **LD-008** — A failed, timed-out, exited, or indeterminate dependency
  transitions the dependent path to unavailable and leaves actionable
  container health and dependency evidence in `docker compose ps` and logs;
  no process-running fallback may restore readiness.
- [ ] **LD-009** — After a dependency recovers, the stack can re-evaluate
  health without recreating persistent Letta or Ollama data, and Letta does
  not accept dependent traffic until its own readiness check passes again.
- [ ] **LD-010** — The health contract distinguishes service readiness from
  model readiness: Ollama may be healthy before the approved model is
  present, while the deployment verification separately proves model
  presence, capacity, and one controlled inference.
- [ ] **LD-011** — Healthchecks and their failure output do not print
  credentials, authorization tokens, full environment files, customer data,
  or model prompts; any required authentication uses the bridge's secret
  injection without exposing the secret in command arguments or logs.
- [ ] **LD-012** — A deterministic Compose validation covers healthy,
  starting, unhealthy, timeout, dependency-loss, dependency-recovery,
  missing-model, and one controlled end-to-end inference cases without
  requiring a public port or an external provider API.

## Non-goals

This specification does not choose container images, exact service names,
health endpoint paths, model identifiers, resource limits, database schema,
public ingress, observability tooling, or a production availability target.
It does not authorize provisioning infrastructure or changing an existing
Compose deployment.
