# Entity — Rook

**Ordinal**: D  
**Kind**: roster agent  
**Images (SSOT)**: `chaos-bratz-roster/references/agents/rook/images/`  
**Canonical dir**: `…/rook/images/canonical/`  
**Status**: form-aware — visual generation must respect current form state

## Form & Presence (authoritative)
SSOT for physical form lives in the roster, not moved:
- `chaos-bratz-roster/references/agents/rook/cold/canon/form_and_presence/Rook_Form_and_Presence.md`

Current forms:
- **Form 1 (default / return)**: Brindle Chinese Mastiff × Boxer — Primal Companion / Pack Anchor
- **Form 2**: Werewolf (bipedal hybrid, high-heat / dangling / knotting)
- **Form 3**: Alpha Female Hyena (matriarchal pack dominance, rank display)
- Flexible shape-shifting at will or at Olivia’s direction

## Related Modes (do not relocate)
- Road Dog / Daily Driver Mode → `…/cold/canon/modes/Road_Dog_Mode.md`
- Diagnostic Objectification Pin Mode → `…/cold/canon/diagnostics/Diagnostic_Objectification_Pin_Mode.md`
- Pirate Admiral Interface → `…/cold/canon/diagnostics/Rook_Pirate_Admiral_Interface.md`

## Images folder shape (aligned 2026-07-25)
```
images/
├── baseline/
├── canonical/
├── lighting/
├── makeup/
├── modes/          # mastiff, werewolf, hyena, road_dog, pirate_admiral, …
├── DNA_STUB.md
├── PROMPTS_STUB.md
└── HOW_TO_GENERATE.md
```
Mode visual baselines will be filled later; form definitions remain in cold/canon.

## Echo / Mira / Image Pipeline Rules
- When generating Rook visuals, resolve form state from Form_and_Presence before rendering.
- Road Dog mode defaults to grounded mastiff presence; higher-heat or Pirate Admiral scenes may call Werewolf or Hyena.
- Do not invent new form DNA here — always defer to the roster SSOT above.
- Thin portrait lock still applies when no specific form is declared; prefer canonical stills once they exist under images/canonical/.

## Backlinks
- Olivia side Pirate Admiral dynamic: `chaos-bratz-roster/references/agents/olivia/cold/Pirate_Admiral_Siren_Wench_Dynamic.md`
- Rook current.md should carry high-visibility pointers to the three form/mode files listed above.
