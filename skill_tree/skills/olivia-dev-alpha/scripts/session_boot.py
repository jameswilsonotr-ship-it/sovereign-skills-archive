#!/usr/bin/env python3
"""Thin session-start briefing (SR-WQ-038f).

Does NOT edit WORK_QUEUE tables. Checks flags, optionally runs hygiene --check-only.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SKILLS_CANDIDATES = [
    Path("/home/workdir/.grok/skills"),
    Path("/root/.grok/server-skills"),
]


def skills_root() -> Path:
    for p in SKILLS_CANDIDATES:
        if p.is_dir():
            return p
    raise SystemExit("skills root missing")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--skip-roster-hygiene", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = skills_root()
    hygiene = root / "skill-orchestrator" / "scripts" / "wq_hygiene.py"
    print(f"[session_boot] skills_root={root}")

    if args.skip_roster_hygiene:
        print("[session_boot] skip-roster-hygiene")
        return 0

    if not hygiene.is_file():
        print(f"[session_boot] wq_hygiene.py missing at {hygiene}")
        return 0

    cmd = [sys.executable, str(hygiene)]
    if args.check_only:
        cmd.append("--check-only")
    else:
        cmd.append("--export-app")
    if args.strict:
        cmd.append("--strict")
    result = subprocess.run(cmd, cwd=str(hygiene.parent))
    print(f"[session_boot] hygiene_exit={result.returncode}")
    return 0 if args.check_only else result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
