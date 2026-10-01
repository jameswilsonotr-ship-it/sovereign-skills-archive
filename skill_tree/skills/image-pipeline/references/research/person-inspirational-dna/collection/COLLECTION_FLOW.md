# Collection Flow — Hybrid Direction + Output Intent (IPQ-066)

**Status**: LIVE 2026-08-13  
**Runs**: On first init of any new person under Person-to-Inspirational-DNA  
**Schema**: `schema/hybrid_direction_output_intent.schema.json`

## When this runs
Before any forensic pass or DNA stub generation for a **new** person.  
Shirley seed already exists; this flow is for the next person and for re-init if direction changes.

## Hard rules
1. **System-wide hard veto**: underage appearance only. Always recorded in `hard_vetoes`.
2. **No forced character locks**. Height, holo-ear, Olivia-quality, target-character hints are selectable, never mandatory.
3. **Heat / Gear fully exposed** to the operator during collection.
4. Answers are written to `references/research/<slug>-inspirational/INIT.json` (machine) and summarized in MANIFEST.

## Human-facing questions (skill asks these in order)

### A. Identity
1. Display name of the person?
2. Filesystem slug? (lowercase, hyphenated)
3. Optional source notes (why this person, known constraints)?

### B. Hybrid Direction
4. Primary visual era to weight heaviest?
5. Secondary eras that may contribute?
6. Optional numeric era weights (0–1)?
7. Which traits are allowed to **travel** onto other bases?
8. Which traits should be **suppressed** unless explicitly requested?
9. Any **original** (non-source) traits of the target character that must be protected?
10. Any original traits to **inject** that are not from the source?

### C. Output Intent (pick one primary)
11. Choose one:
    - `research-only` — substrate + MANIFEST only
    - `mood-board` — visual reference set for browsing
    - `m3-hybrid` — single intentional Generate-Merge hybrid figure
    - `heat-gradient` — series across Heat bands
    - `dna-lock` — lock as new roster agent DNA
    - `extension-pack` — package as true image-pipeline extension(s)
12. Optional free-text clarifying the intent?

### D. Selectable options (all optional / nullable)
13. Height override?
14. Holo ears? (true / false / null)
15. Olivia-quality pass? (true / false / null)
16. Target character hint? (`olivia` | `bunny` | `original` | null) — hint only

### E. Vetoes
17. Confirm hard veto list includes underage appearance. Add any additional vetoes.

## Machine write
After answers, write:

```json
{
  "person_slug": "...",
  "display_name": "...",
  "hybrid_direction": { ... },
  "output_intent": "m3-hybrid",
  "hard_vetoes": ["underage-appearance"],
  "selectable_options": { ... },
  "heat_gear_exposed": true,
  "schema_version": "1.0.0",
  "created_ts": "<ISO-8601>"
}
```

Validate against the JSON schema before proceeding to forensic / DNA stub steps.

## Relation to Shirley seed
Shirley folder was built manually before this flow existed.  
IPQ-067 validates the **pipeline** by applying Olivia-oriented and Bunny-oriented briefs against the existing seed without rewriting the seed.
