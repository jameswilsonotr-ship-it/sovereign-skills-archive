#!/usr/bin/env python3
"""Rename imagine_images artifacts to descriptive names. Best-effort."""
from __future__ import annotations
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/home/workdir/artifacts/imagine_images")

def descriptive(char: str, mode: str, src: Path, prefix: str = "gen") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    stem = re.sub(r"[^a-z0-9]+", "", src.stem.lower())[:8] or "img"
    return f"{prefix}_{char}_{mode}_{ts}_{stem}{src.suffix or ".jpg"}"

def main(char: str, mode: str, path: str, prefix: str = "gen") -> None:
    src = Path(path)
    if not src.exists():
        print(f"missing: {src}")
        sys.exit(1)
    dest = (src.parent if src.parent.name else ROOT) / descriptive(char, mode, src, prefix)
    if src.resolve() == dest.resolve():
        print(dest)
        return
    dest.write_bytes(src.read_bytes())
    print(str(dest))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: rename_artifacts.py <char> <mode> <path> [prefix]")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "gen")
