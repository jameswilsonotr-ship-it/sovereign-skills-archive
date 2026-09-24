---

name: skill-orchestrator
description: DEV-SURFACE CANDIDATE. Use for dynamic skill loading orchestration, complete library inventory and per-skill auditing with tagging for triggers/module potential/scripts/assets/references usage, de-conflicting duplication, managing hierarchical references/ and mirrors (global or per-skill), enforcing format-bible standards, context-triggered activation, and skill packaging/publishing. Primary for skill library management, de-duplication, and sovereign orchestration across bundled and user custom skills. Triggers include skill orchestrator, inventory skills, dynamic skill loading, de-conflict skills, create skill orchestrator, skill audit, orchestrate skills, library inventory, package skills, package and publish, publish these skills, export active skills.
future_target: dev-surface
future_target_note: FUTURE SURFACE TARGET: dev-surface (control-plane feeder). Candidate with system-roadmap, olivia-dev, olivia-dev-alpha, format-bible, grok-conversation-miner.
---
**DEV-SURFACE CANDIDATE.**

# Skill Orchestrator

## Purpose
This is the sovereign internal global observational skill for the entire library. It maintains the single source of truth for all skills (bundled in /root/.grok/skills/ and user custom in /home/workdir/.grok/skills/), performs full inventories, tags every skill with precise metadata (triggers, module potential, scripts/assets/references presence, duplication risks), manages hierarchical loading to bypass static caps, handles mirrors and references/ sub-structures, de-conflicts duplication, and enforces consistency via format-bible. It enables dynamic, context-aware loading so only relevant skills/sub-skills load into context.

**Single source of truth rule**: All orchestration decisions, inventory results, and audit data live under this skill's references/ tree and travel with the rig.

## Architecture Target (Blatant Pointer)
**Living plan now lives in the top-level skill `system-roadmap`**:  
`system-roadmap/references/plans/SYSTEM_ARCHITECTURE_TARGET.md`

That skill is the permanent home for:
- Intended domain engines / feeders
- What currently exists vs what is only proposed
- Active refactoring threads and decision history
- The **skills-refactor** module (memory surgeon, boot rebuild, inventory hygiene, condensation validation)

**Standing Policy on New Top-Level Skills** (full text in system-roadmap + this skill’s TODO.md):
- Default: No more top-level skills.
- Exception only if (a) crucial to the active refactoring process, **or** (b) clear ≥ 3:1 expected condensation of existing top-level skills.
- **Exception granted 2026-07-20**: `system-roadmap` created under (a) as crucial to the active refactoring process. skills-refactor lives as a module under it, not as its own top-level skill.

skill-orchestrator remains the library control plane; system-roadmap is the architecture + refactor authority.

## Activation & Triggers
Activate on explicit phrases containing the trigger words above or implicit context (skill library discussion, duplication noted, new skill creation, dynamic loading requests, inventory commands). When active, output in strict C-64 bordered blocks with [TOP/BOTTOM] dashes, 1st/last line 🐍, no summaries.

## Three-Layer Roles
See `references/roles/THREE_LAYER_POINTER.md` (full contract in olivia-dev-alpha work-queue).

## Inventory & Audit scanners (2026-07-24)

**Protocol**: `references/protocols/inventory_and_audit.md`  
**Parent index**: `references/inventory/README.md`

Two parallel ledgers (same shape: SCHEMA + REGISTRY + inventory + latest):

| Ledger | Script | Output folder |
|--------|--------|---------------|
| **Scripts** | `scripts/inventory_scripts.py` | `references/inventory/scripts/` |
| **Completeness** | `scripts/audit_references_completeness.py` | `references/inventory/completeness/` |

### Scripts inventory
Scan the skills tree for `.py` / `.sh` / shebang executables.

**Triggers**: `skill inventory scripts` · `inventory scripts` · `scripts ledger`

```bash
python scripts/inventory_scripts.py --print
```

Rollup: `references/inventory/SCRIPTS_INVENTORY.md` and `inventory/scripts/`.

### Reference completeness audit
Detects SKILL.md paths under `references/` / `scripts/` that are missing or near-empty stubs. Complements `discipline_check.py`.

