# Dependency inventory — Included Ultra

| Field | Value |
| --- | --- |
| OpenSpec change-id | `second-salvo-34-dependency-inventory` |
| Slot | `S2-34` |
| Scope | Included Ultra only |
| Boundary count | One dependency/license boundary |
| Install policy | No installs or upgrades |

## Boundary

This inventory records one boundary: the material included in the Ultra slice
versus dependencies and licensed material outside that slice. It is an intake
record, not a request to resolve, fetch, install, upgrade, or vendor anything.

## Included Ultra

The Included Ultra slice adds documentation only. It introduces:

- no runtime or package dependency;
- no new third-party source, binary, asset, or generated bundle; and
- no dependency-version or lockfile change.

Accordingly, the dependency side of this boundary is **none introduced**. The
new Markdown is repository-authored documentation. The checked-out base has no
root-level `LICENSE` or `NOTICE` file, so this inventory does not make a
repository-wide license assertion or assign a license to the project.

## Outside the boundary

The following are deliberately not inventoried or included in this slice:

- OD;
- `Willow SKILL.md`;
- existing vendored material elsewhere in the repository;
- external services, downloads, and optional tools; and
- any install or upgrade operation.

Those items require a separate scope decision and must not be treated as
dependencies of Included Ultra based on this document.

## Verification

The boundary can be checked without installing anything:

```bash
git diff --check
git diff --name-only
```

The expected changed path for this slice is only
`docs/burn-wave/DEPENDENCY_INVENTORY.md`.
