# Tailscale fail-closed policy for MCP

This repository's MCP surface must be reachable through the Tailscale mesh
only. A missing or uncertain mesh connection is an authorization failure, not
an invitation to try another route.

## Decision rule

An MCP request is allowed only when all of the following are true at the time
the request is authorized:

1. The Tailscale mesh health probe reports success.
2. The probe completes before its configured deadline.
3. The selected MCP endpoint is a mesh endpoint.

Every other state is **deny**. This includes a dropped mesh, a probe timeout,
an unknown probe result, a probe error, and a stale health result that has not
been revalidated according to the caller's health-check policy.

The authorization result is intentionally binary:

| Mesh/probe state | MCP decision | Route |
| --- | --- | --- |
| Healthy mesh, probe succeeds before deadline | allow | Tailscale endpoint only |
| Mesh drops between requests | deny | no route |
| Probe times out | deny | no route |
| Probe errors or returns an unknown state | deny | no route |
| Mesh is unavailable while a public endpoint is reachable | deny | never public |

## No public-internet fallback

The MCP client MUST NOT:

- replace a Tailscale or MagicDNS endpoint with a public DNS name, public IP,
  proxy, exit node, or relay as a recovery path;
- retry a denied MCP request over the public internet;
- treat ordinary internet reachability as evidence that the mesh is healthy;
- keep an already-authorized connection alive after the mesh authorization has
  been revoked, unless the transport itself has independently proven that it
  remains on the approved mesh path.

Implementations should keep the public endpoint out of the route-selection
function entirely. If a public endpoint is configured for diagnostics, it is
not an MCP fallback and MUST NOT be selected by the authorization path.

## Health-probe timeouts

Health checks are bounded operations. A timeout is a failed health check:

- use a monotonic deadline, not wall-clock time;
- pass the remaining budget to each probe attempt;
- cancel or abandon the probe when its deadline expires;
- return deny without waiting for an unbounded retry;
- do not start an internet probe after a mesh probe times out.

The timeout value is a policy/configuration concern. The security invariant is
that timeout, cancellation, and probe failure all produce the same fail-closed
MCP decision.

## Operational behavior

When denied, the client should expose a machine-readable reason such as
`mesh_unavailable`, `health_probe_timeout`, or `health_probe_error`, while
avoiding secrets and endpoint credentials in logs. A denial should be
observable locally, but logging or telemetry must not require a public network
connection.

Recovery requires a fresh successful mesh probe. Do not silently reuse the
last successful result after a denial.

## Acceptance cases

The executable acceptance model in
`tests/test_tailscale_fail_closed.py` covers these stable cases:

- **AC-001 — mesh drop denies MCP:** an allowed request is followed by a mesh
  drop; the next authorization is denied.
- **AC-002 — no public fallback:** when the mesh is down, an available public
  endpoint is never selected or attempted.
- **AC-003 — probe timeout denies MCP:** a deterministic probe timeout denies
  the request and preserves the configured timeout budget.
- **AC-004 — uncertain health denies MCP:** probe errors and unknown results
  deny the request.

`docs/openspec/SPEC-002` and any `BASIC_TIER` acceptance document are optional
inputs. They are not present in the current base branch. The test suite
discovers them if they are added later and checks that their relevant
acceptance text names the mesh, MCP, public-internet, and timeout invariants.
Their absence is not a reason to make CI access the network.

## Offline/CI requirements

These acceptance checks must run without Tailscale, credentials, DNS, sockets,
or live MCP services. Tests use local deterministic probe doubles only.
Production integrations should inject the health probe and transport so the
same deny behavior can be exercised without making network calls.
