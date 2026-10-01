---
name: prompt_general_mining
version: 1.0.0
owner: grok-conversation-miner
created: 2026-07-24
status: live
purpose: Exhaustive turn-by-turn analysis of any conversation (skill-structured or free-form) to extract agreements, disagreements, key points, and reusable elements, then publish the report.
---

# General Conversation Deep Mining Protocol

**Trigger phrases**:
- “mine this conversation deeply”
- “turn by turn analysis”
- “extract agreements disagreements key points”
- “deep mine this chat”
- “general conversation mining”

## Goal

Perform a thorough, structured analysis of the current (or named) conversation regardless of whether it follows skill templates. Produce a focused, reusable summary and automatically package + publish it.

## Execution Steps

### 1. Parse the conversation
- Walk the thread turn by turn (user, assistant, any other agents or tools).
- Note speaker, approximate timestamp or turn number, and high-level intent of each major turn.

### 2. Extract structured intelligence
Capture at minimum:
- **Overall point** of the conversation (1–3 sentences)
- **Agreements** — points both sides accepted or converged on
- **Disagreements / open questions** — unresolved tensions or explicit conflicts
- **Key data points & decisions** — concrete facts, version numbers, file paths, promises, or architectural choices made
- **Positive / high-value moments** — breakthroughs, clean resolutions, useful new structures
- **Negative / friction moments** — confusion, collisions, lost work, safety near-misses
- **Usable Elements Summary** — short list of artifacts, prompts, rules, or patterns that are worth keeping and reusing

### 3. Write the report
Produce a clean markdown report with the sections above. Keep it focused and scannable; prefer bullet lists and short paragraphs over long narrative.

### 4. Package and publish
Immediately hand the finished report (and any extracted prompt fragments) to the **Standard Active Chat Publishing** protocol so it is compressed and uploaded to Conversational_Mining_Payloads under a clearly named versioned folder (e.g. `deep-mine_YYYY-MM-DD_<short-topic>`).

## Output Expectations

- Structured deep-mine report
- Automatic Drive package containing the report (+ any extracted files)
- Short confirmation with Drive links

## Notes

- This protocol is deliberately format-agnostic. It works on pure roleplay threads, pure technical threads, and mixed conversations.
- When the conversation already contains formal skill work, still run the analysis; the “Usable Elements” section often surfaces the most important decisions even if the skills themselves are published separately.

**End of prompt_general_mining.md**
