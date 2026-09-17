# SPEC-012 — Tailscale ACL Notes

Status: draft specification only  
Scope: policy and review requirements for a Tailscale-protected service  
Execution status: **non-live** — this document does not authorize or perform
Tailscale, firewall, provider, DNS, SSH, or network changes.

## 1. Purpose

This specification records the minimum ACL decisions that must be known before
any Tailscale access path is considered ready. It is intentionally
implementation-neutral: concrete tailnet names, device names, tags, groups,
addresses, ports, auth keys, and operator identities belong in an approved
private change record, not in this repository.

The governing rule is:

> If an identity, destination, policy, state, or verification result is
> missing, ambiguous, stale, or contradictory, deny the operation and stop.

Tailscale reachability is not authorization. Access requires the Tailscale ACL
decision, the destination's host/service policy, and the operator's approved
purpose to agree.

## 2. Non-goals

This specification does not:

- install, enroll, start, stop, or inspect Tailscale;
- create or modify an ACL policy, device, tag, route, DNS record, firewall, or
  SSH configuration;
- provide an auth key, private key, hostname, IP address, or secret;
- approve a tailnet, exit node, subnet router, Tailscale SSH policy, Serve
  endpoint, Funnel endpoint, or public ingress;
- substitute for a provider-console recovery plan or a data-owner approval.

## 3. Global fail-closed invariants

1. **No implicit allow:** an unlisted source, destination, protocol, port,
   capability, or route is denied.
2. **Two-sided enforcement:** the tailnet ACL and the destination host/service
   boundary must each enforce the same intended scope. A permissive result on
   one side does not override a denial on the other.
3. **No bootstrap exception by drift:** temporary public ingress, broad tags,
   reusable credentials, and emergency-wide access are not silently retained.
4. **No evidence, no claim:** a configuration assertion is not accepted without
   reviewable evidence tied to the approved change record.
5. **Safe uncertainty:** timeouts, unavailable control-plane state, partial
   status, and failed verification are treated as denial, not as success.
6. **Recovery remains separate:** the recovery path must be documented and
   authorized independently; it must not be implemented by widening the normal
   ACL.

## 4. TA notes

Each note below is a hard review gate. “Fail closed” means deny the affected
operation, preserve the last known-good policy, and stop for an explicit
decision; it does not mean guessing a value or retrying with broader access.

| ID | Requirement | Fail-closed note |
| --- | --- | --- |
| **TA-001** | **Default deny.** Only explicitly approved source-to-destination flows may be reachable. | If a flow is not represented in the approved policy, deny it. Do not infer access from network membership, device visibility, or a successful ping. |
| **TA-002** | **Identity before access.** Every source must map to an approved human, workload, or tightly scoped device identity. | If the source identity cannot be resolved and attributed, deny access. Never fall back to an IP-only allow. |
| **TA-003** | **Tailnet boundary.** The target tailnet and environment must be named in the private change record. | If tailnet ownership or environment is uncertain, make no enrollment or policy decision. A similarly named tailnet is not an acceptable substitute. |
| **TA-004** | **Least-privilege grouping.** Groups and tags must express the smallest reviewed role or workload boundary. | If a tag or group would grant unrelated destinations, remove the flow from consideration until a narrower classification is approved. |
| **TA-005** | **Destination allowlist.** Access must identify the approved device or service, not merely a broad network or address range. | If the destination is missing, renamed, duplicated, or not uniquely bound to the change record, deny the connection. |
| **TA-006** | **Protocol and port scope.** Each allowed flow must name the required protocol and destination port or service. | If protocol, port, or service ownership is unknown, deny it. Do not use “all ports” to discover what works. |
| **TA-007** | **ACL and host-policy agreement.** The Tailscale policy, host firewall, and service listener must describe the same boundary. | If any layer is broader than the approved boundary, do not proceed. A passing ACL review cannot excuse a public or over-broad listener. |
| **TA-008** | **Public ingress prohibited by default.** Tailscale-only access must not depend on a public application, database, admin, or SSH port. | If private access cannot be proven without public exposure, stop and retain the existing closed posture. Do not open a temporary broad rule as a workaround. |
| **TA-009** | **Administrative access is explicit.** Tailscale SSH and ordinary SSH over the Tailscale interface are distinct designs with separate authorization requirements. | If the approved SSH mode is not recorded, deny administrative access. Do not assume that tailnet membership authorizes shell access. |
| **TA-010** | **Routes and exit nodes are opt-in.** Subnet routes, app connectors, and exit-node use change the reachable boundary and require separate approval. | If a route or exit node is unexpected, unowned, or not in the change record, do not accept or use it. Do not enable a route to repair an ACL mismatch. |
| **TA-011** | **Serve and Funnel are separate surfaces.** Publishing a service through Tailscale Serve or Funnel is not equivalent to private device access. | If publication mode or audience is unclear, keep the service unpublished. Funnel/public reachability is denied unless separately approved. |
| **TA-012** | **Credential and device lifecycle.** Enrollment credentials must be short-lived or otherwise bounded, least-privilege, and revocable; device approval and expiry ownership must be known. | If credential provenance, expiry, revocation, or device ownership cannot be verified, do not enroll, renew, or reuse it. Never place credentials in this repository. |
| **TA-013** | **Name and address integrity.** DNS names, tailnet IPs, and service identities must resolve to the reviewed destination and must not silently change the policy scope. | If name resolution, address ownership, or split-DNS behavior is inconsistent, stop. Do not replace a failed identity check with a guessed address. |
| **TA-014** | **Verification and audit evidence.** Every approved flow needs an owner, purpose, review date, expected result, and redacted evidence in the private change record. | If evidence is absent, partial, stale, or exposes secrets, treat the flow as unverified and deny it until corrected. |
| **TA-015** | **Rollback and lockout safety.** The last known-good policy, independent recovery path, rollback owner, and stop condition must be identified before change. | If recovery is unavailable or the change could strand the operator, do not apply or widen the policy. Use the separately approved recovery path; never solve lockout by making the ACL global. |

## 5. Review record

Before an implementation change is proposed, the private change record should
answer, without embedding secrets:

- Which tailnet and environment are in scope?
- Which source identities, destination services, protocols, and ports are
  approved?
- Which ACL groups/tags, host policy, and service binding enforce each flow?
- Are routes, exit nodes, Serve, Funnel, DNS behavior, and SSH mode explicitly
  disabled or separately approved?
- Who owns enrollment, policy review, evidence collection, and rollback?
- What independent recovery path remains available if private access fails?
- What exact evidence will demonstrate each flow and the absence of public
  exposure?

An unanswered item is a stop condition, not an invitation to broaden access.

## 6. Acceptance criteria for this spec

- The document remains documentation-only and contains no live Tailscale
  operation or environment credential.
- TA-001 through TA-015 are present exactly once and each has a concrete
  fail-closed outcome.
- No note grants access based solely on reachability, tailnet membership, or
  an IP address.
- Public ingress, routes, exit nodes, publication, credentials, evidence, and
  recovery are explicitly bounded.
- A future implementation can map every allowed flow to a private approval
  record without adding secrets to this repository.
