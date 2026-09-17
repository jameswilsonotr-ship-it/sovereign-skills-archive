---
atom: atom-bc-01-lane-roster
parent_change_id: add-included-burn-chew-lanes
capability: burn-chew
visibility: meter-burn-desk
---

# Included burn-chew lane roster

This atom is the source of truth for assigning Hi Cursor agents to the
included-model burn lane. It is intentionally limited to roster ownership and
the apply boundary; it does not change model entitlements or implement a
runtime lane.

## Roster

Each roster entry has exactly one OpenSpec change-id. The parent change-id is
the single assignment for this atom because the roster describes the
`burn-chew` capability as a unit.

| Hi Cursor agent | Model pool | Lane | OpenSpec change-id | Atom |
| --- | --- | --- | --- | --- |
| Hi Cursor agents assigned to included-model burn | Included Cursor Models only | `burn-chew` | `add-included-burn-chew-lanes` | `atom-bc-01-lane-roster` |

The roster does not assign work to On-Demand models and does not increase
On-Demand capacity. No sibling change-id is implied by this entry.

## One-change-id apply rule

When applying OpenSpec work, a Hi Cursor agent must select one change-id and
apply only that change:

```text
/openspec-apply <one-change-id>
```

For this atom, the valid invocation is:

```text
/openspec-apply add-included-burn-chew-lanes
```

Do not pass a sibling change-id, a parent plus a sibling, or a list of
change-ids in one invocation. If the requested work spans more than one
change-id, stop at the boundary and create separate handoffs and
independently reviewable PRs—one atom per PR. Do not silently couple sibling
changes to make the current PR complete.

## Scope guard

- Included Cursor Models burn only.
- No On-Demand expansion.
- No skill or skill-tree live-lock changes.
- No runtime, Google Docs, CONV2_B, or CMV work.
