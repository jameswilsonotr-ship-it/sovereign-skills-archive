# Image Pipeline — Pack Selection Menu (Shared)

**Status**: Live 2026-07-25 (IPQ-024 multi-turn)  
**Used by**: generate-engine + overlay-engine  
**Purpose**: A–E stay visible; pack picks use **numbers**; selection applies to the **last render set**.

---

## Primary Menu Layout (both engines)

Always show this table. **A–E remain the left columns even when a pack category is open.**

| Option | Status | Avg Score | Notes | Pack Category | Count | Range |
|--------|--------|-----------|-------|---------------|-------|-------|
| **A** Formulation / DNA pair | | | | atmosphere | n | 1–n |
| **B** CSP | | | | medium | n | 1–n |
| **C** Heat gradient | | | | photographer | n | 1–n |
| **D** Angle expansion | | | | treatment | n | 1–n |
| **E** Minimal | | | | pose | n | 1–n |
| | | | | **implication** | n | 1–n |
| **Return / Back** | | | | | | |

---

## Multi-turn pack selection (IPQ-024)

### Turn 1 — open a category (no render)
User: `implication` / `photographer` / `pick treatment`

Response must:
1. Keep the **primary A–E table** visible.
2. Below it, show the category list with **numbers only**:

```
Implication techniques (12) — pick a number (no render yet)

 1. Beardsley High-Contrast Ink + Negative Space
 2. Crepax Cinematic Gutter Inference
 …
12. Metaphorical Object Proxying

[Return] back to primary menu only
```

### Turn 2 — pick the number (applies to last render set)
User: `3` or `pack 3`

- Resolve number → pack id in the open category.
- **Apply that pack to the existing last set of renders** (re-prompt / re-render each slot in the last default-six or last option batch with pack terms merged).
- If no last set: say so and offer E Minimal or default-six first.
- Emit scores + forensics (IPQ-019/022) on the new results.

### Return
`return` / `back` / `menu` closes the sub-list; primary table only.

---

## Integration Contract

1. Always surface combined table (A–E left + pack categories).
2. A–E → existing dual-engine paths.
3. Pack category → numbered sub-list, A–E still shown, no image.
4. Number select → apply to **last render set**.
5. Scoring + forensics after those re-renders.

Runtime: `scripts/pack_menu.py`  
Registry: `references/registry/packs.index.json`
