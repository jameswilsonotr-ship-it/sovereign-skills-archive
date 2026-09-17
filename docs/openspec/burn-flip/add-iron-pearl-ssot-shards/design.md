# Design: add-iron-pearl-ssot-shards

## Context

Iron Pearl BASIC SPEC-001 defines Awesome Split / HANDOFF as the authority for
this slice. The layout needs bounded ownership and a write protocol that
detects concurrent clobbering. PR #11 zenoh remains a control-plane reference
only.

## Goals

- Establish repository paths for Awesome Split and HANDOFF SSoT state.
- Define exactly eight shard slots with named ownership.
- Use delta CAS to prevent silent clobber.
- Ban Google Docs as an SSoT medium.

## Non-Goals

- Do not create, edit, or overwrite any `SKILL.md` or skill-tree live-lock
  file (Willow write lock).
- Do not use Google Docs.
- No CONV2_B unpack; never CMV; girl-team is not a fifth mouth.
- No vibe, Vultr spend, or Cold Steel bare-metal work in this slice.
- Do not re-litigate PR #11 zenoh.

## Decisions

1. **Authority:** Iron Pearl BASIC SPEC-001 is the only authority for this
   SSoT shape.
2. **Repository layout:** the SSoT root is
   `docs/iron-pearl/ssot/`. Awesome Split state lives under
   `docs/iron-pearl/ssot/awesome-split/`; HANDOFF state lives under
   `docs/iron-pearl/ssot/handoff/`. The head record is
   `docs/iron-pearl/ssot/head.json`, and append-only deltas live under
   `docs/iron-pearl/ssot/deltas/`.
3. **Shard ownership:** every write names one target slot from this exact
   eight-slot map.

| Slot | State boundary | Ownership label |
|------|-----------------|-----------------|
| `slot-01` | Awesome Split / intent | `awesome-split-owner` |
| `slot-02` | Awesome Split / decisions | `engineer-owner` |
| `slot-03` | Awesome Split / changes | `hi-agents-owner` |
| `slot-04` | HANDOFF / context | `handoff-owner` |
| `slot-05` | HANDOFF / next-actions | `engineer-owner` |
| `slot-06` | HANDOFF / blockers | `gateway-cutover-owner` |
| `slot-07` | HANDOFF / validation | `verification-owner` |
| `slot-08` | HANDOFF / receipts | `ssot-steward` |

4. **Delta CAS:** each delta write includes `slot`, `base_version`,
   `next_version`, and the delta payload. A write is accepted only when
   `base_version` equals the current head version and `next_version` is exactly
   `base_version + 1`. Acceptance atomically appends the delta and advances the
   head to `next_version`.
5. **Stale writes:** a stale `base_version` fails without a partial write or
   implicit merge. The writer rereads the current head, rebases its delta, and
   retries with the new `base_version` and incremented `next_version`.
6. **Medium:** SSoT state is file/repository state under the declared fleet
   paths. Google Docs is explicitly refused as SSoT, handoff medium, or shard
   store.

## Risks

| Risk | Mitigation |
|------|------------|
| Concurrent clobber | Require delta CAS and reject stale base versions |
| Docs creep | Keep the repository paths explicit and refuse Google Docs |
| Ownership ambiguity | Require a named slot and use the fixed ownership map |
| Scope into Steel | Keep the non-goal fence in this change |
