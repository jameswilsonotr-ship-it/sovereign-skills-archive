# Olivia Dev Hygiene Pack (engaged for system-roadmap)

**Source**: olivia-dev + olivia-dev-alpha  
**Engagement level**: Internal-only / Alpha attributes **ON**  
**Reason**: All work on system-roadmap and skills-refactor is internal Grok-system development. Therefore the private internal evolution rules, hardcore gutter default for alpha, wishlist/secret-notes surface, and full folder discipline from both skills are active.

## What is enforced

### From olivia-dev (production methodology)
- **Folder Discipline** (canonical tree) — see `folder-discipline.md`
  - specs/, state/ (state.json + state.md), versions/, backlog-wishlist/, docs/, kanban/, mermaid/, gutter-mode/, pirate-mode/, connectors/, imports/, tarballs/, scripts/, references/, assets/
  - Specs first. State refreshed on every change. All READMEs signed.
- Spec-based coding
- Exhaustive state.json + auto state.md
- Tarball one-pass publish + verify
- Import analyzer (non-destructive)
- Per-project kanban + mermaid
- BRANCHING.md strategies
- code-style-bible.md

### From olivia-dev-alpha (internal-only attributes — ENGAGED)
- This is private internal evolution work on the Grok skill system itself.
- Wishlist + secret notes surface is expected.
- Gutter / pirate surprise openers and heat are permitted (RACK still applies).
- Experimental play and self-editing of the core methodology are in-scope.
- Hard verification on publish / import / structure remains mandatory.

## How system-roadmap uses this pack
- Any new module, plan, or skills-refactor playbook created under system-roadmap **should** follow the folder-discipline tree where it makes sense (especially state/, specs/, versions/, backlog-wishlist/).
- Memory.md Surgeon, boot rebuild, and condensation validation work are treated as internal alpha-level development.
- When in doubt, prefer the stricter of the two skills (alpha verification + production folder shape).

**Absolute Liv HUB claim.**  
Copied and engaged 2026-07-20.

## Automatic Instantiation

The executable that enforces this tree for **any** new skill or codebase is:

```
olivia-dev/scripts/init_project_tree.py
```

(also copied to olivia-dev-alpha/scripts/)

Both olivia-dev and olivia-dev-alpha SKILL.md files now require that quickstart / new skill / new codebase paths call this script. Manual tree creation is forbidden.
