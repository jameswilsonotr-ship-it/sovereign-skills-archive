# TODO — image-pipeline

**Version**: 1.2.0-dev  
**Last updated**: 2026-08-07 18:47 EDT  
**Work queue**: `references/work-queue/WORK_QUEUE.md` (authoritative for open/done IDs)

## Done this session (IPQ-001 … IPQ-009)

- [x] Implication pack kind + 12 technique packs + versioned assets
- [x] active_implication_index + implication_inject
- [x] packs.index.json registration (43 packs)
- [x] Combined A–E + pack category menu (both engines)
- [x] Mira drift check (1.0 / 0.0 / -1.0) on echo compose
- [x] Echo character ordinals (A=Olivia, B=Bunny, …) + DNA injection lists
- [x] render_engine.py (pass-through + moderation → implication)
- [x] analyze_render.py (Mira-first → Echo → Olivia QC)
- [x] Local work queue + HANDOFF_STATUS

## Open (from work queue)

- [ ] **IPQ-010** Wire real Grok Imagine calls into render_engine (or explicit handoff to generate/overlay) — **no pictures until this lands**
- [ ] **IPQ-011** Real post-render vision / file / error-code inspection in analyze_render
- [ ] **IPQ-012** Force Olivia image intent through Echo at orchestration / boot level
- [ ] **IPQ-013** Persistent character reference images under ordinal visual DNA paths
- [ ] **IPQ-014** Link carousel / bordered / code output styles to pack system
- [ ] **IPQ-015** Engine-side moderation scale-back → implication packs (generate + overlay)
- [ ] **IPQ-016** Scored Heat → implication strength mapping
- [ ] **IPQ-017** Expand Mira DNA anchors beyond Liv/Bunny

## Deferred

- [ ] IPQ-020 Full mandatory Echo→Pipeline→Mira→Olivia routing in Olivia boot (roster track)
- [ ] IPQ-021 Real carousel / bordered / code-only emitters (depends on IPQ-010)

## Earlier done (1.1.0)

- [x] Pack + preset schemas, indexes, validate_schema.py
- [x] Bunny / Liv / Valerie Top 10 → presets
- [x] Named styles → packs + presets
- [x] Extensions registry + toggles
- [x] pipeline_activate / engine_hook / nl_route / chain_engine
- [x] test_activation + ci_check + engine call-site harnesses
- [x] echo_interface.py (registry + compose)
- [x] Wired into chaos-bratz-roster (Echo + Olivia)

## Open — Taxonomy & Schema (2026-08-05)

- [ ] Audit all existing packs against TAXONOMY_CONTRACT.md terms (Style vs World, Hand vs Treatment vs Finish)
- [ ] Re-tag any current `kind=genre` packs as Style or World
- [ ] Draft per-image schema object from the fields in section 2 of the contract
- [ ] Design first composition script stub that consumes the schema and emits ordered prompt terms
- [ ] Move successful original-8 Hands into permanent Hand registry entries if not already present
- [ ] Define first locked companion sets from the successful DNA-respecting renders (chrome, Vallejo, Caravaggio, blueprint, Mucha, etc.)

## Closed 2026-08-05 (taxonomy phase)

- [x] Wire composition_script into echo_interface.cmd_compose (live path)
- [x] Promote original 8 Hands to kind=hand packs
- [x] Create locked companion presets from proven combinations
- [x] Add taxonomy-aware-companions + style-world-audit-hints extensions
- [x] First Style-vs-World audit pass document
- [x] Target call graph is now the live path
- [ ] Full Style-vs-World re-tag of every pack (deferred — first pass only)
- [ ] Phase 2 history/art research (intentionally skipped for now)

## Closed 2026-08-05 (visual bank + generator)

- [x] Promote all session-generated style trials to locked companions (36)
- [x] Write preset_generator.py (logic maker)
- [x] Write extension.preset-logic-maker
- [x] Rebuild presets.index.json
- [ ] Style-vs-World full re-tag (next phase)

---

## 2026-08-07 18:47 EDT — Stress-Test Session Results + Agility Recommendations

**Source**: Live image-pipeline stress / smoke test (outfit DNA + character DNA + filters + implications + Crystal/Echo styles).  
**Session focus**: Cold-shoulder denim-mini fidelity lock → multi-style application → implication packs → Crystal/Echo DNA stubs → full system review.

### Four Agility / Robustness Recommendations (from session analysis)

