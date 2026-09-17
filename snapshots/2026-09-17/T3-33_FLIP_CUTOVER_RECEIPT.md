# Receipt — T3-33 flip-cutover checklist

- **UTC date:** 2026-09-17
- **Change ID:** `third-salvo-33-flip-cutover-checklist`
- **Workstream:** `THIRD_SALVO`
- **Slot:** `T3-33`
- **Allowed class:** `INCLUDED Ultra` only
- **Disallowed class:** `On-Demand`
- **Delivery:** OpenSpec change plus paper checklist
- **Execution status:** documentation-only; no runtime flip performed
- **Operating boundary:** offline-only

## Delivered artifacts

- `openspec/changes/third-salvo-33-flip-cutover-checklist/proposal.md`
- `openspec/changes/third-salvo-33-flip-cutover-checklist/specs/third-salvo-33/spec.md`
- `openspec/changes/third-salvo-33-flip-cutover-checklist/flip-cutover-checklist.md`
- `openspec/changes/third-salvo-33-flip-cutover-checklist/tasks.md`

## Validation

- [x] Change ID is consistent across the artifacts.
- [x] T3-33 is the only named slot.
- [x] `INCLUDED Ultra` is the only passing class.
- [x] `On-Demand` is explicitly rejected.
- [x] Ambiguous class values fail closed.
- [x] The checklist requires pre-flip state, post-flip readback, and sign-off.
- [x] The receipt makes no claim that a runtime flip occurred.
- [x] No network action is required by the deliverable.

## Delivery state

**Ready for review.** This receipt records the documentation package only; it
does not authorize or attest to execution of a cutover.
