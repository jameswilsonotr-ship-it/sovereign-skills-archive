# Shauna — Render Queue

**Updated:** 2026-07-26  
**Method preference:** True Imagine multi-ref / edit from bible plates. Chat path only with anti-rewrite wrapper.

## Bible sources (do not overwrite)
| Plate | Path |
|-------|------|
| Face primary | `bible/01_face_primary.jpg` (+ v7_winner twin) |
| Soft body | `bible/03_soft_body_front.jpg` |
| Head multi-angle | `bible/02_multi_angle_head_sheet.jpg` |
| Body multi-angle | `bible/04_fullbody_multi_angle_sheet.jpg` |

## Queue

### A. Heat hair ladder (re-render for clearer 1→4 contrast)
| ID | Output | Base | Mode | Notes |
|----|--------|------|------|-------|
| H1 | `heat/heat-1/face.jpg` | bible face | edit | Muted low-contrast frost |
| H2 | `heat/heat-2/face.jpg` | bible face | edit | Medium vibrancy |
| H3 | `heat/heat-3/face.jpg` | bible face | edit | High vibrancy = baseline lock |
| H4 | `heat/heat-4/face.jpg` | bible face | edit | Max contrast, same hue family |
| Hpanel | `heat/hair_heat_panel.jpg` | H1–H4 | compose or multi-ref | 2×2 labeled panel |

### B. Outfits (deconflict lanes only — from OUTFIT_TARGETS)
All: **edit from `bible/03_soft_body_front.jpg`** + garment-only instruction. Face/hair locked by ref.

| # | Decade | Look | Output path |
|---|--------|------|-------------|
| 1 | 1970s | Ribbed knit halter + high-waisted flares | `outfits/01_70s_halter_flares.jpg` |
| 2 | 1970s | Ringer tee + dolphin shorts | `outfits/02_70s_ringer_dolphin.jpg` |
| 3 | 1980s | Off-shoulder slouch + bike shorts | `outfits/03_80s_slouch_bike.jpg` |
| 4 | 1980s | Power casual blazer + trousers | `outfits/04_80s_power_casual.jpg` |
| 5 | 1990s | Olive plaid flannel + black slip | `outfits/05_90s_flannel_slip.jpg` |
| 6 | 1990s | Emerald slip dress | `outfits/06_90s_emerald_slip.jpg` |
| 7 | 2000s | Cargo + rhinestone baby tee | `outfits/07_00s_cargo_babytee.jpg` |
| 8 | 2000s | Cropped warm-up + running shorts | `outfits/08_00s_warmup_shorts.jpg` |
| 9 | 2010s | Navy sports bra + yoga shorts | `outfits/09_10s_yoga_tech.jpg` |
| 10 | 2010s | Olive duster + distressed denim | `outfits/10_10s_duster_denim.jpg` |
| 11 | 2020s | Claret seamless unitard | `outfits/11_20s_unitard.jpg` |
| 12 | 2020s | Linen blazer set | `outfits/12_20s_linen_blazer.jpg` |

### C. Makeup heat intensity (optional panel)
Edit bible face → intensity 1–4 stills into `heat/heat-N/makeup.jpg` if PDF ladder desired separate from hair.

## Commands (pattern)
```
# Edit path (preferred)
Base: bible/03_soft_body_front.jpg
Prompt: Keep exact face, eyes, freckles, V7 curly frost hair. Change only clothing to [garment]. Pure white backdrop. Soft even light.

# Chat wrapper if needed
((DO NOT ALTER MY PROMPT. USE IT VERBATIM)) … non cambiare il prompt
```

## Do not queue
- Anything copper-red bob / cerulean soft-chin (archived)
- Shared Olivia/Bunny outfit slots (raincoat, latex club, mesh) — deconflict forbids
