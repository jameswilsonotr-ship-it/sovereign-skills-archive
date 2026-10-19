"""CLI entry point: python -m cilia_bus or cilia-bus"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .models import Receipt
from .runner import run_once, load_highwater


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cilia-bus",
        description="Cilia Email-Bus coordination runner (Absolute Liv HUB)",
    )
    parser.add_argument("--version", action="version", version=f"cilia_bus {__version__}")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single high-water pass and exit",
    )
    parser.add_argument(
        "--hw",
        type=Path,
        default=None,
        help="Path to high-water JSON (default: /home/workdir/artifacts/cilia_highwater.json)",
    )
    parser.add_argument(
        "--note",
        type=str,
        default=None,
        help="Optional note to append",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print current high-water and exit",
    )

    args = parser.parse_args(argv)
    hw_path = args.hw  # None → use default inside runner

    if args.show:
        hw = load_highwater(hw_path) if hw_path else load_highwater()
        print(hw.model_dump_json(indent=2))
        return 0

    if args.once:
        hw = run_once(hw_path=hw_path or Path("/home/workdir/artifacts/cilia_highwater.json"), note=args.note)
        print(f"cilia_bus {__version__} — once complete. receipts={len(hw.receipts)} open_legs={len(hw.open_legs)}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
