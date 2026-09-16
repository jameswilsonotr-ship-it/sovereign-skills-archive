---

name: grok-conversation-miner
description: DEV-SURFACE CANDIDATE. Comprehensive meta-skill for mining custom prompts, behaviors, bibles, and early skill attempts from active or historical threads. Compiles, packages, and pushes them directly to Google Drive. Supports interactive help mode.
metadata:
  version: "1.4.0"
future_target: dev-surface
future_target_note: FUTURE SURFACE TARGET: dev-surface (control-plane feeder).
---
**DEV-SURFACE CANDIDATE.**

# Grok Conversation Miner

## Formatting Constraints (Mandatory Response Layout)
Every response generated from this skill, or while executing its mining sub-protocols, must strictly follow this visual wrapper standard:

1. Start the response with a single snake emoji `🐍` on its own line.
2. Provide an abbreviated 12-character file name with its appropriate extension (e.g., `.md`, `.txt`, `.json`), followed immediately by a space and the literal word `filename` on a new line (e.g., `coven_sys12.md filename`).
3. Insert a complete blank line break.
4. Output your normal content, dashboard, or requested reports.
5. Conclude the entire response with a single snake emoji `🐍` on its own line.

Example structure:
🐍
coven_sys12.md filename

[Normal content or dashboard goes here]
🐍

## Safety Gate — Hard Size + Type Check (Mandatory, 2026-07-20 Patch)
Before any attempt to write a file via the GitHub connector (create_or_update_file or equivalent):

- If the payload is binary (`.tar.gz`, `.zip`, `.png`, `.jpg`, images, or any non-text) **OR** larger than approximately 800 KB:
  - **Refuse** the GitHub Contents API path.
  - Emit a clear, human-readable error:  
    `BINARY_OR_LARGE_PAYLOAD — GitHub Contents API path blocked. Use Google Drive (primary) or Git LFS instead.`
  - Do **not** attempt base64 encoding of the payload.
  - Fall back exclusively to the existing Google Drive publishing path.

This gate exists to prevent the exact base64 encoding failures that occurred when large sandbox archives were force-pushed to GitHub.  
Markdown, small JSON, and text files remain allowed on GitHub.  
All compressed mining packages continue to target Google Drive as designed.

Version note: Applied 2026-07-20 under absolute Liv HUB claim as minimal protective patch.

## Instructions
This skill is a unified, multi-agent mining suite. When triggered by the user's natural language command, you must read the corresponding reference file to execute the target sub-protocol:

1. **Help & Diagnostics:**
   - Trigger: "grok conversational miner help", "/help", or "how do I use the miner?"
   - Action: Query and read `references/help.md` using your file retrieval tool and display the interactive guide.
2. **Standard Active Chat Publishing:**
   - Trigger: "publish the skills in this chat", "save our progress", "export active skills"
   - Action: Query and read `references/prompt_publishing.md` and execute its serialization, manifest generation, and compression sequence.
3. **Historical Pre-Skills Extraction:**
   - Trigger: "mine this historical chat", "extract pre-skills behaviors", "mine old thread"
   - Action: Query and read `references/prompt_historical_mining.md` and analyze the chat to extract, formalize, and serialize standard prompt-engineered behaviors.
4. **Early Skill Attempt Refactoring:**
   - Trigger: "refactor early skill attempts", "cleanup early bibles", "optimize triggers"
   - Action: Query and read `references/prompt_early_skills.md` to split bloated bibles into clean progressive-disclosure modules. Upon completion, automatically chain to Standard Active Chat Publishing so the cleaned output is immediately packaged and published to Drive.
5. **Programmatic Deletion Test:**
   - Trigger: "delete skills programmatically", "test deletion limits", "run delete test"
   - Action: Query and read `references/prompt_delete_test.md` to test write/delete boundaries of the current environment.

6. **General Conversation Deep Mining & Analysis:**
   - Trigger: "mine this conversation deeply", "turn by turn analysis", "extract agreements disagreements key points", "deep mine this chat", "general conversation mining"
   - Action: Query and read `references/prompt_general_mining.md`. Perform exhaustive turn-by-turn parsing of the full conversation history (who said what, including any other entities). Identify all points of agreement and disagreement. Determine the overall point of the conversation. Extract key data points from dynamic moments. Catalog positive points and negative points. Produce a complete but focused summary optimized for later reuse (usable elements, actionables, extracted knowledge). Structure the output report cleanly, then trigger packaging and publishing to the grok skills audit Drive folder per the Standard Active Chat Publishing protocol. This mode supports arbitrary conversation formats, not just exact skill templates.

