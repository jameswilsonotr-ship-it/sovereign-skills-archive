#!/usr/bin/env python3
"""Install the vendored cilia_bus wheel if needed, then run one high-water pass.

Windows-safe: default --hw is <skill>/state/cilia_highwater.json
(not /home/workdir/artifacts/...).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WHEEL = ROOT / "wheels" / "cilia_bus-0.1.0-py3-none-any.whl"
DEFAULT_HW = ROOT / "state" / "cilia_highwater.json"


def ensure_installed() -> None:
    try:
        import cilia_bus  # noqa: F401
        return
    except ImportError:
        pass
    if not WHEEL.is_file():
        raise SystemExit(f"missing wheel: {WHEEL}")
    cmd = [sys.executable, "-m", "pip", "install", "--quiet", str(WHEEL)]
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cilia-bus skill once-runner")
    parser.add_argument("--note", type=str, default="woke by GROKBOT")
    parser.add_argument("--hw", type=Path, default=DEFAULT_HW)
    parser.add_argument("--install-only", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args(argv)

    ensure_installed()
    if args.install_only:
        print("Install complete.")
        return 0

    cmd = [sys.executable, "-m", "cilia_bus"]
    if args.show:
        cmd += ["--show", "--hw", str(args.hw)]
    else:
        cmd += ["--once", "--hw", str(args.hw), "--note", args.note]
    print("+", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
