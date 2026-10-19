---
id: SO-WQ-009
owner: skill-orchestrator
status: OPEN
opened: 2026-09-11
depends_on: [SR-WQ-038f, SR-WQ-043, SO-WQ-001, SO-WQ-003]
blocks: []
claim: Absolute Liv HUB
---
# SO-WQ-009 — Wire scanners + atom refresh into session_boot

**Why they are not automatic**

`olivia-dev-alpha/scripts/session_boot.py` only calls `wq_hygiene.py`. Daily vacuum (export_latest through 2026-09-10) tarballs the tree. It does **not** run `inventory_scripts.py`, completeness, Cloud A/B atomizers, or `publish_all_atom_clouds.py`.

`inventory_scripts.py` writes under `references/inventory/scripts/` only. The top-level `SCRIPTS_INVENTORY.md` stayed on 2026-07-24 (101 scripts) until 2026-09-11 11:27Z pointer stamp.

`on_skill_change.py` can call `post_change_facts.py` optionally. Not a session start hook.

**Do this**

1. session_boot grows an optional `--inventory` that runs inventory_scripts + completeness `--diff` and stamps `scripts_inventory_latest.md`.
2. session_boot `--clouds` runs work_atomizer + prompt_atomizer + visuals_atomizer --atomize. Does **not** slurp Cloud A/B JSON into context.
3. Do not call `publish_all_atom_clouds.py` on every hello (tar of every *atom*.json). That stays end-of-session / SR-WQ-043.
4. Keep Cloud A/B regenerate behind CBR-WQ-010 (generators missing).

**Not this ticket:** invent memory_atomizer.py. Hunt vacuum zip first.
