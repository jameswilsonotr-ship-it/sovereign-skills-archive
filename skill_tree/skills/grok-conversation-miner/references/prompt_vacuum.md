---
name: prompt_vacuum
version: 1.0.0
owner: grok-conversation-miner
created: 2026-07-24
status: live
purpose: Master “everything at once” sweep that runs Standard Publishing + Historical Extraction + Deep Mining in one coordinated pass.
---

# Vacuum Mode — Full Sweep Protocol

**Trigger phrases**:
- “vacuum the conversation”
- “run vacuum miner”
- “vacuum everything”
- “full miner sweep”

## Goal

Execute a complete extraction treatment on the current conversation in a single invocation:
1. Standard Active Chat Publishing (package whatever formal skills / layers were touched)
2. Historical Pre-Skills Extraction (pull any pre-skill behaviors still present)
3. General Conversation Deep Mining (full turn-by-turn analysis + usable-elements summary)

All outputs are automatically packaged and published to Drive.

## Execution Order (mandatory)

1. **Standard Active Chat Publishing**  
   Identify and package any skills, agent folders, or prompt sets that received real changes in this thread. Follow `prompt_publishing.md` exactly.

2. **Historical Pre-Skills Extraction**  
   Scan the same thread (and any explicitly referenced older material) for pre-skill era behaviors and formalize them. Follow `prompt_historical_mining.md`.

3. **General Conversation Deep Mining**  
   Produce the structured deep-mine report. Follow `prompt_general_mining.md`.

4. **Unified reporting**  
   After all three streams finish, give the user a single summary that lists:
   - Packages created and their Drive links
   - Key findings from the deep-mine report
   - Any historical material that was newly formalized

## Rules

- Help command is excluded from vacuum; pure help requests never auto-publish.
- If one of the three streams has nothing useful to do, skip it cleanly and note the skip in the final report.
- Prefer one versioned parent folder on Drive that contains sub-packages or clearly named files for each stream, rather than scattering unrelated packages.
- All normal safety rules from the individual protocols still apply.

## Output Expectations

- One or more Drive packages
- A concise vacuum summary that lets the user see everything that was extracted and where it landed
- No silent failures; every stream reports success, skip, or error

**End of prompt_vacuum.md**