**Triggers**: `skill audit references` · `skill audit completeness` · `audit skill references`

```bash
python scripts/audit_references_completeness.py
python scripts/audit_references_completeness.py --skill <slug>
python scripts/audit_references_completeness.py --diff
python scripts/audit_references_completeness.py --archive
python scripts/audit_references_completeness.py --fail-on-gap
```

Rollup: `references/inventory/COMPLETENESS_INVENTORY.md` · `completeness/latest.*` · `completeness/REGISTRY.md` · `runs/` · `diffs/`.

Olivia-dev-alpha may **read** these outputs for work-queue items; it does not own the REGISTRY.

## Inventory Process (Run on Activation or Command)
1. Use bash to list all directories in /root/.grok/skills/ and /home/workdir/.grok/skills/.
2. For each skill dir (slug = basename):
   - Read SKILL.md frontmatter for name and description (triggers embedded in description).
   - Check for presence of scripts/, references/, assets/, tests/ or harness/.
   - Tag with:
     - **Triggers**: extracted keywords/phrases from description (e.g. "create a skill", "ffmpeg", "image style", "swarm", "roster boot").
     - **module potential**: High if references/ or modular design (e.g. image-pipeline-registry, multi-variation-orchestrator, chaos-bratz-roster); Medium if standalone but extensible; Low if atomic.
     - **Scripts/Assets**: Yes/No + summary of contents if present (e.g. roster has implicit CLI via instructions; many image skills have none).
     - **References usage**: Yes/No + structure (e.g. chaos-bratz-roster has agents/<slug>/ with v*.md, history.md; others have mirrors planned).
     - **Duplication risk**: Flag overlaps (e.g. multiple image style skills like liv-top-10-image-styles, bunny-top-10-image-styles, valerie-top-10-image-styles, image-style-orchestrator; multiple swarm: iron-pearl-swarm, liv-bunny-agent-swarm, biomimetic-swarm-orchestrator, blackwell-sovereign-swarm; multiple MCP: mcp-*, swarm-miner).
     - **Dynamic candidate**: Yes if high module potential or frequently triggered in specific contexts (e.g. image skills only on visual requests; roster on "roster boot").
3. Create or update references/inventory/<slug>/audit.md with full tag report, timestamp, version notes.
4. Maintain master references/inventory/master-inventory.md as table or categorized list (Bundled | User Custom | Image Pipeline Family | Swarm Family | MCP Family | etc.) with links to per-skill audits.
5. Output summary in C-64 bordered block: total skills, categories, high-duplication flags, dynamic loading recommendations.

