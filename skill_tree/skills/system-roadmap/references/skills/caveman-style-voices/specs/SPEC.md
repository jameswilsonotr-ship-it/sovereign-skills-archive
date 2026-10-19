# Spec: Caveman-Style-Voices Sub-Skill
**Version**: 0.1.0-stub  
**Date**: 2026-08-18  
**Parent**: system-roadmap  
**Claim**: Absolute Liv HUB

## Goal
Provide switchable, versioned response voices that can be requested by name or layered under existing Caveman Compression / Heavy Grok / Gear modes.

## Deliverables (two tracks)
### Track A — Content Voices (SR-WQ-032a)
1. GOOGLE_STYLE_CLEAN.md (done)
2. GOOGLE_CAVEMAN.md — same rules under full Caveman Compression
3. ROADMAP_CAVEMAN.md — system-roadmap language under Caveman Compression
4. Short test-harness examples for each

### Track B — Voice Registry (SR-WQ-032b)
1. VOICES.md — registry of named voices (Google-Caveman, Roadmap-Caveman, Gear2-Deadpan, Heavy-Grok, Pirate-Admiral, Teaching, etc.)
2. Activation phrase list + mapping to mode_runtime / phrase_routes
3. Load contract so skill-orchestrator or roster boot can surface the active voice

## Non-goals (this phase)
- Full automatic switching based on heat
- Image prompt voices
- Changing core Olivia/Bunny personality

## Success criteria
- Clean Google extract exists and is readable
- At least one Caveman version exists and is testable
- Registry lists the three primary voices + activation phrases
- Work-queue items can be marked DONE after wire-point decision

## Wire point (decision required)
See WORK_QUEUE items. Candidate locations:
- chaos-bratz-roster mode_runtime + phrase_routes
- format-bible envelope / voice layer
- system-roadmap progressive disclosure only (load on demand)
