#!/usr/bin/env python3
"""search_scripts.py — keyword search over every script in the skills tree.

This is the acceleration path: do not write another declarative inventory md
when you can query the tree.

Usage:
  python3 search_scripts.py --q "render profile"
  python3 search_scripts.py --q yaml --skill image-pipeline
  python3 search_scripts.py --q heat --ext py --json
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
EXTS = {".py", ".sh", ".bash", ".js", ".ts"}
SKIP = {".git", "__pycache__", "node_modules", ".venv", "venv", "tarballs"}


def first_doc(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    body = text
    if body.startswith("#!"):
        nl = body.find("\n")
        body = body[nl + 1 :] if nl != -1 else body
    stripped = body.lstrip()
    if path.suffix == ".py" and (stripped.startswith('"""') or stripped.startswith("'''")):
        q = stripped[:3]
        end = stripped.find(q, 3)
        if end != -1:
            return " ".join(stripped[3:end].split())
    for line in body.splitlines()[:12]:
        if line.startswith("#") and len(line) > 3:
            return line.lstrip("# ").strip()
    return ""


def scan(q: str, skill: str | None, ext: str | None) -> list[dict]:
    qn = q.lower()
    hits = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() not in EXTS:
                continue
            if ext and p.suffix.lower() != ext:
                continue
            try:
                rel = p.relative_to(SKILLS_ROOT)
            except ValueError:
                continue
            sk = rel.parts[0]
            if skill and sk != skill:
                continue
            doc = first_doc(p)
            hay = f"{rel} {name} {doc}".lower()
            try:
                body = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                body = ""
            if qn not in hay and qn not in body.lower():
                continue
            hits.append(
                {
                    "skill": sk,
                    "relpath": str(rel).replace("\\", "/"),
                    "name": name,
                    "doc": doc[:180],
                    "bytes": p.stat().st_size,
                }
            )
    hits.sort(key=lambda r: (r["skill"], r["relpath"]))
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", required=True)
    ap.add_argument("--skill")
    ap.add_argument("--ext")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    hits = scan(args.q, args.skill, args.ext)
    if args.json:
        print(json.dumps({"q": args.q, "count": len(hits), "hits": hits}, indent=2))
        return
    print(f"q={args.q!r} count={len(hits)}")
    for h in hits:
        print(f"  {h['relpath']:70}  {h['doc'][:90]}")


if __name__ == "__main__":
    main()
