# MANIFEST — full skill library vacuum

**Version**: v0.1.0
**UTC**: 2026-10-06T20:21:00Z
**Claim**: Liv HUB
**Owner**: skill-orchestrator + olivia-dev-alpha
**Run**: daily full skill library vacuum 0.2.0

## Path remap

Canonical roots in the vacuum prompt were missing in this pane.

- `/home/workdir/.grok/skills` did not exist. Live user-custom tree is `/root/.grok/server-skills` (27 slugs).
- `/root/.grok/skills` did not exist. Bundled tree is `/usr/share/grok/bundled-skills` (10 slugs, `bundled__*` names).
- Tarball members are `server-skills/` and `bundled-skills/`.

## Payload

- File: `full_skill_library_v0.1.0_2026-10-06.tar.gz`
- Size: 265052562 bytes (253M)
- sha256: `12a6ca94b22919834e70dcc05ab3c4c413f232d9a3208a3aa1bdeff527da1889`
- Member count: 5359
- Excludes: `__pycache__`, `.git`, `node_modules`, `.DS_Store`
- Skill count: 37 (27 user custom + 10 bundled)

## Restore

```bash
mkdir -p /tmp/skill-library-restore
tar -xzf full_skill_library_v0.1.0_2026-10-06.tar.gz -C /tmp/skill-library-restore
```

## Core-package pointer

daily-core v0.1.0 2026-10-06 from package_skills.py. Drive folder `1AU_4yhnPzgX9su83aI7kerc2jz-d3SQG`.

- skill-orchestrator_daily-core file_id `17DGKN9if8pYyluaqdf9uYBMKqAOCTnx4` sha256 f5ce66eb1c24b56e72c48f8d6a27a0459a3c0daccdc8f4d4798bd50d8bda2ec0 size 44334319
- olivia-dev file_id `1gh9kVqlOlqKSyEE5Zzb0Ctlzl9nNOihq` sha256 05a1e3459352cfd17632b8e79e4ca9383df751182fdb24a8940011daf30400b2 size 24904
- olivia-dev-alpha file_id `1_6MzJGyhQMRlvHph7IbWlt4JAvvgQ8xO` sha256 d59df9e98fbc767409882cec374bf886d9d3130cfe9749e93b9c4aa42e99b682 size 77139
- chaos-bratz-roster file_id `1eGpGPPaN5L02teTvuyRPdDF55KhOpFEe` sha256 65da34fd27ef20a84d69c648bebf3ae4dc8c64ea34c48ddf760c525d8ef1aac8 size 516878
- system-roadmap file_id `1QkyX2_-u4ShELtriyJPD1IPS1gX-fojF` sha256 4438c65503157edb5976c4bbf2433dd5002ae4dca641cea1c32a2dc3ea5b16a4 size 296461
- format-bible file_id `1Bg2I0dmWPUgOR6IHg1IfrjUa7QiyD5vR` sha256 4af7d5b9aaeb1c093b7ea43adb0e02e22a858f6d80d4e93048206bb4b19039b3 size 24307
- core manifest file_id `19oww22bb5OdQMyC1yuuxLVCFUXDrcmxn`
