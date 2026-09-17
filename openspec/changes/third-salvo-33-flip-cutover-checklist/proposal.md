# Change: T3-33 flip-cutover checklist

- **Change ID:** `third-salvo-33-flip-cutover-checklist`
- **Workstream:** `THIRD_SALVO`
- **Slot:** `T3-33`
- **Allowed class:** `INCLUDED Ultra`
- **Status:** proposed

## Decision

Define the T3-33 cutover as an exact-class flip. The slot is eligible only when
its class is `INCLUDED Ultra`. `On-Demand` is never an eligible class for this
slot, including during fallback, retry, or recovery.

The deliverable is paper-only: a reviewable OpenSpec change, a paper
checklist, and a local receipt. It does not add runtime behavior or perform a
cutover.

## Guardrails

- Keep the change atomic to T3-33.
- Treat any unknown, blank, aliased, or conflicting class value as a stop
  condition.
- Require an explicit pre-flip record, post-flip readback, and sign-off.
- Keep all work offline; do not invoke network services or record credential
  material.
- Do not expand the checklist to neighboring slots.

## Artifacts

- `specs/third-salvo-33/spec.md` — normative requirements and scenarios.
- `flip-cutover-checklist.md` — paper procedure and sign-off fields.
- `tasks.md` — implementation and review tasks.
- `snapshots/2026-09-17/T3-33_FLIP_CUTOVER_RECEIPT.md` — local delivery receipt.

## Non-goals

- No runtime, configuration, or deployment change.
- No automated flip.
- No change to any slot other than T3-33.
- No network, integration, or credential-handling workflow.
