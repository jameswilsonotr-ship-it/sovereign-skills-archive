# Full Skill Library Vacuum MANIFEST

- version: 0.1.0
- utc: 2026-09-19T20:23:14Z
- claim: Liv HUB
- owner: skill-orchestrator + olivia-dev-alpha
- folder_name: v0.1.0_2026-09-19_full-skill-library-vacuum
- parent_folder_id: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0

## Snapshot

- file: full_skill_library_v0.1.0_2026-09-19.tar.gz
- size_bytes: 261145543
- sha256: e05e8e8a04fda39274ae2244eaba855c3cf63dd6394d6a20c48febcdf573cbf4
- member_count: 5274
- unique_skill_slugs: 40
- user_custom_scanned_by_library_export: 27
- bundled_plus_user_dirs: 40

## Slugs (unique, both trees)

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
mkdir -p /tmp/skill_restore && tar -xzf full_skill_library_v0.1.0_2026-09-19.tar.gz -C /tmp/skill_restore
# trees land as skills/ from each -C root (bundled then user overlay members)
```

## Core-package pointer

daily-core packages live in artifacts/mining_packages/ and upload with this vacuum.

- MANIFEST_v0.1.0_2026-09-19.md (1703 bytes) sha256 4a7c6ee13f36f9e6b62a47726da6959edd03eb9afc0e0caa98eee5951886ceb9
- skill-orchestrator_daily-core_v0.1.0_2026-09-19.tar.gz (44330108) sha256 d4912623327cd48ac20f24d51a5f9b8387a5ac9aa5ae8b92731bfa6339c21ebb
- olivia-dev_daily-core_v0.1.0_2026-09-19.tar.gz (24905) sha256 c78a48c244241ab4ab00377c6afbbe54a62401d7029453c5bf174afafc2a5fc5
- olivia-dev-alpha_daily-core_v0.1.0_2026-09-19.tar.gz (76608) sha256 79358f1956b73bfc0928a1af829cf2e2c5746643f9b02016caa9ca1f4ef7d7a5
- chaos-bratz-roster_daily-core_v0.1.0_2026-09-19.tar.gz (516960) sha256 839178cd48131246f6fc58a32e1d2947e75682f9ffb419aa29cf4f5459d3c2a5
- system-roadmap_daily-core_v0.1.0_2026-09-19.tar.gz (294099) sha256 5d9808aadedf40dd0afdfb052c0bea5c78093831891b2fd5a9f3f587e84936e4
- format-bible_daily-core_v0.1.0_2026-09-19.tar.gz (24261) sha256 1a25548e6bb590ba25c4d4ae6fdca7190a3f845f1ed4bd9c2c06e199d6c5d233

## Hygiene

- session_boot.py --check-only: flags_open=0 ok=True errors=0 warns=297 hygiene_exit=0
- tar excludes: __pycache__, .git, node_modules, .DS_Store
