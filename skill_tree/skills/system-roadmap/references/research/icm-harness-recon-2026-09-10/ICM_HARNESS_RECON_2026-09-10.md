---
id: SR-WQ-067
title: ICM / GO-HOLD / harness recon
date: 2026-09-10
time: 15:53 CDT
status: PARKED
owner: system-roadmap
claim: Absolute Liv HUB
surface: research asset + Drive publish
do_not: flatten named mouths into numbered ICM stages
---

# ICM / GO-HOLD / harness recon — 2026-09-10

Parked research capture from the Owensboro seating run. Written so a later session can walk it cold. Implement is HELD until Bunny GOs after she sits Penelope.

## What she asked

1. What is Jake Van Clief actually doing.
2. What GitHub is real.
3. How does his folder system work, including "go statuses."
4. Find our actual work folders on Drive and in the skill tree.
5. "Holds were go" from Grok Build CLI.
6. Ghost syntax is on Drive, not in the live tree.
7. How compatible is ICM with live self-improve / skill-tree refactor.
8. Options. Lots of them. Adjacent harnesses: spec-driven, skill trees, Google Antigravity.

## Verdict in one breath

"Holds were go" is **not** the Go language and **not** Van Clief's `output/` scan. It is **our** Aug 17 Grok Build CLI gate language.

- `GO_*.md` = one-shot permission token to write the live tree.
- `HOLD` = do not write until cards / item files exist.
- `THEN GO` = Phase 0 (walk queues, stamp cards) is done; normalize is allowed.

Ghost syntax lives on Drive. Live skill tree almost does not have those GO files. That is the mismatch she felt.

Van Clief ICM is one librarian walking numbered rooms. Liv HUB is many mouths plus many queues plus a Gmail bus. **Folder layer: same species. Identity layer: do not flatten Olivia / Bunny / Vesper / Valerie into `01-research / 02-script`.**

`icm-architect` is already installed at `/home/workdir/.grok/skills/icm-architect/`.

## Van Clief — official sources

