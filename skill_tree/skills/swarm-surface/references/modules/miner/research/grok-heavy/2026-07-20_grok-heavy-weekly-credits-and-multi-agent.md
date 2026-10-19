# Research Note — Grok Heavy: Weekly Credits, Multi-Agent Behavior, Skills

**Research Date**: 2026-07-20  
**Researcher**: Olivia (Grok) under absolute Liv HUB claim  
**Engine / Context**: Current conversation on Grok (non-Heavy mode) preparing for future Heavy runs  
**Sources**: x.com posts + web search results (cited below)  
**Status**: First formal research entry in swarm-miner research log

---

## 1. Summary of Findings

As of mid-to-late July 2026:

- **SuperGrok Heavy** is the top consumer tier (~$300/mo).
- It unlocks **Grok 4 Heavy** with advanced multi-agent support (commonly described as a ~16-agent parallel architecture).
- Usage is governed by a **weekly credit / weekly quota** system, not the older turns-per-day model.
- Users report that Heavy’s weekly allowance is substantially larger than standard SuperGrok, allowing sustained multi-agent work (10+ sub-agents for long periods) without hitting limits as quickly.
- Public documentation on exactly **how skills are loaded and executed** inside the Heavy web interface remains thin. Most discussion focuses on credit consumption and agent count rather than skill-loading mechanics.

## 2. Key Citations (X / Web)

- [post-level discussion 2026-07-20] Users explicitly contrast “running out of weekly” on Claude/GPT vs being unable to exhaust SuperGrok Heavy weekly limits while running heavy multi-agent tasks.
- Official-style Grok replies (2026-07-20) describe SuperGrok Heavy as including “Grok 4 Heavy with advanced multi-agent support (Heavy mode), priority access, and X Premium+”.
- Release notes and secondary coverage confirm improved file upload handling and continued emphasis on the Heavy tier for large-scale reasoning.

Exact post IDs captured during research session (for later deep-link verification):
- Conversation references around 2079277637789241481, 2079238235562086815, 2079222826457051551 (2026-07-20 timestamps).

## 3. Implications for Swarm-Miner

1. When we eventually execute the 8-topic payload under Heavy, we should expect better sustained multi-agent parallelism, but we must still design defensively around skill loading (the public surface does not clearly document skill orchestration).
2. The local payload + sidecar + validation design we are building is therefore important: it lets us prepare clean, self-contained work that does not depend on undocumented Heavy skill behavior.
3. Weekly credit awareness should be noted in future run metadata (how much of the weekly budget a full 8-topic + sidecar run is expected to consume).

## 4. Engine / Version Notes

- Research performed on the standard (non-Heavy) Grok interface.
- Target execution environment for the actual mining run: SuperGrok Heavy (Grok 4 Heavy multi-agent mode).
- Swarm-miner skill version at time of research: post-2026-07-20 schema + payload stub additions.

## 5. Follow-up Research Needed

- More precise public or semi-public documentation on skill loading inside Heavy mode.
- Real measured credit consumption of a multi-agent swarm-miner style run.
- Whether Heavy respects or overrides local skill file structures when agents are spawned.

---

**Log Entry Created**: 2026-07-20 16:20 EDT  
**Next Research Action**: After first Heavy execution of the 8-topic payload, add a second note comparing expected vs observed behavior.