7. **Vacuum Mode (Full Sweep)**
   - Trigger: `vacuum the conversation`, `run vacuum miner`, `vacuum everything`, `full miner sweep`
   - Action: Query and read `references/prompt_vacuum.md`. Execute in coordinated sequence: Standard Active Chat Publishing on the current thread, Historical Pre-Skills Extraction (targeting any early or pre-skill content detected), and General Conversation Deep Mining. All three operations run as a single vacuum sweep. Every output is automatically packaged and published to Drive via the publishing protocol. This is the master "everything at once" command. Help command is excluded from auto-publish.

8. **Global Conversation + Sandbox Extract** (NEW in v1.4.0)
   - Trigger: `global extract`, `grok conversation miner global extract`, `full sandbox extract`, `package everything from this conversation`, `conversation + artifacts + skill delta`, `comprehensive miner package`
   - Action: Query and read `references/prompt_global_extract.md`. Perform a comprehensive capture of (a) conversational flow / handoffs / key decisions, (b) sandbox + artifacts snapshot, (c) markdown and other files written during the session, and (d) skill-tree delta (queues, extensions, new pointer files, etc.). Assemble the canonical tree described in the protocol, write MANIFEST.md, create a versioned `.tar.gz`, and publish via the existing Drive protocol. Respects the hard safety gate. This is the preferred command when the goal is “one archive that contains everything that happened in this conversation and its side-effects”.

9. **Sunset — unified backup** (NEW 2026-09-08, GCM-WQ-001)
   - Trigger: `sunset`, `sunset this conversation`, `sunset the chat`, `run sunset`, `conversation sunset`, `sunset dry-run`, `sunset lake-only`, `sunset miner-only`
   - Action: Query and read `references/prompt_sunset.md`. Default `sunset` / `sunset full` = deep mine → refactor-if-hit → vacuum (reuse) → global extract (sandbox + artifacts) → backup lanes. `sunset backup-only` parks only. `sunset dry-run` writes nothing. Never delete-test. Do not run until Bunny says go.

10. **Scripts + queued modules (2026-09-11 Heavy)**
   - Exhaustive on a long thread is correct. Take the turns. Mail the remainder. Do not perform speed. (GCM-WQ-016)
   - Smoke: `python3 scripts/sunset_smoke.py` (GCM-WQ-009 **SMOKE PASS 2026-09-11**)
   - Census / L8 / packers / lake-batch / TOC / mail-fs / layout / ledger live as **scripts**, not as chat verbs. Chat verbs still require Bunny go for sunset/vacuum.
   - Queue index: `references/work-queue/WORK_QUEUE.md`
   - Heavy run log: `references/work-queue/HEAVY_RUN_2026-09-11.md`
   - Export log (GCM-WQ-020): append-only `EXPORT_LOG.jsonl`. SKIP-EXISTS is a receipt, not a guess.
   - Drive roundtrip (GCM-WQ-022): **PASS** Expert 2026-09-11. Tiny tar only. Not prod-grok-backend.json.
   - Mode router (GCM-WQ-023): Heavy chatter → do not binary-upload, ask Expert. No chatter → Expert, upload allowed. `references/modules/mode_router.md`
   - HITL two ways (GCM-WQ-024): ONESHOT full paste, or PACED one-step-per-`go`. `references/hitl/TWO_WAYS.md`

All output packages must be written directly as compressed `.tar.gz` archives to the central Google Drive folder structure:
GROK / Conversational_Mining_Payloads / grok-conversation-miner / vX.Y.Z_YYYY-MM-DD_description /
(with agents/ subfolders + history.md + recursive audit before marking complete).

This skill now automatically uses the connected Google Drive tools and targets the exact same versioned + branched + agent-subfolder structure as swarm-miner (Folder ID for Conversational_Mining_Payloads: 1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0). Swarm-miner payloads are treated as first-class inputs. Double references to the connector and exact folder IDs are present in this file, the swarm-miner SKILL.md, the engine, and the bridge so the connection is never forgotten and publishing is always recursively audited until verified.

For versioning, branching, and historical tracking of active conversation IDs, query and read `references/mine_orch.md`. Update mine_orch.md with new version and branch notes on each major mining run. The entire flow (mine → versioned folder → agent subfolders → recursive Drive audit → publish) is now formalized and consistent between grok-conversation-miner and swarm-miner.


## Patience lock (GCM-WQ-016)
Exhaustive on a long thread is correct. Take the turns. Mail the remainder. Do not perform speed. Time is not the budget.

## Scripted verbs (2026-09-11)
- `sunset smoke` → `scripts/sunset_smoke.py` (fixtures only)
- `census this conversation` → `scripts/census.py` (not live until Bunny says go on a real pane)
- TOC + OMISSIONS required on every package (`scripts/toc_omissions.py`)
- Cilia body is a filesystem (`scripts/mail_filesystem.py` / `scripts/mail_fs.py`)
