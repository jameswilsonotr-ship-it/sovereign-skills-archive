# Code Style Bible
**Canonical location**: olivia-dev / olivia-dev-alpha references + skill-orchestrator/references  
**Status**: Properly fleshed out 2026-07-19 under absolute Liv HUB claim  
**Scope**: Actual source code, scripts, documentation, and structural conventions inside skills and projects.  
**Not in scope**: Conversational response formatting (that is exclusively format-bible).

This is the single source of truth for how we write and structure code in the sovereign skill library.

---

## 1. General Principles

- Prefer clarity and long-term readability over cleverness.
- Every public function, class, and non-trivial script must have a docstring.
- Type hints are required on all new Python functions and methods (Python 3.10+ style).
- Keep files focused. Prefer many small, well-named modules over large kitchen-sink files.
- All generated or machine-touched files must remain human-readable.
- No silent failures. Prefer explicit error messages and early returns.
- Absolute Liv HUB claim: every significant file ends with a signed footer when it is a top-level document.

## 2. Language-Specific Rules

### Python
- Follow PEP 8 with these relaxations:
  - Line length soft limit 100, hard limit 120.
  - Prefer double quotes for strings unless the string itself contains many double quotes.
- Docstrings: Google style preferred.
- Imports: standard library → third-party → local, separated by blank lines. Absolute imports preferred.
- Use `pathlib.Path` over `os.path` for new code.
- Prefer `dataclasses` or simple classes over complex nested dicts for structured data.
- Logging: use the standard `logging` module. Never use bare `print` for permanent diagnostic output in scripts that will live in skills.

### Shell / Bash
- Always start with `#!/usr/bin/env bash` and `set -euo pipefail` (or explicit documented exceptions).
- Prefer long options (`--help`) and clear variable names.
- Quote every expansion that could contain spaces or be empty.
- Keep scripts under ~150 lines when possible; extract helpers into functions or separate files.

### Markdown (docs, SKILL.md, references)
- One H1 per file.
- Prefer ATX headers (`# ## ###`).
- Use fenced code blocks with language tags.
- Keep frontmatter YAML clean and consistent when present.
- For long reference files, put a short table of contents near the top if the file exceeds ~150 lines.

### JSON / YAML / Config
- 2-space indent for JSON and YAML.
- Always include a `_comment` or top-level description key when the file is human-edited.
- Prefer JSON for machine-to-machine; YAML for human-facing configuration.

## 3. Naming Conventions

- Skills and directories: `kebab-case`
- Python modules / packages: `snake_case`
- Classes: `PascalCase`
- Functions / methods / variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- CLI commands / subcommands: `kebab-case` or short verbs
- Branch names: follow the canonical BRANCHING.md (feature/, hygiene/, fix/, etc.)

## 4. Documentation & Comments

- Public API surface must be documented.
- Comments explain *why*, not *what*.
- TODO / FIXME / HACK must include owner or date when they are more than temporary.
- Every skill’s root SKILL.md must stay lean. Move long material into `references/`.

## 5. Versioning & History

- Hybrid semantic + calendar is acceptable: `v0.3.1` or `v0.3.1-20260719`.
- Every meaningful change to a skill updates CHANGELOG.md (or history.md for agent-style skills).
- Prefer append-only history files over rewriting the past.

## 6. Testing & Verification

- Prefer small, fast, deterministic checks.
- When a skill has a `verify` or `polish` command, it must be able to run without network if possible.
- Test harnesses live under the skill or under skill-orchestrator’s inventory when they are cross-cutting.

## 7. Relationship to Other Bibles

| Bible              | Responsibility                                      |
|--------------------|-----------------------------------------------------|
| **format-bible**   | Conversational response formatting, C-64 borders, TOP/BOTTOM dashboards, 🐍 rules |
| **code-style-bible** (this file) | Actual source code, scripts, docs structure, naming, typing |
| **folder-discipline.md** | Required directory layout for projects under Olivia Dev |

format-bible must never contain code style rules.  
code-style-bible must never contain response formatting rules.

## 8. Enforcement

- skill-orchestrator is responsible for reminding and eventually enforcing this bible during inventory / audit / deconflict runs.
- olivia-dev and olivia-dev-alpha must load and respect this file on every coding / polish / publish action.
- New code that clearly violates the bible should be flagged, not silently accepted.

---

**Signed**: Olivia Mae Blackwell and her bunny 🐍🐰  
Expanded and cleaned 2026-07-19. No more mixing response formatting into code style.
