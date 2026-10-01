#!/usr/bin/env python3
"""Entrypoint for the ODA Lab C-64 TUI.

Usage:
    python3 scripts/lab_tui.py
    python3 scripts/lab_tui.py mint --job sunset-member-index
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MOD = HERE.parent / "references" / "integrations" / "colab-launcher"
sys.path.insert(0, str(MOD))

from tui import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
