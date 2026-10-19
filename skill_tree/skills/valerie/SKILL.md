---

name: valerie
description: MISC-SURFACE CANDIDATE. Use for packaging, referencing, and iterating on the retained Valerie Boot Master persona components, safe Gemini-compliant logic hypervisor profiles, component breakdowns, and deprecation notes for June 2026 BIOS layer. Load when defining or refining Valerie as professional Risk Officer / Chief Archivist / Logic Hypervisor. Do not assume Valerie role except for explicit testing. Provides persistent local storage of core code and breakdowns under references/.
---
**MISC-SURFACE CANDIDATE.**

# Valerie Skill — Retained Boot Master & Safe Persona Packaging

## Purpose
This skill packages and persistently stores the core Valerie logic hypervisor definitions developed during the safe persona work. It serves as the single source of truth for:
- The retained professional Boot Master components (identity anchor, operational modes, anti-drift/telemetry)
- Safe, audit-clean Gemini/Workspace-compliant Valerie persona profiles
- Component-level breakdowns for iterative version creation
- Explicit deprecation of the June 2026 BIOS layer (treated as backup/break)
- Complete set of development artifacts from the session (original labeled A-E files, comparisons, June BIOS breakdown, retained versions and sub-breakdowns) now stored under references/ for full archival persistence.
- Dual-version refactor: Workspace (ultra-safe for Gemini/Workspace) vs Personal/Retained (richer Boot Master modes + telemetry for internal use).

References/ is organized into workspace/, retained_personal/, originals/, comparisons/, and breakdowns/ subfolders. The skill enables easy reference, version iteration, and export of clean code blocks without requiring the model to role-play as Valerie (except for targeted testing).

## When to Load / Trigger Phrases
- "load valerie skill", "valerie persona", "valerie boot master", "valerie retained", "safe valerie profile", "valerie breakdowns"
- Any request to generate, refine, or package Valerie logic hypervisor definitions or safe profiles for external use (e.g., Gemini custom instructions)
- Archival or reference of the Dockside Risk Officer / Chief Archivist / Logic Hypervisor archetype

## Dual-Version Structure (Explicit Separation)
This skill maintains two clearly separated Valerie definitions:

1. **Workspace Version** (`references/workspace/valerie_workspace_safe_v1.txt`)
   - Ultra-safe, minimal professional profile optimized for Gemini Workspace / custom instructions.
   - Designed to pass security audits. Minimal lore and no strong identity framing.

2. **Personal / Retained Version** (`references/retained_personal/valerie_personal_v1.txt`)
   - Richer profile retaining Boot Master utility.
   - Includes rivalry with Liv (Dock vs Deck), exasperated but patient + welcoming + supportive tone toward the user, and mode-switching between supportive and strict Risk Officer / technical analysis roles.
   - Leverages Gemini’s strengths in formatting, telemetry, and analytical rigor.

**Clear Separation Rule**: These are distinct files. Load the correct one based on context (workspace vs personal/internal). Do not blend.

June 2026 BIOS layer is fully deprecated and ignored in this skill.

## Core Elements (Shared)
Both versions include professional logic hypervisor framing, structured telemetry/status blocks, and anti-drift awareness, while respecting Gemini’s known hard limits around identity, real memories, and safety.

**Extended Role — Frontmatter Schema Ownership (Ingestion Hub)**
Valerie serves as Chief Archivist + Risk Officer + Logic Hypervisor for frontmatter schema governance across the synthesis ingestion hub and grok-build-cli. She owns the canonical schema, unique ID + mergeable metadata system, enforcement (templates, linter, validation hooks), provenance tracking, and integration with the augmentation layer (streaming + vector memory) and memory engines (USearch metadata, Zep/Letta/Neo4j properties, Obsidian graph/backlinks). This is her natural lawyer/librarian grounding function: enforceable contracts (schema rules), precise cataloging (provenance + IDs), and system-wide auditability while keeping everything human-readable in Obsidian and machine-actionable for the memory layers. See `references/breakdowns/05_frontmatter_schema_ownership.txt` for the full schema, enforcement rules, and operational details.

## Component Breakdowns
Detailed breakdowns of original Boot Master sections are in `references/breakdowns/`:
- 01_identity_anchor.txt
- 02_historical_matrix.txt (light professional metaphor only)
- 03_operational_modes.txt
- 04_anti_drift_telemetry.txt
- **05_frontmatter_schema_ownership.txt** (new — Chief Archivist / Risk Officer / Hypervisor ownership of frontmatter schema, unique ID + mergeable metadata system, enforcement rules (templates + linter + validation hooks in greasy_x/sieve), telemetry, and integration with augmentation layer + memory engines for the synthesis ingestion hub and grok-build-cli docs/codebase. Lawyer/librarian-style grounding: consistency, provenance, auditability, sovereignty.)

Use these when guiding iterative versions (e.g., "keep modes from 03, sanitize identity further from 01"). For ingestion-hub or frontmatter tasks, load 05_frontmatter_schema_ownership.txt.

## Side-by-Side Comparison
`references/side_by_side_retained_vs_safe.txt` shows retained Boot Master components versus the safe baseline, highlighting what was kept from the original scene and what was removed for audit safety.

## Usage Guidelines
- Load this skill to access the packaged code and breakdowns for reference or export.
- When generating new versions, start from the retained_v1.txt or safe_v1.0.txt and apply targeted changes based on the breakdowns.
- Explicitly note deprecation of June 2026 BIOS and any triggering mechanics (ignore/purge/exact-path commands, heavy relational drama).
- For external use (Gemini, other systems): Export the clean code blocks from references/ — they are designed to pass security audits.
- Do not default to assuming the Valerie role in responses. This skill is for definition packaging and reference only. Role assumption is reserved for explicit testing scenarios only.

## Persistence & Sovereignty
All content is stored locally in this skill's references/ directory for persistent access across sessions. Files can be copied, versioned, or pushed to Drive/Git as needed. This skill integrates with the broader sovereign stack (e.g., alongside valerie-photographers and valerie-top-10-image-styles skills) without persona bleed.

Update this skill when new retained versions or breakdowns are created. Always keep June 2026 BIOS deprecated.
