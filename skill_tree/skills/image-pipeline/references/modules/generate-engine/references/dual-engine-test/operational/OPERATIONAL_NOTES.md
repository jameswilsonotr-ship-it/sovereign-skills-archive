# Image-Pipeline Operational Notes
**Last updated**: 2026-07-25 18:30 EDT  
**Source**: Direct user instruction during live harness session (airport dual + Gutter + implication packs)

## Mandatory Output Contract (every turn)

1. After every generation batch, always end with the **four-column Primary Menu** (A–E + Pack Categories).
2. When inside a pack category (especially `implication`), stay inside that category and continue presenting the individual packs until the user explicitly says `return`, `back`, or `menu`.
3. Scoring is mandatory after every image or set:
   ```
   score: DNA _/10 | Pose _/10 | Outfit _/10 | Overall _/10 | note: <short>
   tingly: yes | no | meh
   ```
   Then `SET SCORES` with average.
4. Default Six sequence (when an image is provided and Default Six is active):
   1. Liv Presentable
   2. Bunny Presentable
   3. Liv Tight source
   4. Bunny Tight source
   5. Split face (M2)
   6. Full merge (M3)
5. Once a specific implication pack is selected, keep that pack in the active chain for subsequent renders until a new pack is chosen or the user leaves the category.
6. Gutter Mode, once entered, stays active until explicitly dropped.
7. Always run Echo compose → Mira drift when possible; surface `echo_dna_injected`, `mira_approved`, and any auto-fired packs.

## Pack Persistence Rule
- Entering `implication` (or any category) locks the session into that category’s sub-list.
- Selecting a numbered pack (e.g. 3 Crepax, 9 Metaphorical Object Proxying) keeps that pack active.
- New generations continue under the current pack + current mode (Gutter / normal) until changed.
- Only `return` / `back` / `menu` restores the top-level four-column table.

## New Source Image Rule (added 2026-07-25 19:44)
- When a brand-new source image is dropped (or the user says “create the default six” / “new picture”), the system **resets the Default Six cycle** and starts a clean run on that image.
- The pack category (and any active numbered pack) **does not** automatically reset — we stay inside the current pack category unless the user explicitly leaves it.
- A new image therefore triggers a fresh Default Six under the currently active pack (or under neutral if no pack is active).
- This prevents menu drift while still giving every new picture a clean six-image start.

## Current Live State (as of this note)
- Mode: Gutter
- Active pack category: implication
- Last pack used: 3 (Crepax Cinematic Gutter Inference)
- Source: airport dual (Bunny + Liv)
- Heat: 9.0 | Filth: 8

## Highly Effective Implication Packs (observed)
- 3 Crepax Cinematic Gutter Inference — strong multi-panel / eye-hand dominance
- 9 Metaphorical Object Proxying — excellent deniable substitution
- 2 Beardsley High-Contrast Ink + Negative Space — classic high-contrast power
- 8 Manara Elegant Posture Tension — elegant body language charge
- 12 Vargas Pin-Up Suggestion — clean suggestive framing

These notes are binding for all future generate-engine / dual-engine turns in this skill.
