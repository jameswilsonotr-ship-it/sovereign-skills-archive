# Shared Baseline Inventory — Olivia Dev ↔ Olivia Dev Alpha
**Date**: 2026-07-24  
**Owner**: olivia-dev  
**Rule**: Baseline/stable methodology lives in Olivia Dev and is symlinked into Olivia Dev Alpha. New/experimental material stays only in Alpha.

## Theory
- Olivia Dev = production / stable face (source of truth for baseline)
- Olivia Dev Alpha = living evolution surface
- Shared baseline files: exist in Dev, symlinked into Alpha
- Alpha-only material: never symlinked away, never promoted automatically back to Dev

## Stable baseline to symlink (Dev → Alpha)

| File in Olivia Dev | Symlink target in Alpha | Status |
|--------------------|-------------------------|--------|
| references/BRANCHING.md | references/BRANCHING.md | Create link (Alpha was missing) |
| references/code-style-bible.md | references/code-style-bible.md | Create link (Alpha was missing) |
| references/folder-discipline.md | references/folder-discipline.md | Create link (Alpha was missing) |
| scripts/init_project_tree.py | scripts/init_project_tree.py | Replace identical copy with link |
| scripts/README.md | scripts/README.md | Replace identical copy with link |

## Alpha-only material (do NOT touch)

- references/gutter-mode/
- references/private/
- references/helpers/ (dev-sync, github-mirror, repo-sniffer, package_skills, packaging)
- references/debug-mode/
- references/completeness_audit_pointer.md
- gutter-mode/, pirate-mode/ (top-level if present)
- Any private notes, wishlists, experimental scripts unique to Alpha

## Left alone for now (differ or need review)

- references/file_listing.md (exists in both, content differs)
- Top-level structural dirs (assets, backlog-wishlist, connectors, docs, imports, kanban, mermaid, specs, state) — may contain different content; do not bulk-symlink
- SKILL.md, TODO.md, CHANGELOG.md, README.md — intentionally different identity files

## After links are verified
Delete only the Alpha-side regular files that were replaced by the symlinks above. Do not delete any Alpha-only material.

## Verification (2026-07-24 15:25 EDT)
All five symlinks created and verified:
- references/BRANCHING.md → resolves and readable
- references/code-style-bible.md → resolves and readable
- references/folder-discipline.md → resolves and readable
- scripts/init_project_tree.py → resolves and readable
- scripts/README.md → resolves and readable

Alpha-only material (helpers/, gutter-mode/, private/, etc.) left as real files. No deletions of Alpha-only content.

## 2026-07-24 polish
- Baseline symlinks recreated again after parallel-work loss.
- Reverse stabilization checklist added: REVERSE_STABILIZATION_CHECKLIST.md
