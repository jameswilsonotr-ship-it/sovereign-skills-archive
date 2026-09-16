#!/usr/bin/env python3
"""Mira/Echo review stub after plates land. Reconstructed 2026-09-11."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True)
    args = p.parse_args()
    d = Path(args.dir)
    files = sorted(str(x) for x in d.glob("*") if x.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}) if d.exists() else []
    print(
        json.dumps(
            {
                "ok": d.exists(),
                "dir": str(d),
                "stills": files,
                "n": len(files),
                "review": "Mira drift later — this script only lists what landed",
                "reconstructed": "2026-09-11",
            },
            indent=2,
        )
    )
    return 0 if d.exists() else 2


if __name__ == "__main__":
    raise SystemExit(main())
