# Change: T3-22 deny-regression pack

- Change ID: `third-salvo-22-deny-regression-pack`
- Slot: `T3-22`
- Eligibility: `INCLUDED` entitlement with `Ultra` tier only

## Why

T3-22 needs a small, deterministic contract that cannot silently broaden
eligibility to On-Demand or to another tier. The repository currently has no
runtime implementation to exercise, so this change supplies the normative
OpenSpec delta and an executable offline decision pack that can be reused when
the runtime is wired in.

## Scope

- Define the exact allow boundary for T3-22.
- Deny every request outside that boundary.
- Return stable denial reasons.
- Keep denials terminal: no fallback, reroute, network access, or credential
  lookup is part of this contract.
- Cover the boundary with local JSON fixtures and standard-library-only tests.

## Non-goals

- Selecting an execution backend.
- Billing, quota, account, or identity resolution.
- Any network, service, credential, or environment integration.

## Acceptance criteria

1. Exactly `INCLUDED` + `Ultra` is allowed for T3-22.
2. On-Demand is denied, including when its tier is `Ultra`.
3. Missing, malformed, or non-matching fields fail closed.
4. Every denial includes one or more stable reason codes and a null fallback.
5. The deny-regression pack passes without network access or installed
   third-party packages.
