# Full skill library vacuum — MANIFEST

- version: 0.1.0
- utc_date: 2026-09-27
- utc_built: 2026-09-27T20:20:00Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- slugs: 40
- tarball: full_skill_library_v0.1.0_2026-09-27.tar.gz
- size_bytes: 261177759
- sha256: 50622fc6915e7a1994f9c6cca666955ac7a283fcb7b0624aaa17d7f0fc2af232
- member_count: 5293
- layout: bundled/ ( /root/.grok/skills ) + user/ ( /home/workdir/.grok/skills )
- core-package pointer: artifacts/mining_packages/MANIFEST_v0.1.0_2026-09-27.md
- drive_parent: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0
- drive_folder_id: 1xvHTW5rHgpWSGo6yGFvySwDq0MSyWhln
- folder_name: v0.1.0_2026-09-27_full-skill-library-vacuum

## Slugs (unique)

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

```
mkdir -p /tmp/restore && tar -xzf full_skill_library_v0.1.0_2026-09-27.tar.gz -C /tmp/restore
# bundled -> /root/.grok/skills
# user -> /home/workdir/.grok/skills
```

## Hygiene

- excluded: __pycache__, .git, node_modules, .DS_Store
- session_boot --check-only: flags_open=0 ok=True errors=0 warns=297
