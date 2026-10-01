# image-pipeline registry

**SSOT for pack/preset schemas and indexes**  
**WQ-012** — stabilized 2026-07-24

## Files (do not scatter)

| File | Role |
|------|------|
| `pack.schema.json` | JSON Schema for atomic packs |
| `packs.index.json` | Catalog of packs |
| `preset.schema.json` | JSON Schema for presets |
| `presets.index.json` | Catalog of presets |
| **This README** | Path map + consumer contract |

## Consumer contract (Echo / compose)

1. Prefer `python scripts/echo_interface.py registry` when available.  
2. Otherwise read `packs.index.json` + `presets.index.json` as the catalog.  
3. Validate new packs/presets against the matching `*.schema.json` before merge.  
4. **Do not** invent a second registry under modules/ — module CHANGELOGs are module-local history only.

## Related paths

| Concern | Path |
|---------|------|
| Visual assets index | `../visuals/index.md` |
| Skill-level changelog | `../../CHANGELOG.md` (root) |
| Docs pointer | `../../docs/changelog.md` → root CHANGELOG |
| Generate/overlay module logs | `../modules/*/CHANGELOG.md` |

## Durability
Registry JSON is authority under this folder. Copies elsewhere are refresh-only if ever required (see Alpha DURABILITY hybrid policy).
