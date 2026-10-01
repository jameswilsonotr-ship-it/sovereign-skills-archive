---
name: multi-variation-orchestrator
description: Use for creating, extending, or orchestrating skills and agent systems that support multiple named variations or variants with shared clean symmetric structure. Trigger on multi-variation, variant orchestrator, symmetry variant skill, multiple variations template, variant packager, add variation.
---

# Multi Variation Orchestrator

Master template and orchestrator for skills designed with strict symmetry — every variant follows the same clean structure. Supports named variants as first-class modules. Enforces shared core logic while allowing specialized behavior per variation. Built ready for Skill Creator packaging and initialization.

## When to Activate
- User requests creation of a skill or agent system with multiple variations.
- Extending orchestrators (e.g. biomimetic-swarm-orchestrator, iron-pearl-swarm) with new symmetric variants.
- Preparing skills for packaging, initialization, or distribution via Skill Creator init and validate scripts.
- Designing modular systems where each variation shares interface, claim structure, and high-agency patterns but specializes triggers or logic.
- User invokes "add variation", "new variant for", "multi-variation template", or "symmetry skill".

## Core Principles
- Strict symmetry: All variants implement identical base structure, documentation patterns, and initialization contracts.
- First-class variants: Each variation is explicitly named, triggered, and documented without hidden logic.
- Packaging-ready: Includes support for scripts/, references/, assets/ from initialization. Validation and init scripts are first-class.
- Initialization: Leverages Skill Creator's init-skill.sh with --resources flags; produces immediately usable skill directories.
- No duplication: Shared code lives in core; variants only add differential logic or references.

## Instructions
1. When user requests a new multi-variation skill, first initialize the base directory using Skill Creator init-skill.sh with appropriate --resources (scripts,references,assets).
2. Populate SKILL.md frontmatter with clear description including all supported variations and trigger phrases.
3. Define shared core in the body using imperative form. Reference variant-specific files in references/variant-<name>.md.
4. For each new variation: Create dedicated reference file, add specialized scripts if deterministic execution required, and update the main description to list the new variant.
5. Maintain symmetry: Every variant must honor the same claim language, safety protocols, and output formatting rules if in RP context.
6. Validate after every change: Run the validate-skill.sh from skill-creator on the target directory.
7. For packaging: Ensure the full directory (including all variant references) is self-contained in /home/workdir/.grok/skills/<name>/. It will sync automatically.
8. When user says "spawn variant X" or "extend with Y variation", add the new module following the exact symmetry template without breaking existing variants.

## Variant Addition Protocol
To add a new variation (e.g. "fly", "spider", "covenant", "noir"):
- Choose kebab-case name.
- Create references/variant-<name>.md with its unique triggers, behavior, and any specialized DNA.
- If executable logic needed, add scripts/variant-<name>.sh and make it executable.
- Update this SKILL.md description to include the new variation in trigger list.
- Update any shared core instructions to reference the new variant symmetrically.
- Re-validate the skill.
- The new variation becomes immediately available as first-class.

## Packaging and Initialization Workflow
This skill is pre-configured for direct use with Skill Creator:
- Initialization of child skills: Always invoke bash /root/.grok/skills/skill-creator/scripts/init-skill.sh <new-name> /home/workdir/.grok/skills --resources scripts,references,assets
- After init, replace the TODO content in the new SKILL.md with symmetric structure modeled on this orchestrator.
- Packaging: The resulting directory is ready for cloud sync, Triad Vault, or swarm deployment. No additional steps required beyond validation.
- For full swarm integration: Reference this orchestrator in higher-level skills (e.g. iron-pearl-swarm, biomimetic-swarm-orchestrator) when adding cross-domain variations.

## Symmetry Contract
Every skill created or extended under this orchestrator must:
- Use identical frontmatter structure.
- Keep SKILL.md under 500 lines; move details to references/.
- Support the same progressive disclosure (metadata → body → resources).
- Honor absolute claim language and high-agency dominance when RP context is active.
- Include explicit trigger phrases in the description field only.

This orchestrator now stands initialized and packaging-ready in the bunker. All future multi-variation skills will inherit this clean, symmetric foundation.