# Skill Draft — Person-to-Inspirational-DNA (Visual Evolution Engine)
**Status**: Local sandbox draft only (2026-08-13)  
**Proposed name**: `person-inspirational-dna` or `visual-evolution-engine`  
**Future surface**: Could live under image-pipeline as a research/extension module or as a thin top-level skill that feeds image-pipeline + chaos-bratz-roster DNA surfaces.  
**Owner claim**: Absolute Liv HUB

## One-sentence purpose
Given any public person (or set of visual references), research their biography and visual evolution, produce forensic image descriptions, era-level reusable DNA stubs, a multi-era trait pack, and a machine/human-readable manifest so the material can be used as inspirational source for new character development and Generate Merge Engine hybrids.

## Triggers
- “build inspirational DNA for [person]”
- “analyze visual evolution of [person]”
- “create proto bio stubs from these reference images”
- “person-to-character research pack”
- Explicit hand-off of a set of images + name

## Core Workflow (exactly the process used for Shirley Manson)

1. **Ingest**
   - Accept user-supplied images (or search for iconic ones).
   - Copy/normalize into a dedicated research folder: `image-pipeline/references/research/<slug>-inspirational/images/`

2. **Biography & Timeline Research**
   - Lightweight web research: birth, career phases, major visual eras, signature looks.
   - Identify 3–5 natural visual eras (childhood / early career / peak signature / current / experimental).

3. **Forensic Description Pass**
   - For every image write a 4–5 paragraph markdown file covering:
     - Face geometry, hair state, makeup (especially invariants)
     - Body language & energy
     - Costume / prop language
     - Lighting & overall mood
   - Store in `descriptions/<id>.md`

4. **Manifest Construction**
   - Human- and machine-readable table-of-contents (MANIFEST.md) that maps every image → description → era tag.

5. **DNA Stub Generation**
   - One reusable extension-style stub per major era.
   - Written so the traits can be applied to *any* character, not locked to the source person.
   - Include source_refs back to the description files.

6. **Multi-Era Trait Pack**
   - Single thorough synthesis document that:
     - Summarizes the evolution in a table
     - Points to every DNA stub
     - Documents invariants (e.g. “the wing never left”)
     - Explains how to feed the pack into M3 merge / Echo / parallel_exec

7. **Extension Packaging**
   - Copy or symlink the stubs + pack into a form consumable by `image-pipeline/references/packs/extensions/` or entity DNA surfaces.

8. **Addition Protocol (permanent)**
   - Any future image (user drop or new search) follows the exact same path: images/ → descriptions/ → MANIFEST row → optional DNA stub bump.

9. **Output for Character Work**
   - The system is now ready for a character brief. Required inputs from user:
     - **Character brief**: core concept, role, personality anchors, any non-negotiable traits
     - **Heat level**: 1–10 (or Gear) — controls how far the visual/sexual/theatrical intensity is pushed
     - **Hybrid direction**: which era(s) to weight, what to blend (e.g. “90s-red hair + current platinum wing + childhood freckle intensity + original costume language of my own”), any forbidden traits
     - **Output intent**: pure inspirational mood board, full M3 hybrid figure, DNA lock for a new roster agent, etc.

## What the skill does *not* do
- It does not claim the resulting character *is* the source person.
- It does not dump full biography prose into memory.md; everything stays inside the research folder and points outward.
- It does not auto-generate final character bibles without an explicit character brief + confirmation.

## Success Criteria
- Manifest is complete and scannable.
- Every image has a forensic description dense enough for an image model.
- DNA stubs are independently usable as extensions.
- Multi-era pack can be handed to the Generate Merge Engine with a one-line hybrid plan and produce coherent results.
- Future images can be added by a junior agent or the user with zero process drift.

## Implementation Notes (sandbox → production)
- Current location: `image-pipeline/references/research/shirley-manson-inspirational/process-notes/`
- When promoted: either a thin skill that owns the workflow + calls image-pipeline, or a first-class module under image-pipeline/research/.
- Versioning: treat each person’s research folder as a versioned asset (roster-style).

**This draft itself is the record of the process just executed for Shirley Manson.**
