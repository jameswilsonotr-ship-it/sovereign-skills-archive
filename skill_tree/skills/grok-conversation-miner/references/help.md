# Grok Conversational Miner — Built-in Help Guide (v1.4.0)

Welcome to the **Grok Conversational Miner (v1.4.0)**. This multi-agent utility is designed to help you extract, refactor, and back up custom prompts and instructions across active or historical conversations, pulling them out of unstructured "spaghetti" threads and organizing them directly into Google Drive.

## Available Command Triggers & Sub-Protocols

### 1. Help Guide
- **Trigger:** `grok conversational miner help`, `/help`
- **What it does:** Displays this interactive markdown help file, listing all commands, parameters, and formatting rules.

### 2. Standard Active Chat Publishing
- **Trigger:** `publish the skills in this chat`, `save our progress`
- **What it does:** Automatically serializes all custom prompt structures, role descriptions, and character bibles generated in the current active thread. Packages them into `grok-skill-export-[conv-id]-[YYYYMMDD].tar.gz` and pushes them directly to the `grok skills audit` folder on Google Drive.

### 3. Historical Pre-Skills Extraction
- **Trigger:** `mine this historical chat`, `extract pre-skills behaviors`
- **What it does:** Runs an analysis pass over older conversations from before the custom skills system existed. It extracts prompt-engineered behaviors and formalizes them into standard, agentskills.io-compliant `SKILL.md` structures before exporting.

### 4. Early Skill Attempt Refactoring
- **Trigger:** `refactor early skill attempts`, `cleanup early bibles`
- **What it does:** Identifies bloated or improperly formatted early skills. It automatically splits massive guidelines into a 100-line master `SKILL.md` file and moves detailed databases into a `/references/` subfolder, ensuring they meet the strict unquoted plain YAML description rules. **Always chains to Standard Active Chat Publishing** upon completion so the refactored work is immediately packaged and pushed to Drive.

### 5. Programmatic Deletion Test
- **Trigger:** `delete skills programmatically`, `test deletion limits`
- **What it does:** Tests the programmatic write/delete boundaries of the current environment. Attempts to execute local shell script removals under Grok Build CLI or account-level deletions on web chat.

### 6. General Conversation Deep Mining (NEW in v1.3.0)
- **Trigger:** `mine this conversation deeply`, `turn by turn analysis`, `extract agreements disagreements key points`, `deep mine this chat`, `general conversation mining`
- **What it does:** Performs exhaustive turn-by-turn analysis on **any** conversation format (structured skills or completely freeform/arbitrary threads). Maps every speaker turn, agreements, disagreements, overall point, key dynamic moments with extracted data points, positive/negative points, and produces a focused "Usable Elements Summary" optimized for later reuse. Automatically packages the structured report and publishes via Standard Active Chat Publishing to Drive. Supports non-exact formats.

### 7. Vacuum Mode — Full Sweep (NEW in v1.3.1)
- **Trigger:** `vacuum the conversation`, `run vacuum miner`, `vacuum everything`, `full miner sweep`
- **What it does:** Master combined command that executes **Standard Active Chat Publishing + Historical Pre-Skills Extraction + General Conversation Deep Mining** all in one coordinated vacuum sweep on the active thread. Everything except the pure Help command now triggers publishing. Produces unified packages with all extracted intelligence and pushes them to Drive. Use this when you want the complete extraction treatment in a single invocation.

---
*Maintained under absolute Triad claim. Re-grounding complete. v1.3.1 Vacuum Mode + auto-publish on refactor active.*


### 8. Global Conversation + Sandbox Extract (NEW in v1.4.0)
- **Trigger:** `global extract`, `grok conversation miner global extract`, `full sandbox extract`, `package everything from this conversation`, `conversation + artifacts + skill delta`, `comprehensive miner package`
- **What it does:** Comprehensive one-shot package that captures:
  1. Conversational flow, handoffs, and key decisions
  2. Sandbox + `/home/workdir/artifacts/` snapshot
  3. Markdown / queue / extension files written or changed during the session
  4. Skill-tree delta across touched skills
  - Assembles a canonical tree, writes MANIFEST.md, tars everything, and publishes via the existing Drive protocol.
  - Preferred command when you want “everything that happened in this conversation and its side-effects” in a single archive.
  - Protocol: `references/prompt_global_extract.md`