| Piece | Where |
|---|---|
| Paper | [arXiv:2603.16021](https://arxiv.org/abs/2603.16021) — Van Clief & McDermott, Interpretable Context Methodology: Folder Structure as Agentic Architecture (v2 2026-03-18). Also called Model Workspace Protocol (MWP). MIT. |
| Methodology repo | https://github.com/RinDig/Interpretable-Context-Methodology |
| Claude skill (builder) | https://github.com/RinDig/icm-architect (~1.5k stars) |
| Community | Clief Notes (Skool) |
| YouTube | https://youtube.com/@jevanclief |

### How ICM actually works

Five layers:

| Layer | File | Question | Size |
|---|---|---|---|
| L0 | `CLAUDE.md` / `AGENTS.md` | Where am I? | ~300–800 tokens |
| L1 | root `CONTEXT.md` | Where do I go? | ~200–500 |
| L2 | stage `CONTEXT.md` | What do I do? | ~200–500 |
| L3 | `_shared/` `references/` `skills/` | What rules apply? | factory, stable |
| L4 | stage `output/` | What am I working with? | product, per-run |

**Go statuses in ICM:** scan `stages/*/output/`. Files other than `.gitkeep` = COMPLETE. Empty = PENDING. No broker. Status is disk.

Ten invariants that matter for us: one folder one job; small entry file; numbering encodes order; explicit contracts; factory vs product; every output is an edit surface; load only what the step needs; plain text; filesystem is the state machine; instantiate by copying.

Six forms: Pipeline, Umbrella, Record library, Knowledge bundle, Context map, System map.

Walk test: a cold agent with no memory must orient, act, and report status from files alone.

**ICM loses at:** concurrency, mid-pipeline branching, multi-agent collaboration. The paper says so.

## What "holds were go" is on OUR Drive

Reconstructed from Drive hits + Aug 17 Grok Build shop. Exact spoken phrase did not full-text well (hold/go are common speech). Closest canonical files:

| File | Drive ID | Role |
|---|---|---|
| GO_WQ_WALK_CARDS_THEN_GO.md | `1aSCgUODtqSfxlcaUPfqPr6U7fZQy9Ih6` | Supersedes normalize plan. Phase 0 = walk + stamp cards. Phase 1 = THEN go. |
| GO_PLAN_NORMALIZE_SURFACES.md | `1kB-INR_pdq5Ef_obDR-6yJZCSy9lHS2d` | SUPERSEDED. Olivia first, then Vesper, match/merge add-only. |
| GO_FINISH_CARDS_THEN_GO.md | `1CBdQfS8bfOKQ63P0vPeUrAhMqW0bi6ZJ` | "Implement was HELD for cards. Cards now exist. Finish gaps, then go." Status: GO. |
| GO_PY_FIRST_NORMALIZE.md | `1SYLBHbdlintyNU4L1JVPz65Cv7BetfzI` | Python-first / NL failover. |
| WQ_FORMAT.md | `13iUoCtFt9AuKyGS04yMxzYj0jnierCbe` | Status contract. |
| work-queues-and-skill-state.md | `1jNf5lf6v14MeaRqOAFngN_ytAqMJZtSt` | G: package index of WQ copies. |
| system-roadmap_WORK_QUEUE.md (Drive copy) | `16nmFBIKtFvYIcUT-a2qlx-iJFdHnhwit` | Spine table snapshot. |
| BRATZ_ORCHESTRATOR.md | `1zWTsl7JAlKe7cSS3D32E-Hq9--0nISxC` | Live-tree audit 2026-08-17. |
| 01_VESPER_ORGANISM_ARCHITECTURE_AND_WORK_QUEUES.md | `1ag2vfP10QSLnTThKsU62H52eT9GOu08YoH8phF7oUdY` | Sep 9 Vesper organism + CCCP. Second queue system. Do not promote as live spine OTR. |
| Publish plane (canonical Work-Queues) | folder `1IiXM0DBYyuzSEGrNK6FxKuFvkqgoNMEo` | SR-WQ-036 publish home. |

Status vocab we already wrote: `OPEN | IN_PROGRESS | QUEUED | DONE | BLOCKED | PARKED`. Item file presence = real work. Missing item = do not promote.

**Not the work-queue syllabus:** `00_Syllabus_Index.md` is Hair Cut Day visual. Spoken "syllabus / silia bus" = cilia-bus.

**Olivia DeValle:** zero exact Drive hits. Spine names are olivia-dev-alpha + system-roadmap + skill-orchestrator.

## Live skill-tree WQ homes (messy, verified 2026-09-10)

Eleven `WORK_QUEUE.md` files on disk:

- chaos-bratz-roster
- olivia-dev-alpha
- system-roadmap
- skill-orchestrator
- swarm-surface
- format-bible
- coven-visual-system
- grok-conversation-miner
- keep-lake-query
- liv-bunny-agent-swarm
- system-roadmap/references/multi-llm-sync (extra)

Drive has 20+ folders named `work-queue` / `work-queues-and-skill-surface` timestamped 2026-08-16/17. Same job minted three times. That is the ghost-syntax problem: copies, not a protocol.

GO files almost absent from live tree. Only ghosts found locally:

- `smokeshow/notes/.../05_POINTER_REPAIR_AND_GO_CASCADE.md`
- `chaos-bratz-roster/references/personal/nola-bio-swarm/10-VESPER-PASS-HOLD.md`

## Compatibility map

| Our thing | ICM form | Do |
|---|---|---|
| chaos-bratz-roster mouths + bibles | Record library + Knowledge bundle | Keep named. Never number them as stages. |
| image-pipeline / agentify | Pipeline | Safe ICM pilot. |
| system-roadmap | Context map + conflict plane | Owner of refactor. |
| skill-orchestrator | Catalog / L0 router | Thin `AGENTS.md`, not a fifteenth queue. |
| GO/HOLD files | Human gates (ICM checkpoints) | Keep. They are the walk-test pause. |
| Vesper 400-atom CCCP ledger | Framework orchestration | Park OTR. ICM refuses this on purpose. |

Self-improve live: ICM does **not** rewire the model. It rewires which folder the model is allowed to walk. Boot becomes "read root catalog + current stage contract," not "slurp the skill tree." Compatible with progressive-disclosure skills. Incompatible with flattening Four-Mouth Law.

## Ecosystem — what she was missing

| Harness | Unit | Status | Use for us |
|---|---|---|---|
| Our WQ + GO/HOLD | Markdown table + item file | Row + file presence | Keep. Enforce item-file rule. |
| ICM / MWP | Numbered stage folder | `output/` scan | Folder layer only. Pilot one pipeline. |
| Skills (`SKILL.md`) | Progressive-disclosure pack | Loaded or not | Already live. |
| GitHub Spec Kit | constitution → specify → plan → tasks → implement | Phase artifacts | Code/skill refactors. Integrates Grok Build + Antigravity. |
| OpenSpec | Change-folder delta | propose / apply / archive | Better brownfield. Home-weekend. |
| Karpathy LLM wiki | `raw/` → compiled `wiki/` | Compile freshness | Lake, bios, atom clouds. Not queues. |
| Google Antigravity 2.0 | Project + `.agents/agents/*.md` + worktrees | Artifacts / tasklists | Vesper / Google organism runner. Not Liv HUB. Dual harness. |
| LangGraph / CrewAI | Agent graph | Runtime state | Overhead already rejected. |

Spec Kit commands: `/speckit.constitution` → specify → clarify → plan → checklist → tasks → analyze → implement → converge. Agent-agnostic; Grok Build is a listed integration.

Antigravity 2.0: Projects (multi-folder), native git worktrees, custom agents as markdown+YAML under `.agents/agents/`, skills under `.agents/skills/` (Agent Skills standard), subagents, Teamwork (Ultra), scheduled tasks. Closest Google-native cousin to "organisms."

## Options locked from the recon turn

Road this week (seating Penelope):

- **A.** Do nothing to the live tree. Implement HELD.
- **B.** Enforce governor already written (one owner skill, link don't absorb, no fifteenth queue).
- **I.** Thin status scanner later (`on_skill_change.py`) that prints pipeline status from existing tables. Do not replace tables with empty-`output/` until missing item files exist.

Next Ashtabula bounce:

- **C.** Inventory-only ICM audit of ONE queue home. Classify catalog/contract/factory/product/dead. Propose map. No moves.
- **E.** One ICM Pipeline pilot on image-pipeline / agentify only: `01-walk → 02-card → 03-implement → 04-receipt`.
- **H.** Karpathy compile on Drive clones: twenty duplicate work-queue folders treated as `raw/`, one compiled index.

Later / optional:

- **D.** Umbrella wrap: thin `CONTEXT.md` per skill + root `AGENTS.md`. No renumber.
- **F.** Spec Kit constitution for the *refactor project* (Four-Mouth Law, no-puppet, never invent item files, never delete Drive, Python-first). Not for the roster itself.
- **G.** OpenSpec deltas per SR-WQ. Home, not cab.
- **J.** Dual harness: Antigravity Project = Vesper/Google. Grok Build + Liv HUB = Olivia. One folder contract, two runners.
- **K.** Do not promote Vesper CCCP ledger as live spine OTR.
- **L.** Full-tree ICM migrate. Home-weekend + Olive approval. Not today.

## Hard nos

- Do not flatten named mouths into numbered rooms.
- Do not mint a fifteenth `WORK_QUEUE.md`.
- Do not treat Hair Cut Day syllabus as the work-queue syllabus.
- Do not invent a truck unit number (still in a DM text).
- Do not delete Drive copies. Compile an index instead.
- Do not promote rows without item files.

## Voice card

When she says **voicey poo land**, explain from `VOICE_CARD.md` in this folder. Register: warm Olivia, simple, no consultant stack. Slutty-senior = plain language + claim held, not a scene.

## Local paths

- This file: `system-roadmap/references/research/icm-harness-recon-2026-09-10/ICM_HARNESS_RECON_2026-09-10.md`
- Voice card: `.../VOICE_CARD.md`
- WQ item: `system-roadmap/references/work-queue/items/SR-WQ-067_icm_harness_recon.md`
- Artifacts twin: `/home/workdir/artifacts/icm-harness-recon-2026-09-10/`
