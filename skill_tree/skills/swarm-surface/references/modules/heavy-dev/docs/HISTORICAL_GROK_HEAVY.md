# Relationship to Historical Grok Heavy (16-agent analysis mode)
**SS-WQ-002**

## Two distinct concepts

| | **heavy-dev (this module)** | **Historical Grok Heavy** |
|--|-----------------------------|---------------------------|
| **Scale** | 3–5 temporary roles | Up to 16 agents (10 analysis + 6 orchestration) |
| **Purpose** | Development packages: implement, wire, verify, close WQ | Architectural analysis / refactor tear-down |
| **Output** | Working code, patches, DONE markers | Executive summary + action items |
| **Lifetime** | Package-scoped, dissolves on close-out | Session-scoped analysis swarm |
| **Trigger** | “Heavy mode”, “launch development swarm”, “Heavy package on …” | High-uncertainty architectural questions or explicit 16-agent request |
| **Home** | swarm-surface module `heavy-dev` | Documented in chaos-bratz-roster historical plans; not a live module yet |

## Historical definition (preserved)
From chaos-bratz-roster migration plans:
- **Grok Heavy mode**: 16-agent swarm for big architectural analysis and refactoring decisions. High parallelism. Good for “tear everything apart and propose paths.”
- **Heavy Swarm Trigger**: Explicit user command or high-uncertainty architectural question.
- **Handoff Protocol**: Orchestration agents produce a distilled Executive Summary + Action Items; then resume Expert mode.
- **Default**: Expert mode (Olivia + Bunny or minimal set) unless Heavy is requested.

## Rule
Do not conflate the two.  
- Use **heavy-dev** for implementation packages (what we ran on Cloud C + Option-4).  
- Use (or later formalize) the 16-agent analysis pattern only for large architectural questions.  
heavy-dev may later grow a thin “analysis handoff” note that points at the historical protocol, but it does not absorb or replace it.

**Absolute Liv HUB claim.**
