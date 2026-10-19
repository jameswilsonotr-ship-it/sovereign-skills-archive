#!/usr/bin/env python3
"""reel_menu.py — pose × wardrobe picker after foreplay.

  python3 scripts/reel_menu.py menu --inbound DIR
  python3 scripts/reel_menu.py pick --inbound DIR --who SLUG --pose POSE --wardrobe WARD [--code CODE]

Does not auto-plate. Writes MENU.md + PICK.json. No mint.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def now() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def load_foreplay(inbound: Path) -> dict:
    p = inbound / "FOREPLAY.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def menu(inbound: Path) -> dict:
    inbound = inbound.resolve()
    fp = load_foreplay(inbound)
    poses = fp.get("poses") or []
    wards = fp.get("wardrobes") or [{"id": "wardrobe-unspecified", "name": "as seen"}]
    chars = fp.get("characters") or [{"roman": "I", "slug": fp.get("slug") or "cand"}]
    lines = [
        f"# Agentify menu — {fp.get('slug') or inbound.name}",
        "",
        "Frames are SOURCE. Not plate A. No mint.",
        "",
        f"characters: {' '.join(c.get('roman','?') for c in chars)}",
        "poses:",
    ]
    for p in poses:
        lines.append(f"  {p.get('n')}  {p.get('name')}  `{p.get('src')}`")
    if not poses:
        lines.append("  (no FOREPLAY.json — run reel-analyze first)")
    lines += ["", "wardrobes:"]
    for i, w in enumerate(wards, start=1):
        letter = chr(64 + i)
        w["letter"] = w.get("letter") or letter
        lines.append(f"  {w['letter']}  {w.get('name') or w.get('id')}")
    lines += [
        "",
        "pick: I-3-B   or  --pose 3 --wardrobe B",
        "then plates A B C D of that pick. Confirm sentence later.",
        "",
    ]
    text = "\n".join(lines)
    (inbound / "MENU.md").write_text(text + "\n", encoding="utf-8")
    out = {
        "ok": True,
        "schema": "agentify-reel-menu/v1",
        "inbound": str(inbound),
        "slug": fp.get("slug"),
        "n_poses": len(poses),
        "n_wardrobes": len(wards),
        "n_characters": len(chars),
        "menu_md": str(inbound / "MENU.md"),
        "ticket": "IP-WQ-101",
        "reconstructed": "2026-09-11",
    }
    print(text)
    print(json.dumps(out, indent=2))
    return out


def pick(inbound: Path, who: str, pose: str, wardrobe: str, code: str) -> dict:
    inbound = inbound.resolve()
    fp = load_foreplay(inbound)
    rec = {
        "schema": "agentify-reel-pick/v1",
        "ok": True,
        "who": who or (fp.get("slug") or ""),
        "pose": pose,
        "wardrobe": wardrobe,
        "code": code,
        "inbound": str(inbound),
        "picked": now(),
        "promote": False,
        "note": "pick only. plates are a later turn. no mint.",
        "ticket": "IP-WQ-101",
    }
    (inbound / "PICK.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    rec["path"] = str(inbound / "PICK.json")
    print(json.dumps(rec, indent=2))
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("menu")
    m.add_argument("--inbound", required=True)
    k = sub.add_parser("pick")
    k.add_argument("--inbound", required=True)
    k.add_argument("--who", default="")
    k.add_argument("--pose", default="")
    k.add_argument("--wardrobe", default="")
    k.add_argument("--code", default="")
    args = p.parse_args()
    if args.cmd == "menu":
        out = menu(Path(args.inbound))
        return 0 if out.get("ok") else 2
    out = pick(Path(args.inbound), args.who, args.pose, args.wardrobe, args.code)
    return 0 if out.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
