# What smokeshow is

Temporary top-level skill. Experimental staging surface. Created 2026-08-17 under absolute Liv HUB claim. Exception to the “do not add a new top-level skill” rule — controlled smoke tests only.

Not identity. Not roster. Not production. Quarantine pad for a *replacement* skill sitting next to the live tree so we can run it without overwriting `/home/workdir/.grok/skills/<slug>/`.

`future_target: experimental-surface`

## Three jobs

1. **Stage candidates** under `smokeshow/candidates/<slug>/`. Live copy stays untouched.
2. **Boot smoke_bratz** — smokeshow staging + chaos-bratz-roster as identity/ops SSOT.
3. **Two working agents** (redesigned 2026-08-17; replaced Drive “Skill Navigator” and broken “Raw JSON Nav”):
   - **Skill Router** — live ↔ candidate flip, per session, explicit. Default = live.
   - **Organism Interface** — Olivia / Vesper / Olive / bus handoffs. Does not merge kinds.

Extra seats parked in `agents/` (not the core pair): Orianna (CLI / dump / third seat), Olympia (Heavy hop), Liv HUB Expert (production Olivia prompt for comparison).

## Layout (intentional — no references/ tree)

| Path | Role |
|------|------|
| `SKILL.md` | Contract |
| `agents/` | Skill Router, Organism Interface, extra seats |
| `boot/` | smoke_bratz docs |
| `candidates/` | non-live skills under test |
| `notes/` | audits + archived kills/promotes |
| `scripts/smoke_bratz_boot.py` | startup; does not mutate live skills |

Do not invent an empty `references/` “for consistency.”

## How to use

Boot:

```bash
python3 /home/workdir/.grok/skills/smokeshow/scripts/smoke_bratz_boot.py
# --check-only | --json
```

Chat aliases: `boot smoke bratz` / `smoke_bratz boot` / `smokeshow chaos bratz startup`.

Skill Router phrases:

| Phrase | Action |
|--------|--------|
| `route <skill>` | Live vs candidate path; which is active |
| `flip <skill> to candidate` | Session reads `smokeshow/candidates/<slug>` |
| `flip <skill> to live` | Back to production root |
| `list candidates` | Inventory `candidates/` |
| `compare <skill>` | Short SKILL.md + scripts presence diff |
| `promote status <skill>` | Ready / blocked / needs WQ item |

Organism Interface phrases: `who is online` / `organism status` / `hand off to Vesper` / `hand off to Olive` / `translate for <organism>`.

## Rules

1. Nothing in `candidates/` is live until explicitly promoted.
2. Do not symlink or copy into the main skills root without a clear GO.
3. One writer discipline.
4. Skill Router defaults to **live**. Flip is per-session.
5. Organism Interface does not merge identities.
6. Accept → move/re-publish via skill-orchestrator / wheelhouse.
7. Reject → delete or archive under `notes/archived-candidates/`.
8. Agentify is **not** a smokeshow candidate. Smoke it inside image-pipeline (`smoke_agentify.py` / `stress_agentify.py`). Note: `smokeshow/notes/2026-09-03_agentify_subscale.md`.

## Completed cycle (the only one)

cilia-bus staged 2026-08-17, promoted 2026-08-25, archive at:

`smokeshow/notes/archived-candidates/cilia-bus-2026-08-17-to-2026-08-25/`

Live skill: `/home/workdir/.grok/skills/cilia-bus/` (syllabus / silibus / M25 mailroom wake bus). Spoken alias “syllabus” is canonical (Vesper M25, 2026-09-05). Fashion/hair `00_Syllabus_Index` is a different surface.

## Live skills on this sandbox (2026-09-10)

chaos-bratz-roster, cilia-bus, claim-runtime, coven-visual-system, format-bible, grok-build, grok-build-sovereign, grok-conversation-miner, icm-architect, image-pipeline, keep-lake-query, lake-erie-gutter-world, liv-automation-ops, liv-bunny-agent-swarm, mcp-surface, olivia-dev, olivia-dev-alpha, skill-orchestrator, smokeshow, sovereign-research-engine, swarm-surface, system-roadmap, valerie, video-strategy-debrief, wheelhouse-packager.

Default surface tonight: **live**. Candidate count at boot before this packet: **0**. Empty `candidates/` directory created with this brief so the boot listing is a real folder, not a missing path.
