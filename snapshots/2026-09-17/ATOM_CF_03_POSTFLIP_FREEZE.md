# atom-cf-03 post-flip freeze

**Parent change-id:** `add-burn-flip-cutover`
**Atom:** `atom-cf-03-postflip-freeze`
**Status:** Faye HOLD lifted
**Tag:** Meter Burn Desk

## Freeze

Once active coding has flipped:

- Hi **MUST NOT** spawn new included-burn Ultra agents.
- Gage is observe-only: it may report meter state but may not assign agents
  or initiate spend.
- Meter Burn Desk is observe-only: it may record and communicate state but
  may not launch agents or initiate spend.

## Boundaries

- This atom documents the post-flip freeze; it does not execute the flip.
- No spend, provisioning, or billing action is authorized.
- Willow's `SKILL.md` remains untouched.
- One atom equals one PR: this note is the only deliverable for
  `atom-cf-03-postflip-freeze`.
