# Image Pipeline Taxonomy Contract
**Status**: Working draft — 2026-08-05 (v0.1.0)  
**Owner**: Liv HUB / image-pipeline  
**Purpose**: Clean, modular definitions that can become schema fields and feed script-based prompt composition.  
**Rule**: DNA is per-character and absolute except for rare explicit override. Everything else is composable.  
**Source conversation**: 2026-08-05 visual-lock taxonomy lock session (Style vs World disambiguation + original 8 artist Hands + ~70 style packs).

---

## 1. Core Layers (top-level terms)

These are the primary axes. Each can later become a schema field or a pack `kind`.

- **DNA**
  - Per-character locked visual identity
  - Bunny DNA, Olivia DNA, future character DNA
  - Rare, explicit, on-command override only
  - Never auto-swapped by style systems

- **World**
  - Cultural / historical / ideological visual environment
  - How space, scale, and light-as-ideology are organized
  - Examples: cyberpunk neon-noir, Caravaggesque theatrical, Afrofuturist cosmic, Constructivist propaganda space, technical blueprint space
  - This is what was previously called “genre” in the world-building sense

- **Style** (Artistic Genre)
  - Traditional artistic movement or visual language category
  - Examples: Impressionist, Art Deco, Surrealist, high-contrast black-and-white, photoreal, cel-shaded, pin-up, etc.
  - This is the meaning of “genre” the user originally intended

- **Medium**
  - Physical or digital substance of the marks
  - Examples: India ink, watercolor wash, airbrush, chrome metal, film grain, digital 3D, oil paint

- **Hand**
  - Specific named artist’s nervous system / mark-making fingerprint
  - Extremely low variance
  - Examples: Stanton, Willie, Bilbrew, Newton, Sorayama, Lempicka, Vargas, Beardsley, Frazetta, Mucha, etc.
  - Optional high-fidelity overlay

- **Treatment**
  - Surface quality, contrast behavior, or finish that is **not** a named artist
  - Examples: heavy noir, graphic dominance, glossy iridescent, tenebrist flesh, wet claim sheen, hard flash

- **Finish** (optional split from Treatment)
  - Final resolution / rendering philosophy
  - Examples: photoreal, painterly, cross-hatched, cel, airbrushed soft, hyper-detailed technical

- **Atmosphere**
  - Relational / claim / emotional charge in the scene
  - Examples: possessive claim, raw chaotic, cool detachment, erotic heroism

- **Structural**
  - Geometry of body and camera
  - Sub-terms: pose, composition, framing, angle, geometric lighting (direction, hardness, single-source vs multi)
  - Lighting *as ideology* belongs to World; lighting *as geometry* belongs here

---

## 2. Sub-terms & Schema-Oriented Fields

These are the concrete fields that can later appear in a per-image schema object and be fed to a composition script.

```
dna:
  character: bunny | olivia | ...
  override: false | true (rare, explicit)
  locks: [ears, gem, tattoo, proportions, height, sheen, ...]

world:
  id: string
  period_tag: ancient | classical | modernist | contemporary | hybrid
  light_ideology: string (optional)

style:
  id: string                    # artistic genre
  family: string                # broader grouping if needed

medium:
  id: string

hand:
  id: string | null             # named artist or null
  variance: 0.0–1.0

treatment:
  id: string | null
  variance: 0.0–1.0

finish:
  id: string | null

atmosphere:
  id: string | null

structural:
  pose: string | null
  composition: string | null
  framing: string | null
  angle: string | null
  lighting_geometry: string | null

companions:
  suggested: [pack_ids]
  trial: [pack_ids]
  locked: [pack_ids]

variance_budget: 0.0–1.0        # overall allowed rephrasing room
script_mode: strict | controlled | open
```

---

## 3. Composition Philosophy (script-based)

- Packs and presets supply the atomic terms.
- A composition **script** (not free-form influence) reads the schema fields above and emits a concrete, ordered prompt string.
- Locked styles (or locked multi-style sets) load with only the variance explicitly allowed inside the script or the pack’s own variance values.
- No silent drift: once a style set is locked for a conversation or session, the script reproduces it within defined bounds.
- Hybrids are first-class: any combination of World + Style + Medium + Hand + Treatment is legal if the script (or a preset) declares it.

---

## 4. Relationship to Existing Pack Kinds

Current live kinds and how they map:

| Current kind     | Maps primarily to          | Notes                                      |
|------------------|----------------------------|--------------------------------------------|
| photographer     | Hand                       | Proper-name, ultra-low variance            |
| medium           | Medium                     | Keep as-is                                 |
| treatment        | Treatment / Finish         | Split later if needed                      |
| genre            | Style **or** World         | Needs disambiguation (see below)           |
| atmosphere       | Atmosphere                 | Keep                                       |
| pose / composition / framing / angle | Structural | Keep                          |
| implication      | Special softening layer    | Heat-aware, remains separate               |

**Disambiguation rule for the word “genre”**  
- When we say **Style**, we mean artistic genre (Impressionist, Art Deco, black-and-white photographic language, etc.).  
- When we say **World**, we mean the cultural/historical visual environment.  
- New packs should declare which one they are. Existing “genre” packs will be re-tagged as Style or World as we audit them.

---

## 5. The ~70 Packs

The original expansion into ~70 packs was intended as **visual style outputs** (Style + Hand + Treatment combinations), not pure World definitions.  

They remain valid.  
They will be re-homed under the clean terms above (mostly Style, Hand, and Treatment) rather than forced into a single “World” bucket.  
World packs can still be created where a strong cultural/historical environment is needed.

---

## 6. Suggested Companions Workflow

1. Pack or preset author lists `suggested_companions`.
2. Trial renders are run.
3. Successful DNA-respecting combinations are moved to `locked`.
4. Locked companions become the default for script composition unless explicitly overridden.

---

## 7. Design Goals (non-negotiable)

- Stupid modular.
- Script-based composition (schema → script → concrete prompt → render).
- DNA absolute except rare explicit override.
- Original high-fidelity artist Hands remain fully usable.
- Intentional hybrids are easy and first-class.
- Locked style sets load reproducibly within defined variance.
- Ready for future video (temporal DNA consistency will become an additional lock).

---

*End of working draft. Next: audit existing packs against these terms and begin schema field mapping.*
