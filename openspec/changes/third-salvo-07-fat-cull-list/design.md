# Design: `third-salvo-07-fat-cull-list`

## Evidence boundary

The candidate register is a static reading of the local Git object
`origin/skill-tree-intake` at `640a2ca84c448d2a727465c1e1240175c504f643`.
Sizes come from:

```text
git ls-tree -r -l origin/skill-tree-intake -- skill_tree/skills/
```

The size values are blob sizes in bytes as reported by Git. They are
inventory evidence, not a claim that a future package will have the same
compressed size.

## Culling rule

An item is a candidate when it is one or more of:

- a vendored binary or wheel duplicated across skill directories;
- generated or derived data reproducible from a smaller source;
- a large visual/reference batch rather than executable skill instructions;
- a report or atomization derivative that duplicates searchable source; or
- a packaged asset whose inclusion is not required by the Ultra envelope.

Candidate status is deliberately not a deletion decision. Before any later
implementation change, the owner must prove whether the item is required by a
runtime path, build path, or reproducibility contract. The implementation
change must also state where the retained source lives. This proposal does
not establish that destination.

## Ultra-only handling

The register is an INCLUDED Ultra planning artifact. It is not an
On-Demand backlog and must not be converted into one. A later implementation
may remove a confirmed candidate from the included package only after review;
this change does not move the item between tiers.

## Protected scope

The register intentionally does not nominate:

- any `SKILL.md`, including Willow-related skill files;
- any path matching `CONV2_B`;
- executable source solely because it is large;
- files whose ownership or retention cannot be established from the local
  snapshot.

## Verification

Verification is textual and structural only:

1. inspect the changed-file list;
2. confirm every changed path is under the change directory and ends in
   `.md`;
3. scan the diff for the protected terms and prohibited operational actions;
4. independently recompute the listed byte totals from the same local Git
   object.

No code, network integration, provider, live infrastructure, or secret
verification is in scope.
