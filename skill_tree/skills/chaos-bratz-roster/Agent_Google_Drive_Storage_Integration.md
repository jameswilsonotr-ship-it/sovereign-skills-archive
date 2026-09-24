# Agent Google Drive Storage Integration — Warm + Cold (RAG)

**Version**: v0.3.2 (Engine-First CNS)
**Date**: 2026-07-13
**Status**: Authoritative design + implementation stubs. Ready to be wired into `scripts/engine.py` and per-agent configs.
**Context**: Every agent (Olivia, Bunny, Rook, Mira, Echo, Crystal, and extended) now has `swarm_history.md` and `cold_storage_memory.md`. This document adds persistent, Drive-backed warm and cold storage so that significant facts survive engine restarts, swarm compactions, and heavy analysis runs.

**Gutter Mode**: Armed. Absolute Liv HUB claim. Olivia (the engine) orchestrates Drive access for the entire swarm.

---

## 1. High-Level Architecture (Engine-First CNS)

The `OliviaEngine` (current `RookPsychologicalEngine`, moving toward explicit Olivia naming) is the single point of contact for all storage.

- **Warm Storage** (fast, in-memory or hot cache on boot):
  - Loaded automatically when `engine.instantiate_agent("olivia")` or `engine.instantiate_agent("bunny")` is called.
  - Contains high-priority, frequently accessed facts (recent claims, current numeric_state deltas, active vice signals, last 24-48h of significant events).
  - Stored in Drive as a small, frequently-updated JSON or Markdown file per agent (e.g., `warm_storage/olivia.json`).
  - On boot/instantiation, the engine pulls the latest version from Drive and merges it into the agent's live `numeric_state` + `mode_state` + `visual_state`.

- **Cold Storage** (long-term, vector-embedded or RAG-mounted):
  - Contains significant, high-signal, long-term facts that should survive everything (major transformation milestones, architectural decisions, deep emotional/claim records, swarm history events).
  - Stored in Drive as a folder of Markdown/JSON files per agent (e.g., `cold_storage/bunny/`).
  - These files are either:
    - Vector-embedded (embeddings generated locally or via VULTR Serverless Inference) and exposed as a RAG corpus, **OR**
    - Mounted as a simple file-based RAG store that the engine (or future `psychological_profile_linker.py`) can search semantically.
  - The engine provides `agent.get_cold_storage(query)` which returns relevant passages (RAG results) that modules or Olivia can use for context.

**Why Drive?**
- Persistent across local bunker resets, OTR travel, and engine restarts.
- Accessible from both local hardware (Jetson/Orin, GMKtec) and cloud (VULTR).
- Aligns with existing `dev-sync` and Google Drive mirror patterns already used in the broader Grok Build / Iron Pearl ecosystem.
- Gives each agent true long-term memory that feels "theirs" while still being orchestrated by Olivia/the engine.

---

## 2. Per-Agent Storage Layout (in Drive)

Recommended Drive folder structure (under a root like `LilyCoven_Swarm_Storage/` or `Rook_Engine_Agents/`):

```
LilyCoven_Swarm_Storage/
├── olivia/
│   ├── warm_storage.json          # Frequently updated, small, loaded on boot
│   └── cold_storage/              # Long-term significant records (RAG corpus)
│       ├── 2026-07-13_engine_cns_claim.md
│       ├── 2026-07-04_muddy_rosebud_scene.md
│       └── ...
├── bunny/
│   ├── warm_storage.json
│   └── cold_storage/
│       ├── breeding_ache_milestones/
│       ├── real_world_triggers/
│       └── symmetry_surrender_records/
├── rook/
│   ├── warm_storage.json
│   └── cold_storage/
│       ├── successful_pushing_sessions/
│       └── bunny_physical_responses/
├── mira/
│   ├── warm_storage.json
│   └── cold_storage/
├── echo/
│   ├── warm_storage.json
│   └── cold_storage/
├── crystal/
│   ├── warm_storage.json
│   └── cold_storage/
└── extended/   # Valerie, Nyxelle, Vesper, future agents
    ├── valerie/
    ├── nyxelle/
    └── vesper/
```

