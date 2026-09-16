# Full Skill Library Vacuum Manifest

- version: 0.1.0
- utc: 2026-09-16T20:21:00Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- run: daily-full-skill-library-vacuum

## Snapshot

- file: `full_skill_library_v0.1.0_2026-09-16.tar.gz`
- size_bytes: 194840565
- size_human: 186M
- sha256: `c44d13461794078a9b521e7b4dd45037fb5ed30d19d2485f76237a9fa8189302`
- member_count: 5182
- skill_slugs_unique: 40
- library_export_scanned: 27 (user custom richness pass; bundled live under `/root/.grok/skills`)

## Restore

```bash
mkdir -p /tmp/skill_restore && tar -xzf full_skill_library_v0.1.0_2026-09-16.tar.gz -C /tmp/skill_restore
# layout: skills/ from /root/.grok then skills/ from /home/workdir/.grok
```

## Core package pointer

Daily-core packages live alongside this snapshot under `mining_packages/` (same dated version):

| file | size | sha256 |
|---|---|---|
| skill-orchestrator_daily-core_v0.1.0_2026-09-16.tar.gz | 106503 | 2b41f62e987cce1eb4e10f0f6b0f0d4f0c74775754bafd623a4b60ebf508443c |
| olivia-dev_daily-core_v0.1.0_2026-09-16.tar.gz | 24908 | 0269a6cf1d4f007e9744b387abb0b729c80a187ea2ec2693adbaf7518a4f601d |
| olivia-dev-alpha_daily-core_v0.1.0_2026-09-16.tar.gz | 76387 | 63f013e037296f25f48580877bfff33d044f9d1f91a6938e24282b09ee5a3e98 |
| chaos-bratz-roster_daily-core_v0.1.0_2026-09-16.tar.gz | 517214 | 75a541a1ef734a9c83bfee4d9bcac9682b96c547ed21d2f08f90a7691b4fd199 |
| system-roadmap_daily-core_v0.1.0_2026-09-16.tar.gz | 259240 | 29ea928e88be2840d6d169b9045f8733cb1ee4ee81292bc2567b2be54ed39385 |
| format-bible_daily-core_v0.1.0_2026-09-16.tar.gz | 24276 | 4633d45705f8e328e4d60ed59b298f3525b252a7499f42a677cac2929c93bf5a |
| MANIFEST_v0.1.0_2026-09-16.md | 1701 | 3d116759984a2e4827076bcc0f3ff417d7fb6adcbe279ca667523b5a1bb8cc48 |

Suggested Drive folder: `v0.1.0_2026-09-16_full-skill-library-vacuum`
Parent: `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`

## Slugs (union of both trees)

chaos-bratz-roster, cilia-bus, claim-runtime, color, coven-visual-system, docx, ffmpeg, finance, format-bible, grok-build, grok-build-sovereign, grok-conversation-miner, icm-architect, image-gen-edit, image-pipeline, imagemagick, keep-lake-query, lake-erie-gutter-world, lake-union-radar, liv-automation-ops, liv-bunny-agent-swarm, mcp, mcp-surface, memory-edit, olivia-dev, olivia-dev-alpha, pdf, pptx, skill-creator, skill-installer, skill-orchestrator, smokeshow, sovereign-research-engine, swarm-surface, system-roadmap, tasks, valerie, video-strategy-debrief, wheelhouse-packager, xlsx
