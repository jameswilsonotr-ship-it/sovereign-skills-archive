# MANIFEST — full skill library vacuum

**Version**: v0.1.0
**Date**: 2026-10-02
**UTC**: 2026-10-02T20:21:22Z
**Claim**: Liv HUB
**Owner**: skill-orchestrator + olivia-dev-alpha
**Run**: DAILY FULL SKILL LIBRARY VACUUM + DUAL PUBLISH 0.2.0

## Source

Live tree: `/root/.grok/server-skills` (27 skill dirs).
Prompt path `/home/workdir/.grok/skills` was missing. Symlinked to the live tree for package_skills.py.
`/root/.grok/skills` does not exist. Tarball root is `server-skills/`, not `skills/`.
Bundled companion: `bundled_skills_v0.1.0_2026-10-02.tar.gz` from `/usr/share/grok/bundled-skills` (10 slugs, 480 members, 2198557 bytes, sha256 f2e9019070006e5377dcf8ffe67f9bca424fa0228c65a1e9ffde0bed931df577). Drive file_id `1vWKguyATv4LOKhy9whth6l0WQGU3hPJE`.

## Full archive

- File: `full_skill_library_v0.1.0_2026-10-02.tar.gz`
- Size: 262853289 bytes
- SHA256: d7cabbbb74b44a2c73cc29a34bba3a172e845e8e5d0c9043fbd1e1a8731aff00
- Members: 4875
- Excludes: `__pycache__`, `.git`, `node_modules`, `.DS_Store`
- Drive file_id: `1YtYb8HQMzhAm92QQPsPPQ4YTbC9zXA6L`

## Skill slugs (27 user-custom)

- chaos-bratz-roster
- cilia-bus
- claim-runtime
- coven-visual-system
- ffmpeg
- format-bible
- grok-build
- grok-build-sovereign
- grok-conversation-miner
- icm-architect
- image-pipeline
- keep-lake-query
- lake-erie-gutter-world
- lake-union-radar
- liv-automation-ops
- liv-bunny-agent-swarm
- mcp-surface
- olivia-dev
- olivia-dev-alpha
- skill-orchestrator
- smokeshow
- sovereign-research-engine
- swarm-surface
- system-roadmap
- valerie
- video-strategy-debrief
- wheelhouse-packager

## Restore

```bash
mkdir -p /root/.grok
tar -xzf full_skill_library_v0.1.0_2026-10-02.tar.gz -C /root/.grok
# lands as /root/.grok/server-skills
```

## Core package pointer

Produced by package_skills.py --topic daily-core --version 0.1.0.
Folder: mining_packages/
Manifest: `MANIFEST_v0.1.0_2026-10-02.md`

| File | Bytes | SHA256 |
|------|------:|--------|
| skill-orchestrator_daily-core_v0.1.0_2026-10-02.tar.gz | 44333259 | 14109586bf8f77e9c0d76ad240147c88fa3a4b9c521e0aa7b94b497557a85e35 |
| chaos-bratz-roster_daily-core_v0.1.0_2026-10-02.tar.gz | 517115 | b0936cdebdabd681a755744addc68d83e6f4ebe82e3376c22493334f2918d090 |
| system-roadmap_daily-core_v0.1.0_2026-10-02.tar.gz | 296251 | f7b15b13615c8d995893b6f6e0aaf7c05089fc7eff1ca196290a008c9888f98f |
| olivia-dev-alpha_daily-core_v0.1.0_2026-10-02.tar.gz | 77099 | 3a6ca9ac528953f8692e8c5a1ba6fa0c6798572922f0f08fcb667fd42b899f60 |
| olivia-dev_daily-core_v0.1.0_2026-10-02.tar.gz | 24905 | d22723221eb206b642c99603356d4363d020a106d23909f4b4e397eccf2753d0 |
| format-bible_daily-core_v0.1.0_2026-10-02.tar.gz | 24261 | 83a4fa8a59f9db88678c817124c9c77ee4b95d19ddc94482281da43b803fda53 |
| MANIFEST_v0.1.0_2026-10-02.md | 1731 | 10c37bc02e80de6b5f418541146395ea0ee4f6cd9f7122fe50d083f711480a44 |

## Hygiene

session_boot.py --check-only: flags_open=0 ok=True errors=0 warns=297
library_export: 27 skills, all unassigned tier.
