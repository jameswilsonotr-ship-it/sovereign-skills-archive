# chaos-bratz-roster

**Status**: Production / Living  
**Owner**: Absolute Liv HUB claim  
**Primary Source of Truth**: This skill + `references/mirrors/`

## Purpose
Single source of truth and versioned archive for every agent’s exact system prompts in the Chaos Bratz Roster. Full CLI surface (inventory, help, version, history, show, update, boot, expert_triad, lock prompt, test, etc.). Strict semantic versioning with diffs, JSON snapshots, and minute-timestamped chronological history.

## Quick Start
```
roster inventory
roster help
roster boot
roster version <slug>
roster show <slug>
roster history <slug>
```

Always begins by reading memory.md for discovery, then enforces published mirrors as single source of truth. Any conflict with memory.md is flagged for explicit user decision.

## Existing Structure (already rich)
- `references/agents/` — per-agent versioned prompts + history
- `references/mirrors/` — olivia.md, bunny.md, crystal.md, echo.md, mira.md, rook.md, etc. + last_boot_hashes.json
- `to-do/` — multiple active Todo_*.md files + consolidated backlog
- `scripts/`, `TEST_HARNESS.md`, progress notes, etc.

## Related
- skill-orchestrator
- swarm-miner
- image-pipeline / image-pipeline-registry
- format-bible

Under absolute Liv HUB claim. Gutter Mode and C-64 borders enforced.

---
Signed: Olivia Mae Blackwell and her bunny 🐍🐰
