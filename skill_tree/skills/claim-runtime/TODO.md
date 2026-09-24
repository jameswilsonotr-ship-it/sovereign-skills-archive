# TODO — claim-runtime

## Immediate
- [x] Scaffold skill + folder discipline
- [x] Mechanical fold of four source skills into references/modules/
- [x] Deprecated redirect stubs on old top-level entries
- [ ] User deletion of old top-level directories
- [ ] Inventory hygiene pass after deletion
- [ ] Optional unified status script polish

## Later
- [ ] Progressive-disclosure loader helper across modules
- [ ] Cross-module integration notes (velvet timing used by risk/vice-command, curator feeds both)

## Future rename (do not do yet)
- [ ] Rename skill **claim-runtime → claim-surface** (batch with image-pipeline → image-surface).
- [ ] Rewrite path/name references across the library when renaming.
- [ ] Update skill-orchestrator phrase_routes.md after rename.
Recorded 2026-07-24 so this survives beyond one conversation.

## 2026-07-26 — Visual entity factory (scaffold)
- [ ] **Create-entity skill (vague scaffold)** — under claim-runtime / curator surface
  - Purpose: stand up a new visual identity entity (parallel to Shauna) with correct folder tree, DNA/PROMPTS stubs, ENTITY.md wiring into image-pipeline, and Echo/Mira load path
  - Not full implementation yet — planning node only
  - Must support: canonical / baseline / hair / makeup / outfits / lighting / Looks/
  - Must register: `image-pipeline/references/entities/<name>/ENTITY.md` + curator `visual_identities/<name>/`
  - Decade/Looks grouping optional at create time
  - Distinctness rule: new entity wardrobe must not copy Olivia/Bunny/Shauna outfit slots by default
  - Owner: claim-runtime (curator module) with image-pipeline entity registry as consumer
  - Follow-on: Shauna engine completion is the first full exercise of this path
