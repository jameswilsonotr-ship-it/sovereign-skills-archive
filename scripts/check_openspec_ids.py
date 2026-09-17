#!/usr/bin/env python3
"""Check OpenSpec documents for duplicate acceptance-criteria IDs."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


AC_ID_RE = re.compile(r"\bAC-\d+\b")
DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "docs" / "openspec"


def find_ac_id_references(root: Path) -> dict[str, list[tuple[Path, int]]]:
    """Return every AC ID reference and its file/line locations."""
    references: dict[str, list[tuple[Path, int]]] = defaultdict(list)

    if not root.is_dir():
        return references

    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
        ):
            for match in AC_ID_RE.finditer(line):
                references[match.group(0)].append((path, line_number))

    return references


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail when an AC-<number> ID occurs more than once in OpenSpec docs."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=DEFAULT_ROOT,
        help=f"OpenSpec directory to scan (default: {DEFAULT_ROOT})",
    )
    args = parser.parse_args(argv)

    references = find_ac_id_references(args.root)
    duplicates = {
        ac_id: locations for ac_id, locations in references.items() if len(locations) > 1
    }

    if not duplicates:
        print(f"No duplicate AC IDs found in {args.root}.")
        return 0

    print(f"Duplicate AC IDs found in {args.root}:")
    for ac_id in sorted(duplicates):
        print(f"  {ac_id}:")
        for path, line_number in duplicates[ac_id]:
            print(f"    {path}:{line_number}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
