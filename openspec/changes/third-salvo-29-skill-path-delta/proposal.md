# OpenSpec change: T3-29 skill-path delta

- **Change ID:** `third-salvo-29-skill-path-delta`
- **Salvo:** third
- **Slot:** `T3-29`
- **Inclusion class:** `INCLUDED` / `Ultra`
- **Operating mode:** offline

## Summary

Record the canonical skill-entrypoint paths available from the local skill-tree
intake as an inventory-only delta. Every row is explicitly classified as
`INCLUDED_ULTRA`; `ON_DEMAND` is not a permitted classification for this
change.

## Scope

- Add a deterministic, sorted path inventory for the 58 canonical `SKILL.md`
  entrypoints in the local intake ref.
- Record the baseline and source revisions used to calculate the delta.
- Add an auditable receipt with counts, hashes, and fence checks.

No skill payloads are copied or modified by this change. No network, runtime,
or credential behavior changes.

## Acceptance criteria

1. The change ID, salvo, slot, and inclusion class are stated consistently in
   every OpenSpec artifact.
2. The inventory contains unique, repository-relative paths only.
3. Every inventory row is `INCLUDED_ULTRA` and no row is `ON_DEMAND`.
4. The inventory is reproducible from the recorded local source revision.
5. The receipt reports the offline validation result.
