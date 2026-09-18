# Shauna — Looks

**Purpose:** Record common visual groupings (era / decade / scene packs) so ordinal plates (face, body, hair, makeup, outfit, lighting) stay consistent when we build or swap a full look.

**Rule:** A Look is not a single image. It is a named bundle that points at which canonical / hair / makeup / outfit / lighting assets belong together, and why.

**Fill order:** By decade (or era block). Add one folder per decade as we lock looks for that period.

---

## Required fields for every Look entry

Each Look file (or decade index row) must declare:

| Field | What it is |
|-------|------------|
| **look_id** | Stable slug, e.g. `2005_urban_nightclub` |
| **era / decade** | e.g. `2005`, `1990s`, `1970s`, `Y2K`, `contemporary` |
| **display_name** | Human label |
| **why** | One short paragraph: what this grouping is for and when Echo/Mira should pick it |
| **face** | Path or ordinal to face primary / alt (usually `canonical/01_face_primary`) |
| **body** | Soft body or fullbody plate used as dress base |
| **hair** | Hair target id(s) from `HAIR_TARGETS.md` / `hair/` |
| **makeup** | Makeup level or panel cell (heat 1–4 or named scheme) |
| **outfit** | Outfit target id from `OUTFIT_TARGETS` / `outfits/` |
| **lighting** | Preferred lighting plate or grid cell |
| **accessories** | Optional list (jewelry, shoes, props) |
| **notes** | Drift risks, banned combos, multi-ref tips |

Optional but preferred:
- **reference_stills** — paths to approved renders for this look
- **prompt_block** — short ready prompt or pointer into `PROMPTS_V7.md`
- **heat** — if the look is heat-scaled (low / mid / high / gutter)

---

## Folder layout (decade-ready)

```
Looks/
  README.md                 ← this file
  INDEX.md                  ← master list of all look_ids by decade
  2000s/                    ← one folder per decade as filled
  1990s/
  1970s/
  1950s/
  contemporary/
  _template.md              ← copy for new look entries
```

Decade folders stay empty until a look is locked for that era. Do not invent looks ahead of approved plates.

---

## System role

- **Echo** reads `Looks/INDEX.md` + the active look file when a scene or bible plate asks for an era pack.
- **Mira** drift-checks the chosen ordinals against the look’s declared face/body/hair/makeup/outfit set.
- Individual ordinal folders (`canonical/`, `hair/`, `makeup/`, `outfits/`, `lighting/`) remain the asset SSOT. Looks only **group and explain** them.

---

## Status

- Structure created: 2026-07-26
- Locked assets available to group: face primary, soft body front
- Multi-angle / hair(V7) / makeup panel / outfits: still pending — do not reference missing ordinals as if complete
