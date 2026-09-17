# T3-06 thin-KEEP map

**Change-id:** `third-salvo-06-thin-keep-map`
**Slot:** `T3-06`
**Phase:** post-coherence
**Mode:** documentation only
**Allowed lane:** INCLUDED Ultra only
**Forbidden lane:** On-Demand, always

This is a thin, reference-only map. `KEEP` means preserve the boundary and
leave the named surface untouched; it does not grant permission to copy,
rewrite, call, provision, or mint that surface.

| Surface | KEEP handling | T3-06 action |
| --- | --- | --- |
| This OpenSpec change and map | KEEP as the atomic T3-06 record | Review only |
| Coherent repository documentation used to review this slot | KEEP as read-only context | Refer only; do not duplicate |
| Willow `SKILL.md` and skill-tree live locks | KEEP / hard fence | No create, edit, or overwrite |
| `CONV2_B` | KEEP / hard fence | No unpack, inspect, or modify |
| External/provider surfaces | KEEP / hard fence | No calls or synchronization |
| Secrets, tokens, keys, and credentials | KEEP / hard fence | Do not request, add, expose, or store |
| Vultr live infrastructure | KEEP / hard fence | No provision, connect, or operate |
| Linear state | KEEP / hard fence | No mint, create, update, or sync |
| On-Demand billing lane | KEEP / hard fence | Never use; stop if INCLUDED Ultra is unavailable |

## Acceptance gate

Accept T3-06 only when all of the following remain true:

- The diff contains this OpenSpec change and this map only.
- The reserved change-id remains the sole change identity.
- The work is post-coherence and has no unresolved contradiction.
- The execution lane is INCLUDED Ultra.
- No On-Demand path is present.
- No protected surface in the map has been touched.

If any gate fails, stop the slot and return it for review. Do not repair the
failure through a sibling change, provider call, live operation, or external
coordination.
