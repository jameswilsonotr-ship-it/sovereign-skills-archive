# Final Output / Render Engine — Contract (IPQ-014 / IPQ-021)

**Status**: LIVE 2026-07-25  
**Scripts**: `scripts/render_engine.py`, `scripts/presentation_emit.py`

## Forced routing
Olivia → Echo compose (DNA + Mira) → render_engine → **tool `generate_image`** (default) → persist receipt → `render_file` on the saved path → analyze_render.

**SSOT:** `references/modules/shared/RENDER_ROUTE_LOCK.md` (LIVE 2026-08-28).

Do **not** emit `render_generated_image` / `render_edited_image` as the production path. Those tags print as dead text in this client and write nothing to the lake. Gamma (`gamma___generate_image`) is a paid CDN spare door only.

## Output modes / format packs
| Mode / pack | Behavior |
|-------------|----------|
| **single** | One image (default) |
| **carousel** | N consecutive frames in one response; label Carousel i of N; scores + SET SCORES |
| **slideshow** | One slide per turn; label Slide i of M; wait for next |
| **code** | Prompt + trace only, no image |
| **image+code** | Image + code block |
| **bordered** | single + `border-deterministic` style |

## Style packs
- `border-none` (default) / `border-deterministic` (from photographer/implication/treatment)
- `code-exposed` / `code-hidden`
- `forensics-on` / `forensics-off`
- `title-above` / `title-below`

## Agent instructions
`presentation.agent_instructions` is authoritative for how to emit. Always follow after scores (IPQ-019) and forensics when enabled (IPQ-022).

## Borders
Deterministic border terms are merged into the prompt when style is `border-deterministic`. Fallback: subtle neutral frame. No fixed border asset library required.
