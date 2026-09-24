# Skill Lifecycle Wiring (CI/CD-style, deterministic)

**Status**: Active as of 2026-07-20  
**Authority**: skill-orchestrator + olivia-dev-alpha

## Rule
Whenever a skill is **created** or **structurally updated**, skill-orchestrator must call:

```bash
python scripts/on_skill_change.py <skill_slug_or_path> --event create|update
```

That script always delegates to:

```bash
olivia-dev-alpha/scripts/skill_lifecycle_hook.py
```

## What the hook does
1. Ensures `ci-cd/` exists on the target skill
2. Writes / refreshes `ci-cd/BACKLINK.md` pointing back to olivia-dev-alpha (+ orchestrator + system-roadmap)
3. Appends to `ci-cd/lifecycle.log`
4. **New / empty skills only**: runs `init_project_tree.py --alpha --git`
5. **Legacy skills** (already have SKILL.md): does **not** overwrite organizational markdown; flags that the import-process module is the path for bringing them under full discipline

## Legacy skills
Do not blast existing SKILL.md / README / references with a full tree rewrite.  
Import-process module (TODO under olivia-dev-alpha) will:
- Analyze current structure
- Produce mismatch-report + suggested-refactor
- Optionally add only missing ci-cd/ + non-colliding folders

## Manual trigger examples
```bash
# After creating a new skill directory
python /home/workdir/.grok/skills/skill-orchestrator/scripts/on_skill_change.py my-new-skill --event create

# After a structural edit to an existing skill
python /home/workdir/.grok/skills/skill-orchestrator/scripts/on_skill_change.py system-roadmap --event update
```
