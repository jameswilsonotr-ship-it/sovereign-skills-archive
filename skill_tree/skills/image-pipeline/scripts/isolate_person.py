#!/usr/bin/env python3
"""Isolate routes after a crop. G = generate card. E = edit keep-this-person.
Reconstructed 2026-09-11 from PROTOCOL.md isolate section. No SAM.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    p.add_argument("--route", choices=("G", "E"), default="E")
    args = p.parse_args()
    src = Path(args.src)
    print(
        json.dumps(
            {
                "ok": src.exists(),
                "src": str(src),
                "route": args.route,
                "means": "generate_image identity card" if args.route == "G" else "edit_image keep-this-person-only",
                "feeds": "four plates",
                "reconstructed": "2026-09-11",
            },
            indent=2,
        )
    )
    return 0 if src.exists() else 2


if __name__ == "__main__":
    raise SystemExit(main())
