#!/usr/bin/env python3
"""Menu A WHY / B AGENT / C GENERATE / D OVERLAY. Reconstructed 2026-09-11 from PROTOCOL.md."""
from __future__ import annotations

import argparse
import json

MENUS = {
    "A": "WHY — analysis first, four-plate dump unless vetoed",
    "B": "AGENT — candidate card + four plates",
    "C": "GENERATE — generate-engine four plates",
    "D": "OVERLAY — overlay-engine on kept parent or crop",
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--menu", default="C", choices=list(MENUS))
    p.add_argument("--src", default="")
    args = p.parse_args()
    print(
        json.dumps(
            {
                "ok": True,
                "menu": args.menu,
                "intent": MENUS[args.menu],
                "src": args.src,
                "default_if_process_these": "C",
                "reconstructed": "2026-09-11",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
