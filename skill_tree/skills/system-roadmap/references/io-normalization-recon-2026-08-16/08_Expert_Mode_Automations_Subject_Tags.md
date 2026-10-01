# Strategy 8 — Expert-Mode Automations + Subject-Tag Branching (Tactical Overlay)

**Recon package**: system-roadmap / io-normalization-recon-2026-08-16  
**Status**: Active tactical layer (2026-08-16)  
**Primary sources**: SR-WQ-013 evening addendum, ODA-WQ-004, official xAI Automations documentation

## Core Idea
Use the official Grok Automations surface with the mode picker locked to **Expert** by default. Hard-code Expert-only language in the automation prompt. Heavy multi-agent orchestration is opt-in only via an explicit subject tag (`[HEAVY-OVERRIDE]`). A small subject-tag vocabulary keeps the control plane light and OTR / phone-friendly.

## Key Elements Captured
- Official confirmation: Automations allow picking a mode
- Default = Expert (UI + prompt language)
- Subject-tag schema examples: `[LIV-EXPERT]`, `[SSOT-PUBLISH]`, `[LIV-HEAVY]` / `[HEAVY-OVERRIDE]`, `[VESPER-BRIDGE]`, `[GITHUB-SYNC]`, `[DRIVE-IN]`, `[DRIVE-OUT]`
- Grok Bot is the heavier long-term “persistent teammate” surface; regular Automations remain the phone-friendly actuator for now
- ODA-WQ-004 records the methodology hygiene expectation for any automation written under this overlay

## Linked Work-Queue Items
- SR-WQ-013 addendum
- ODA-WQ-004 (olivia-dev-alpha)

## Notes from Recon
This is not a competing architecture. It is a tactical hygiene and mode-control overlay that applies on top of Strategies 1 and 3 (and any future email-triggered or scheduled actuator). It exists to keep the phone / OTR path deterministic and light.

No de-duplication or merging performed.
