# FORKS.md — top-level pins + deep RinDig ICM upstream analysis

Generated/expanded: **2026-09-16 23:01 CT** (burn-wave local). Source of short pin table: `mis6-harness/FORKS.md`.

Rule: every third-party library we care about pinning gets its **own** top-level repo under
`jameswilsonotr-ship-it/<name>`. No git submodules. No nest under Thunderclap.

---

## Done

| Upstream | Our fork | Notes |
|---|---|---|
| RinDig/Interpretable-Context-Methodology | jameswilsonotr-ship-it/Interpretable-Context-Methodology | TOP-LEVEL. Van Clief & McDermott ICM. MIT. |
| RinDig/icm-architect | jameswilsonotr-ship-it/icm-architect | skill already local; freeze the method |

## List-only (fork when we freeze)

| Upstream | Why |
|---|---|
| modelcontextprotocol/python-sdk | phone-bridge / MCP |
| astral-sh/ruff | CI lint |
| pytest-dev/pytest | CI |
| encode/httpx | connector transport |
| duckdb/duckdb | lake query (wheels stay out of this PR) |

## Thunderclap

Thunderclap stays a coordination surface for **MIS-7 ICM walk only** until human GO.
Do **not** nest Interpretable-Context-Methodology under Thunderclap.

## Do not fork / do not vendor here

- langchain, lancedb, chromadb
- Imagine / Grok image clients
- 21MB duckdb wheels (keep-lake-query vendors separately)
- Inkbox (Cursor connector is live; phone-bridge v0 is Termux/Tailscale)

---

## Deep upstream analysis — RinDig Interpretable-Context-Methodology

**Upstream:** https://github.com/RinDig/Interpretable-Context-Methodology  
**Stars / forks (point-in-time scrape):** ~1201 / ~208  
**License:** MIT  
**Paper:** https://arxiv.org/abs/2603.16021  
**Author framing:** Jake Van Clief — *folder structure as agent architecture*  
**Local shallow clone:** `/home/box/workspace/burn-wave/clone/Interpretable-Context-Methodology/`

### Thesis

ICM replaces framework-level multi-agent orchestration with filesystem structure. Numbered stage folders encode sequence; markdown contracts (`CONTEXT.md`) encode what to load and what to emit; plain-text files in `output/` are the handoff protocol and the human edit surface.

### Five design principles

1. **One stage, one job** — Unix / Parnas information hiding.
2. **Plain text as the interface** — markdown handoffs; no proprietary state DB in the loop.
3. **Layered context loading** — load only what the current stage needs.
4. **Every output is an edit surface** — human can edit stage N output before stage N+1.
5. **Configure the factory, not the product** — `_config` / brand / voice once; many runs.

### Five-layer routing

| Layer | File | Question | Role |
|---|---|---|---|
| L0 | `CLAUDE.md` / `AGENTS.md` | Where am I? | always-on routing (~800 tok) |
| L1 | root `CONTEXT.md` | Where do I go? | task → stage map |
| L2 | stage `CONTEXT.md` | What do I do? | **control point** — Inputs/Process/Outputs |
| L3 | `references/`, `_config/`, `skills/` | What rules apply? | factory (stable) |
| L4 | `output/` | What am I working with? | product (per-run) |

Target stage context budget: **2k–8k tokens**, vs monolithic 30k–50k prompts.

### Stage contract shape

Every stage `CONTEXT.md`: Inputs table, Process steps, Outputs table. Optional Checkpoints + Audit for creative stages.

### Fifteen conventions — Liv HUB relevance

Steal for Thunderclap: stage contracts, output handoffs, one-way refs, selective section routing, canonical sources, CONTEXT=routing, checkpoints, audits, docs-over-outputs.
CAREFUL: bundled skills — do NOT flatten named mouths into skill bundles.

### Where ICM loses

Real-time multi-agent tight loops; high concurrency; automated mid-pipeline branching.

### MCP note

ICM = context structuring; MCP = tool integration. Complementary.

---

## Deep upstream analysis — RinDig/icm-architect

**Upstream:** https://github.com/RinDig/icm-architect  
**Our fork:** https://github.com/jameswilsonotr-ship-it/icm-architect  
**Local skill:** `/workspace/agentify/skill-tree/custom-skills/icm-architect/`

### MIS-7 hard nos

1. Do not write the live skill tree until human GO — Thunderclap only.
2. Do not flatten Olivia / Bunny / Vesper / Valerie into numbered stages.
3. Do not mint a fifteenth WORK_QUEUE.md.
4. Do not delete Drive WQ clones; index only.
5. Do not invent missing WQ item files.
6. Willow Skilltree keeps live SKILL.md write lock.

### Recommended walk

1. Inventory-only audit of ONE queue home.
2. Pilot Pipeline on image-pipeline: `01-walk → 02-card → 03-implement → 04-receipt`.
3. Umbrella wrap later.
4. Full-tree migrate = home-weekend with Olive approval.

### Pin SHAs

| Repo | Upstream SHA | Frozen? |
|---|---|---|
| Interpretable-Context-Methodology | `02ba5d85c7871b75c7c702a2d8da6524723d53d4` | no |
| icm-architect | TBD | no |

Full long-form analysis + convention dumps remain on box at `/home/box/workspace/burn-wave/forks-analysis/`.
