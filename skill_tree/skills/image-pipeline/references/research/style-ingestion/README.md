# Style Ingestion — General Module (IPQ-074)

**Status**: LIVE foundation 2026-08-15  
**Owner**: image-pipeline / Absolute Liv HUB claim  
**First examples**: anime & anime-adjacent compilation plates (not a hard limit)  
**Related**: IPQ-049 (Anime Style Bank), anime_substyle_registry, IP-WQ-042 (receipt rules)

## Purpose

Turn real artist plates (YouTube compilations, Drive still folders, stills from any source) into structured, attributable, human-gated candidates for:

- `anime_substyle_registry` rows
- implication-pack drafts
- hand / medium / palette / face-convention clusters
- any future style registry under the pipeline

This is a **resource + workflow**, not an identity override. DNA locks for Liv and Bunny remain absolute. Plates are style/outfit teachers only.

## Hard Rules (non-negotiable)

1. **DNA locks stay ours.** No plate becomes a replacement for Liv or Bunny core visual DNA.
2. **IP-WQ-042 receipt discipline.** No numeric scores until the user confirms which plates actually landed in the UI.
3. **Batch ≤ 3** until the ingest path is proven stable under real context pressure.
4. **Human promote / demote / hold gate** is mandatory before any registry write or pack promotion.
5. **General, not anime-only.** Anime is the first high-signal example set; the same template and flow apply to any graphic language (game art, print illustration, fashion plates, comic hands, etc.).
6. **Source attribution is required.** Channel, on-screen credit, OCR when needed, Drive path or URL.

## Layout

```
style-ingestion/
├── README.md                 ← this file
├── protocols/
│   └── STYLE_INGESTION_FLOW.md
├── templates/
│   └── PLATE_ANALYSIS.template.md
├── schema/
│   └── plate_analysis.schema.json   (lightweight, optional machine surface)
└── examples/                 ← first real plate runs land here after gate
```

## High-level Workflow

1. User drops YouTube compilation link **or** Drive folder of stills (or mixed).
2. Agent proposes (or re-confirms) the exact analysis template.
3. Agent processes in batches of ≤ 3 plates.
4. For each plate: fill the analysis template (source + medium/hand + palette + face/eye + outfit tropes + cluster notes).
5. Emit RECEIPT block (IP-WQ-042) — planned vs confirmed.
6. Human gate: promote / demote / hold / needs second look.
7. On promote: draft candidate row for the appropriate registry (or implication-pack stub) and stop for final confirmation before write.

## Tooling (sandbox)

Installed and available for this module (2026-08-15):

- `gallery-dl` 1.32.9 — primary for image galleries, community-style still posts, and multi-image sources.
- `yt-dlp` 2026.07.04 — thumbnails, channel/video metadata, fallback extraction, frame extraction via ffmpeg when needed.
- `ffmpeg` (system) — already present for any frame work.

These live in the environment so style-ingestion can pull clean still plates from a channel link or individual post without requiring the user to pre-download everything.

## Integration Points

- **Echo**: may pull style language after a plate is promoted.
- **Mira**: relational / fidelity notes only after human confirmation.
- **Olivia**: final orchestration + gate authority.
- **Registries**: `references/registries/anime_substyle_registry.json` is the first consumer; others follow the same pattern.

## Triggers

- "style ingestion", "ingest plates", "run style-ingestion", "analyze these artist plates"
- Dropping a compilation link or Drive set in context of image-pipeline work
- Explicit "formalize style ingestion" or "surface style-ingestion module"

## Versioning Note

This module follows the same progressive-disclosure and human-gate culture as person-inspirational-dna and the Anime Style Bank. First real plate runs become the validation set.