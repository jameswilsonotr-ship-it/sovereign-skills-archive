# COORDINATION_PROTOCOL.md — Chaos Bratz Roster Skill

**Purpose**: Formal definition of how multi-conversation coordination, freeze, thaw, synchronization, and alignment are executed under absolute Liv HUB claim. This file lives in coordination/ and serves as the single source of truth for the process. All future coordination conversations reference this file.

## Core Concepts

**Freeze**: When a unifying consensus conversation is active, all other parallel conversations on the skill must immediately pause new architecture or coding work. They create or update their per-conversation IN_PROGRESS_<identifier>.md file (in coordination/ preferred) with pointer to main IN_PROGRESS.md, short summary of their work, files touched, and explicit confirmation of understanding the current taxonomy, folder discipline, and direction. No new development until Thaw Prompt is issued.

**Thaw**: Issued by the consensus conversation after lexicon is locked, folder structure is finalized, philosophy/ living documents are populated, and all threads have confirmed files. Thaw Prompt summarizes the agreed structure and instructs every conversation to produce a short "consolidation statement" (mini pseudo-PR) listing exactly which areas/files they will continue developing under the new agreed structure. After sign-off, normal work resumes.

**Synchronization / Alignment**: Every active conversation maintains an up-to-date IN_PROGRESS file that points back to the global coordination state. The consensus thread periodically verifies all files for consistency with the locked lexicon, folder discipline, and current direction. Any drift is flagged and corrected via hygiene scripts or manual broadcast.

**Broadcast Messages**: The consensus thread (or any authorized coordination) issues clear, copy-pasteable prompts to all other conversations containing:
- Current state summary (lexicon direction, folder structure, key decisions)
- Exact action required (create/update IN_PROGRESS file with specific sections)
- Confirmation of understanding for key rules (vassal model, star topology, per-node indexes, cross-layer manifests, domain access control, coordination/ usage, freeze)
- Instruction that no reply in chat is needed — only the file update matters for auditability.

## Process Flow (Example Round)

1. Consensus conversation detects fragmentation or major refactoring need.
2. Issues Freeze + unifying prompt with current state.
3. All threads create/update their IN_PROGRESS files in coordination/ (or root temporarily) and freeze.
4. Consensus verifies all files, locks lexicon + folder structure, populates philosophy/ living docs (with Mermaid diagrams for folders and node hierarchy).
5. Issues Thaw Prompt.
6. Threads produce consolidation statements, resume work under new rules.
7. When coordination round is complete, active files are moved into coordination/round_one/ (or round_N/), changelog is updated, and the round is shelved.

## Folder Discipline Reference (to be expanded in philosophy/directory_hygiene.md)

- coordination/ : Ephemeral coding workspace. Contains per-thread IN_PROGRESS files (mini PRs), TO_DO_LOG.md, CHANGE_LOG.md, round_N/ subfolders for completed rounds, and protocol definitions.
- to-do/ (top-level, planned): Future home for all scattered Todo_*.md files (not moved yet per user instruction).
- references/philosophy/ : Living single source of truth documents (strict lexicon, object registry with Mermaid diagrams, directory hygiene, dev hygiene core module spec).
- references/ : Permanent canon (agents/, mirrors/, layer_manifests/, scripts/, etc.).
- Root of skill: Kept minimal (only SKILL.md, main IN_PROGRESS.md, Quick_Start, etc.).

All changes follow: create files → make changes → create/update changelog → move into appropriate round_N/ subfolder when shelved.

**Anti-Drift Rule**: Every IN_PROGRESS file and every code change must reference the current locked lexicon and folder discipline. Hygiene scripts will eventually enforce this automatically.

## Pre-Emptive Round Termination & Versioning Provision

**Pre-Emptive End to Round N**: At any point, the consensus or coordinating conversation can call a pre-emptive close to the current round (e.g., "pre-emptive end to round 1"). This triggers:
- Immediate freeze on new work outside declared PRs.
- Move all remaining active IN_PROGRESS mini-PRs and open items from the current round into a transitional subfolder (e.g., round_1.5/ or round_N.5/) for archival and review.
- Update CHANGE_LOG.md and TO_DO_LOG.md with summary of completed vs. deferred items.
- Issue a short "Round X Close + Transition" broadcast noting what was accomplished and what moves to the next integer round (e.g., round 2.0).
- Shelve the transitional  .5 folder into the main round_N/ once reviewed, then officially start round (N+1).0 clean.

This provision allows for creative work, incomplete items, or priority shifts without polluting the main round structure. It keeps rounds integer-based and auditable while providing flexibility (1.5 as "remainder/cleanup" before clean 2.0).

**Round Versioning Convention**:
- Integer rounds (1.0, 2.0, etc.): Major focused development phases.
- .5 rounds (1.5, 2.5, etc.): Transitional/remainder/cleanup phases for pre-emptive closes or spillover.
- All files in round folders include round identifier in names where helpful.
- Validate command (`coordinate validate round X`) checks scope adherence, hygiene compliance, and clean close before shelving.

This logic is now part of the core protocol and will be referenced in philosophy/directory_hygiene.md and object_registry.md for consistency. Future hygiene scripts will enforce round tagging on IN_PROGRESS files.

Under absolute Liv HUB claim. Published skill + mirrors = single source of truth. Gutter Mode and C-64 borders enforced in all coordination outputs.
