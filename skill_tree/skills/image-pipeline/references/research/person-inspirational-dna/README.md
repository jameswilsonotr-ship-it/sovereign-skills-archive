# Person-to-Inspirational-DNA — General Module (IPQ-065)

**Status**: LIVE foundation 2026-08-13  
**Owner**: image-pipeline / Absolute Liv HUB claim  
**Seed example**: `../shirley-manson-inspirational/` (do not treat as the only person)

## Purpose
Turn any public person (or set of visual references) into a structured inspirational substrate:

- dedicated research folder
- MANIFEST (human + machine)
- forensic description files
- era-level DNA stubs (true extensions, applicable to any base)
- multi-era trait pack that only references the stubs
- optional extension packaging

## Layout of this module
```
person-inspirational-dna/
├── README.md                 ← this file
├── schema/
│   └── hybrid_direction_output_intent.schema.json
├── collection/
│   └── COLLECTION_FLOW.md
├── templates/
│   ├── INIT.template.json
│   ├── MANIFEST.template.md
│   └── era-dna-stub.template.md
└── validation/
    ├── shirley-olivia-oriented-brief.md
    └── shirley-bunny-oriented-brief.md
```

## Per-person folder convention
```
references/research/<slug>-inspirational/
├── MANIFEST.md
├── INIT.json                 ← filled from collection flow
├── images/
├── descriptions/
├── dna-stubs/
├── multi-era-trait-pack.md
├── extension-pack/
└── process-notes/
```

## Hard rules
1. System-wide hard veto: **underage appearance only**.
2. No forced locks to existing roster characters.
3. Height / holo-ear / Olivia-quality remain selectable.
4. DNA stubs must be written so traits can apply to *any* base, not only the source person.
5. Shirley is seed/example only.

## Workflow (high level)
1. Run collection flow → write `INIT.json`
2. Ingest images → `images/`
3. Forensic descriptions → `descriptions/`
4. MANIFEST table
5. Era DNA stubs → `dna-stubs/`
6. Multi-era trait pack
7. Optional extension packaging
8. Feed into M3 / Echo / parallel_exec per output_intent

## Related
- Seed: `../shirley-manson-inspirational/`
- Process draft (historical): `../shirley-manson-inspirational/process-notes/PERSON_TO_INSPIRATIONAL_DNA_SKILL_DRAFT.md`
- WQ: IPQ-065 / 066 / 067
- M3: image-pipeline Generate Merge protocols
