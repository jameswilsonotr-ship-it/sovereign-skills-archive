# Design: add-included-burn-chew-lanes

## Context

OP ORDER: burn Ultra included toward approximately 80% before reset, then flip
to Vultr headless. OpenSpec basic tier only. Atomic change-ids are already
sequenced by Architect; this capability defines how agents chew them safely.

## Goals

- Provide deterministic chew lanes for included Cursor Models burn.
- Require packetized atomic PRs: one agent, one change-id, and
  `/openspec-apply`.
- Explicitly fence against On-Demand spend, vibe, SKILL touch, Google Docs,
  and plating/avatar mint.

## Non-Goals

- Do not create, edit, or overwrite any `SKILL.md` or skill-tree live lock
  files (Willow write lock).
- No On-Demand spend increase.
- No vibe-coding.
- No Google Docs.
- No plating/avatar mint.
- No `CONV2_B` unpack; never CMV; girl-team not fifth mouths.
- No Vultr live provision in this slice (gateway is a separate change-id).
- Do not re-litigate PR #11 zenoh.

## Decisions

1. **Included-only:** chew tasks count against Cursor Models included quota;
   On-Demand paths are forbidden.
2. **Atomic:** an agent applies one OpenSpec change-id without requiring
   sibling code.
3. **Owners:** Hi spawns; Engineer and Code Monkey apply specs; Architect owns
   slice text.
4. **Bunny YES:** any accidental spend-adjacent step still requires
   Olette → Bunny YES (such a step should not appear in this lane).

## Risks

| Risk | Mitigation |
| --- | --- |
| Agents drift into vibe | Basic-tier OpenSpec only; tasks are checkbox-bound. |
| On-Demand burn while OVER | Explicit Non-Goal and scenario. |
| `SKILL.md` collision | Willow lock Non-Goal on every change. |
