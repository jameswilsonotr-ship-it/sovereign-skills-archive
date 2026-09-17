# SPEC-020 — Included Quota Chew

**Status:** Draft  
**Scope:** Cursor-native, included-quota usage before the active quota period
resets  
**Normative language:** “MUST”, “MUST NOT”, and “SHOULD” are requirements.

## 1. Purpose

This specification defines how a consumer may use remaining included Cursor
quota before the provider’s reset boundary. It is a quota-accounting contract,
not an implementation, scheduler, or operating procedure.

The contract is intentionally **included-only**. It does not authorize
overage, paid fallback, quota borrowing, or overdraft (“OD”).

## 2. Definitions

- **Included quota:** Usage granted by the active Cursor plan for the current
  quota period, excluding separately billed or overage usage.
- **Burn unit:** The provider-reported unit used to debit included quota.
  Depending on the Cursor product surface, this may be tokens, requests,
  credits, or another metered unit.
- **Quota period:** The interval identified by Cursor by a start timestamp and
  an effective reset timestamp.
- **Pre-reset window:** The interval in which the current quota period is
  active and its reset timestamp has not passed.
- **Reservation:** A temporary hold against remaining included quota for a
  candidate request.
- **Commit:** The final provider-confirmed debit for actual eligible usage.
- **OD:** Any debit, reservation, or fallback that makes included quota
  negative or charges outside the included allowance.

## 3. Requirements

### IQ-001 — Included source

Every burn covered by this specification MUST debit only the active Cursor
plan’s included quota.

### IQ-002 — Cursor attribution

Each burn MUST be attributable to the intended Cursor account, team, or
workspace and to exactly one quota period.

### IQ-003 — Provider authority

The provider’s quota and billing metadata MUST be authoritative for remaining
included quota, burn-unit conversion, model eligibility, and reset timing.
Local estimates MUST NOT override provider state.

### IQ-004 — Period identity

Every reservation, commit, release, rejection, and reconciliation event MUST
carry the quota-period identity used for the decision.

### IQ-005 — Pre-reset eligibility

A request MAY qualify for included burn only while its quota period is active
and the effective reset timestamp has not passed.

### IQ-006 — Reset boundary

The reset timestamp MUST be treated as an exclusive boundary for the outgoing
period. Usage accepted after that boundary MUST NOT be committed to the
outgoing period.

### IQ-007 — Atomic availability check

Quota availability check and reservation MUST be one atomic decision. A
request MUST NOT start as an included burn based on a stale or separately
observed balance.

### IQ-008 — No over-reservation

A reservation MUST NOT exceed the provider-confirmed remaining included quota
for its period.

### IQ-009 — Concurrent burns

Concurrent requests MUST draw from one shared period balance. Their combined
reservations MUST NOT exceed the remaining included quota.

### IQ-010 — Hard non-negative floor

The included balance MUST have a hard floor of zero. No state transition may
produce a negative included balance, even temporarily.

### IQ-011 — No fallback spend

If included quota is unavailable, insufficient, stale, or ambiguous, the
request MUST be rejected, deferred, reduced, or otherwise kept out of scope.
It MUST NOT fall back to paid usage, overage, a different billing account, or
an unapproved credential.

### IQ-012 — Eligible request surface

Only usage that Cursor identifies as eligible for the active plan’s included
quota MAY be committed under this specification. A model or feature with a
premium multiplier MUST use the provider’s actual included-unit accounting.

### IQ-013 — Actual-use commit

A commit MUST use provider-confirmed actual usage rather than the requested
maximum, a local estimate, or a guessed token count.

### IQ-014 — Partial usage

When a request consumes less than its reservation, the unused reservation MUST
be released and only actual eligible usage MUST be committed.

### IQ-015 — Failed or cancelled usage

Failed or cancelled requests MUST NOT be committed as unused quota. Any
provider-confirmed usage from such a request MUST still be reconciled as
actual usage.

### IQ-016 — No quota transfer

Included quota MUST NOT be transferred between Cursor accounts, workspaces,
quota periods, or unrelated plan entitlements.

### IQ-017 — No rollover assumption

Unused included quota MUST NOT be assumed to roll over across the reset
boundary unless Cursor explicitly reports that rollover as part of the active
entitlement.

### IQ-018 — Reset reconciliation

At reset, all outgoing-period reservations MUST resolve to commit, release, or
provider-reported exception. An unresolved reservation MUST NOT be silently
carried into the new period.

### IQ-019 — Idempotent accounting

Repeated delivery of the same provider usage or reset event MUST NOT double
commit, double release, or otherwise alter the final included balance more
than once.

### IQ-020 — No-OD acceptance invariant

An implementation conforms only if, for every quota period:

1. all committed burns are provider-eligible included usage;
2. no committed or reserved balance is negative;
3. no outgoing-period burn is committed after its reset boundary;
4. every nonzero commit is explainable by provider-confirmed actual usage; and
5. no OD, paid fallback, overage, borrowing, or cross-entitlement debit occurs.

## 4. Explicit non-goals

This specification does not define:

- a scheduler or burn-rate target;
- a user-interface workflow;
- a model-selection policy beyond included-eligibility accounting;
- a Cursor API integration;
- a retry, queue, or notification implementation;
- paid usage, overage, overdraft, or other OD behavior.
