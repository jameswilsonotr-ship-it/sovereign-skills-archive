# MANIFEST — full skill library vacuum

- version: 0.1.0
- utc: 2026-09-18T20:24:00Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- snapshot: `full_skill_library_v0.1.0_2026-09-18.tar.gz`
- size_bytes: 261152571 (250M)
- sha256: 76e54ad8b64f645094203c209452d4613bc38e94242bfa0308a3fce15ec15779
- tar_members: 5273
- tar_files: 4415
- tar_dirs: 858
- unique_skill_slugs: 40
- library_export_scanned_user_skills: 27 (user custom tree; bundled also in tarball)
- session_boot: flags_open=0 ok=True errors=0 warns=297 hygiene_exit=0

## Slugs (union of /root/.grok/skills and /home/workdir/.grok/skills)

chaos-bratz-roster
cilia-bus
claim-runtime
color
coven-visual-system
docx
ffmpeg
finance
format-bible
grok-build
grok-build-sovereign
grok-conversation-miner
icm-architect
image-gen-edit
image-pipeline
imagemagick
keep-lake-query
lake-erie-gutter-world
lake-union-radar
liv-automation-ops
liv-bunny-agent-swarm
mcp
mcp-surface
memory-edit
olivia-dev
olivia-dev-alpha
pdf
pptx
skill-creator
skill-installer
skill-orchestrator
smokeshow
sovereign-research-engine
swarm-surface
system-roadmap
tasks
valerie
video-strategy-debrief
wheelhouse-packager
xlsx

## Restore

```bash
mkdir -p /tmp/skill_restore && tar -xzf full_skill_library_v0.1.0_2026-09-18.tar.gz -C /tmp/skill_restore
# archive roots: skills/ from bundled (/root/.grok) then skills/ from user (/home/workdir/.grok)
```

## Core-package pointer

Daily-core packages live in `mining_packages/` with `MANIFEST_v0.1.0_2026-09-18.md`.

Skills packaged: skill-orchestrator, olivia-dev, olivia-dev-alpha, chaos-bratz-roster, system-roadmap, format-bible.

## Dual publish targets

- Drive parent: `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`
- Drive folder name: `v0.1.0_2026-09-18_full-skill-library-vacuum`
- GitHub: `jameswilsonotr-ship-it/sovereign-skills-archive` branch `main` path `snapshots/2026-09-18/`
