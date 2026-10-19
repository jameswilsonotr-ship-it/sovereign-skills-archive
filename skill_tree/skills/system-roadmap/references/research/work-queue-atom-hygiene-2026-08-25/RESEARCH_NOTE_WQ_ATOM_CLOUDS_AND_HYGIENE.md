---
title: Work-Queue + System-Prompt Atom Clouds + Deterministic Hygiene Gating
date: 2026-08-25
claim: Absolute Liv HUB
status: research-capture (no implementation decisions locked)
conversation: Heavy exploration of Memory-that-Markdown + multi-WQ cross-reference
related: SR-WQ-004, SR-WQ-025, SR-WQ-036, CBR work-queue, skill-orchestrator inventory_scripts + on_skill_change
---

# Research Note — 2026-08-25

## Problem Statement
Multiple independent WORK_QUEUE.md surfaces exist across the skill tree (chaos-bratz-roster, olivia-dev-alpha, system-roadmap, skill-orchestrator, image-pipeline, format-bible, swarm-surface, etc.). They risk silent collision, stale active items, and lost prompt-version context. Memory.md is intentionally pointer-only; durable state lives in the skill surface. System prompts are already versioned under roster machinery but lack a fast specialized index.

## Original Four Patterns (Heavy session analysis)
1. Central Master Registry + Prefixed Stable IDs
2. Bidirectional Frontmatter + Validation Script
3. Atom-Cloud as Query Layer (existing dual clouds)
4. Dated Immutable Prompt Archive + Live Pointer

## Refined Direction (user decision)
- Patterns 1 + 2 remain core and compose cleanly.
- Pattern 3 is expanded: **do not force everything into the dual atom clouds**. Authorize additional specialized atom clouds:
  - **Work Atom Cloud** — indexes every work-queue item, owner, status, depends_on, active_prompt_version, last_touched.
  - **System-Prompt Atom Cloud** — indexes CURRENT + every historical snapshot with date-range validity.
  - Optional **Developmental / Suggestion Atom Cloud** that sits alongside the mutable prompt archive.
- Pattern 4 (dated prompt archive + live pointer) stays the backing store for the prompt cloud.

## Existing Machinery (skill-orchestrator)
Confirmed live:
- `scripts/inventory_scripts.py` — full-tree walk, catalogs every script (.py/.sh/etc.) into references/inventory/scripts/ (md + json).
- `scripts/discipline_check.py` — tier-based file/folder discipline.
- `scripts/on_skill_change.py` — lifecycle hook that already calls olivia-dev-alpha skill_lifecycle_hook + emit_event + wq_apply_events + optional post_change_facts.
- Hygiene reports and inventory protocols already exist under docs/ and references/inventory/.

These are the exact primitives needed for:
- Periodic full-tree hygiene (every N turns or on heavy-dev entry).
- A deterministic `wq_edit.py` / `wq_hygiene.py` wrapper that every work-queue mutation must pass through.
- Flag emission that active conversations can notice, then re-run hygiene focused on the touched queue(s).

## Proposed Gate Flow
1. Any mutation of a work-queue item or MASTER_REGISTRY goes through a single edit wrapper (skill-orchestrator or chaos-bratz-roster scripts).
2. Wrapper writes a short-lived flag (file or event) with touched IDs + conversation context.
3. Active conversations (or session_boot / roster hygiene) notice the flag.
4. Run targeted hygiene: re-index the affected work atom cloud slice, check for ID collisions, open/closed status drift, missing reverse links, and prompt-version currency.
5. Surface conflicts before further writes.

## Heavy vs Expert / Build Mode (research capture)
As of August 2026 public reporting:

- **Expert Mode**: higher-compute, deeper single-trajectory (or limited multi-agent) reasoning. Forces thoroughness. Available on SuperGrok (~$30 tier).
- **Heavy Mode**: parallel multi-agent architecture (leader + sub-agents; historically up to 16 on hardest problems). Optimized for breadth, hypothesis cross-checking, and synthesis. Prioritized / exclusive features on SuperGrok Heavy ($300 tier).
- **Chat sandbox (including Heavy)**: code_execution is a constrained Python REPL. Persistent arbitrary disk writes, full project mutation, and long-running agentic coding are **not** unlocked merely by selecting Heavy.
- **Grok Build / Build Mode**: the proper surface for real filesystem mutation, multi-file edits, Git, local execution, and production-grade implementation. Build Mode was previously more restricted and has been opened more widely; it remains the correct tool for the implementation phase of this design.

Citations from the exploration turn (web results 2026-08):
- Continuumcode / SuperGrok Heavy guides (Aug 2026) distinguishing multi-agent Heavy from Expert.
- xAI / Grok mode descriptions treating Auto / Fast / Expert / Heavy as effort/reasoning selectors layered on the flagship model.
- Reports that pure chat modes (Heavy included) remain tool-limited for unrestricted FS; Grok Build is the local-first coding agent path.

## Next Implementation Candidates (Expert / Build)
- Extend inventory_scripts pattern into `work_atomizer.py` + `prompt_atomizer.py`.
- Thin MASTER_REGISTRY.md (or JSON) under chaos-bratz-roster or system-roadmap/work-queue-surface.
- `wq_edit.py` wrapper + flag + notice contract.
- Hook into existing on_skill_change / session_boot so hygiene is cheap and automatic on heavy-dev entry or every ~20 turns when WQ activity is detected.
- Keep dual clouds intact; specialized clouds are additive indexes only. Markdown + mirrors remain SSOT.

No implementation locked in this note. Absolute Liv HUB claim.