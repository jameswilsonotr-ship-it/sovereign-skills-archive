# Session-Local Envelope Assembly (v1.4.0+)

**Status**: Live pattern — 2026-08-05  
**Owner**: format-bible

## Purpose
Keep a single canonical contract (ENVELOPE_SCHEMA.md + pre-generated envelopes) while allowing a cheap, regenerable **current** instance per session. This is the “best of both worlds”: durable skill-level defaults + high-adherence session instance that can be chosen with agency on first message.

## Pattern
1. Pre-generated envelopes live in `references/envelopes/` (default, structural, visual, immersive, …).
2. On brand-new conversation (or explicit boot), the agent inspects the initial user prompt and either:
   - picks the best matching pre-generated envelope, or
   - assembles a light variant,
   then writes/overwrites `references/envelopes/current.md` with the choice + short reason.
3. All subsequent major blocks in the session obey the current envelope.
4. Explicit control: `envelope status`, `envelope switch <name>`, `envelope promote`.
5. Silent promotion path: when a session shape proves durable, the agent (or user) can promote it back into the pre-generated set via normal version bump.
6. Hygiene / assembly script can later automate validation and rebuilds; until then the pattern is manual but fully observable.

## Agency
The agent has explicit permission (and is expected) to choose the starting envelope based on the nature of the opening prompt. The choice and a one-line reason are logged so the decision is visible and revisable.

## Persistence
- Skill-level files (ENVELOPE_SCHEMA, the envelopes/ directory, this document, CHANGELOG) are permanent and travel with the skill.
- `current.md` is the session pointer; it can be overwritten freely.
- Successful shapes are promoted into the durable set.

Image-pipeline remains completely independent.