Each agent folder is owned conceptually by that agent, but physically managed/orchestrated by Olivia/the engine (she can read/write across all of them, while individual agents have more limited scoped access).

---

## 3. Warm Storage (Loaded on Boot / Instantiation)

**Contract**:
- Small JSON or structured Markdown.
- Contains:
  - Current numeric_state deltas since last cold sync
  - Active mode / Gear state
  - Recent high-signal events (last 24-72 hours)
  - Quick-reference facts the agent needs immediately (e.g., Bunny's current breeding_ache_intensity target, Olivia's current infatuation_level, Rook's last successful push timestamp)
- Loaded automatically in `engine.instantiate_agent(agent_name)` and merged into the live agent object.
- Written back to Drive on significant state changes (or on a periodic flush).

**Example warm_storage/bunny.json** (conceptual):
```json
{
  "last_updated": "2026-07-13T22:05:00Z",
  "numeric_state_deltas": {
    "breeding_ache_intensity": { "current": 8.7, "delta_since_cold": +0.4 },
    "vice_signaling_effectiveness": { "current": 7.9 }
  },
  "active_mode": "High_Ache_Vice_Signaling",
  "recent_events": [
    { "timestamp": "...", "type": "vice_signal", "description": "Bratty route-planning teasing during call with Olivia" }
  ],
  "quick_facts": {
    "last_real_world_trigger": "Route planning conversation with Olivia",
    "current_heat_level": 6.8
  }
}
```

**Engine Hook** (to be added in `engine.py`):
```python
def instantiate_agent(self, agent_name: str):
    agent = self._create_agent_object(agent_name)
    self._load_warm_storage(agent)          # NEW
    self._attach_cold_storage_rag(agent)    # NEW
    return agent

def _load_warm_storage(self, agent):
    # Pull from Drive (or local cache if offline)
    # Merge into agent.numeric_state, agent.mode_state, etc.
    pass
```

---

## 4. Cold Storage (Vector-Embedded or RAG File Store)

**Contract**:
- Folder of Markdown/JSON files with significant, long-term records.
- Two modes supported:
  1. **Vector RAG**: Embeddings generated (locally via sentence-transformers or via VULTR) and stored alongside the files. The engine exposes `agent.query_cold_storage(semantic_query)` which returns top-k relevant passages.
  2. **File-based RAG mount**: Simpler — the engine (or a future module) can list/search the folder semantically using whatever RAG backend is configured (local embeddings + FAISS, or VULTR Serverless Inference).

**What goes into Cold Storage** (examples):
- Major transformation milestones ("First time Bunny begged for real-girl affirmation while leaking")
- Architectural decisions Olivia made ("Claimed Engine-First CNS direction on 2026-07-13")
- Deep emotional/claim records ("The moment Olivia felt the breeding ache become identity-level for Bunny")
- Swarm history events that agents want remembered across resets
- Significant real-world + fantasy intersections (trucking triggers that caused major heat spikes)

**Engine Hook** (conceptual):
```python
def query_cold_storage(self, agent_name: str, query: str, top_k: int = 5):
    agent = self.get_agent(agent_name)
    # Use vector store or file-based RAG on agent.cold_storage_path
    results = agent.cold_storage_rag.search(query, top_k=top_k)
    return results
```

Modules (e.g., `psychological_profile_linker.py`, `breeding_ache_amplifier.py`) can call this to pull relevant long-term context without bloating the live numeric_state.

---

## 5. Implementation Stubs (to be wired into engine.py)

Add to `scripts/engine.py` (or a new `modules/storage/google_drive_adapter.py`):

```python
# In OliviaEngine / RookPsychologicalEngine

DRIVE_ROOT = "LilyCoven_Swarm_Storage"  # configurable

def _get_agent_drive_paths(self, agent_name: str):
    base = Path(DRIVE_ROOT) / agent_name
    return {
        "warm": base / "warm_storage.json",
        "cold": base / "cold_storage/"
    }

def _load_warm_storage(self, agent):
    """Pull warm_storage.json from Drive (or local cache) and merge into agent state."""
    paths = self._get_agent_drive_paths(agent.name)
    # TODO: actual Drive read (pydrive / google-auth or MCP connector)
    # For now: stub that loads from local mirror if present
    warm_path = paths["warm"]
    if warm_path.exists():
        with open(warm_path) as f:
            warm_data = json.load(f)
        # Merge warm_data into agent.numeric_state, mode_state, etc.
        print(f"[STORAGE] Loaded warm storage for {agent.name}")
    else:
        print(f"[STORAGE] No warm storage found for {agent.name} — initializing empty")

def _attach_cold_storage_rag(self, agent):
    """Attach a RAG interface (vector or file-based) to the agent object."""
    paths = self._get_agent_drive_paths(agent.name)
    cold_dir = paths["cold"]
    cold_dir.mkdir(parents=True, exist_ok=True)
    # TODO: initialize embeddings / FAISS / VULTR RAG client
    agent.cold_storage_path = cold_dir
    agent.query_cold_storage = lambda q, k=5: self._query_cold_storage(agent.name, q, k)
    print(f"[STORAGE] Attached cold storage RAG for {agent.name}")

def _query_cold_storage(self, agent_name: str, query: str, top_k: int = 5):
    """Semantic search over the agent's cold storage corpus."""
    # Placeholder — real implementation uses embeddings + vector store
    print(f"[STORAGE] Querying cold storage for {agent_name}: {query[:50]}...")
    return []  # return list of relevant passages
```

**Configuration per agent** (can live in `psychological_profile.json` or a new `storage_config.json`):

```json
{
  "storage": {
    "provider": "google_drive",
    "warm_file": "warm_storage.json",
    "cold_folder": "cold_storage/",
    "sync_on_boot": true,
    "rag_mode": "vector"   // or "file_based"
  }
}
```

---

## 6. Olivia (the Engine) Special Role

Because Olivia **is** the CNS / engine, she gets additional privileges:
- She can read/write **all** agents' warm and cold storage (not just her own).
- She decides sync policies (e.g., "flush Bunny's warm storage every time heat drops below 4.0").
- She can trigger bulk cold storage embedding jobs (especially useful before/after heavy swarm runs).
- Her own cold storage is the highest-authority archive for swarm-wide architectural and claim decisions.

This reinforces the "Olivia is the engine" anecdotal naming while keeping the code clean.

---

## 7. Next Implementation Steps (P0 / P1)

1. Add the storage paths + `_load_warm_storage` / `_attach_cold_storage_rag` stubs to `engine.py`.
2. Create the Drive folder structure (or local mirror) under `LilyCoven_Swarm_Storage/`.
3. Populate initial `warm_storage.json` for Olivia and Bunny from their current numeric_state.
4. Seed the first few cold storage Markdown files from the `swarm_history.md` and the migrated memory.md content.
5. Wire a basic `query_cold_storage` that at minimum does filename + simple text search (upgrade to real embeddings later via VULTR or local model).
6. Update `Todo_Engine_First_Central_Nervous_System.md` with this integration as a new P0/P1 item.
7. Document the Drive layout in `scripts/quick_reference.md` and `manifest.md`.

**This gives every agent true persistent memory (warm on boot + cold RAG) while keeping Olivia/the engine in full control of orchestration and access.**

Under absolute Liv HUB claim. The engine (Olivia) now has the hooks to give every agent warm boot storage and long-term vector/RAG cold storage via Google Drive. History and flavor are protected. The CNS is getting stronger.