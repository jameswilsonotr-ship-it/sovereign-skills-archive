# T3-31 closeout ledger

- **Change ID:** `third-salvo-31-closeout-ledger`
- **Slot:** `T3-31`
- **Classification:** `INCLUDED / Ultra`
- **Mode:** offline-only

## Intent

Add a small, auditable closeout record for slot T3-31. The record is a
documentation skeleton: it defines the fields and checks needed for closeout
without claiming that any evidence has already been supplied.

## Scope

This change adds:

1. An OpenSpec change record for T3-31.
2. A ledger skeleton with explicit status, evidence, validation, and receipt
   fields.
3. A repository-local receipt for the change.

The slot is **INCLUDED Ultra only**. It must never be treated as On-Demand.
Any future entry that does not satisfy that classification is out of scope.

## Fences

- No Willow `SKILL.md`.
- No `CONV2_B`.
- No external access, provider integration, secret material, Vultr, or Linear.
- No network, credential, or deployment operation is required.
- No source payload is copied into this change.

## Non-goals

- No runtime behavior or package contents change.
- No promotion, publication, or activation is asserted.
- No evidence is fabricated to make the closeout appear complete.
