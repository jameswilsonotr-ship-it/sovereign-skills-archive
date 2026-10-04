# MANIFEST full skill library vacuum

- version: 0.1.0
- utc: 2026-10-04T20:20:00Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- debug_note: path remap. Scripts expect /home/workdir/.grok/skills and /root/.grok/skills. Live custom tree is /root/.grok/server-skills. Symlinks staged for package_skills.py and library_export.py. Full tarball packs server-skills + bundled-skills once (not a double of the same symlink).

## Payload

- file: full_skill_library_v0.1.0_2026-10-04.tar.gz
- size_bytes: 265051787
- sha256: 88d51058fae352c680cdd5726069450b95e1c87cb723bc81d6dd42a7730b510c
- member_count: 5357
- skill_count: 37 (27 custom + 10 bundled)
- drive_file_id: 1Ri8RDdJnDWVqS-oXpA7mtZF_T0-mrZ-U

## Restore

```
tar -xzf full_skill_library_v0.1.0_2026-10-04.tar.gz -C /restore
# yields server-skills/ and bundled-skills/
```

## Core package pointer

daily-core v0.1.0_2026-10-04 under mining_packages/
skills: skill-orchestrator, olivia-dev, olivia-dev-alpha, chaos-bratz-roster, system-roadmap, format-bible
parent_folder_id: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0
folder_id: 1p8MBirRlco3oeeIinRZg0A0UfWQohFyY
