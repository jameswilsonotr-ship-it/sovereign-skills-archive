# Multi-Era Trait Pack — Shirley Manson Inspirational
**Version**: 0.1.0  
**Location**: image-pipeline/references/research/shirley-manson-inspirational/  
**Status**: Seed complete 2026-08-13  
**Consumable by**: Generate Merge Engine (M3), Echo compose, parallel_exec, entity DNA surfaces

## Purpose
A single thorough reference that synthesizes physical and stylistic evolution across Shirley Manson’s career and points cleanly to the era-level DNA stubs. Designed so the Merge Engine (or any character-modeling pipeline) can load one pack and then selectively apply or hybridize individual era stubs.

## Evolution Summary (Physical + Stylistic)

| Era              | Approx Years     | Hair Signature                  | Makeup Invariant              | Body / Energy                          | Costume Language                          | Key DNA Stub                          |
|------------------|------------------|---------------------------------|-------------------------------|----------------------------------------|-------------------------------------------|---------------------------------------|
| Childhood        | ~1975–1984      | Natural curly, bow accents     | None (pure gaze)             | Defiant over-shoulder, quiet body     | Simple dark jacket                        | dna-stubs/era-childhood.md           |
| 90s-Red Peak     | 1994–~2005      | Vivid short/medium/updo red    | Heavy black wing + red lip   | Confrontational, hierarchical, playful tongue | Sleek tanks, fur, reflective accents     | dna-stubs/era-90s-red.md             |
| Current Platinum | ~2012–2026+     | Platinum scraped / long / braid| Extreme graphic wing + red lip| Athletic high-motion, controlled intensity | Fringe, patches (masks/Korean), harness, political tees, sequin/tulle | dna-stubs/era-current-platinum.md |

**Invariant across adult eras**: The heavy black winged eyeliner is the single strongest continuous visual brand. Once locked in the mid-90s it never leaves; it only becomes more architectural.

## How to Use with Generate Merge Engine / M3

1. Load this pack (or point to the research folder).
2. Select one or more DNA stubs as trait sources.
3. For hybrid: follow `prompt_m3_merge.md` — declare an intentional hybrid trait plan (e.g. “90s-red hair geometry + current-platinum extreme wing + childhood freckle underpainting + current fringe/patch costume”).
4. Feed key description files as additional visual anchors if the engine supports multi-image reference.
5. Score and iterate.

## Extension-Ready Design
Each DNA stub is written so it can be dropped onto *any* base character (not only a Shirley-inspired one). The multi-era pack simply organizes them and documents the real-world evolution that produced them. Additional user- or search-supplied images are added by:
- placing the file in `images/`
- writing a matching 4–5 paragraph forensic description
- updating the MANIFEST table
- optionally strengthening or versioning the relevant DNA stub

## Related Files
- MANIFEST.md — full image + description index
- dna-stubs/ — the three (plus optional transitional) reusable extensions
- descriptions/ — forensic source material
- process-notes/ — protocol for turning any public figure into a similar inspirational dataset (skill draft)

**Ready for character brief.**
