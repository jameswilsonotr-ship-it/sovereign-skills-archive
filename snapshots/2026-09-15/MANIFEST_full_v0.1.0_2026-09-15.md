# Full Skill Library Vacuum Manifest

- version: 0.1.0
- utc: 2026-09-15T20:21:00Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- run: daily full skill library vacuum + dual publish

## Snapshot

- artifact: `full_skill_library_v0.1.0_2026-09-15.tar.gz`
- size_bytes: 195883182
- size_human: 187M
- sha256: `42c9d2227d7f2ab4b762ff01c6e759577ad457651a4890e95666110f654f9882`
- member_count: 5182 (848 dirs, 4334 files)
- slug_count_unique_dirs: 40
- library_export_scanned: 27 (user-custom rich inventory; bundled extras in tarball)
- sources:
  - `/root/.grok/skills` (bundled, ~12M)
  - `/home/workdir/.grok/skills` (user custom, ~263M)
- excludes: `__pycache__`, `.git`, `node_modules`, `.DS_Store`

## Slugs (union find, 40)

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
mkdir -p /tmp/skill_restore
tar -xzf full_skill_library_v0.1.0_2026-09-15.tar.gz -C /tmp/skill_restore
# members land as skills/ (twice: bundled then user overlay order from tar -C)
```

## Core package pointer

Daily-core packages live in `artifacts/mining_packages/`.
Drive folder: `v0.1.0_2026-09-15_full-skill-library-vacuum` (`1qJsYXImp9KsYafZvJHGsYJf5cS2DqWmh`)
Parent: `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`
