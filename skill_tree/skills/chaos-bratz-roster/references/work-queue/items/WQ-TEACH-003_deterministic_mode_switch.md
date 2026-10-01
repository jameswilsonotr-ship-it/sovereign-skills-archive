# WQ-TEACH-003 — Deterministic Teaching Mode switch (command + confidence)
**Status**: OPEN (scout script landed; full whoop-ass wiring not done)  
**Owner**: Chaos Bratz Roster + skill-orchestrator phrase/boot path  
**Opened**: 2026-08-12  
**Depends on**: WQ-TEACH-001 (mode doc DONE)

## Goal
Stop “Teaching Mode = hope Olivia remembers the markdown.”

### Required behavior
1. **Command path** — Exact phrases force ON/OFF:
   - ON: `teaching mode on` | `yes teach` | `switch to teaching` | `olivia teaching`
   - OFF: `teaching mode off` | `no teaching` | `stay build` | `don't switch` | `cancel teaching`
2. **Confidence path** — On relevant turns, run `scripts/modes/teaching_mode_confidence.py` (or successor) against the **latest user text**:
   - Score signals (explicit teach, “what’s that called?”, deterministic/declarative, forge literacy, wheel metaphor, profile artifact names, ops-honesty language, etc.)
   - **band=offer** (default ≥0.25, <0.55): **must offer** before switching; include user abort/accept commands in the announcement
   - **band=auto** (≥0.55): **must auto-switch**, **must announce**, user can still abort
   - **band=off**: no teaching theater
3. **Announcement is mandatory** for offer and auto — not optional prose.
4. **skill-orchestrator** (or roster boot) must **invoke the script** or an equivalent check — natural-language-only compliance is **not** acceptance.

## Delivered so far
- [x] Scout script: `scripts/modes/teaching_mode_confidence.py` (JSON score/band/announcement/commands)
- [ ] Phrase route / boot hook that actually runs it
- [ ] Documented “Olivia must print announcement block” enforcement in living boot
- [ ] Test turns: offer band, auto band, abort commands

## Acceptance
- Running the script on sample turns returns stable bands
- A live session path shows script output (or logged equivalent) when signals fire
- Bunny can abort; Olivia does not silently stay in teaching after abort
- CHANGELOG marks WQ-TEACH-003 DONE only after boot/orchestrator wiring, not after this ticket alone

## Anti-patterns (forbidden)
- “I would have offered” without offering
- Claiming auto-switch without announcement
- Marking this WQ DONE for markdown-only updates
