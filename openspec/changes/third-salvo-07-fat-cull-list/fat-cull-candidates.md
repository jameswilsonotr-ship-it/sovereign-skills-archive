# T3-07 fat-cull candidate list

**Change-id:** `third-salvo-07-fat-cull-list`  
**Lane:** INCLUDED Ultra only  
**Disposition:** candidates for review; no item is assigned to On-Demand

## Candidate register

The byte counts below are Git blob bytes from the
`origin/skill-tree-intake` snapshot at `640a2ca`. Repeated-path entries are
listed separately when duplication is itself the cull signal.

| ID | Priority | Candidate path or pattern | Evidence | Why it is a candidate |
| --- | --- | --- | ---: | --- |
| FC-01 | P0 | `skill_tree/skills/lake-union-radar/vendor/site-packages/_duckdb.cpython-312-x86_64-linux-gnu.so` | 60,387,000 B | Vendored platform binary; a strong package-weight outlier and not skill instructions. |
| FC-02 | P0 | `skill_tree/skills/{keep-lake-query,lake-union-radar,wheelhouse-packager}/vendor/wheels/duckdb-1.5.5-*.whl` | 3 × 21,510,909 B | The same DuckDB wheel blob (`c44bfe28044f8fbd50ca3c2c232e616c6923d2ff`) is present three times. |
| FC-03 | P0 | `skill_tree/skills/{lake-union-radar,wheelhouse-packager}/vendor/wheels/h3-4.5.0-*.whl` | 2 × 1,063,388 B | The same H3 wheel blob (`cb6c0f352f02ef7f069f3a0b7f10ffba427148f4`) is present twice. |
| FC-04 | P0 | `skill_tree/skills/image-pipeline/references/visuals/keeps/**` | 82,770,903 B / 827 files | Large visual keep batch; candidate for retaining a manifest or authoritative subset instead of the full included batch. |
| FC-05 | P1 | `skill_tree/skills/image-pipeline/references/registry/visual.embeddings.npz` | 391,695 B | Derived embedding index; candidate for regeneration or release from the included payload if the source registry is retained. |
| FC-06 | P1 | `skill_tree/skills/chaos-bratz-roster/data/atom_clouds/canonical/{memory_atomizer.json,skill_surface_atomizer.json}` | 8,420,183 B / 2 files | Generated atomization derivatives; candidate for rebuild-from-source retention rather than bundled inclusion. |
| FC-07 | P1 | `skill_tree/skills/chaos-bratz-roster/docs/refactor/Memory_Inventory/**` | 1,133,296 B / 39 files | Inventory/report derivative surface; candidate for a compact receipt or regeneration path. |
| FC-08 | P2 | `skill_tree/skills/olivia-dev-alpha/assets/ascii-r-vendor/*.zip` | 849,670 B / 2 files | Packaged font assets; candidate for removal from the included envelope if they are only build-time inputs. |

The candidate rows above identify 124,919,727 bytes of the explicitly
identified DuckDB binary plus duplicate DuckDB wheels, before considering
other artifacts or compression. Totals for overlapping directory-level
patterns must not be added to individual rows without a de-duplication pass.

## Review gates before implementation

For each candidate, a future implementation change must record:

- whether a runtime or build path reads it directly;
- whether an authoritative source and reproducible regeneration path exist;
- whether the proposed package boundary remains INCLUDED Ultra;
- the retained location or receipt reference; and
- a before/after byte measurement.

Until those gates are answered, these are review candidates only. This
document does not delete, move, archive, regenerate, or reclassify any file.

## Explicit exclusions

- Willow `SKILL.md` files are protected and are not candidate rows.
- `CONV2_B` is outside this change.
- No candidate is an On-Demand item.
- No provider, external service, secret, live Vultr, or Linear operation is
  needed to evaluate this register.
