# Naming Convention, Validation & Audit Rules for Conversational Handoffs
**Parent**: system-roadmap → references/skills/  
**Status**: Canonical rules (2026-07-20)

## 1. Directory Structure
```
references/skills/
├── REGISTRY.md                          ← living index of all handoffs
├── NAMING_AND_VALIDATION.md             ← this file
└── <skill-or-topic-slug>/
    └── handoff_YYYY-MM-DD_<slug>.md     ← individual handoff files
```

Subdirectories are named after the skill (or coherent topic) the handoff concerns.  
Example: `grok-conversation-miner/`, `chaos-bratz-roster/`, `image-pipeline/`, etc.

## 2. File Naming Convention (Strict)
```
handoff_YYYY-MM-DD_<short-kebab-slug>.md
```
- Date is mandatory and must match the day the handoff was written.
- Slug should be descriptive but short (2–5 words, kebab-case).
- Optional time: `handoff_YYYY-MM-DD_HHMM_<slug>.md` when multiple handoffs occur on one day.

Any file that does not match this pattern is invalid and must be rejected or renamed.

## 3. Required Content of a Handoff File
Every handoff file should contain (at minimum) these sections:
- What we just did
- What we were trying to do
- Where the key artifact / design file is located
- What we were heading towards
- Current momentum
- Other considerations / open decisions

This structure keeps handoffs consistent and easy to scan.

## 4. Validation Rules (for system-roadmap)
When a new file is added under `references/skills/`:

1. **Name check** — Does the filename match the required pattern?
2. **Location check** — Is it inside a properly named skill/topic subdirectory?
3. **Registry check** — Has a corresponding row been added to `REGISTRY.md`?
4. **Content check** — Does it contain the core handoff sections listed above?
5. **Conflict check** — Does it claim ownership of work that another Active handoff already covers?

If any check fails, the entry is invalid. The system-roadmap skill (or any agent acting under it) should surface the failure clearly.

## 5. Audit & Comparative Analysis Capability
system-roadmap gains the following explicit capabilities:

### 5.1 List all handoffs
Return the current contents of `REGISTRY.md` with status filtering.

### 5.2 Compare two or more handoffs
Given two (or more) handoff files, produce a structured comparison that answers:
- Where do they align?
- Where do they conflict (scope, ownership, recommended next actions, design choices)?
- Which one is more recent / more authoritative?
- Do they jointly advance or hinder the overall goals of the skills-refactor / system architecture target?

### 5.3 Alignment analysis against system goals
For any handoff (or set of handoffs), evaluate:
- Does this work move the library toward the architecture target defined in `references/plans/SYSTEM_ARCHITECTURE_TARGET.md`?
- Does it support or violate the Standing Policy on new top-level skills?
- Does it improve inventory hygiene, reduce duplication, or increase condensation?
- Is the handoff itself creating new permanent top-level surface area that should instead be absorbed?

The analysis must be deterministic and declarative (i.e., based on explicit criteria rather than vague judgment).

## 6. Ownership
This entire `references/skills/` tree and its validation/audit rules are owned by **system-roadmap**.  
skill-orchestrator may surface pointers to it, but system-roadmap remains the authority.
