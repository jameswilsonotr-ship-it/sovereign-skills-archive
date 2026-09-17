# Cutover flip playbook

**Atom:** `atom-cf-02-flip-playbook`  
**Parent:** `add-burn-flip-cutover`  
**Status:** Faye HOLD lifted; live cut remains gated.

## Sequence

1. Stop starting new **burn-chew** work. Do not expand the queue during the
   freeze.
2. Announce the freeze to **Meter Burn Desk** and keep the announcement
   attached to the cutover record.
3. ACK **Iron Pearl** as the single source of truth (SSoT). Resolve any
   conflicting target or status against that record.
4. Obtain an explicit **Bunny YES**. Faye's lifted HOLD is not a substitute
   for this approval.
5. Only after Bunny YES, point coding at the **Vultr headless** target. Use
   only the approved target details already supplied by the operators; never
   invent an IP, key, token, or endpoint.

## Live-cut gate

The live cut is **not authorized** until the Bunny YES, Iron Pearl SSoT ACK,
Meter Burn Desk freeze announcement, and approved Vultr target details are
all recorded. If any item is missing, stop at the gate and ask for the
missing operator input.

This atom is documentation-only: no provisioning, spending, credential
creation, or infrastructure changes. It does not add or modify `SKILL.md`.
