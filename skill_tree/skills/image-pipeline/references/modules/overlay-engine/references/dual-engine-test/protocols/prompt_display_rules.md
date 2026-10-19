# Protocol — Prompt display rules
**Load whenever emitting any image.**

1. Bold title line per image (descriptive; no `pending render id`).
2. **Emit path (2026-08-28 lock):** overlay uses `edit_image`. From-scratch uses `generate_image`. Persist receipts. Show with `render_file`. Do not emit `render_generated_image` / `render_edited_image` tags. See parent `RENDER_ROUTE_LOCK.md`.
3. Image display with **short** alt only (a few words).
4. **Exactly one** fenced code block with the full prompt — no second copy in prose or alt text.
5. After a set: scores (see `prompt_scoring.md`), then menu.
6. Prefix artifacts `gen_` (generate) or `ovl_` (overlay) when renaming on disk. Persist under `artifacts/rendered/`.
