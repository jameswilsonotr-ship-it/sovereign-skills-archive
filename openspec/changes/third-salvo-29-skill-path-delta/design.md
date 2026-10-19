# Design: T3-29 skill-path delta

## Inputs

| Name | Value |
| --- | --- |
| Baseline | `main` at `cfdc68d` |
| Offline source | `origin/skill-tree-intake` at `640a2ca` |
| Path root | `skill_tree/skills/` |
| Entry-point rule | path basename is exactly `SKILL.md` |

The source ref is already present in the local Git object database. This
change does not fetch, call, or resolve anything outside the checkout.

## Delta algorithm

1. Enumerate tracked paths from the source revision.
2. Keep paths below `skill_tree/skills/` whose basename is `SKILL.md`.
3. Remove paths already present in the baseline revision.
4. Sort lexicographically and reject duplicates.
5. Emit one tab-separated row per remaining path with the fixed class
   `INCLUDED_ULTRA`.

The resulting delta is 58 paths. The inventory is intentionally a path
manifest, not a copy of the skill contents.

## Classification contract

`INCLUDED_ULTRA` is the only accepted inclusion class for T3-29. The
inventory consumer must treat every listed path as part of the included Ultra
surface. No fallback, lazy-loading, or `ON_DEMAND` interpretation is allowed.

## Validation

The receipt records:

- source and baseline revisions;
- row count;
- unique-path check;
- path-root and basename checks;
- class check;
- offline-only check;
- SHA-256 of the inventory file.
