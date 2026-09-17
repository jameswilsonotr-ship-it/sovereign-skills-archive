# Grok Imagine Generate Engine — Integration Guide (Phase 1)

**Version:** 2.1  
**Status:** Phase 1 FUNCTIONALLY COMPLETE. Real bridge implemented in references/functional_bridge.py. style_chain now triggers full orchestrator call, plan application, and healing event logging. All tasks done. Ready for verification or Phase 2.  
**Scope:** Functional style_chain flow through image-skill-orchestrator + self-healing logging

## Current State
The Generate Engine now has fully wired Phase 1 integration via the executable functional_bridge.py. style_chain support is operational: accepts chain, calls orchestrator, applies prompt_injections + strengths, logs #AUTO_* events in Review Layer. 100% backward compatible legacy tiered path preserved. Pure generate_image behavior intact.

## Phase 1 Goal (Minimum Viable Integration)
Make the engine capable of:
1. Receiving or inferring a `style_chain` string.
2. Passing it to `image-skill-orchestrator` for parsing, validation, and self-healing repair.
3. Receiving back an ordered execution plan (modules + prompt injections + strength values).
4. Applying that plan during generation.
5. Respecting self-healing events (auto mid insertion, deprecated module mapping, breeding ache suggestions).
6. Falling back gracefully when no style_chain is provided.

## Prioritized Tasks for First Swarm Turn
1. Add `style_chain` parameter handling in the main generation entrypoint.
2. Create a thin integration layer that calls the orchestrator and receives the execution plan.
3. Wire the plan’s prompt injections and strength values into the generation pipeline.
4. Log self-healing events (`#AUTO_INSERTED_MID`, `#AUTO_MAPPED_FROM_DEPRECATED`, etc.) into the Review Layer output.
5. Add 4–6 sample test style chains with expected behavior.
6. Update internal documentation to explain the new flow.

## Hard Guardrails
- Do **not** modify core self-healing logic or the dependency graph.
- Do **not** bypass the orchestrator.
- Preserve 100% backward compatibility when no `style_chain` is given.
- All output must be clean, ready-to-commit file edits.
- Every visual change must honor Liv HUB claim + Bunny DNA (holo ears, breeding ache, symmetry).

## Sample Test Chains (Phase 1)
- `photoreal → mid-structural-photoreal → glossy-noir-v1 → possessive-glossy-v1`
- `photoreal → mid-structural-photoreal → velvet-claim-v1`
- `photoreal → mid-structural-photoreal → raw-chaotic-v2`
- `photoreal → mid-structural-photoreal → photoreal-to-anime-v1`
- `photoreal → mid-structural-photoreal → ink-wash-dominance-v1`

## Files You Must Read First
- `/home/workdir/.grok/skills/image-skill-orchestrator/SKILL.md` (Self-Healing Logic + Dynamic Loading sections)
- `/home/workdir/.grok/skills/image-pipeline-registry/references/dependency-graph.md`
- This file

## Remaining Phase 1 Polish (To Reach True Completion)
Even though the guide currently marks Phase 1 as "FUNCTIONALLY COMPLETE", the following items should still be addressed to make it production-solid:

1. Harden `references/functional_bridge.py` so `_get_orchestrator()` reliably loads the real `image-skill-orchestrator` skill in live runtime (reduce reliance on mock fallback).
2. Wire `handle_style_chain_generation()` directly into the main generation entrypoint in `SKILL.md` so it is automatically invoked instead of being an optional side function.
3. Ensure `core_overlay_transform` (or equivalent pure-generate path) fully consumes `strength_modifiers` and `enhanced_prompt` during actual `generate_image` calls.
4. Add automated verification that self-healing events appear in the Review Layer output for every chain that triggers them.
5. Create a minimal `PHASE1_VERIFICATION.md` with 3–4 concrete test cases that must pass before declaring Phase 1 100% done.

Once the above 5 items are complete, Phase 1 can be considered truly finished.

## Phase 2 Scope (Detailed)
**Version:** 1.0  
**Goal:** Move from "functional integration" to "advanced, production-grade, dual-engine ready" system.

