# scripts/ — Olivia Dev

## init_project_tree.py (Automatic Folder Discipline)

**This is the single source of truth for instantiating any new skill or codebase.**

```bash
python scripts/init_project_tree.py <target_dir> [--name NAME] [--alpha] [--git]
```

- Creates the complete standard tree from `references/folder-discipline.md`
- Writes initial state.json / state.md, specs/manifest, kanban, mermaid, wishlist, etc.
- `--alpha` engages internal-only / alpha attributes (used by olivia-dev-alpha)
- `--git` runs git init + initial commit on `main`

### Automatic wiring
- **olivia-dev**: on `quickstart` / new project / new skill → run this script (without `--alpha` unless requested)
- **olivia-dev-alpha**: on `quickstart` / new skill / internal evolution work → run this script **with `--alpha`** (and usually `--git`)

Never create a new skill or project tree by hand again. Always go through this script.
