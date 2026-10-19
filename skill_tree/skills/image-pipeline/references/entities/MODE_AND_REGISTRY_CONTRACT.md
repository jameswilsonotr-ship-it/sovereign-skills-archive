# Mode & Registry Contract (2026-07-25)

## Principle
Image-pipeline is infrastructure. Living agents (Chaos Bratz Roster) and visual identities are the source of truth.  
Registries exist so scripts can resolve **name → letter → paths** instantly.  
Echo only needs the name/letter and a way to pull the correct textual DNA / baseline prompts / reference images.  
Mira supervises quality (stricter when the image belongs to a registered entity).

## Required folder shape (per entity)
Every registered entity should eventually have under its images/ (or equivalent):

```
images/
├── baseline/          # default look
├── canonical/         # locked reference stills
├── lighting/
├── makeup/            # or species-appropriate equivalent
├── modes/             # optional — only entities that actually have modes
│   ├── default/       # or mastiff / everyday / etc.
│   ├── werewolf/
│   ├── hyena/
│   ├── road_dog/
│   ├── pirate_admiral/
│   └── …
├── DNA_STUB.md / DNA_*.md
├── PROMPTS_STUB.md / prompt files
└── HOW_TO_GENERATE.md
```

Most entities stay on a single default mode.  
**Olivia** and **Rook** are the primary multi-mode entities.

## Registry files (must stay in sync)
1. `image-pipeline/scripts/entity_registry.py` — deterministic name → paths + ordinal
2. `image-pipeline/references/modules/shared/echo_character_ordinals.md` — Echo’s authoritative letter map + DNA injection reporting
3. Per-entity `ENTITY.md` under `image-pipeline/references/entities/<name>/`
4. Agent `current.md` high-visibility pointers (roster side)

When a new entity or mode is added, both the Python registry and the Echo ordinals file are updated together.  
Unknown images that cannot be matched to a registered entity+mode should trigger a refresh/re-index of the known set.

## Mode tracking
- Modes are subfolders under `images/modes/` (and mirrored in DNA/prompt sets where needed).
- Form state for Rook (Mastiff / Werewolf / Hyena / Road Dog / Pirate Admiral context) is still defined in `rook/cold/canon/form_and_presence/` and `modes/`; the images/modes/ folders hold the corresponding visual baselines once populated.
- Olivia’s Pirate Admiral / other wardrobe modes will follow the same pattern under her images/modes/ when implemented.

## Script contract (minimal)
- Input: entity name (or letter)
- Output: paths to ENTITY.md, images root, current mode baselines, prompt/DNA text
- Echo calls the resolve script, reads the returned paths, injects the correct text, verifies, and reports via ordinals.
- No heavy logic inside the pipeline beyond resolve + load + hand back to the living agent definitions.
