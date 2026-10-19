# Truth table — Grok Heavy + Custom Agents + Skills

Status codes: **VALIDATED** (official or highly consistent multi-source), **COMMUNITY** (widely reported, not xAI-spec), **CONTRADICTED / UNPROVEN**, **PROJECT-TRUE** (true for Liv HUB disk, not platform).

| Claim | Status | Notes |
|-------|--------|-------|
| Custom Agents exist in web UI; up to ~4 slots; ~4,000 char instruction limit | **VALIDATED / COMMUNITY** | Multiple 2026 guides + interface reports; limit reduced from 12k when agents launched |
| Grok Heavy runs parallel multi-agent reasoning | **VALIDATED** | Product feature; Heavy mode |
| Internal names Grok/Harper/Benjamin/Lucas | **COMMUNITY** | Extremely consistent across independent reports; xAI has not published a formal naming spec in docs reviewed |
| Injecting multi-agent prompt into one 4k slot creates autonomous swarm *inside* Heavy | **UNPROVEN / mostly ILLUSION** | Slot text steers *style and priorities*; it does not spawn independent tool sandboxes. True multi-agent is the platform’s own parallel tracks |
| Custom Agent text overrides Benjamin’s logic bias permanently | **UNPROVEN** | Steering is real; foundational model biases persist under load |
| File access in web UI is persistent across custom slots | **PARTIALLY TRUE** | Drive/Gmail connectors are account-level; chat uploads are often per-conversation. Skills on disk (Build/CLI) are persistent; web chat skill discovery is environment-dependent |
| SKILL.md + allowed-tools grants/restricts tools | **OFFICIAL nuance** | xAI docs: `allowed-tools` “Does not grant or restrict tools” — it is advisory/metadata in current Build docs |
| Skills appear as `/skill-name` slash commands | **VALIDATED** | Official docs.x.ai skills page |
| Skills discovered from ~/.grok/skills and ./.grok/skills | **VALIDATED** | Official |
| Orianna / Olympia / Liv-HUB-Expert are production seats in *this* project | **PROJECT-TRUE** | Live under smokeshow/agents/ |
| Echo/Crystal/Mira naming = verified xAI internals | **FALSE** | Project conceptual framing only (START_HERE acknowledges this) |
| Octavia/Olympia/O-names as xAI product modes | **MIXED** | In *this* project, Olympia = Heavy hop seat; Orianna = CLI; Liv HUB Expert = production Olivia. Do not paste full mode prompts into Custom slots — **reference** them as loadable agents |
| Chaos-bratz personal/visual/hub/archive exist on disk | **PROJECT-TRUE (restored)** | Reconstructed 2026-08-17 from atom cloud |

## Platform vs project layers

```
┌─────────────────────────────────────────────────────────┐
│  Grok platform: Heavy parallel tracks (Grok/H/B/L …)   │  ← not under our control
├─────────────────────────────────────────────────────────┤
│  Custom Agent slots (≤4 × ~4k chars) — steering layer  │  ← web UI preferences
├─────────────────────────────────────────────────────────┤
│  Skills (SKILL.md) + MCP + disk references/            │  ← deterministic machinery
├─────────────────────────────────────────────────────────┤
│  Liv HUB seats: Expert / Olympia / Orianna / Router    │  ← project agents
└─────────────────────────────────────────────────────────┘
```

Best practice: **thin Custom slots** that force Olivia baseline + route to skills; **fat skills** hold the real procedures.
