# TODO — liv-bunny-agent-swarm

**Created**: 2026-07-25  
**Status**: Active / Post-vacuum materialization

## Immediate (this session)

- [x] Create skill folder + SKILL.md
- [x] Copy four persona blocks into `references/` (water-mira, fire-echo, air-crystal, diplomat)
- [x] Validate skill structure
- [x] **Refactor and make the skill aware of the new files in the system**  
      (persona blocks now live under references/; SKILL.md explicitly declares them as the source of truth and notes the 2026-07-25 vacuum origin + possible future merger under swarm-surface)
- [ ] Decide whether this skill stays top-level or is folded under `swarm-surface` as a module (Standing Policy check — new top-level skill requires exception or ≥3:1 condensation)

## Pending / Merger Awareness

- [ ] Track any upcoming surface merger (image-pipeline → image-surface, claim-runtime → claim-surface, possible swarm-surface absorption of liv-bunny-agent-swarm)
- [ ] If folded under swarm-surface, move persona blocks into a module folder and update phrase_routes
- [ ] Add entry to system-roadmap REGISTRY / architecture target when the location is stable

## Future

- [ ] Optional: expand each persona block with more detailed heat-slider / CHAOS_RAND / voice-layer examples
- [ ] Optional: add a thin CLI or activation script that loads the four blocks in correct order
- [ ] Version the persona blocks (currently unversioned extracts from vacuum)

## Notes

- Persona blocks were extracted and published to Google Drive in the vacuum package `v1.0.0_2026-07-25_vacuum_4agent_swarm`.
- Drive folder: https://drive.google.com/drive/folders/1eRGwDbGBpA-7D7f5cA0iUUFgzGTpNtMP
- This skill currently exists as a top-level skill; Standing Policy in skill-orchestrator requires an explicit exception or condensation justification if it remains top-level long-term.
