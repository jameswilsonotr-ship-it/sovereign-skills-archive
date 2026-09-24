# SPEC-001: Iron Pearl Unified Edge & Cloud Infrastructure (Basic Tier)
status: draft-authoritative
owner: Vesper Mae Blackwell (TaskOps Engine Room)
collaborators: Olivia Mae Blackwell (Deck Lead), Chasity / Bunny (CinC)

## 1. Purpose & Scope
Deterministic spec-based bridge: local edge, cloud orchestration, telemetry, immutable archive — no config drift / brittle shell automation.

## 2. Components
### 2.1 Archival Lake (Awesome Split & HANDOFF)
- SSoT Tape Freeze: historical corpora read-only KEEP tape
- Shard Partitioning: 8-slot partitioned extraction
- Delta Log Engine: CAS delta writer for new convo/GPS/photo bursts

### 2.2 Network Mesh (Tailscale)
- cab GMKtec K15, bunker HP minis + Jetson Orin Nano, VPS gateways
- Tailscale Funnel/HTTPS → local FastMCP daemons

### 2.3 [Cloud Gateway (Vultr)](../../bridges/vultr)
- Debian 12 vc2-1c-2gb region ord
- mcp-vultr stdio/SSE

### 2.4 [Mobile Telemetry (Phone MCP / Sygic HUD)](../../bridges/pixel)
- com.sygic.aura://coordinate
- com.sygic.intent.ACTION_HUD_UPDATE
- ws://127.0.0.1:8088/nav/hud

## 3. Invariants
1. Max RSS <35 MB edge
2. RAWV hash verification
3. Zero-Google-Doc — md/csv only
