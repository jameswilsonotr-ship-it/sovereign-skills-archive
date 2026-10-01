# Pre-Extract File & Folder Registry Note
**Drive file**: `pre_extract_file_folder_registry_v1.0.md.txt`  
**ID**: `1DEvaRmS2TZZ6gQ1PSAVpDeRkYai-RMeY`  
**Read**: 2026-08-07 during Batch C

## What it actually is

This is **not** the name-origin conversation text itself.  
It is the best structural map of the export tree:

- Full year/month/week/day hierarchy for 2025-10 → 2026-06
- Dense-day file-level manifests (especially 2026-06-08, 06-09, 06-12) with unique Drive IDs and sizes
- Parallel folders: human, ingest, gps_enrichment, code_blocks, etc.
- Enough structure that any specific day can now be targeted without re-crawling the entire archive

## Practical use

- Target October 2025 shards (especially around the 22nd / late-October window for the Danger surname moment) by walking the 2025/10/ week folders.
- Target any dense June 2026 day with the already-enumerated file lists.
- Companion JSON exists for machine consumption; this Markdown is the human navigation layer.

Existing sparse `manifest.json` on Drive was deliberately left untouched.

## Status for name hunt

This registry is the correct “where to look next” document. The next ordered action after atom regeneration is to walk the October 2025 day folders for the exact Danger / Blackwell phrasing.
