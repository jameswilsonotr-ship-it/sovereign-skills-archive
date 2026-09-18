# Style Ingestion Flow (IPQ-074)

**Status**: LIVE 2026-08-15  
**Owner**: image-pipeline  
**Parent module**: references/research/style-ingestion/

## Goal

Reliable, attributable, human-gated path from real artist plates → candidate rows for style registries or implication-pack drafts.

## Standing Constraints

- IP-WQ-042: RECEIPT before any scores. No scores until user confirms landed plates.
- Batch size ≤ 3 until stable under real context pressure.
- DNA locks (Liv + Bunny) are never replaced or overwritten by ingested plates.
- Human promote / demote / hold is the only path into registries.

## Flow Steps

1. **Intake**  
   User provides YouTube link (channel, community post, or video) and/or Drive folder of stills.  
   Prefer still-image sources (community posts that drop 8–10 images) over pure video compilations when possible.  
   Agent acknowledges and confirms the analysis template will be used.  
   Tooling available in sandbox: `gallery-dl` for multi-image / community-style stills, `yt-dlp` for thumbnails + metadata + fallback, `ffmpeg` for any needed frame work.

2. **Template Confirmation**  
   Re-surface or lightly adapt `templates/PLATE_ANALYSIS.template.md` if the source type is unusual.  
   Wait for explicit go or first plate set.

3. **Batch Extraction**  
   Process ≤ 3 plates.  
   For each: fill the full analysis template (source attribution mandatory).

4. **RECEIPT Block** (IP-WQ-042)  
   ```
   RECEIPT
   planned: N
   attempted: [ids]
   confirmed_by_user: …
   dropped: …
   context_warning: true|false
   batch_size_guidance: ≤3 while open
   suspected: context_length | moderation | concurrent_limit | style_conflict | generate_vs_edit | unknown
   ```

5. **Human Gate**  
   Present the three (or fewer) filled analyses.  
   Ask only for promote / demote / hold / needs-second-look per plate or per cluster.

6. **Candidate Draft** (on promote)  
   Propose exact registry row language or implication-pack stub.  
   Do not write to disk until final confirmation.

7. **Write & Index** (after final confirmation)  
   Append to the appropriate registry or create the pack draft under the correct location.  
   Log the source plate IDs and gate decision in process notes.

## Integration

- First consumer: `references/registries/anime_substyle_registry.json`
- Future consumers: any hand / medium / palette / implication registry
- Echo may consume promoted language after the write
- Olivia retains final orchestration and gate authority

## Failure / Partial Modes

- Missing attribution → hold and request clearer source or OCR pass
- Ambiguous cluster → hold and request additional plates or human direction
- Context pressure / dropped cards → emit RECEIPT, reduce batch, continue with confirmed only