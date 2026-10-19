#!/usr/bin/env python3
"""Canonical engine hook. Module copies under generate-engine/overlay-engine shim here."""
from __future__ import annotations

import argparse
import json


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("request", nargs="?", default="")
    p.add_argument("--engine", choices=("generate", "overlay"), default="generate")
    args = p.parse_args()
    print(
        json.dumps(
            {
                "ok": True,
                "engine": args.engine,
                "request": args.request,
                "next": "phrase_routes + generate_image / edit_image",
                "reconstructed": "2026-09-11 — was only a shim target, never on Drive",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
