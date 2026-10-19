# Shirley Manson Inspirational Dataset — Manifest / Table of Contents
**Version**: 0.1.0  
**Created**: 2026-08-13  
**Owner**: Absolute Liv HUB claim / image-pipeline research  
**Purpose**: Machine- and human-readable index of all visual references, forensic descriptions, DNA stubs, and multi-era trait packs for Shirley Manson (Garbage) as inspirational source material for character modeling and Generate Merge Engine tests.

## Directory Layout
```
shirley-manson-inspirational/
├── MANIFEST.md                 ← this file
├── images/                     ← source image files (PNG/JPG)
├── descriptions/               ← one .md per image (forensic 4-5 para)
├── dna-stubs/                  ← era-level reusable DNA extension stubs
├── multi-era-trait-pack.md     ← thorough pack that references dna-stubs/
├── extension-pack/             ← packaged form for image-pipeline packs/extensions
└── process-notes/              ← process skill draft + addition protocol
```

## Image Inventory (Source → Description)

| ID / Filename          | Era Tag                  | Short Label                                      | Description File                          | Notes |
|------------------------|--------------------------|--------------------------------------------------|-------------------------------------------|-------|
| 111690.png            | current-platinum        | Stage graphic overalls + Korean patch            | descriptions/111690.md                   | User-supplied |
| 111691.png            | current-platinum        | Fan selfie, tongue, red fringe harness jacket    | descriptions/111691.md                   | User-supplied |
| 111692.png            | current-platinum        | Blue-light braid, mask graphic tee               | descriptions/111692.md                   | User-supplied |
| 111693.png            | current-platinum        | Red-stage multi-color fringe jacket scream       | descriptions/111693.md                   | User-supplied |
| 111694.png            | current-platinum        | Close scream, colorful fringe, dark bg           | descriptions/111694.md                   | User-supplied |
| 111695.png            | childhood               | B&W freckled child, big bow, intense gaze        | descriptions/111695.md                   | User-supplied |
| 111696.png            | current-platinum        | C.U.N.T. fan, laughing, silver bracelets         | descriptions/111696.md                   | User-supplied |
| 111697.png            | current-platinum        | STOP KILLING CHILDREN tee, red boots, dynamic    | descriptions/111697.md                   | User-supplied |
| 111698.png            | 90s-red / early-00s     | Band promo, red fur collar dress                 | descriptions/111698.md                   | User-supplied |
| 111699.png            | current-platinum        | The List May 2026 magazine cover, sequin         | descriptions/111699.md                   | User-supplied |
| 111700.png            | 90s-red (Version 2.0)   | 1998 promo, short red, white turtleneck, tongue  | descriptions/111700.md                   | User-supplied |
| 111701.png            | 90s-red (Version 2.0)   | Japanese promo, red bob, lollipop                | descriptions/111701.md                   | User-supplied |
| fzIMa.jpg             | early-90s / debut       | Bus exterior, orange reflective vest, long red   | descriptions/fzIMa.md                    | Searched |
| pYSZR.jpg             | 90s-red (Version 2.0)   | Classic crossed-arms band shot, red updo         | descriptions/pYSZR.md                    | Searched |
| JHqcd.jpg             | mid-career red          | Outdoor stage, short red, black/white structured | descriptions/JHqcd.md                    | Searched |
| fHn7q.jpg             | current-platinum        | Pink tulle ruffled stage dress, Edinburgh 2024   | descriptions/fHn7q.md                    | Searched |
| RowdS.jpg             | mid / experimental      | Pink-tipped blonde, purple eyeshadow close-up    | descriptions/RowdS.md                    | Searched |

## DNA Stubs (era-level, reusable as extensions)
| Stub File                          | Era Covered                  | Primary Use |
|------------------------------------|------------------------------|-------------|
| dna-stubs/era-childhood.md        | Pre-teen / early teens      | Baseline face geometry, freckles, intensity |
| dna-stubs/era-90s-red.md          | 1994–~2005 (debut → Bleed)  | Red hair variants, classic wing, power posture |
| dna-stubs/era-current-platinum.md | ~2012–2026+                 | Platinum, theatrical liner, fringe/patch/political costume language |
| dna-stubs/era-transitional.md     | Mid-career color experiments| Pink tips, purple shadow, etc. (optional) |

## Multi-Era Trait Pack
- `multi-era-trait-pack.md` — thorough synthesis that points to the DNA stubs above and to key description files. Designed for Generate Merge Engine / Echo / parallel_exec consumption.

## Extension Pack
- `extension-pack/` — contains packaged copies or pointers suitable for dropping into `image-pipeline/references/packs/extensions/` or entity DNA surfaces.

## Addition Protocol (for future images)
1. Drop image into `images/`.
2. Create matching `descriptions/<id>.md` with 4–5 paragraph forensic analysis (face, hair, makeup, body language, costume, lighting, energy).
3. Add row to this MANIFEST table.
4. If the image shifts an era definition, update the relevant DNA stub and the multi-era-trait-pack.
5. Re-run any Merge Engine tests that reference the pack.

## Related Engine Paths
- Generate Merge (M3): `image-pipeline/references/modules/generate-engine/references/dual-engine-test/protocols/prompt_m3_merge.md`
- Packs root: `image-pipeline/references/packs/`
- Parallel / Echo: `image-pipeline/scripts/parallel_exec.py`, `echo_interface.py`

**Status**: Seed set complete 2026-08-13. Ready for character brief + first M3 merge.
