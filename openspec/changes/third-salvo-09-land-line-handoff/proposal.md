# Change: T3-09 land-line handoff

- **Change ID:** `third-salvo-09-land-line-handoff`
- **Salvo slot:** `THIRD_SALVO` / `T3-09`
- **Status:** proposed
- **Scope:** documentation and OpenSpec only
- **Eligibility:** Included Ultra only

## Summary

Record the T3-09 land-line handoff as one atomic, offline OpenSpec change and
provide Mina, Bea, and Ora with a shared handoff note. The handoff is a
coordination contract; it does not add runtime behavior, provider
integration, infrastructure, or credentials.

## Contract

1. The reserved change ID is exactly
   `third-salvo-09-land-line-handoff`.
2. The slot is eligible for **Included Ultra only**.
3. **On-Demand is never eligible** for this slot. It must not be used as a
   fallback, alias, retry path, or implied execution mode.
4. The change is documentation-only and must be completed offline.
5. The atomic delivery is one pull request titled exactly
   `salvo: T3-09 land-line-handoff`.
6. The delivery must not modify `Willow SKILL.md`, add or process `CONV2_B`,
   call an external/provider service, add secrets, contact Vultr live
   infrastructure, or mint a Linear item.

## Non-goals

- Implementing a runtime land-line, routing, scheduler, or provider adapter.
- Changing a skill definition or conversation payload.
- Provisioning, testing, or contacting Vultr.
- Creating Linear work, credentials, or any external record.

## Deliverables

- This OpenSpec change, including its requirement scenarios and task list.
- `docs/handoffs/third-salvo-09-land-line-handoff.md`, addressed to Mina,
  Bea, and Ora.

## Acceptance

- The change ID, slot, title, and eligibility gate appear consistently in
  the OpenSpec files and handoff note.
- The handoff note gives each recipient an explicit review/acknowledgement
  action without requiring an external call.
- The final diff contains documentation only and stays within the fences in
  this proposal.