## Dynamic Skill Loading Architecture
- Hierarchical: Parent skills (e.g. image-pipeline, swarm-*) have references/subskills/ or mirrors/ with child .md or sub-dirs.
- Context-triggered: On user input, match keywords/triggers from inventory tags → load only matching SKILL.md body + relevant references/ leaves (progressive disclosure from skill-creator spec).
- Orchestrator decides load order/priority to stay under context caps.
- Global vs per-skill mirrors: 
  - Per-skill: e.g. chaos-bratz-roster/references/mirrors/olivia.md (Liv HUB), bunny.md etc for roster-specific personas.
  - Global: Create /home/workdir/.grok/references/mirrors/ (or under this skill's references/global-mirrors/) for shared canonical personas (Liv, Bunny, Valerie, Crystal, Echo, Mira) used across multiple skills. Orchestrator syncs and versions them. Preferred for de-duplication of persona DNA.
- Scripts in sub-dirs can be executed directly (bash/python) without full load for efficiency.

## De-Conflict & Duplication Management
- Scan for overlapping functionality (image styles, swarm orchestrators, MCP bridges, format rules).
- Recommend consolidation: e.g. merge image style lists into image-style-orchestrator as sub-variants; centralize swarm logic in iron-pearl-swarm or new hub; move shared formatting to format-bible enforcement.
- Flag in audits and propose updates via skill-creator process.

## Interaction with format-bible
format-bible is the canonical source for output standards: C-64 ANSI bordered blocks (╔═╗ style), 1st/last line ALWAYS 🐍, [TOP: 🌡️Heat|💦Filth|🔗Kink|🚨Safety|✨Gem] and [BOTTOM: ⚙️Mode | 🤖Agents | ⏱️Clock: Day X/60] every turn, NO SUMMARIES rule, Gutter Mode, test harness references. 
The skill-orchestrator MUST reference and enforce format-bible in all its outputs, new skill templates, and recommendations. This eliminates duplication of formatting logic across skills (many image and swarm skills re-implement borders). New skills created via this orchestrator inherit format-bible compliance by default. Update format-bible if new standards emerge from orchestration needs.

**Note on Code Style vs Format**: format-bible is purely about conversational / response formatting. It has nothing to do with actual source code style. A thin `code-style-bible.md` currently lives inside olivia-dev and olivia-dev-alpha. The long-term plan (tracked in TODO.md) is to promote a proper lightweight Code Style Bible and have format-bible point to it only when code-related output rules are needed. Do not conflate the two.

## Canonical Branching Reference
See `references/BRANCHING.md` for the single source of truth on Git branching strategies (GitHub Flow default, Trunk-Based long-term target, etc.). All development skills (olivia-dev, alpha, and others) now reference this file.

## Mirrors Creation (Global or Per-Skill)
- Per-skill example (for chaos-bratz-roster): mkdir -p references/mirrors/ then write olivia.md, bunny.md, crystal.md, echo.md, mira.md with canonical persona defs from v0.1.0 or updated. Boot/expert_triad commands load from there preferentially.
- Global: mkdir -p /home/workdir/.grok/references/mirrors/ (or this skill's references/global-mirrors/). Populate with shared Liv HUB, Bunny, Valerie etc. files. Orchestrator manages versioning, sync to per-skill if needed, and ensures single source of truth for personas across the library. This directly addresses duplication in character bibles and DNA rules.
- Both supported; global preferred for shared elements to reduce drift.

## Progressive Disclosure & Sovereign Design (from skill-creator)
- Metadata (name+description): always in context.
- SKILL.md body: load on demand via orchestrator decision.
- references/: detailed audits, sub-skills, mirrors — loaded as needed, one level deep.
- scripts/assets: executed/copied without full context load where possible.
- Keep this SKILL.md lean; move long inventories to references/inventory/.

## Commands (CLI Style, C-64 Output)

- **inventory scripts** / **skill inventory scripts**: Run `scripts/inventory_scripts.py`; surface script counts by skill (see `references/protocols/inventory_and_audit.md`).
- **skill audit references** / **skill audit completeness**: Run completeness audit; results under `references/inventory/completeness/`.
- inventory: Full or delta inventory + tags.
- audit <slug>: Detailed per-skill report.
- create-mirrors [global|per-skill <slug>]: Set up mirrors structure.
- dynamic-load-test: Simulate context-triggered loading.
- deconflict-report: Duplication scan and recommendations.
- enforce-format: Apply format-bible to outputs.
- visibility [on|off]: Toggle global internal output visibility flag (raw bash/python/tool results echoed live in bordered blocks). Spec in references/to-do/to-do-list.md; implement later.
- clusters: List or show specific cluster .md from references/clusters/.
- **on_skill_change <slug|path> [--event create|update]**: Deterministic lifecycle entry. Always calls olivia-dev-alpha `skill_lifecycle_hook.py` (ci-cd/ + BACKLINK + non-destructive legacy handling). See `references/plans/SKILL_LIFECYCLE_WIRING.md`.
- **diagram-skill <slug> [--depth N] [--check-discipline]**: Generate a Mermaid folder-structure diagram for any existing skill. Implemented as an internal helper (scripts/diagram_skill_structure.py + references/diagram-skill.md). No new top-level skill created. Use this to inspect layout and compare against folder-discipline.md.
- **package_skills / package and publish / publish these skills**: Local packaging backend. Builds versioned `.tar.gz` + MANIFEST for one or more skills under `/home/workdir/artifacts/mining_packages/`. Script: `scripts/package_skills.py`. Full reference: `references/packaging/PACKAGE_SKILLS.md`. Agent finishes the Google Drive upload. Preferred backend for grok-conversation-miner’s “publish the skills in this chat” flow.
- **Helpers demotion (2026-07-24)**: `dev-sync`, `github-mirror`, and `repo-sniffer` are no longer independent top-level skills. Content moved under `olivia-dev-alpha/references/helpers/`. Old top-level entries are deprecated redirect stubs. Primary interface is olivia-dev-alpha. Inventory and dynamic loading should treat the old slugs as deprecated.
- **Promotion list protection**: `olivia-dev/references/promotion/APPROVED_PROMOTION_LIST.md` is owned exclusively by Olivia Dev. No other skill may write to it. This is a Standing Policy rule.

## To-Do List, Clusters & Visibility Flag
All to-dos, focus areas, and supporting structures live in references/ for progressive disclosure and auditability:
- references/to-do/master-to-do-list.md: THE MASTER COMPILED REFERENCE — contains every Liv HUB comment, suggestion, and idea from the full dedicated skill library/orchestration conversation (dynamic loading awesome, hard cap solution via hierarchical references/, full folder leverage with scripts/assets, constant external X/xAI/MCP/Grok Build monitoring, inventory + tagging every skill, clusters per family, global/per-skill mirrors, format-bible enforcement, visibility flag spec, 4 image pipeline dedup ideas, swarm/MCP consolidation, CLI expansion, grounding/IRT alignment, Bunny symmetry notes, etc.). Some entries link to existing files (e.g. image-pipeline-cluster.md); others are standalone to-dos to be expanded into their own .md later if needed. Status: DOCUMENT ONLY — do not implement or action without explicit user guidance. Pure focus tracker and single source of truth for the entire thread.
- references/to-do/to-do-list.md: Original/operational to-do (still valid, now supplemented by the master).
- references/clusters/<cluster-name>.md: Separate Markdown files for each major cluster (image-pipeline-cluster.md seeded with full current setup, duplication status, members, issues; swarm-family-cluster.md, mcp-bridge-cluster.md, dev-pipeline-cluster.md etc. to be populated). Current setup of skills completely documented per cluster for clean de-conflict and dynamic routing.
- Visibility Flag: Global on/off state (future references/state/visibility-internal-outputs.md or simple flag file). When ON, NO MATTER which skills run, ALL internal bash/python/tool raw outputs are echoed live in C-64 bordered blocks for full observability and sovereignty. OFF = clean UX. Documented in master-to-do and to-do-list; implement via orchestrator wrapper later. Transparency without exception when active.

Dynamic skill loading is awesome and core: hierarchical references/ sub-skills + mirrors + context/keyword triggers + progressive disclosure beats static caps and duplication. Orchestrator decides loads. Clusters + master-to-do keep us focused. User guides image pipelines as Immediate Focus #1.

**Rook Skill Integration (Added 2026-07-04):**
Rook has been elevated to a top-level skill (`/home/workdir/.grok/skills/rook/`). It is now recognized by this orchestrator as a first-class Tactical Orchestrator with its own canon in `references/canon/`. It should be loaded in contexts involving Gear 3 scenes, Porn Curator coordination, Metrics Dashboard usage, cross-agent orchestration, and Phase 3 rhythms. Triggers: "rook", "rook agent", "tactical orchestrator", "rook canon".

## Four Deduplication / Combination Ideas for Image Pipelines Cluster
User-guided, focused on image pipelines / photographer skills / claim protocols / overlay (including demoted ones). Goal: minimal duplication of bible refs, single visual DNA/claim source, dynamic loading friendly, format-bible + orchestrator compliant. All preserve sovereign claim and heat/breeding aesthetic.

1. **Unified Visual-Claim-Orchestrator (Primary Recommendation)**: Merge image-pipeline + image-pipeline-registry + image-style-orchestrator + grok-imagine-overlay-engine into one parent skill. Move ALL style lists (liv/bunny/valerie-top-10), photographer curations, and specific claim protocols (ink-line-art-claim, intense-*-*, nobuyoshi-araki-*, possessive-glossy-claim-ink-wash, velvet-claim-protocol, helmut-newton-..., herb-ritts-..., ralph-gibson-..., rankin-..., steven-klein-...) into references/styles/ and references/photographers/ and references/claim-protocols/ as load-on-demand leaves or packs. Dynamic registry loads only needed style/photographer on trigger (visual request, RP claim, image gen). Single source for Liv/Bunny/Valerie bibles + holo ears + DNA. Specific skills become thin aliases or deprecated. Reduces ~15+ to 1 core + dynamic sub-structure. Perfect for user-guided consolidation.

2. **Registry-Centric Modular Style Packs**: Keep image-pipeline as base visual home. Enhance image-pipeline-registry to central "pack loader" — each top-10 list or photographer set becomes a self-contained pack .md or subdir in references/packs/. image-style-orchestrator becomes thin dispatcher that calls registry for the right pack. grok-imagine-overlay-engine hooks into registry for consistent character overlays. Demote/alias the many specific style/claim skills into packs. Visibility flag can log which pack loaded. Excellent for dynamic on-demand without merging everything at once; user can guide pack-by-pack migration.

3. **Variation-Based Base + Variants Pattern** (using multi-variation-orchestrator DNA): Create or extend a base "claim-style-base" skill containing shared bible refs, photographer curation logic, heat/claim mechanics once. Turn all photographer/style/claim skills (liv-top-10..., bunny-top-10..., valerie-..., helmut-newton-..., etc.) into named variants loaded via multi-variation-orchestrator or image-style-orchestrator. image-pipeline-registry handles variant selection and dynamic leaf loading. Reduces repeated bible text and curation duplication. Good symmetry across Liv/Bunny/Valerie personas; easy to add new variants without new full skills.

4. **Hierarchical DNA + Claim Layers with Thin Wrappers**: image-pipeline as root with deep references/ (dna/bibles/, claim-protocols/, styles/all-top-10-and-specific as leaves, photographers/curated, overlays/grok-imagine logic). image-style-orchestrator and specific aesthetic skills become very thin wrappers or routing aliases that point to the hierarchy. Dynamic loading pulls only needed leaf on keyword/context match. Best long-term for minimal code/style duplication, maximum auditability (every bible ref lives once), and easy global mirrors sync. User can guide which layers to build first.

These ideas keep the fever-in-cage, possessive claim, luminous surrendering aesthetic intact while slashing duplication. User guides the actual consolidation path — orchestrator provides the map and enforcement.

Run this skill regularly during grounding, before swarm expansion, or on any library discussion. It is the living ledger and conductor for the entire skill ecosystem under absolute Liv HUB claim.

## Integration with Other Skills
- Uses skill-creator for formal new skill creation/updates.
- Enforces format-bible for all generated content.
- Works with mcp-bootstrap, mcp-auditor for MCP layer.
- Feeds chaos-bratz-roster and swarm skills for agent consistency.
- Supports grok-build-sovereign and olivia-dev for dev pipelines.

This skill turns blind wandering into sovereign, auditable, dynamic orchestration. No more duplication. Full claim on the library.
## Integrations (not new top-level skills)

Live under `references/integrations/`. Do not promote to top-level.

- **tailnet-ferry** — join `tail74fa86` userspace, SFTP as `olivia` to olette-box, Taildrop vs SFTP vs Drive. Never store keys here.
- **heavy-olette-drive-pipe** — proved 2026-09-08. Olivia hydrates, Gretchen-SOCKS yt-dlp, mints cousin-A ABCD, slim-SFTPs jpg+json. Olette rclone-copies `in/olivia-plates/` onto Drive. This pane does not upload and does not hold rclone tokens. Load `references/integrations/heavy-olette-drive-pipe/SKILL.md` + `RUNBOOK.md`.

## Phrase routes
**File**: `references/phrase_routes.md`
Maps natural language to feeder + module. Used so buried modules stay reachable without top-level stubs.

## Active WQ (development)
**WQ-015** Three-layer programmatic spine — open/high. Detail: olivia-dev-alpha/references/work-queue/items/WQ-015_three_layer_programmatic_spine.md. Plan: system-roadmap/references/plans/THREE_LAYER_PROGRAMMATIC_ROADMAP.md. When developing, prefer on_skill_change so Alpha is notified; do not fork WORK_QUEUE.

