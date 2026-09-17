# Preset Logic Maker

**Extension id**: extension.preset-logic-maker  
**Default**: true  
**Purpose**: Documents and enables the decision process used to invent new locked-companion style presets.

## Logic rules (encoded in scripts/preset_generator.py)

1. **Character rotation** — always cycle Olivia / Bunny / Shauna (hard DNA locks required).
2. **Novelty bias** — prefer styles / media / treatments that are under-represented in the current locked set.
3. **Chrome / cyberpunk dampening** — once a chrome threshold is hit, down-weight or avoid those tags.
4. **Controlled variance** — keep `variance_budget` in 0.25–0.35 unless explicitly opened.
5. **DNA absolute** — every generated prompt must carry the full character DNA block; no exceptions.
6. **Forensic output** — every candidate emits both a BRIEF JSON block and a ready-to-render prompt skeleton.
7. **Promotion path** — trial → grade (B+ or better) → locked companion file under `presets/locked-companions/`.

## Usage

```bash
python3 scripts/preset_generator.py --count 6 --characters olivia,bunny,shauna
python3 scripts/preset_generator.py --json --avoid chrome,cyberpunk
python3 scripts/preset_generator.py --list-known
```

## Prompt terms (when extension is active)

- prefer under-used style families when inventing new locked companions
- respect DNA hard locks for Olivia, Bunny, and Shauna
- emit script-mode controlled with moderate variance_budget
- do not re-introduce saturated chrome/cyberpunk unless explicitly requested
