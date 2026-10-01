#!/usr/bin/env python3
"""
engine_hook.py — local entrypoint for grok-imagine-overlay-engine.

Canonical implementation: image-pipeline/scripts/engine_hook.py
This wrapper exists so skill-local paths resolve and calls stay one-way (pipeline = SSOT).
Do not fork logic here; edit image-pipeline only.
"""
from __future__ import annotations
import runpy
import sys
from pathlib import Path

CANON = Path("/home/workdir/.grok/skills/image-pipeline/scripts/engine_hook.py")

def main() -> int:
    if not CANON.exists():
        print(f"ERROR: canonical missing: {CANON}", file=sys.stderr)
        return 2
    # Preserve argv for the canonical script
    sys.argv[0] = str(CANON)
    runpy.run_path(str(CANON), run_name="__main__")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
