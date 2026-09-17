# Design: add-burn-flip-cutover

## Context

Burn Flip Swarm OP ORDER: burn included -> flip to Vultr headless (Docker+Letta+Ollama, Tailscale-only). Dependencies: meter-watch, burn-chew, vultr-gateway, iron-pearl-ssot, phone-mcp-hud. Current meters still need included burn (1% -> ~80%); OD OVER; reset Sep 17.

## Goals

- Playbook armed by included >=~80% OR reset.
- Preconditions: slices 1-5 applied (or Architect waiver).
- Freeze new Cursor included burn after successful flip.
- Bunny YES before live gateway cut.

## Non-Goals

- Do not create/edit/overwrite any `SKILL.md` / skill-tree live lock files (Willow write lock).
- No CONV2_B unpack; never CMV; girl-team not fifth mouths.
- No vibe; no Google Docs.
- No Cold Steel bare-metal in this cutover.
- No inventing Vultr IPs/keys/spend; no OD increase.
- Do not re-litigate PR #11 zenoh.
- Do not auto-provision Vultr without Bunny YES (Olette asks).

## Decisions

1. **Triggers:** meter-watch included >=~80% OR reset detection.
2. **Deps:** change-ids 1-5 must be applied or waived.
3. **Freeze:** Hi stops spawning included-burn chew agents post-flip.
4. **Authority:** Olette deconflicts; Bunny YES for live cut.

## Risks

| Risk | Mitigation |
|------|------------|
| Flip before gateway ready | Precondition checklist on slices 1-5 |
| Continued Ultra burn after flip | Explicit freeze requirement |
| Unauthorized provision | Bunny YES halt |
