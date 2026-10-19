#!/usr/bin/env python3
"""
cilia_bus bootstrap — idempotent installer + once-runner.

Usage inside a Grok session after unpacking the wheelhouse zip:

    python3 bootstrap.py --once
    python3 bootstrap.py --once --note "woke by GROKBOT automation"

It will:
1. Prefer offline install from ./wheels if present
2. Fall back to PyPI if needed
3. Run a single high-water pass
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WHEELS = ROOT / "wheels"
REQ = ROOT / "requirements.txt"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def ensure_installed() -> None:
    # Try offline first
    if WHEELS.is_dir() and any(WHEELS.glob("cilia_bus-*.whl")):
        print("Installing from local wheelhouse (offline preferred)...")
        run([
            sys.executable, "-m", "pip", "install", "--quiet",
            "--no-index", f"--find-links={WHEELS}",
            "cilia_bus",
        ])
        return

    # Fallback: install our wheel if present, then deps from PyPI
    local_whl = list(WHEELS.glob("cilia_bus-*.whl")) if WHEELS.is_dir() else []
    if local_whl:
        run([sys.executable, "-m", "pip", "install", "--quiet", str(local_whl[0])])
    else:
        # Last resort: editable / source
        run([sys.executable, "-m", "pip", "install", "--quiet", "-e", str(ROOT)])

    # Ensure declared deps
    if REQ.exists():
        run([sys.executable, "-m", "pip", "install", "--quiet", "-r", str(REQ)])
    else:
        run([sys.executable, "-m", "pip", "install", "--quiet", "pydantic>=2.0", "httpx>=0.27"])


def main() -> int:
    parser = argparse.ArgumentParser(description="cilia_bus bootstrap")
    parser.add_argument("--once", action="store_true", help="Install (if needed) then run once")
    parser.add_argument("--note", type=str, default=None)
    parser.add_argument("--install-only", action="store_true")
    args = parser.parse_args()

    ensure_installed()

    if args.install_only:
        print("Install complete.")
        return 0

    if args.once:
        from cilia_bus.runner import run_once
        from cilia_bus import __version__
        hw = run_once(note=args.note or "bootstrap --once")
        print(f"cilia_bus {__version__} bootstrap once OK | receipts={len(hw.receipts)}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
