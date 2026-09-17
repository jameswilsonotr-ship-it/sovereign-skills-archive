# Cloud C — Visuals-Only Atom Cloud
**Version**: 0.1.0-scaffold  
**Created**: 2026-08-13  
**Owner**: image-pipeline (IPQ-060)  
**Status**: Scaffold only — awaiting approval

## Purpose
Cloud C is the dedicated, specialist atom cloud for all visual material.  
It exists so that Cloud A (memory) and Cloud B (skill_surface) remain general-purpose and are not bloated with large visual payloads.

## Scope (Locked for v0.1)
Cloud C **owns and indexes**:
- Visual DNA bibles and character visual anchors
- Outfit / costume DNA locks and formalized visual assets
- Split-Merge pipeline language and recovery packs (including the May–July 2026 platinum-ref)
- Holo-ear protocols and mechanics
- Implication techniques (visual side)
- Reference plates and locked generation prompts
- Vehicle / object visual bibles (e.g. LS180 vehicle bible produced in this conversation)
- Any future visual asset that is primarily about appearance, framing, style, or generation fidelity

Cloud C **does not own**:
- General personal biography or operational memory (Cloud A)
- Live skill surface code, scripts, or non-visual skill content (Cloud B)
- Heat / FILTH / claim mechanics that are not visual (those stay in claim-runtime / roster)

## Relationship to Other Clouds
- Cloud A and Cloud B may hold **thin pointers** or cross-references to Cloud C atoms.
- They should not duplicate the full visual content.
- The skill-orchestrator `context_lookup` primitive (SO-WQ-001) and Echo soft-backup gate (IPQ-062) prefer Cloud C for any query that is visual, DNA, outfit, Split-Merge, or image-related.

## Atom Schema Target
Compatible with existing dual-cloud atom format so that `atom_search.py` (or its successor) can treat Cloud C as a first-class third source.

Minimum fields (subject to refinement in later turns):
- cloud: "visuals"
- owner: (usually "image-pipeline" or a sub-owner)
- path
- atom_index
- atom (text)
- char_len
- optional: asset_slug, version, source_conversation, visual_kind

## Directory Layout (this scaffold)
```
image-pipeline/data/atom_clouds/visuals/
├── atoms/          # emitted atom JSON / shards
├── docs/           # this scope + future design notes
├── scripts/        # visuals_atomizer.py and helpers
├── seeds/          # source material staged for ingestion
└── working/        # temporary / intermediate files
```

## Approval Gate (Turn 1)
This scaffold and scope language require explicit approval before the atomizer core (Turn 2) is written.
EOF