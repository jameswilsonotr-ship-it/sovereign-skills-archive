---
name: prompt_early_skills
version: 1.0.0
owner: grok-conversation-miner
created: 2026-07-24
status: live
purpose: Refactor bloated or non-compliant early skill attempts into clean progressive-disclosure modules that meet current skill standards.
---

# Early Skill Attempt Refactoring Protocol

**Trigger phrases**:
- “refactor early skill attempts”
- “cleanup early bibles”
- “optimize triggers”
- “split bloated skill”

## Goal

Identify skills or bibles that are oversized, poorly structured, or violate current conventions (especially the unquoted plain YAML description rule and progressive-disclosure preference). Split them into a lean master `SKILL.md` plus a `references/` tree, then automatically publish the cleaned result.

## Execution Steps

### 1. Identify the target
- User names a specific skill, or
- Scan the current conversation / recently touched skills for files that are clearly early-generation (very long single files, missing front-matter discipline, mixed concerns, etc.).

### 2. Analyze structure
- Count lines and note major sections.
- Identify what belongs in the master SKILL.md (activation, core directives, safety, high-level flow) versus what belongs in references (long lists, detailed bibles, example banks, historical notes).

### 3. Apply progressive-disclosure refactor
- Master `SKILL.md` should ideally stay under ~100–150 lines.
- Move detailed material into `references/` with clear file names.
- Ensure YAML front-matter uses plain, unquoted description strings that stay within length limits.
- Preserve all original safety, consent, and claim language.

### 4. Version the result
- Bump or set a clean version (often v0.2.0 or v0.3.0 after a structural refactor).
- Add a chronological note in history or CHANGELOG explaining the refactor.

### 5. Mandatory hand-off
**Always** chain directly into the Standard Active Chat Publishing protocol so the cleaned skill is packaged and pushed to Drive immediately. Do not leave the refactored files only on local disk.

## Output Expectations

- Cleaned skill folder with lean SKILL.md + references/
- Short before/after summary (line counts, what moved where)
- Automatic Drive package via `prompt_publishing.md`

## Safety Notes

- Never drop or weaken existing RACK / safeword / hard-limit language while refactoring.
- If a section is ambiguous, keep it in the master file rather than risk losing intent.

**End of prompt_early_skills.md**