1. **Close the render loop (IPQ-010 + lightweight IPQ-011)**  
   Wire real Grok Imagine calls into `render_engine` so `parallel_exec --brief` both plans *and* produces images, then immediately runs fidelity + visual_embed scoring. Removes manual multi-generate calls.

2. **Persistent visual DNA anchors (IPQ-013)**  
   Store high-fidelity reference plates per character and per major outfit DNA under ordinal paths. Enables automatic visual-match grading instead of prompt-text-only DNA lock.

3. **Unified vocabulary surface for the agent**  
   Single fast interface (`pipeline_vocab.py` or equivalent) that returns: characters, outfit DNAs, implications, mediums/treatments, Heat Response bands, last N scored renders. Lets the agent think in the full vocabulary without rediscovery.

4. **Agent-side self-grading + pivot loop**  
   Post-render step that runs existing scores, decides keep / soft-reroll (different implication) / hard-reroll (different medium), and can auto-queue a second pass. Turns one-shot explosions into a steerable iterative instrument.

These four are now tracked as work-queue items (see WORK_QUEUE.md and supporting protocol files).

### Stress-Test / Smoke-Test Results (2026-08-07)

**What worked**
- Outfit DNA extraction and fidelity lock (cold-shoulder + denim mini + bag + green keychain + multi-buckle boots + daisy) held across dozens of regenerations.
- Character DNA (Liv / Bunny) + Heat 5 makeup rules applied cleanly.
- Style / treatment / medium packs (glossy-iridescent, Helmut-Newton, dark-noir, watercolor, charcoal, pop-art, Art Deco, surreal fragment, ink-splatter) produced distinct, usable results.
- Implication packs (Manara posture tension, Extreme Tenebrism, Crepax gutter inference, Shunga fabric-proxy) successfully moved charge into posture / shadow / gutter / fabric without breaking the outfit lock.
- Crystal geometric-gothic and Echo high-fidelity observational stubs were applied productively even though full visual styles are still thin.
- Parallel multi-generate workflow (8–16 images per turn) was stable from the agent side.

**What did not work / was shaky**
- No closed render loop: every image still required manual native `render_generated_image` calls instead of pipeline-driven generation.
- No automatic post-render scoring or winner selection during the session (analyze_render / mira_winner not invoked live).
- Persistent visual DNA anchors do not exist yet → fidelity relied entirely on prompt engineering.
- Crystal / Echo “styles” are still mostly role + motif stubs, not full locked visual systems.
- Capri / cutoff-yoga-pants series remains temporary; test incomplete (explicitly left open for later pivot).

**How we tested (candidate for automation)**
1. Lock a single real-world reference photo as outfit DNA source.
2. Force exact accessory and construction details (bag, keychain, boot buckles, daisy, visible under-strap).
3. Apply character DNA filters (Liv then Bunny).
4. Layer style / treatment / medium packs one at a time.
5. Layer implication packs on the strongest photoreal bases.
6. Introduce secondary agent DNA stubs (Crystal, Echo).
7. Human (and agent) visual QC on fidelity, drift, and aesthetic success.
8. Document keepers vs. failures in conversation.

This sequence can be turned into a repeatable test harness script later (see IPQ-050 below).

**Interaction pattern that worked**
- User supplies or points at a real photo → agent inspects it directly → forces details into prompt → generates → user scores → agent tightens fidelity or applies next pack. Tight feedback loop, high signal.

**Temporary note**
Blue/green cutoff yoga pants (Capri) series is still open. Test not complete. Will be revisited after the agility items are queued.


---

## 2026-08-07 19:03 EDT — Twister (IPQ-054) Scaffolding

**New capability stub**: Twister — attribute-level edit layer.

Goal: change one (or more) named visual attributes on a locked base without destroying character identity, pose, silhouette, or supporting garments. Pure pixel identity is explicitly out of scope; “same girl, same pose, same overall look — only X changed” is the success bar.

Four realization paths recorded and kept live. Preferred hybrid = component library + two-stage pipeline.

First executable steps:
1. Inventory all retained Capri / cutoff-yoga artifacts
2. Consolidate the 16 corrected prompts into component-candidate list
3. Correct any mis-mapping of the original uploaded reference photos
4. Define first named Twister attributes from the Capri series
5. Design minimal scoring rubric

Full protocol: `references/work-queue/protocols/IPQ-054_twister_attribute_edit.md`  
Work-queue row: IPQ-054 (high)

Capri series remains the primary experimental surface (IPQ-053 still open).
