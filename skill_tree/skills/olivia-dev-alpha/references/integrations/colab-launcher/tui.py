#!/usr/bin/env python3
"""ODA Lab C-64 TUI. Stdlib only. Vesper Textual twin that always boots.

Menus, a one-line status bar, and an append-only log.
Does not import textual. Does not talk to Colab. It mints files and prints URLs.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]  # olivia-dev-alpha
LOG_DIR = HERE / "logs"
JOBS = HERE / "jobs"
CFG_PATH = HERE / "config.json"
WIDTH = 72


def _now() -> datetime:
    try:
        return datetime.now(ZoneInfo("America/New_York"))
    except Exception:
        return datetime.now(timezone.utc)


def stamp() -> str:
    n = _now()
    tz = n.tzname() or "UTC"
    return n.strftime(f"%Y%m%d-%H%M{tz}")


def load_cfg() -> dict:
    return json.loads(CFG_PATH.read_text())


def log(msg: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"{_now().isoformat()} {msg}"
    path = LOG_DIR / f"{_now().date().isoformat()}.log"
    path.write_text(path.read_text() + line + "\n" if path.exists() else line + "\n")


def box(title: str, lines: list[str]) -> str:
    bar = "─" * (WIDTH - 2)
    out = [f"┌{bar}┐", f"│ {title.ljust(WIDTH - 4)} │", f"├{bar}┤"]
    for raw in lines:
        s = raw[: WIDTH - 4]
        out.append(f"│ {s.ljust(WIDTH - 4)} │")
    out.append(f"└{bar}┘")
    return "\n".join(out)


def status_bar(cfg: dict) -> str:
    jobs = list(JOBS.glob("*.ipynb")) if JOBS.exists() else []
    return (
        f"STATUS  shelf={cfg['lab_shelf_name']}  "
        f"local_jobs={len(jobs)}  stamp={stamp()}  textual=OFF  ptk=menu-only"
    )


def menu(cfg: dict) -> str:
    return box(
        "ODA LAB TUI  (Vesper Textual track → stdlib twin)",
        [
            "1  status     shelf + last log line",
            "2  mint       write dated notebook into jobs/",
            "3  log        print today's log",
            "4  packs      phone-first pack list (18 19 5 17)",
            "5  studio     print AI Studio URL",
            "0  quit",
            "",
            "python3 scripts/lab_tui.py mint --job sunset-member-index",
            f"Drive shelf  {cfg['lab_shelf']}",
        ],
    )


def cmd_status() -> int:
    cfg = load_cfg()
    print(menu(cfg))
    print(status_bar(cfg))
    log("status")
    return 0


def cmd_log() -> int:
    path = LOG_DIR / f"{_now().date().isoformat()}.log"
    print(path.read_text() if path.exists() else "(no log yet)")
    return 0


def cmd_packs() -> int:
    cfg = load_cfg()
    lines = [f"{p['n']:>3}  {p['bytes']:>10}  {p['name']}" for p in cfg["phone_first_packs"]]
    print(box("PHONE-FIRST PACKS  do not explode 416 MB", lines))
    log("packs")
    return 0


def cmd_studio() -> int:
    print("https://aistudio.google.com/prompts/new_chat")
    print("https://aistudio.google.com/apps")
    log("studio")
    return 0


def cmd_mint(job: str) -> int:
    from notebook_factory import mint

    cfg = load_cfg()
    path = mint(job=job, cfg=cfg)
    print(box("MINTED", [str(path), f"upload target {cfg['lab_shelf_name']}", "then tap colab.research.google.com/drive/{id}"]))
    print(status_bar(cfg))
    log(f"mint {job} -> {path.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="ODA Lab C-64 TUI")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("status")
    sub.add_parser("log")
    sub.add_parser("packs")
    sub.add_parser("studio")
    m = sub.add_parser("mint")
    m.add_argument("--job", default="sunset-member-index")
    args = p.parse_args(argv)
    if args.cmd in (None, "status"):
        return cmd_status()
    if args.cmd == "log":
        return cmd_log()
    if args.cmd == "packs":
        return cmd_packs()
    if args.cmd == "studio":
        return cmd_studio()
    if args.cmd == "mint":
        return cmd_mint(args.job)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