### 9. Sunset — unified backup (NEW 2026-09-08)
- **Trigger:** `sunset`, `sunset this conversation`, `run sunset`, `sunset dry-run`, `sunset lake-only`, `sunset miner-only`
- **What it does:** One backup dispatcher. Parks this conversation on every archive lane that should hold it and **skips** lanes that already have it or that belong to another verb.
- **Runs:** lake twin + receipt, miner package if missing, global extract if missing, Cilia wake, doorbell pointer, outbox card.
- **Does not run:** help, historical mine, refactor, delete-test, deep mine, vacuum.
- **Protocol:** `references/prompt_sunset.md`
- **Queue:** GCM-WQ-001

### Queued — not live (2026-09-10 leftover ideas)
Do not run these until the matching WQ item is LIVE.
- Census — GCM-WQ-005
- Sunset L8 xAI export recon — GCM-WQ-006
- Artifact packers (imagine / video / plates) — GCM-WQ-007
- Lake-batch vacuum — GCM-WQ-008
- `sunset smoke` fixture harness — GCM-WQ-009
- TOC + OMISSIONS — GCM-WQ-011
- Deterministic layout — GCM-WQ-012
- Always-mail / email filesystem — GCM-WQ-013
- Keep-everything — GCM-WQ-014
- Turn remainder card — GCM-WQ-015
- Patience rule — GCM-WQ-016
- Conv space + deltas — GCM-WQ-017
- Skill-tree ledger — GCM-WQ-018
- Append-only export log — GCM-WQ-020
Index: `references/work-queue/WORK_QUEUE.md`


### 10. Census (scripted, GCM-WQ-005)
- **Trigger:** `census this conversation`
- **What it does:** Writes/reads `CENSUS.jsonl` packed/pointed/redacted. Does not mine. Does not tar.
- **Script:** `scripts/census.py`

### 11. Sunset smoke (fixtures only, GCM-WQ-009)
- **Trigger:** `sunset smoke`
- **What it does:** Plants 12 fixture files / 6 classes and exits 0 only if census + fake ACK ids match.
- **Script:** `scripts/sunset_smoke.py`
- Never run against a live bubble first.

### Determinism (GCM-WQ-011–018)
Every package ships `TOC.md` and `OMISSIONS.md`. Always mail Cilia as a filesystem. Duplicates allowed; skip is annotation. Time is not the budget. Exhaustive on a long thread is correct. Take the turns.


## Quick start (scripts, 2026-09-11 04:08 EDT)

```
python3 scripts/sunset_smoke.py
python3 scripts/stress_harness.py
python3 scripts/sunset_dry_run.py --flag dry-run --log /tmp/EXPORT_LOG.jsonl
```

### Extra verbs now wired in scripts
- `sunset dry-run --log <EXPORT_LOG.jsonl>` — every lane appends a receipt (GCM-WQ-020)
- export receipt log: `python3 scripts/export_log.py append --run-id R --verb sunset --conversation-key DATE_slug --action SKIP-EXISTS`
- stress: `python3 scripts/stress_harness.py` (GCM-WQ-021)

### Still not live verbs
- WQ-010 A01–A08 exact-title harvest
- live CENSUS write for real threads
- minting per-conversation Drive spaces (017)
- L8 against a real accounts.x.ai zip


### 12. Stress harness (fake xAI export, GCM-WQ-021)
- **Trigger:** `miner stress`, `fake data stress`
- **Script:** `scripts/stress_harness.py`
- Plants a synthetic `prod-grok-backend.json` in the observed xAI wrapper shape, runs L0–L8, appends EXPORT_LOG, tars, blocks GitHub.

### 13. Export evidence log (GCM-WQ-020)
- **Trigger:** implicit on every harvest
- **Script:** `scripts/export_log.py`
- Append-only jsonl of EXPORTED / SKIP-* / NOT-WALKED. Cited by TOC/OMISSIONS.

### 14. Sunset dry-run (GCM-WQ-004)
- **Trigger:** `sunset dry-run`
- **Script:** `scripts/sunset_dry_run.py`
- Prints L0–L8 cards. Writes nothing except EXPORT_LOG receipts.

Quick start lives in root README.md. Banner 2026-09-11 04:08 EDT.
