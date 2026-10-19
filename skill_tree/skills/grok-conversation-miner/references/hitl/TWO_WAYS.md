---
title: Two ways we HITL-test
version: 1.4.0
stamp: 2026-09-11 05:10 EDT
queue: GCM-WQ-024
applies_to: grok-conversation-miner first; all skills via system-roadmap
---

# Two harnesses. Same packet. Different mouth.

## ONESHOT (HITL-001 default)
Paste the long block. Agent runs the named VARIANT in one turn. Writes TELEMETRY.json. Stops.
Use at a desk when you can read a dump.

## PACED (HITL-001-P)
Paste the short paced block once. Agent does **one step**, then waits.
You say `go` / `next` / `step N`. That is the whole UI. Built for the cab.
Agent never advances without that word. Agent never stacks steps to "save you time."

Shared rules for both:
- Dry unless last line is exactly `GO WET`
- Same folder + TELEMETRY.json schema
- Mode detect first (Heavy vs Expert)
- No KEEP slurp, no prod-grok-backend.json, no delete
- Missing verb = `NOT-IN-SKILL`, still finish the packet

This is the final testing harness shape for the skill tree. Miner owns the first paste. system-roadmap owns the copy rule for every other skill.
