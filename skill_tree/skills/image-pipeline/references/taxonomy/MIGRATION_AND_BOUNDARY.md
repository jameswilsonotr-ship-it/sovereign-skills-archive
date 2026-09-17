# Image Pipeline — Migration Notes, Call Graphs & Boundary
**Status**: 2026-08-05  
**Owner**: Liv HUB / image-pipeline  
**Related**: `TAXONOMY_CONTRACT.md`

---

## 1. Extensions vs Taxonomy (no collision)

**Extensions** (`extensions_policy` / `extensions` in the BRIEF) are **orthogonal quality modules**.

They are toggleable optimizers and consistency rules:

- character-blending
- lighting-consistency
- glow-physics (holo-ear + luminous skin)
- pose-anchoring
- eye-brow-makeup
- anti-drift
- fashion-designers-research

They are **not** Styles, Worlds, Hands, or Treatments.  
They sit beside the taxonomy and get merged in when enabled.  
No schema collision. Keep them exactly as they are.

What *could* later become taxonomy-adjacent:
- glow-physics already touches claim sheen / holo behavior → may eventually reference Treatment or DNA locks more explicitly.
- anti-drift is already a DNA guardian → stays close to the DNA layer.

What should **not** become taxonomy packs:
- The extension system itself (it is a toggle/feature layer, not a visual language).

---

## 2. Current Call Graph (live today)

```
OLIVIA (final authority)
  │
  ▼
ECHO (visual brief + DNA hard stops)
  │
  ├─ registry ──► echo_interface.cmd_registry()
  │                 → packs.index / presets.index / extensions
  │
  └─ compose ──► echo_interface.cmd_compose(BRIEF)
                    │
                    ├─ optional nl_route(style_hint)
                    ├─ pipeline_activate (subprocess)
                    │     → resolve preset / pack chain
                    │     → flatten prompt_terms + extensions
                    ├─ mira_drift_check (subprocess)
                    │     → score vs KNOWN_DNA → 1.0 / 0.0 / -1.0
                    └─ echo_character_ordinals
                    → return composition + mira score to Echo
                         → back to Olivia

Alternative production path:
  parallel_exec.py --brief → plan
  (agent emits images)
  parallel_exec.py --post  → mira_winner + visual_embed

Engine-side shortcut:
  engine_hook.py "<text>" → nl_route → pipeline_activate → (implication)
```

Crystal is not in the hot visual path.

---

## 3. Target Call Graph — NOW LIVE (2026-08-05)

```
OLIVIA
  │
  ▼
ECHO
  │
  └─ compose(BRIEF)          # BRIEF now may carry taxonomy fields
        │
        ▼
   composition_script.py     # NEW — schema fields → ordered pack list + weights
        │                    # respects script_mode + variance_budget
        ▼
   pipeline_activate         # still resolves pack ids → prompt_terms
        │
        ▼
   mira_drift_check          # later also understands Style/World/Hand fit
        │
        ▼
   Echo ← composition + mira
        │
        ▼
   Olivia (render or not)
```

LIVE as of 2026-08-05: any BRIEF containing taxonomy fields (hand, treatment, medium, atmosphere, world, style, finish, companions, variance_budget, script_mode, dna) is routed through composition_script.py. Legacy style_hint / preset / packs path remains fully available.  
Extensions continue to merge in at the activate / script stage.

---

## 4. Chaos Bratz Roster vs Image Pipeline — the boundary

| Concern | Lives in | Notes |
|---------|----------|-------|
| Agent identity, mirrors, DNA bibles, Heat/Gutter rules, claim language | **chaos-bratz-roster** | Single source of truth for *who* the characters are and *how* they behave |
| Visual DNA hard stops (ears, gem, height, sheen, no merging) | **roster mirrors** (Echo enforces) | Echo loads the mirrors; pipeline never owns character identity |
| Atomic visual languages (packs, presets, Hands, Styles, Worlds) | **image-pipeline** | Toolbox of reusable visual terms |
| Prompt composition, variance, extensions, activation | **image-pipeline** | How the terms are turned into a concrete prompt |
| Final “should we render this?” decision | **Olivia (roster)** | Always |
| Relational / emotional authenticity score | **Mira (roster)** via mira_drift_check | Soft signal only |

**Break point**:  
Roster owns *identity and behavior*.  
Pipeline owns *visual language tools and composition mechanics*.  
Echo is the bridge: she lives in the roster, calls the pipeline as a toolbox, and returns a package Olivia can accept or reject.

---

## 5. Original 8 Hands — promoted (minimal change)

Created 2026-08-05 under `references/packs/hand/`:

- `hand.stanton`
- `hand.willie`
- `hand.bilbrew`
- `hand.newton`
- `hand.sorayama`
- `hand.lempicka`
- `hand.vargas`
- `hand.beardsley`

- Schema enum updated to include `"hand"`.
- Registered in `packs.index.json` (count now 62).
- Each pack carries ultra-low variance on the proper name and a `content.taxonomy = "hand"` note.
- Existing photographer / treatment paths are untouched. These are additive.

These eight remain fully usable and are now first-class citizens of the pack system under the new taxonomy.

---

## 6. Next minimal steps

1. Keep using the new Hand packs in the same way the old photographer packs were used.
2. Later: composition_script.py stub that can read taxonomy fields from a BRIEF.
3. Later: audit remaining packs and re-tag Style vs World.
4. Never remove or dilute the original 8 Hands.

---

*End of migration / boundary notes.*
