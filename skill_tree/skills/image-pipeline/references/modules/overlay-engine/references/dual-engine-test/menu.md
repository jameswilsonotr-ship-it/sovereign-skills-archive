> **IPQ-024**: Pack sub-menus use **numbers**. A–E table stays visible. Picking a number applies the pack to the **last render set** (multi-turn: open category → then number). See `modules/shared/pack_menu.md`.

# Dual-Engine Test Menu (Living State)
**Last updated**: 2026-07-25

## Primary Menu (A–E + Pack Categories)

The original dual-engine options remain the first columns.  
Pack categories are additional columns on the same table.  
Selecting a pack category expands its individual packs (no image rendered yet).  
Return always comes back to this table.

| Option | Status | Avg Score | Notes | Pack Category | Count | Range |
|--------|--------|-----------|-------|---------------|-------|-------|
| **A** Asyncio Actor | | | Concurrent actor-style generation | atmosphere | 2 | 1–2 |
| **B** CSP Channel | | | Sequential channel-style generation | medium | 1 | 1 |
| **C** Heat Gradient (H3/H6/H9) | | | Parallel heat levels | photographer | 14 | 1–14 |
| **D** Angle Expansion | | | front / ¾ / profile | treatment | 12 | 1–12 |
| **E** Minimal (Clean only) | | | Clean Liv + Clean Bunny | pose | 2 | 1–2 |
| | | | | **implication** | **12** | **1–12** |
| **Return / Back** | | | | | | |

**How it works**
- A / B / C / D / E → run the corresponding dual-engine test path (existing behavior).
- atmosphere / medium / photographer / treatment / pose / implication → expand that pack category into a sub-list of individual packs. **No image is rendered.**
- After picking a specific pack from the sub-list, confirm to add it to the active chain, then return here or say “render”.
- `return` / `back` / `menu` always restores this primary table.

Runtime helper: `python scripts/pack_menu.py` or `python scripts/pack_menu.py --category implication`  
Full contract: `references/modules/shared/pack_menu.md`

---

## Status Tracking Rules
- Update this file (or the in-response table) after every completed option.
- Record average score for the option.
- Note partial failures or DNA issues in the Notes column.
- The menu is the source of truth for “what has been run”.

## Current Session Snapshot (Deer Suit 2026-07-24)

| Option | Status | Avg Score | Notes |
|--------|--------|-----------|-------|
| **A** Asyncio Actor | Complete (partial) | ~7.8–8.2 | Shark-fin hair on Liv + empty-file failures on rear |
| **B** CSP Channel | Complete | 8.20 | 4/4 landed; Liv hair still unstable on rear |
| **C** Heat Gradient | Failed write | — | 4 images generated, 0 written to disk |
| **D** Angle Expansion | Partial | 8.4 | 1 of 4 landed |
| **E** Minimal | Failed write | — | 4 images generated, 0 written to disk |
| **F** Keep | Available | — | |

**Default Dual-Engine baseline average**: 8.29 (8 images)

### Merge options (M2 / M3 — M1 retired)
- **M2** Split face — Liv + Bunny both readable in one frame
- **M3** Full merge — intentional hybrid (label as hybrid)
Offer after first clean pair or on request. Output contract: one code block per image only; no pending render id lines.
