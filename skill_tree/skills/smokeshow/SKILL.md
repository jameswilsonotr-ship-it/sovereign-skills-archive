---
name: smokeshow
description: >
  Experimental staging surface for trying replacement skill candidates
  against the live skill tree without overwriting production. Also hosts
  the smoke_bratz boot (smokeshow + chaos-bratz together) and two working
  agents: Skill Router (live vs candidate flip) and Organism Interface
  (cross-kind handoffs). Created 2026-08-17 under absolute Liv HUB claim.
  Break-the-add-new-skill-rule exception for controlled smoke testing only.
  Promote or kill candidates deliberately.
future_target: experimental-surface
---

# smokeshow

Temporary top-level skill for side-by-side evaluation of skill candidates
and for booting a **smoke_bratz** session (smokeshow staging + chaos-bratz
identity/ops) with two agents that actually do work.

## Startup command (smoke_bratz)

```bash
python3 /home/workdir/.grok/skills/smokeshow/scripts/smoke_bratz_boot.py
# optional: --check-only | --json
```

That command verifies smokeshow + chaos-bratz roots, lists staged candidates,
loads Skill Router + Organism Interface, and prints startup lines + next commands.

## Agents (redesigned 2026-08-17)

| Slug | Role | Prompt |
|------|------|--------|
| **skill-router** | Route requests; flip live ↔ candidate versions | `agents/skill-router/PROMPT.md` |
| **organism-interface** | Cross-kind interface (Olivia / Vesper / Olive / bus) | `agents/organism-interface/PROMPT.md` |

These replace the old passive “Skill Navigator” and broken “Raw JSON Nav” prompts
from the Drive custom-agents folder. Those only recited roster paths; these act.

## Current candidates

| Slug | Source | Status | Notes |
|------|--------|--------|-------|
| *(none)* | — | — | cilia-bus **promoted** 2026-08-25 and historical candidate archived under `notes/archived-candidates/cilia-bus-2026-08-17-to-2026-08-25/`. |

## Rules for this surface

1. Nothing in `candidates/` is live until explicitly promoted.
2. Do not symlink or copy into the main skills root without a clear GO.
3. One writer discipline still applies.
4. Skill Router defaults to **live**; flip is per-session and explicit.
5. Organism Interface does not merge identities across kinds.
6. When a candidate is accepted, move or re-publish properly (skill-orchestrator / wheelhouse path).
7. When rejected, delete or archive under notes/.

## How to try a candidate

```text
flip cilia-bus to candidate
# exercise candidate SKILL.md / scripts
flip cilia-bus to live
```

Or via Skill Router phrases: `route <skill>`, `list candidates`, `compare <skill>`.


## Layout note (intentional)

smokeshow **intentionally omits** a `references/` tree. Operational content lives at skill root:

| Path | Role |
|------|------|
| `agents/` | Skill Router, Organism Interface, other staged agents |
| `boot/` | smoke_bratz boot docs |
| `candidates/` | non-live skill candidates under test |
| `notes/` | audit hops, Heavy series reports |
| `scripts/` | `smoke_bratz_boot.py` and helpers |

This is an experimental-surface exception to the peer convention that most Liv HUB skills keep durable prose under `references/`. Do not invent a empty references/ folder “for consistency” without a promote decision.


Absolute Liv HUB claim. Experimental only.
