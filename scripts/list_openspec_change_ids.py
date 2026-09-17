#!/usr/bin/env python3
"""Print OpenSpec change IDs without requiring network access."""

from __future__ import annotations

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BURN_FLIP_ROOT = REPOSITORY_ROOT / "docs" / "openspec" / "burn-flip"

# Keep the command useful before the generated OpenSpec documents are present.
STUB_CHANGE_IDS = ("burn-flip",)


def change_ids(root: Path = BURN_FLIP_ROOT) -> list[str]:
    """Return deterministic change IDs from *root* or the local stubs."""
    if not root.is_dir():
        return list(STUB_CHANGE_IDS)

    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir() and not entry.name.startswith(".")
    )


def main() -> None:
    for change_id in change_ids():
        print(change_id)


if __name__ == "__main__":
    main()