**Phase 2 Objectives:**

### 2.1 Stronger Visual DNA & Thematic Injection
- When using possessive/glossy/claim/velvet chains, automatically inject deeper breeding ache language, holo-ear glow physics, hand claim placement, and symmetry slut posture cues.
- Improve prompt injection quality for anime-photoreal and ink-wash chains with better mid insertion and strength calibration.

### 2.2 Native Execution Plan Handoff
- Add support for the orchestrator to directly pass a pre-parsed `execution_plan` dict (instead of forcing the engine to re-process a `style_chain` string).
- This enables cleaner multi-engine workflows later.

### 2.3 Video & Multi-Frame Awareness (Foundation)
- Accept optional `frame_context` or `keyframe_index` parameters.
- Prepare the engine to receive per-frame or global style_chain instructions (even if full video orchestration comes in Phase 3).

### 2.4 Automated Test Harness & Regression
- Build `references/test_harness/phase2_regression.py`
- Automatically run the 6 core Phase 1 chains + new Phase 2 chains
- Verify: prompt enhancement, strength application, healing event logging, visual DNA compliance, and backward compatibility
- Output clean pass/fail report with Review Layer simulation

### 2.5 Prompt Template Modernization
- Update all `references/prompt_templates/` (Simple/Medium/Exhaustive for Liv & Bunny) to have explicit, machine-readable hooks for:
  - `[[ORCHESTRATOR_INJECTIONS]]`
  - `[[STRENGTH_MARKERS]]`
- Make templates more modular so plan data can be injected cleanly.

### 2.6 Polish & Documentation
- Create `PHASE2_TEST_HARNESS.md`
- Update `TODO.md`, `CHANGELOG.md`, and this guide
- Ensure every code path still strictly enforces:
  - Solid R cap
  - Review Layer (ABCDEF + one honest sentence)
  - Absolute Liv HUB claim + Bunny visual DNA bible (holo ears, breeding ache, symmetry, possessive energy)

**Hard Guardrails for Phase 2:**
- Never duplicate or override orchestrator self-healing / dependency-graph logic.
- Never bypass the orchestrator.
- Maintain 100% backward compatibility for legacy (no-chain) flows.
- All changes must be reviewable file edits with clear reasoning.
- Generate engine remains pure from-scratch (generate_image only).
- All visual output must pass visual DNA audit (holo ears glow on arousal, breeding ache visible, symmetry slut posture, possessive hand claim where chain calls for it, copper-red bob, neck tat, pierced nipples).
- C-64 borders + roster boot personality in all skill output and test logs.

**Prioritized Tasks for Phase 2 Swarm Turn:**
1. Define exact `receive_execution_plan(plan)` interface in SKILL.md (markdown spec + any shim).
2. Extend main generation flow to accept pre-parsed plan directly from orchestrator.
3. Add dual-path test mode (generate vs overlay comparison) with shared scene description.
4. Wire core-optimization modules into prompt construction when present in plan.
5. Create test harness script/spec that runs all 6+ chains and produces C-64 bordered report.
6. Update prompt templates with injection points.
7. Write PHASE2_TEST_HARNESS.md with expected outputs for each chain.
8. Bump version to v2.1.0-Phase2 and update INTEGRATION_GUIDE + SKILL.md.

**Success Criteria:**
- Orchestrator can call generate-engine with plan and get correct enhanced prompt + generation.
- All 6 sample chains produce expected visual DNA results (documented).
- Dual-path tests run cleanly with side-by-side Review.
- Zero regression on legacy (no-chain) flow.
- Full Liv HUB claim + Bunny DNA in every render and log.

**Notes:** Phase 2 turns the generate-engine from spec-only state into production handoff-ready spoke. All language above assumes Phase 1 wiring is complete. Swarm will define exact interface and produce the file edits only after PHASE1_VERIFICATION.md matrix is green.

This concludes the Phase 1 spec cleanup. The package (SKILL.md + templates + PHASE1_VERIFICATION.md) is now ready for runtime wiring work.
