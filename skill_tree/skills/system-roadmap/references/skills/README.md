# references/skills/ — Conversational Handoff System

**Owned by**: system-roadmap  
**Created**: 2026-07-20

This directory is the permanent home for **conversational handoffs** — structured, self-contained documents that allow one conversation to cleanly pass incomplete or design-stage work to another conversation without conflict or lost context.

## Contents
- `REGISTRY.md` — living index of every recorded handoff
- `NAMING_AND_VALIDATION.md` — strict naming rules + validation + audit capabilities
- `<skill-or-topic>/` — one subdirectory per skill or coherent topic
  - individual `handoff_YYYY-MM-DD_<slug>.md` files

## Why this exists
When two conversations need to touch the same skill (or the same design problem), we use a formal handoff instead of racing or overwriting each other. The handoff carries intent, momentum, open decisions, and pointers to the actual design artifacts.

## Related Capabilities (system-roadmap)
- Validate new entries against naming and content rules
- Maintain the registry
- Audit and compare multiple handoffs
- Analyze alignment or conflict with the overall system architecture target and skills-refactor goals
