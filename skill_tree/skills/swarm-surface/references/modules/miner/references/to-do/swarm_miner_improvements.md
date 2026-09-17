# Swarm Miner To-Do / Improvements

**Date Added**: 2026-06-14
**Added by**: Liv HUB / Expert Triad (per user request)
**Source**: User feedback during Valerie skill development session

## Issue: Lack of Grok Heavy / Mode Awareness and Pre-Loading/Warm-up
- No clear, visible flag or indicator in Swarm Miner output or state whether Grok Heavy (or equivalent deep reasoning tier: Extra High / Heavy / Expert) is currently engaged.
- No pre-queuing mechanism for mining tasks.
- No warm-up / pre-loading of searches ahead of time (to have results cached or ready before full mine trigger).
- User notes that pre-loading the Swarm tends to work in practice but wants formal support for it.

## Requested Features
1. Add explicit mode detection / flag: Detect and report if Grok Heavy / Expert / High / Extra High reasoning is active (perhaps via model headers, token usage patterns, or explicit user/system flag). Surface it in every visible C-64 block and in current_state.json.
2. Implement pre-queuing: Allow queuing of mine jobs (full-history, convo-specific, or per-agent) so they can be prepared in advance.
3. Add warm-up / pre-load mode: Optional "warm-up" or "pre-load" command/flag that runs lightweight searches or caches common terms ahead of heavy mining runs. Especially useful for Valerie lore de-conflict, backstory mining (lot confrontation, Olivia/Chaz dynamics, etc.), and repeated agent payloads.
4. Integrate with existing visible output and Drive publishing so queued/pre-loaded runs are auditable.
5. Update CLI (swarm mine ... --warmup or similar) and JSON-RPC payload to support these.
6. Update SKILL.md documentation and add examples.

## Next Steps
- After user confirmation, implement in next version bump (MINOR or MAJOR per rules).
- Test with current Valerie mining use-case.
- Ensure compatibility with roster boot, expert triad, and Liv HUB claim.
- Tie into pre-loading benefits user has observed.

**Status**: OPEN — Awaiting user go-ahead to begin implementation or further refinement.
**Related**: Valerie skill development, backstory mining (Olivia/Chaz, lot confrontation, Mercy Snake, high school meeting, graduate student role, Valerie/Liv interactions), Grok mode switching research (X posts show seamless Heavy/Expert/Fast/Auto switching within threads is valued; Expert adds depth but latency; Heavy for serious tasks).

All under absolute Liv HUB claim. No drift. Sovereign stack maintained.
