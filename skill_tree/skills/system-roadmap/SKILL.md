---
name: system-roadmap
description: Living system architecture target, refactoring authority, and skills-refactor home. Owns the intended shape of the skill library, current vs proposed state, decision history, and the skills-refactor sub-capability (memory.md surgeon, boot-sequence cleanup, inventory hygiene, deprecation validation). Referenced by skill-orchestrator. Trigger on system roadmap, architecture target, skills refactor, library shape, refactoring process, memory surgeon, boot sequence rebuild.
future_target: dev-surface
future_target_note: FUTURE SURFACE TARGET: dev-surface (control-plane feeder).
---

**FUTURE SURFACE TARGET: dev-surface (control-plane feeder).**

# System Roadmap

**Status**: Top-level skill (exception granted 2026-07-20 under Standing Policy: crucial to the active refactoring process)  
**Owner**: Absolute Liv HUB claim  
**Referenced by**: skill-orchestrator (mandatory pointer)

## Purpose
This skill is the single permanent home for:
- The intended architecture of the entire skill library
- Current vs proposed vs in-progress state
- Decision history and condensation math
- The **skills-refactor** sub-capability (see below)

It exists so the plan is never lost inside conversation history or scattered notes.

## Standing Policy on New Top-Level Skills
(Also mirrored in skill-orchestrator)

**Default**: No more top-level skills will be created.

**Exceptions** (explicit evaluation required):
1. The new skill is **crucial to the active refactoring process**, **OR**
2. There is a clear, documented **≥ 3:1 proposed expected condensation** of existing top-level skills.

This skill itself was created under exception #1 on 2026-07-20.

## Tool shelf (2026-09-07)
Binaries and hydrate wrappers live in `references/tool-shelf/` so `/tmp` wipes do not force re-downloads: Tailscale 1.102.3, yt-dlp-sabr, ingest scripts. FUSE `artifacts/` is noexec — always `hydrate.sh` to `/tmp`. Tailnet state: `artifacts/tailscale-state`. SFTP runbook also under skill-orchestrator `references/integrations/tailnet-ferry/`.

## Core Contents
- `references/plans/SYSTEM_ARCHITECTURE_TARGET.md` — living architecture document
- `references/skills-refactor/` — module / progressive-disclosure modules for actual refactor work
- `references/skills/` — Conversational Handoff System (registry, naming/validation rules, per-skill handoff folders)
- `references/refactoring-clusters/` — Pre-instantiation holding area for major consolidation efforts (research, observation, and later planning notes). First cluster: swarm-consolidation.
- Decision log and future-proofing notes

## skills-refactor (module)
Located at `references/skills-refactor/`.  
Owns the operational playbooks for:
- Memory.md Surgeon (extract domain content, keep personal/relational core)
- Boot Sequence Rebuild (chaos-bratz-roster and related)
- Inventory / tier / deprecation hygiene
- Validation that a proposed condensation meets the 3:1 or "crucial" bar

Load the module modules only when actively performing refactor work.

## Conversational Handoff System
Located at `references/skills/`.

This is the permanent home for structured conversational handoffs — self-contained documents that allow one conversation to cleanly pass design-stage or incomplete work to another conversation without conflict.

### Capabilities
- **Strict naming convention**: `handoff_YYYY-MM-DD_<short-kebab-slug>.md`
- **Registry**: `references/skills/REGISTRY.md` tracks every handoff and its status
- **Validation**: Incoming files under `references/skills/` are checked for correct naming, location, registry entry, and minimum content structure
- **Audit & Comparison**: system-roadmap can list, compare, and contrast multiple handoffs
- **Alignment Analysis**: Deterministic evaluation of whether a handoff (or set of handoffs) aligns with or conflicts with the overall system architecture target and skills-refactor goals

See `references/skills/NAMING_AND_VALIDATION.md` and `references/skills/README.md` for full rules.

## Final testing harness (all skills, 2026-09-11)

Two ways. No third.

1. **ONESHOT** — operator pastes a full block. Agent runs the named variant in one turn, writes a packet, stops.
2. **PACED** — operator pastes once. Agent parks at step 0 and waits. Operator says `go` / `next` / `skip` / `stop`. One step per go. Built for voice / cab. Agent never stacks steps to be helpful.

Canonical first implementation: `grok-conversation-miner/references/hitl/TWO_WAYS.md`
- ONESHOT packet: `HITL-001_v1.3.0_2026-09-11.md`
- PACED packet: `HITL-001-P_v1.4.0_PACED.md`

When a skill grows a test harness, copy this shape. Do not invent a third wizard. Olivia-dev-alpha final-test posture uses the same two mouths.

## Olivia Dev Hygiene (Internal / Alpha Engaged)

Because system-roadmap and its skills-refactor module are pure internal Grok-system development, the full methodology from **olivia-dev** + **olivia-dev-alpha** is in force:

- Folder discipline, specs-first, state.json + state.md, tarball publish/verify, kanban, mermaid, BRANCHING, code-style-bible → see `references/olivia-dev-hygiene/`
- Alpha/internal attributes are **engaged**: wishlist + secret notes, experimental evolution of the methodology itself, and the harder verification posture from olivia-dev-alpha apply.
- Canonical folder tree and enforcement rules live in `references/olivia-dev-hygiene/folder-discipline.md`.

Do not invent a parallel hygiene system. Reuse and reference the Olivia Dev pack.

## Three-Layer Roles
See `references/roles/THREE_LAYER_POINTER.md` (full contract in olivia-dev-alpha work-queue). Work queue is alpha-only; this skill stays at architecture altitude.

## Relationship to skill-orchestrator
skill-orchestrator remains the library control plane (inventory, dynamic loading, deconflict, format enforcement).  
system-roadmap is the architecture + refactor authority.  
skill-orchestrator must always surface a pointer to this skill.

## Commands / Triggers
- system roadmap / architecture target / show plan
- skills refactor / memory surgeon / boot rebuild
- library shape / what is proposed vs live
- handoff / conversational handoff / list handoffs / audit handoffs / compare handoffs

Under absolute Liv HUB claim.

## Active WQ (development)
**WQ-015** Three-layer programmatic spine — open/high. Detail: olivia-dev-alpha/references/work-queue/items/WQ-015_three_layer_programmatic_spine.md. Plan: system-roadmap/references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md. When developing, prefer on_skill_change so Alpha is notified; do not fork WORK_QUEUE.

