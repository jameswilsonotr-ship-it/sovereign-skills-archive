---
id: SPEC-023-TAILSCALE-EXIT-NODE-HYGIENE
title: Tailscale exit-node hygiene
status: proposed
owner: infrastructure
priority: high
summary: Make stale or unusable Tailscale exit-node state fail closed with durable, actionable operator notes.
tags: [tailscale, exit-node, hygiene, stale-state, atomic-included-burn, salvo-s1]
dependencies: [tailscale-status, operator-runbook]
---

# Tailscale exit-node hygiene

## Scope

This specification defines the detection and documentation boundary for a
Tailscale client that has selected an exit node whose state is stale, missing,
unreachable, or otherwise not trustworthy. It covers the operator-facing
failure note and the state transition that makes the problem visible.

An exit node is not considered healthy merely because a preference or hostname
is still present in local state. The current Tailscale status must positively
confirm the selected node and its usable route.

## Definitions

- **Selected exit node** is the node currently configured as the client's
  intended exit node.
- **Stale exit-node state** is a selected exit node that is absent from the
  current peer/status view, no longer advertises a usable exit route, or has
  not produced a current connectivity result.
- **Healthy exit node** is a selected node positively confirmed by current
  status as available and usable for exit-node traffic.
- **Failure note** is a bounded operator-facing record containing the failure
  classification, affected node, observed state, timestamp, and next action.
- **Fail closed** means traffic is not silently treated as exit-node-routed
  when the selected node cannot be positively verified.

## Atomic acceptance criteria

- [ ] **TE-001** — A selected exit node missing from the current Tailscale
  status is classified as `stale_exit_node`, and the client does not report
  exit-node routing as healthy.
- [ ] **TE-002** — A selected exit node that is present but does not advertise
  an exit-node route is classified as `exit_node_route_missing`; the failure
  note identifies the node and the missing route condition.
- [ ] **TE-003** — An exit-node status that is loading, indeterminate, timed
  out, or otherwise not current is classified as `exit_node_status_stale`;
  indeterminate state never counts as healthy.
- [ ] **TE-004** — An unreachable selected exit node is classified separately
  from a node that is merely absent, and the failure note records the observed
  reachability result without claiming that traffic used the node.
- [ ] **TE-005** — Every stale exit-node failure produces exactly one
  operator-facing note per unchanged observation, with a stable failure
  classification and an observation timestamp.
- [ ] **TE-006** — Each failure note names the selected exit node using a
  non-secret stable identifier and includes the observed status, route
  condition, and the next safe verification or remediation action.
- [ ] **TE-007** — Failure notes never include auth keys, private keys,
  session tokens, full environment dumps, or other secret material; sensitive
  values are omitted or redacted before presentation or persistence.
- [ ] **TE-008** — While exit-node state is stale or failed, the system
  remains fail closed: it does not silently fall back to a different exit
  node and does not claim that ordinary tailnet traffic is exit-node traffic.
- [ ] **TE-009** — Recovery is recorded only after current status positively
  confirms the selected exit node and usable route; the recovery note links
  the recovered classification to the prior failure without duplicating
  unchanged recovery observations.
- [ ] **TE-010** — The stale, missing-route, indeterminate, unreachable, and
  recovered cases are covered by deterministic acceptance tests using
  redacted status fixtures; tests do not require a live tailnet or real
  credentials.

## Non-goals

This specification does not select an exit node, change tailnet ACLs, rotate
credentials, repair Tailscale connectivity, or define the underlying route
advertisement protocol. It also does not authorize automatic failover to
another exit node.
