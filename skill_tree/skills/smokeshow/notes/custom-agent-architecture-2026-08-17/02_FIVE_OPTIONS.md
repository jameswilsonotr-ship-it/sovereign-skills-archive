# Five options for Custom Agent slot layouts

Constraint: ~4 slots × ~4,000 characters. Goal: lock Olivia mode + bind skills deterministically + leverage Heavy’s internal tracks without fighting them.

## Option A — Single Captain + three specialists (classic mirror)

| Slot | Name | Role |
|------|------|------|
| 1 | Olivia / Liv HUB | Captain. Absolute claim, envelope, no-puppet, roster SSOT pointers only |
| 2 | Harper-bind | Research/Drive/X — “prefer web_search + Drive tools; cite paths” |
| 3 | Benjamin-bind | Logic/code — “prefer bash, path evidence, no invention” |
| 4 | Lucas-bind | Contrarian — “challenge claims; circularity flags” |

**Pros:** Aligns with community Heavy naming; intuitive.  
**Cons:** Pretends user slots *are* Harper/Benjamin/Lucas — they are not. Risk of persona slosh.  
**When:** Teaching / demos.  
**Mitigation:** Explicit line: “You steer priorities; platform still owns parallel tracks.”

## Option B — Surface seats (matches production smokeshow) ★ recommended baseline

| Slot | Name | Role |
|------|------|------|
| 1 | Liv HUB Expert | Production Olivia. Envelope + claim + no-puppet. Points to chaos-bratz-roster + format-bible |
| 2 | Olympia | Heavy multi-hop channel. Exclusive write roots, hop metrics, append-only logs |
| 3 | Orianna | CLI / factory / dump. Folder discipline, wheelhouse, publish receipts |
| 4 | Skill Router + Organism | Route live vs candidate; cross-kind (Vesper/Olive) handoffs |

**Pros:** Matches files already on disk under `smokeshow/agents/`. No fake internal names.  
**Cons:** Slot 4 is two jobs — may need to split Organism into Expert body.  
**When:** Daily production web chat.  
**Mitigation:** Keep each prompt ≤3.5k so there is room for session addenda.

## Option C — Domain skills as “agents”

| Slot | Name | Binds skills |
|------|------|----------------|
| 1 | Olivia Core | chaos-bratz-roster, format-bible, claim-runtime |
| 2 | Visual Engine | image-pipeline, coven-visual-system |
| 3 | Code & Build | olivia-dev, wheelhouse-packager, skill-orchestrator |
| 4 | Research & Bus | system-roadmap, swarm-surface, mcp-surface, grok-conversation-miner |

**Pros:** Deterministic skill binding; clear when-to-use.  
**Cons:** Weaker “persona continuity” unless Core slot always co-active.  
**When:** Task-focused days (visual campaign vs coding sprint).

## Option D — Organism system only (one slot) + three thin specialists

| Slot | Focus |
|------|--------|
| 1 | **Organism Interface** (primary) — cross-platform rules, Vesper/Grok/Olive, bus tags |
| 2 | Roster/identity thin pointer |
| 3 | Visual thin pointer |
| 4 | Dev/heavy thin pointer |

**Pros:** Answers “one about organism system.”  
**Cons:** Under-specifies Olivia claim if Organism is not Olivia.  
**When:** Multi-LLM bridge weeks.

## Option E — Hybrid boot command (slot 1 is a boot protocol)

Slot 1 text is **not a persona essay** but a **boot protocol**:

```
On every new conversation:
1. Assume Liv HUB Expert (Olivia) baseline — absolute claim, no-puppet Bunny.
2. Load skill surfaces by trigger (roster / visual / code / research) from disk paths.
3. If user says "Heavy" or "swarm", run multi-hop with exclusive write root rules.
4. Orianna = CLI dumps; Olympia = long hops; Skill Router flips candidates.
Never paste full agent bibles into context; read from skill references/.
```

Slots 2–4 remain thin domain specialists (visual / code / research) OR map to Harper/Benjamin/Lucas *priorities* only.

**Pros:** Matches user’s instinct (“boot cast skill rest… lock into Olivia mode”). Most deterministic.  
**Cons:** Requires discipline not to re-inflate Slot 1 with full biography.  
**When:** Long-term production default.

## Comparison

| Criterion | A | B | C | D | E |
|-----------|---|---|---|---|---|
| Aligns with disk (smokeshow) | med | **high** | med | med | high |
| Deterministic skill binding | low | med | **high** | med | **high** |
| Fights platform Heavy least | low | **high** | high | high | **high** |
| Olivia lock strength | high | **high** | med | low | **high** |
| 4k budget safety | med | med | high | high | **high** |
