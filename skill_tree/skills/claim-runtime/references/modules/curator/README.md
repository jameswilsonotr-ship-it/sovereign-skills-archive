## Visual inventory (disk-only)

```bash
python ../../scripts/visual_inventory.py list --folder hair --page 1
python ../../scripts/visual_inventory.py pick --folder hair 1 2 3 4
python ../../scripts/visual_inventory.py audit
```

Agent must `read_file` selected absolute paths to show images inline (max 6).

# porn-curator

**Status**: Active  
**Owner**: Absolute Liv HUB claim  

## Purpose
Long-form Blacked/stylized filth recommendations, Gutter Claim or Breeding Ache themed rotations, visual previews, or testing the full porn curation engine with all extensions.

## Triggers
porn curator, filth recommendation, Gutter Claim rotation, raw recommendation, dripping and raw, or any high vice-signaling request for long-form content.

## Structure
```
porn-curator/
├── SKILL.md
├── README.md
├── TODO.md
├── CHANGELOG.md
├── characters/
│   └── shauna/          ← locked visual character (Kara Bare / early Shawna Lenee DNA)
│       ├── README.md
│       ├── DNA_LOCKS.md
│       ├── BASELINE.md
│       ├── OUTFIT_INVENTORY.md
│       └── MESH_SERIES.md
```

## Characters
- **Shauna** (`characters/shauna/`) — Copper-red chin-length razor bob with magenta tips, soft youthful face (fuller cheeks / rounded chin), fair freckled skin, blue eyes. Multi-era wardrobe + mesh series ready. Load DNA lock + baseline before generation.

## Related
- vice-command-orchestrator
- risk-fantasy-claim-protocol
- chaos-bratz-roster (Gutter Mode + visual DNA)
- image-pipeline

Under absolute Liv HUB claim. Full RACK and visual DNA enforcement.

## Library Tier & Consolidation Note (2026-07-19)
This skill is part of the tiered library architecture owned by **skill-orchestrator**.
See: `skill-orchestrator/references/plans/TIERED_LIBRARY_ARCHITECTURE.md` and `references/inventory/CURRENT_TIERS.md`.

## Atom Cloud (session / canonical)

See `atoms/README.md` for the full dual-layer design.

Quick use:
```bash
# search (session preferred)
python atoms/search.py "feet"
python atoms/search.py "inflation" --kind hybrid

# promote when session is ready (explicit only)
python atoms/promote_union.py          # dry-run
python atoms/promote_union.py --apply  # write canonical + manifest
```

- Session overlays live under `atoms/sessions/`
- Canonical under `atoms/canonical/`
- Legacy global `atoms/curator_atom_cloud.json` is left untouched by default
- Schema v0.4.0-session adds owner / excitement / interaction_log / kind
