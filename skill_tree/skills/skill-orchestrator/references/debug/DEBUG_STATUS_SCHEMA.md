# Debug Status Schema
**Version**: 0.1.0 — 2026-07-24  
**Owner**: skill-orchestrator  
**Contract source**: olivia-dev-alpha `references/debug-mode/DEBUG_MODE_CONTRACT.md` v0.2.0  
**Paired contract**: keep schema version and contract version coordinated; do not drift outcome vocabulary. Schema fields unchanged; contract expanded with promotion rules, menu shape, and version-bump procedure.

## Purpose
Single place for the orchestrator to know which skills are debugging, what the last outcome was, and where to read the notes — without owning per-skill debug logic.

## Status Record (one per opted-in skill)

```yaml
skill_name: grok-imagine-generate-engine
contract_version: "0.1.0"          # version of DEBUG_MODE_CONTRACT the skill claims
mode: idle | debug | formulation   # current mode
last_outcome: passed | failed | moderated | no-file | partial | null
last_outcome_at: 2026-07-24T15:50:00Z
notes_path: references/dual-engine-test/debugging_notes.md
registry_path: references/dual-engine-test/registry.md   # optional
todo_path: TODO.md
active_item: null | "DNA density ladder"   # what is under test, if any
version_at_debug: "0.2.4"          # skill version when last debug activity occurred
```

## Global Debug Table
skill-orchestrator maintains (or regenerates on audit):

| skill_name | mode | last_outcome | last_outcome_at | contract_version | notes_path |
|------------|------|--------------|-----------------|------------------|------------|
| ...        | ...  | ...          | ...             | ...              | ...        |

## Harvest Rules
- On inventory / audit: read each opted-in skill’s status line or status file if present; update the table.
- On explicit `debug status` / `who is debugging`: present the table.
- Do not parse full debugging_notes.md unless the user asks for detail; the table is the summary.

## Status Line Format (emitted by skills)
Skills should emit a single short line or YAML block that matches the Status Record fields above when entering/leaving debug mode or after a scored outcome. Example:

```
DEBUG_STATUS skill=grok-imagine-generate-engine mode=formulation last_outcome=no-file active_item="DNA density" contract=0.1.0
```

Orchestrator may also read a small `debug_status.yaml` inside the skill if the skill chooses to write one.

## Non-Goals
- Orchestrator does not run the skill’s tests.
- Orchestrator does not score images or prompts.
- Orchestrator does not replace OliviaDevAlpha’s versioning or menu rules.

## How observation works (envelope harvest)
1. Speaking skills emit format-bible envelope front matter (skill, mode, debug_outcome, clock).
2. On `debug status`, inventory, or audit, skill-orchestrator scans for:
   - YAML front matter blocks matching ENVELOPE_SCHEMA
   - `DEBUG_STATUS ...` one-liners
3. Those fields update the global debug status table.
4. Full skill bodies are not required in context — the envelope is the observation surface.
5. format-bible `references/ENVELOPE_SCHEMA.md` is the stamp; this schema is the ledger.

## Code example
See `envelope_harvest_example.md` for parse/harvest pseudocode and sample table output.

## Audit command
Run `references/debug/audit_debug_status.py` for a progress-barred scan of opted-in skills (generate, overlay, roster, format-bible) and a status table.


## STALE_FACT (inactivity ≥ 7 days)

Canonical emission line (see `STALE_FACT.md`):

```
STALE_FACT skill=<slug> last_activity=<ISO8601> days_idle=<N> source=completeness|debug|both window_days=7
```

On emit: if skill is opted-in and mode is debug/formulation → set mode=idle.  
Do not write the alpha work queue. Alpha reacts by setting WQ items to `stale`.
