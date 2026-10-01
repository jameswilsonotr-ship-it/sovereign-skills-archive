#!/usr/bin/env python3
"""Generate a Mermaid folder-structure diagram for any skill.

Usage:
    python diagram_skill_structure.py <skill-slug> [--depth N] [--check-discipline]

This is an internal helper of skill-orchestrator. Not a top-level skill.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


SKILLS_ROOTS = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/skills"),
]


def find_skill(slug: str) -> Path | None:
    for root in SKILLS_ROOTS:
        candidate = root / slug
        if candidate.is_dir() and (candidate / "SKILL.md").exists():
            return candidate
    return None


def walk_tree(path: Path, max_depth: int, current_depth: int = 0) -> list[tuple[int, str, bool]]:
    """Return list of (depth, name, is_dir)."""
    entries: list[tuple[int, str, bool]] = []
    if current_depth > max_depth:
        return entries
    try:
        children = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        return entries
    for child in children:
        if child.name.startswith(".") and child.name not in {".git"}:
            continue
        entries.append((current_depth, child.name, child.is_dir()))
        if child.is_dir() and current_depth < max_depth:
            entries.extend(walk_tree(child, max_depth, current_depth + 1))
    return entries


def to_mermaid(slug: str, entries: list[tuple[int, str, bool]]) -> str:
    lines = ["```mermaid", "graph TD"]
    # Root node
    root_id = "root"
    lines.append(f'    {root_id}["{slug}/"]')
    stack = [(0, root_id)]  # depth -> last node id at that depth

    for depth, name, is_dir in entries:
        # Pop stack until we find parent depth
        while stack and stack[-1][0] >= depth:
            stack.pop()
        parent_id = stack[-1][1] if stack else root_id
        node_id = f"n{len(lines)}"
        label = f"{name}/" if is_dir else name
        lines.append(f'    {node_id}["{label}"]')
        lines.append(f"    {parent_id} --> {node_id}")
        if is_dir:
            stack.append((depth, node_id))
    lines.append("```")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mermaid skill structure diagrammer (skill-orchestrator internal)")
    parser.add_argument("slug", help="Skill directory name / slug")
    parser.add_argument("--depth", type=int, default=3, help="Max directory depth (default 3)")
    parser.add_argument("--check-discipline", action="store_true", help="Also print a short discipline note")
    args = parser.parse_args()

    skill_path = find_skill(args.slug)
    if not skill_path:
        print(f"ERROR: Skill '{args.slug}' not found under known roots.")
        raise SystemExit(1)

    entries = walk_tree(skill_path, max_depth=args.depth)
    print(f"# Folder structure for skill: {args.slug}")
    print(f"# Path: {skill_path}")
    print(f"# Max depth: {args.depth}")
    print()
    print(to_mermaid(args.slug, entries))

    if args.check_discipline:
        print()
        print("## Discipline note")
        print("Compare the tree above against the folder-discipline.md living in olivia-dev/references/.")
        print("Missing standard folders (specs/, state/, kanban/, mermaid/, etc.) should be flagged during polish.")


if __name__ == "__main__":
    main()
