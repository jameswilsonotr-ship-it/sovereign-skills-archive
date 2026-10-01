#!/usr/bin/env python3
"""
Minimal deterministic search for Cloud C only.
Exists so visual atoms are queryable right now, before the library-wide
atom_search (IPQ-064 / SO-WQ-003) is restored.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ATOM_FILE = Path(__file__).resolve().parents[1] / "atoms" / "visuals_atoms.json"

def load_atoms():
    if not ATOM_FILE.exists():
        return []
    data = json.loads(ATOM_FILE.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []

def search(query: str, limit: int = 8, kind: str | None = None):
    atoms = load_atoms()
    q = query.lower().strip()
    terms = [t for t in re.split(r"\s+", q) if t]
    scored = []
    for a in atoms:
        text = (a.get("atom") or "").lower()
        score = sum(1 for t in terms if t in text)
        if kind and a.get("visual_kind") != kind:
            continue
        if score > 0 or not terms:
            scored.append((score, a))
    scored.sort(key=lambda x: (-x[0], x[1].get("atom_index", 0)))
    return [a for _, a in scored[:limit]]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--kind", default=None)
    p.add_argument("--status", action="store_true")
    args = p.parse_args()
    if args.status:
        atoms = load_atoms()
        print(json.dumps({"cloud": "visuals", "atom_count": len(atoms), "file": str(ATOM_FILE)}, indent=2))
        return
    results = search(args.query, limit=args.limit, kind=args.kind)
    print(json.dumps({"query": args.query, "count": len(results), "results": results}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
