#!/usr/bin/env python3
"""GCM-WQ-012 deterministic conversation space."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gcm_lib import LAYOUT, run_id, stamps


def make_space(root: Path, slug: str, verb: str = "harvest") -> Path:
    rid = run_id(slug)
    space = root / rid
    space.mkdir(parents=True, exist_ok=True)
    for name in LAYOUT:
        target = space / name
        if name.endswith(".md"):
            if not target.exists():
                hdr = stamps()
                target.write_text(
                    f"# {name}\n\n"
                    f"run_id: {rid}\n"
                    f"slug: {slug}\n"
                    f"verb: {verb}\n"
                    f"stamp_utc: {hdr['stamp_utc']}\n"
                    f"stamp_ny: {hdr['stamp_ny']}\n"
                    f"claim: {hdr['claim']}\n"
                    f"skill: {hdr['skill']}\n",
                    encoding="utf-8",
                )
        else:
            target.mkdir(exist_ok=True)
    meta = space / "00_HEADER.md"
    return space


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--verb", default="harvest")
    args = p.parse_args(argv)
    space = make_space(args.root, args.slug, args.verb)
    print(json.dumps({"space": str(space), **stamps()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
