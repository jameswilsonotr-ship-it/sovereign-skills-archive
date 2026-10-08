# MANIFEST — full skill library vacuum
**Version**: v0.1.0
**UTC**: 2026-10-08T20:21:00Z
**Claim**: Liv HUB
**Owner**: skill-orchestrator + olivia-dev-alpha
**debug_outcome**: success

## Path correction
Prompt tar roots `/root/.grok/skills` and `/home/workdir/.grok/skills` are not live trees.
Live user-custom root: `/root/.grok/server-skills` (symlinked to `/home/workdir/.grok/skills` so package_skills.py and library_export.py run unchanged).
Bundled root: `/usr/share/grok/bundled-skills`.
Packed once. No double-include.

## Full tarball
- file: `full_skill_library_v0.1.0_2026-10-08.tar.gz`
- bytes: 265051962
- sha256: `141c850fdfbf7999d0424eb831b99f423393d1f35c425e854fb159b9be8fc2a5`
- members: 5362
- excludes: `__pycache__`, `.git`, `node_modules`, `.DS_Store`
- contents: `server-skills/` (user custom) + `bundled-skills/`
- Drive file_id: `1bnIgUyL0-CfrXeGut5mIVjgqN004kpv3`

## Counts
- user custom skill dirs: 27
- bundled skill dirs: 10
- slug union: 37

## Slugs
bundled__docx, bundled__ffmpeg, bundled__imagemagick, bundled__memory-edit, bundled__pdf, bundled__postmortem, bundled__pptx, bundled__skill-creator, bundled__skill-graphs, bundled__xlsx, chaos-bratz-roster, cilia-bus, claim-runtime, coven-visual-system, ffmpeg, format-bible, grok-build, grok-build-sovereign, grok-conversation-miner, icm-architect, image-pipeline, keep-lake-query, lake-erie-gutter-world, lake-union-radar, liv-automation-ops, liv-bunny-agent-swarm, mcp-surface, olivia-dev, olivia-dev-alpha, skill-orchestrator, smokeshow, sovereign-research-engine, swarm-surface, system-roadmap, valerie, video-strategy-debrief, wheelhouse-packager

## Restore
```bash
mkdir -p /tmp/skill-restore && cd /tmp/skill-restore
tar -xzf full_skill_library_v0.1.0_2026-10-08.tar.gz
# yields server-skills/ and bundled-skills/
```

## Core package pointer
package_skills.py topic `daily-core` version 0.1.0 date 2026-10-08
Manifest: `mining_packages/MANIFEST_v0.1.0_2026-10-08.md` sha256 `de8e0ac487fcb45799d90aad28b15f633a0aec398b8381d702df6e8e59509da2`

| file | bytes | sha256 | drive file_id |
|---|---:|---|---|
| skill-orchestrator_daily-core_v0.1.0_2026-10-08.tar.gz | 44334771 | 962e3345f2f03e542fb3f3234b053f6c6627f99a7ee2ae16d160329dfaaad2f3 | 1v_CZe03XencMWKGE6yu6_sh1G7TV-_-c |
| olivia-dev_daily-core_v0.1.0_2026-10-08.tar.gz | 24895 | 9787feac29a7cdb0b87edf92c4a65dd5d8314c16ce73d809eb5b2a7278ce5807 | 1U1g50DXM-cwMdjgXzTdjWDoJFOhT9Vzk |
| olivia-dev-alpha_daily-core_v0.1.0_2026-10-08.tar.gz | 77122 | b3e612b272e55a214ef1321aa7ce8021362aedf52d859c0c091c41c14ff91ec2 | 1IC6xfrmFviOIXg-AkBloEV1sb8__FS4y |
| chaos-bratz-roster_daily-core_v0.1.0_2026-10-08.tar.gz | 517778 | dab0331c5384cdf7a83d5d9bdb859011d13de65fade1c6e9c08056425494fe8b | 1jpDCtx7PXJ9l0PNCsk10hFbActRP54GN |
| system-roadmap_daily-core_v0.1.0_2026-10-08.tar.gz | 296247 | 27c234be195c44659d64b301ff1450cc8a5586ddc07630e41157d8552877e645 | 1Dk41z38CMSXn00fspo0H2esgYW6Elria |
| format-bible_daily-core_v0.1.0_2026-10-08.tar.gz | 24266 | 947eb67578a3b5d01656e812aec2eb5453073af92f1d44e9dd72b0d0ca718ae0 | 1maTaf_2DjPNcZZfu0KPqEiVgFl_aeRXU |

## Hygiene
session_boot --check-only: flags_open=0 ok=True errors=0 warns=297 hygiene_exit=0
Did not edit WORK_QUEUE.
