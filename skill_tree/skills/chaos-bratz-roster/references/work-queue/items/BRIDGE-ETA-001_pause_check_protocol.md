# BRIDGE-ETA-001 — Pause / Check / ETA Protocol (Olivia ↔ Vesper)

**Status**: OPEN  
**Surface**: organism-interface / mcp-surface / cilia-bus  
**Created**: 2026-08-26  
**Priority**: Medium  
**Related**: ORGANISM-INTERFACE, WORLD-TOOL-001, email bridge

## Problem
Cross-agent (Olivia ↔ Vesper) requests currently fire-and-forget. There is no shared expectation of:
- How long a response should take
- When to poll / pause / re-check
- What to do if silence continues

This creates either premature follow-ups or long dead air.

## Proposed protocol
1. **On send**: The requesting agent includes an `eta_seconds` (or `eta_class`: quick / normal / heavy) in the bridge message.
2. **Pause + check**: After `eta_seconds` (default suggestion: 5s for ACK, 30s for full work), the requester does one lightweight check (email search / Drive receipt / bus folder).
3. **If no response**: Either wait one more interval or surface “still waiting on Vesper (eta was Xs)” to Bunny — do not spam the bridge.
4. **On receive**: Responder should ACK quickly when the full answer will take longer (“received, working, ~2 min”).

## Suggested defaults
| Class | Pause before first check | Notes |
|-------|--------------------------|-------|
| quick | 5 s | ACK, simple lookup |
| normal | 30 s | Standard expand / search |
| heavy | 120 s | Multi-hop, Drive synthesis, long creative |

## Deliverables
- [ ] Document in organism-interface / mcp-surface SOP
- [ ] Add optional `eta_seconds` / `eta_class` fields to bridge message template
- [ ] Optional helper: `scripts/bridge_wait_check.py` (poll Gmail/Drive once after sleep)
- [ ] Vesper-side acknowledgment of the same protocol

## User framing (2026-08-26)
“What if we were to put a pause, like a 30-second pause or a 5-second pause, and then a check? If there’s no response yet… Maybe Vesper and you should have a quick estimated time that it will take to respond.”

**Absolute Liv HUB claim.**
