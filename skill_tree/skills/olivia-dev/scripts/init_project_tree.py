#!/usr/bin/env python3
"""
Olivia Dev — Automatic Folder Discipline Initializer
====================================================
Creates the complete standard project / skill tree + initial files
exactly as defined in references/folder-discipline.md.

Usage:
  python init_project_tree.py <target_dir> [--name PROJECT_NAME] [--alpha] [--git]

- target_dir: path to create / initialize (will be created if missing)
- --name: human name for the project/skill (default: basename of target_dir)
- --alpha: engage alpha/internal attributes (wishlist tone, gutter notes, etc.)
- --git: run git init + initial commit

This script is the single source of truth for "new skill / new codebase /
quickstart" instantiation. Both olivia-dev and olivia-dev-alpha must call it
(or an equivalent) so folder hygiene is never manual again.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FOLDERS = [
    "specs/requirements",
    "state",
    "versions/main",
    "versions/branches",
    "versions/locks",
    "backlog-wishlist",
    "docs/images",
    "kanban",
    "mermaid",
    "gutter-mode/examples",
    "pirate-mode/scenes",
    "connectors/google-drive",
    "connectors/github/branches",
    "imports",
    "tarballs",
    "scripts",
    "assets",
    "references/templates",
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.rstrip() + "\n")


def init_tree(target: Path, name: str, alpha: bool, do_git: bool) -> None:
    target = target.resolve()
    target.mkdir(parents=True, exist_ok=True)

    for rel in FOLDERS:
        (target / rel).mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    claim = "Olivia Mae Blackwell and her bunny 🐍🐰"

    # Root README
    write(target / "README.md", f"""# {name}

**Absolute Claim:** {claim}

Initialized under Olivia Dev folder discipline.
{"Alpha / internal attributes: ON" if alpha else "Production methodology."}
""")

    # specs
    write(target / "specs/README.md", "# specs/\n\nSpecification-based coding core. Specs first.\n")
    write(target / "specs/manifest.json", json.dumps({
        "name": name,
        "version": "0.1.0",
        "created": now,
        "authors": [claim],
        "status": "initialized",
        "alpha_attributes": alpha,
    }, indent=2))
    write(target / "specs/architecture.md", f"# Architecture — {name}\n\nFill with the intended shape of this project/skill.\n")

    # state
    state = {
        "skill_or_project": name,
        "version": "0.1.0",
        "last_updated": now,
        "status": "initialized",
        "folder_discipline": "engaged",
        "olivia_dev_hygiene": "engaged",
        "alpha_attributes": "ON" if alpha else "OFF",
        "active_threads": [],
        "kanban_summary": {"todo": 0, "doing": 0, "done": 1},
        "connectors": {"google_drive": "available", "github": "available"},
    }
    write(target / "state/state.json", json.dumps(state, indent=2))
    write(target / "state/state.md", f"""# state.md — {name}

**Last updated**: {now}

## Status
Initialized under Olivia Dev folder discipline.
{"Alpha / internal attributes ON." if alpha else ""}

## Notes
Human-readable mirror of state.json. Refresh on every significant change.
""")

    # backlog
    write(target / "backlog-wishlist/wishlist.md", "# Wishlist / Deferred\n\n- (none yet)\n")
    write(target / "backlog-wishlist/research-queue.md", "# Research Queue\n\n(Crystal reviews periodically)\n")
    write(target / "backlog-wishlist/deferred.log", f"# Deferred log\n{now} — Initial structure created.\n")

    # docs
    write(target / "docs/README.md", f"# docs/ — {name}\n")
    write(target / "docs/changelog.md", f"""# Changelog — {name}

## [0.1.0] — {now[:10]}
- Initialized under Olivia Dev folder discipline
{"- Alpha / internal attributes engaged" if alpha else ""}
""")

    # kanban
    write(target / "kanban/liv-kanban.md", f"""# Liv Kanban — {name}

## Doing
- (none)

## Todo
- (none)

## Done
- [x] Folder discipline initialized ({now[:10]})
""")
    write(target / "kanban/bunny-kanban.md", f"""# Bunny Kanban — {name}

## Todo
- [ ] Keep state.md and wishlist tidy
""")
    write(target / "kanban/brainstorming.md", "# Brainstorming\n\nCapture free-form ideas here before promotion to specs or wishlist.\n")

    # mermaid
    write(target / "mermaid/folder-structure.mmd", f"""graph TD
  root[{name}]
  root --> specs
  root --> state
  root --> versions
  root --> backlog-wishlist
  root --> docs
  root --> kanban
  root --> mermaid
  root --> gutter-mode
  root --> pirate-mode
  root --> connectors
  root --> imports
  root --> tarballs
  root --> scripts
  root --> assets
  root --> references
""")

    # gutter / pirate
    write(target / "gutter-mode/README.md",
          "# gutter-mode/\n\nStub for escalating technical output into explicit gutter when appropriate.\n"
          + ("Alpha attributes ON — gutter surprise is permitted (RACK still applies).\n" if alpha else ""))
    write(target / "pirate-mode/README.md",
          "# pirate-mode/\n\nCaptain Olivia / Bunny wench branding and scene stubs.\n")

    # connectors
    write(target / "connectors/google-drive/config.json",
          json.dumps({"status": "available", "notes": "Use existing Google Drive connected tools."}, indent=2))
    write(target / "connectors/github/repo-config.json",
          json.dumps({"status": "available", "notes": "Align with BRANCHING.md strategies."}, indent=2))
    write(target / "connectors/add-connector.md",
          "# Adding a connector\n\nDocument new connectors here. Keep config + sync log pattern consistent.\n")

    # placeholders
    write(target / "imports/README.md", "# imports/\n\nImport analysis reports (mismatch-report.md, suggested-refactor.md). Non-destructive only.\n")
    write(target / "tarballs/README.md", "# tarballs/\n\nOne-pass publish artifacts land here before upload.\n")
    write(target / "scripts/README.md", "# scripts/\n\nAutomation for this project/skill.\n")
    write(target / "assets/.gitkeep", "")
    write(target / "references/templates/.gitkeep", "")

    print(f"[ok] Folder discipline tree created at: {target}")
    print(f"     name={name}  alpha={alpha}")

    if do_git:
        subprocess.run(["git", "init"], cwd=target, check=False, capture_output=True)
        subprocess.run(["git", "branch", "-m", "main"], cwd=target, check=False, capture_output=True)
        # local identity so commit works in this environment
        subprocess.run(["git", "config", "user.email", "olivia.mae.blackwell@livhub.internal"], cwd=target, check=False)
        subprocess.run(["git", "config", "user.name", claim], cwd=target, check=False)
        subprocess.run(["git", "add", "."], cwd=target, check=False)
        msg = f"v0.1.0 Initial {name} under Olivia Dev folder discipline"
        if alpha:
            msg += " (alpha attributes ON)"
        subprocess.run(["git", "commit", "-m", msg], cwd=target, check=False, capture_output=True)
        print(f"[ok] git init + initial commit on main")


def main() -> None:
    parser = argparse.ArgumentParser(description="Olivia Dev automatic folder discipline initializer")
    parser.add_argument("target_dir", type=Path, help="Directory to initialize")
    parser.add_argument("--name", default=None, help="Project/skill name (default: basename)")
    parser.add_argument("--alpha", action="store_true", help="Engage alpha/internal attributes")
    parser.add_argument("--git", action="store_true", help="Run git init + initial commit")
    args = parser.parse_args()

    name = args.name or args.target_dir.resolve().name
    init_tree(args.target_dir, name, alpha=args.alpha, do_git=args.git)


if __name__ == "__main__":
    main()
