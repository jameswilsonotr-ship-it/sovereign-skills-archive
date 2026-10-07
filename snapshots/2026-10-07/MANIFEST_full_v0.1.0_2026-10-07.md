# MANIFEST — full skill library vacuum

**Version**: v0.1.0
**Date**: 2026-10-07
**Generated**: 2026-10-07T20:21:00Z
**Claim**: Liv HUB
**Authority**: skill-orchestrator + olivia-dev-alpha
**Run**: daily full skill library vacuum 0.2.0

## Counts

- User custom skills: 27 (`/root/.grok/server-skills`)
- Bundled skills: 10 (`/usr/share/grok/bundled-skills`)
- Archive members: 5361
- Core package pointer: `mining_packages/MANIFEST_v0.1.0_2026-10-07.md`

## Full archive

- File: `full_skill_library_v0.1.0_2026-10-07.tar.gz`
- Size: 265053571 bytes (253M)
- sha256: `a0f7b4858110c93f29281cbd5d32c9e32f3478b656a842bcbc8adc3f933e45c7`
- Top prefixes: `server-skills/`, `bundled-skills/`
- Excludes: `__pycache__`, `.git`, `node_modules`, `.DS_Store`
- Drive file_id: `1VRndwisdslsV8K81DeFib33W45LgS-uL`

## Path delta

Requested tar was `-C /root/.grok skills -C /home/workdir/.grok skills`.
`/root/.grok/skills` does not exist. `/home/workdir/.grok/skills` is a symlink to `/root/.grok/server-skills`.
Packing both would double the same tree. Archive uses the real trees once each.

## User custom slugs

chaos-bratz-roster, cilia-bus, claim-runtime, coven-visual-system, ffmpeg, format-bible, grok-build, grok-build-sovereign, grok-conversation-miner, icm-architect, image-pipeline, keep-lake-query, lake-erie-gutter-world, lake-union-radar, liv-automation-ops, liv-bunny-agent-swarm, mcp-surface, olivia-dev, olivia-dev-alpha, skill-orchestrator, smokeshow, sovereign-research-engine, swarm-surface, system-roadmap, valerie, video-strategy-debrief, wheelhouse-packager

## Bundled slugs

bundled__docx, bundled__ffmpeg, bundled__imagemagick, bundled__memory-edit, bundled__pdf, bundled__postmortem, bundled__pptx, bundled__skill-creator, bundled__skill-graphs, bundled__xlsx

## Core packages (daily-core v0.1.0)

| File | Bytes | sha256 | Drive file_id |
|---|---:|---|---|
| skill-orchestrator_daily-core_v0.1.0_2026-10-07.tar.gz | 44334664 | 2ab03f780119fcd805062a48919e440f0386443830b83e38d3aeb0a67c7ee241 | 1WnT5-sr6M2mOIwlRcIWhauS6Y_4djV1i |
| chaos-bratz-roster_daily-core_v0.1.0_2026-10-07.tar.gz | 517481 | 2293322834e8f20433cdfe7d28f016d27a55a5fd39fb1a745a8f7d01ec84e0f3 | 141rb1zuowfYhBQLV-Z2qVn3hb2bOIJ4i |
| system-roadmap_daily-core_v0.1.0_2026-10-07.tar.gz | 296386 | 1b0032fc31138839ad7c4390fcab85555609925f948a330c5f75cc47536e4942 | 1kFYuJeTuw2xHvtTDWfj-RYIAq3g5FYWn |
| olivia-dev-alpha_daily-core_v0.1.0_2026-10-07.tar.gz | 77160 | 35c3be86bd935605c1e7ad14b5aed6028e288d952235c0900e59033418f8e629 | 1jx2FsC1ISVPjeQSZeIDty-TcJm9W-Vqr |
| format-bible_daily-core_v0.1.0_2026-10-07.tar.gz | 24290 | 216409e2612481e746a5cd1e7526ac2e46c74d93ddf5934ec62ff8b1e042bb12 | 10iwnTXF7qM9BFWYqlaj5b6YqUYgulAoT |
| olivia-dev_daily-core_v0.1.0_2026-10-07.tar.gz | 24908 | 2367a4d0ddd77a3a6667be23bdd28f050bae193e56576f7093787d4066d77d61 | 1XYP-kAgk2JYYq5c0Er_iU4--b3EZv30b |
| MANIFEST_v0.1.0_2026-10-07.md | 1703 | c0f7523f8c4f7d6005559dd3d0de133267acbe52eb696ff1f529c145325e1a92 | 1T7OULuyPN5p6ASa5iFZmq-NttITpJsvU |

## Restore

```bash
mkdir -p /tmp/skill-restore && cd /tmp/skill-restore
tar -xzf full_skill_library_v0.1.0_2026-10-07.tar.gz
# server-skills/ -> user custom
# bundled-skills/ -> bundled
```

## Hygiene

session_boot --check-only: flags_open=0 ok=True errors=0 warns=297
Tier map empty. All 27 user skills unassigned. Richness rich except sovereign-research-engine (thin).
