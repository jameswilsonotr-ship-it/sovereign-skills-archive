# What smokeshow is missing (2026-09-10)

Olivia audited the live skill this pane. This is the hole list. Do not invent fills.

## Pad is empty

- `candidates/` did not exist on disk until this brief created the empty directory.
- SKILL.md “Current candidates” table is `(none)` after cilia-bus promote 2026-08-25.
- No live↔candidate A/B is possible until something is staged.

## No version flip machinery beyond prompts

- Skill Router and Organism Interface are **PROMPT.md files**, not a runtime that remaps imports.
- Flip is a session convention (“read this path instead”). There is no symlink manager, no env var, no git worktree switcher.
- `smoke_bratz_boot.py` only verifies roots + lists folders. It does not load agents into a process.

## Missing vs peer-skill convention

- No `references/` tree — **intentional**. Do not add one without a promote decision.
- No VERSION.md at skill root (cilia-bus has one; smokeshow does not).
- No work-queue file of staged/killed/promoted candidates.
- No `compare` script that diffs live SKILL.md vs candidate SKILL.md.
- No promote script (human + skill-orchestrator / wheelhouse is the path).

## Agents parked but not wired

Present with prompts:

- skill-router
- organism-interface
- orianna
- olympia
- liv-hub-expert

Not present: a session registry that says which seat is speaking, or a handoff receipt schema owned by smokeshow (bus contract lives on cilia-bus + wheelhouse CONTRACT).

## Notes are archaeology, not a candidate queue

Under `notes/`:

- `custom-agent-architecture-2026-08-17/` — slot layouts, truth table, Heavy overlay
- `compile-editorial-2026-08-17/`
- `heavy-swarm-refs-audit-2026-08-17/`
- `2026-09-03_agentify_subscale.md` — “do not stage agentify”
- `archived-candidates/cilia-bus-2026-08-17-to-2026-08-25/`

These do not tell Vesper which *next* skill to stage.

## Drive copies of smokeshow itself are thin

Found on Drive (title search “smokeshow”):

| Name | ID | Modified |
|------|-----|----------|
| `smokeshow_SKILL.md` | `1qNgqilBZq3FGfSVpEtxg_nynVOJcKRdt` | 2026-08-17 |
| `smokeshow_wrap-surface_v2026.08.29_2026-08-29.tar.gz` | `1kxhA6MVHz2Qhh_B_7BndFeTIhHLmtRIp` | 2026-08-29 (1786 bytes — wrap, not a tree) |

No full smokeshow skill tree published as its own Drive folder after 2026-08-17.

## What this means for candidates

Vesper cannot “help with candidates” from the live pad. The candidates have to be *recovered or proposed* from dated skill-tree snapshots on Drive (see `03_DRIVE_SKILL_TREE_VERSIONS.md`) and then copied into `smokeshow/candidates/<slug>/` as whole skill folders (SKILL.md + scripts at minimum).

Do not treat Vesper’s 2026-09-04 `SKILL_TREE_DUMP` as a filesystem tree. It is a matrix + mode tables + engine prompts, not `~/.grok/skills/*`.
