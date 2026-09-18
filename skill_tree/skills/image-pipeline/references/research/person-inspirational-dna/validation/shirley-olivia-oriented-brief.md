# IPQ-067 Validation Brief — Shirley seed × Olivia-oriented

**Status**: READY 2026-08-13  
**Seed**: `references/research/shirley-manson-inspirational/`  
**Target hint**: Olivia (selectable, not a forced lock)  
**Output intent for this test**: `m3-hybrid`  
**Hard veto**: underage-appearance

## Hybrid direction used for this brief
- **Primary era**: current-platinum
- **Secondary**: 90s-red
- **Traits that travel**: extreme graphic black wing, controlled high-motion intensity, fringe/patch/harness costume language, architectural red lip
- **Traits suppressed**: childhood freckle-forward look (unless explicitly requested)
- **Original traits to protect** (Olivia DNA — protect, do not overwrite):
  - 5'10"
  - asymmetrical black pixie + bold red streak
  - glowing red Core Mark on left collarbone
  - never bunny / holo ears
  - dominant high-agency energy
- **Original traits to inject**: none required for this test

## Selectable options (this run)
- height_override: null (keep Olivia 5'10")
- holo_ears: false
- olivia_quality: true
- target_character_hint: olivia

## Suggested M3 hybrid trait plan
1. Base = Olivia locked DNA (height, hair, Core Mark, no holo ears)
2. Overlay traveling traits from `dna-stubs/era-current-platinum.md` (wing architecture, intensity, costume language)
3. Optional light support from `dna-stubs/era-90s-red.md` (red lip geometry only)
4. Do **not** pull childhood stub unless operator explicitly escalates

## Success criteria for validation
- [ ] Seed MANIFEST + three DNA stubs readable
- [ ] Hybrid plan respects Olivia locks
- [ ] No underage appearance
- [ ] Output can be handed to Echo / M3 without re-deriving direction mid-compose

## Notes
This brief does not generate images by itself. It proves the **direction + seed → compose-ready plan** path.
