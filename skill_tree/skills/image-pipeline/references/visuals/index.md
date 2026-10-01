# visuals index

**SSOT index for versioned visual assets**  
**Path**: `image-pipeline/references/visuals/`  
**WQ-012** — 2026-07-24

## Layout

```
references/visuals/
  index.md                 ← this file
  assets/                  ← versioned assets by category/slug
  file_listing.md
  visuals-from-memory.md   ← import notes (not live SSOT)
```

## Rules
1. New visual components land under `assets/<category>/<slug>/` with version + history when using roster-style homogenization.  
2. Update **this index** when adding a major category or canonical asset.  
3. Root `CHANGELOG.md` records skill-level releases; asset-level history stays in the asset folder.  
4. DNA / bible visual rules may live under `assets/dna-bible-visual-rules/` or skill references — link from here when promoted to canon.

## Categories (live)
| Path | Notes |
|------|--------|
| `assets/` | Auto-detected / homogenized visual assets |
| `assets/dna-bible-visual-rules/` | DNA bible visual rules (if present) |
| `assets/constant-filming/` | Always-on continuous multi-camera recording + republication protocol |
| `assets/constant-filming/always-on-cam-protocol/` | **v0.2.0 LIVE DEFAULT — DEEPENED** — 2026-08-02. Always-on multi-cam + interaction speech defaults + Rook enforcement + Mira ache linkage. Ambient reality. |
| `assets/costumes/` | Locked outfit / costume sets for Olivia + Bunny (and future agents) |
| `assets/costumes/strappy-bondage-micro-set/` | **v0.1.0 GENESIS LIVE** — 2026-08-13. Heat 7 micro black leather hot pants + small black nipple pasties + complex multi-strap bondage harness. Full DNA locks + skin-tone series status. |

## Changelog pointer
- Skill: `/home/workdir/.grok/skills/image-pipeline/CHANGELOG.md`  
- Docs stub: `docs/changelog.md` → see root CHANGELOG  

## Registry relationship
Packs/presets catalogs: `../registry/` (`packs.index.json`, `presets.index.json`).  
Visuals index is **assets**, not pack schema — keep separate.
