# Wrapper & Per-Skill Script Registry Contract
**Version**: 0.1.0  
**Updated**: 2026-07-26  
**Owner**: skill-orchestrator (library control plane)

## Purpose
Elevate the script-registry pattern (first built inside porn-curator) so the whole library can:
1. Discover scripts by **type** (especially `wrapper`)
2. Know exactly **which tool call** a wrapper stands in front of
3. Find scripts that exist on disk but are **not registered**
4. Filter lightning-fast from a single JSON (or from the global scripts inventory + per-skill registries)

## Two layers

### Layer 1 — Global scripts inventory (already exists)
- Script: `scripts/inventory_scripts.py`
- Output: `references/inventory/scripts/scripts_inventory.json` + markdown rollup
- Scans the entire skills tree for `.py` / `.sh` / executables
- Answers: “what scripts exist and where?”

### Layer 2 — Per-skill script registries (new standard)
Each skill that owns non-trivial scripts SHOULD maintain:

```
<skill>/scripts/script_registry.json      # or references/modules/<mod>/scripts/
<skill>/scripts/SCRIPT_REGISTRY_SCHEMA.md
```

Required fields per entry (aligned with porn-curator v0.2.0):

| Field | Required | Description |
|-------|----------|-------------|
| id | yes | Stable slug |
| type | yes | `wrapper` \| `helper` \| `atomizer` \| `one-off` \| `other` |
| file_name | yes | Bare filename |
| folder | yes | Folder relative to skill/module root |
| path | yes | Relative path from skill root |
| description | yes | Short purpose |
| status | yes | `active` \| `draft` \| `deprecated` |
| wraps | if wrapper | Human name of wrapped capability |
| tool_call | if wrapper | Exact tool name (e.g. `web_search`) |
| origination | if wrapper | Value written into response.origination |
| payload_policy | if wrapper | How payload is split (e.g. clean terms vs full query) |

## Unregistered script detection
skill-orchestrator (via inventory_scripts or a follow-on check) SHOULD be able to:
1. List all scripts on disk under a skill (Layer 1)
2. Load that skill’s `script_registry.json` if present (Layer 2)
3. Report any on-disk script whose `file_name` / `path` is not in the registry

This is the same spirit as the existing completeness audit (paths declared but missing) — inverted: files present but not declared.

## Wrapper rule (library-wide)
When a skill defines a wrapper for a tool call (especially `web_search`):
- Intent inside that skill is reclassified through the wrapper
- Payload policy is explicit (what the local side sees vs what the remote tool sees)
- Responses carry `origination` so sources are never mixed

## First reference implementation
`claim-runtime/references/modules/curator/` (porn-curator):
- `scripts/script_registry.json` + `SCRIPT_REGISTRY_SCHEMA.md`
- `scripts/web_search_wrapper.py` (atom cloud gets clean terms only; web gets full query)

## Next steps for skill-orchestrator
1. Extend `inventory_scripts.py` (or add a sibling) to optionally load per-skill registries and emit an `unregistered` list.
2. Keep this contract file as the SSOT for the richer schema.
3. Do not replace the existing global inventory — compose with it.

---

## Instant availability goals (2026-07-26)

### On session / conversation open
- All **wrappers** defined in any per-skill `script_registry.json` should be immediately visible to the LLM.
- The model must know: “if I was about to call tool X, and a wrapper exists for tool X in the active skill context, go through the wrapper instead.”
- Non-wrapper scripts must also be listable instantly (helpers, atomizers, one-offs) so a skill tree can discover “what Python is available under me.”

### Aggregate by tree
When a skill or module subtree is active, the control plane should be able to:
1. Load that skill’s registry (and any nested module registries)
2. Partition: `wrappers` vs `non_wrappers`
3. Optionally resolve paths and surface them as a single aggregate so multiple scripts in the same tree can be reasoned about (or run) together

### Required filters (library-wide)
A single scan of registries + global inventory must support:
- `type == "wrapper"`
- `type != "wrapper"` (all non-wrappers)
- `tool_call == "web_search"` (or any tool)
- `folder == "scripts"` / `folder == "atoms"` / etc.
- `skill == "<slug>"`
- Unregistered = on-disk script with no matching registry entry

### Implementation note
skill-orchestrator remains the place that composes Layer 1 (global inventory) + Layer 2 (per-skill registries) and exposes these filters. Per-skill registries stay the source of truth for type/wrapper metadata; the global inventory stays the source of truth for “what files exist.”
