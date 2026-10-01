# Design: third-salvo-06-thin-keep-map

## Context

T3-06 is a Third Salvo slot whose post-coherence output is a thin KEEP map,
not a code or infrastructure change. The map is intentionally narrow: it
names the retained contract surface and the boundaries that must remain
untouched while the slot is reviewed.

## Goals

- Bind the packet to exactly `third-salvo-06-thin-keep-map`.
- Keep the deliverable to documentation and a compact map.
- Permit INCLUDED Ultra only.
- Make every prohibited side effect visible in the review contract.
- Keep the map stable after coherence review unless this change-id is
  explicitly superseded.

## Non-Goals

- Do not create, edit, or overwrite any Willow `SKILL.md` or skill-tree live
  lock file.
- Do not unpack, inspect, or modify `CONV2_B`.
- Do not make external or provider calls.
- Do not add, expose, or handle secrets, tokens, keys, or credentials.
- Do not provision, connect to, or operate Vultr live.
- Do not mint, create, update, or synchronize anything in Linear.
- Do not use On-Demand. The lane is INCLUDED Ultra only.
- Do not add runtime code, dependencies, generated assets, or binary payloads.

## Decisions

1. **Atomic identity:** every artifact in this packet names the reserved
   change-id and belongs only to T3-06.
2. **Thinness:** the KEEP map records labels, boundaries, and handling. It
   does not duplicate source material or claim ownership of excluded systems.
3. **Post-coherence basis:** coherence is a review gate for this packet, not
   a reason to expand its scope. Any unresolved contradiction stops the lane
   rather than being resolved through an external call or an adjacent change.
4. **Execution boundary:** INCLUDED Ultra is the only allowed lane. An
   On-Demand path is a contract violation, not a fallback.
5. **Offline authority:** the repository documents in this change are the
   complete deliverable; no external system is required to read or verify
   the map.

## Risks

| Risk | Mitigation |
| --- | --- |
| Thin map grows into implementation work | Keep the artifact list and non-goals explicit |
| On-Demand substitution | Treat any On-Demand path as a hard failure |
| Scope crosses a protected surface | Review the hard-fence rows before acceptance |
| Coherence is mistaken for permission to edit | Stop on contradiction; do not widen the change |
