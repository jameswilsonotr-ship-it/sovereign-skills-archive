#!/usr/bin/env python3
"""
Curator atom cloud search helper.

Prefers the newest session overlay (rich v0.4 schema), then falls back to
canonical, then to the legacy global file. Never mutates anything.

Usage:
  python3 search.py "anal"
  python3 search.py "feet" --limit 5
  python3 search.py "hyena" --session-only
  python3 search.py "inflation" --kind kink
  python3 search.py "tattoo" --owner olivia
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ATOMS_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = ATOMS_DIR / "sessions"
CANONICAL = ATOMS_DIR / "canonical" / "curator_atom_cloud.json"
LEGACY = ATOMS_DIR / "curator_atom_cloud.json"

SESSION_GLOB = "curator_session_atom_cloud_*_v0.4.json"


def load(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARN: failed to load {path}: {e}", file=sys.stderr)
        return {}


def latest_session() -> Optional[Path]:
    cands = sorted(SESSIONS_DIR.glob(SESSION_GLOB), key=lambda p: p.stat().st_mtime, reverse=True)
    if cands:
        return cands[0]
    # any session
    cands = sorted(SESSIONS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0] if cands else None


def score(atom: Dict[str, Any], q: str) -> int:
    """Simple relevance: higher is better."""
    text = " ".join([
        str(atom.get("atom", "")),
        str(atom.get("id", "")),
        str(atom.get("path", "")),
        " ".join(atom.get("tags", []) or []),
        str(atom.get("source", "")),
    ]).lower()
    if q not in text:
        return 0
    s = 1
    if atom.get("id", "").lower() == q or q in atom.get("id", "").lower():
        s += 5
    if q in (atom.get("atom") or "").lower()[:80]:
        s += 2
    # boost by excitement if present
    try:
        s += min(int(atom.get("excitement", 0) or 0), 5)
    except (TypeError, ValueError):
        pass
    return s


def collect_atoms(prefer_session: bool = True, session_only: bool = False) -> List[Dict[str, Any]]:
    atoms: List[Dict[str, Any]] = []
    seen_ids = set()

    def add(cloud: Dict[str, Any], source_label: str):
        for a in cloud.get("atoms", []):
            aid = a.get("id") or a.get("path") or (a.get("atom") or "")[:48]
            if not aid or aid in seen_ids:
                continue
            seen_ids.add(aid)
            a = dict(a)  # shallow copy
            a["_source_layer"] = source_label
            atoms.append(a)

    if prefer_session or session_only:
        sp = latest_session()
        if sp:
            add(load(sp), f"session:{sp.name}")

    if session_only:
        return atoms

    if CANONICAL.exists():
        add(load(CANONICAL), "canonical")
    if LEGACY.exists():
        add(load(LEGACY), "legacy")

    return atoms


def search(
    query: str,
    limit: int = 8,
    kind: Optional[str] = None,
    owner: Optional[str] = None,
    session_only: bool = False,
) -> List[Dict[str, Any]]:
    q = query.lower().strip()
    if not q:
        return []

    all_atoms = collect_atoms(prefer_session=True, session_only=session_only)
    scored = []
    for a in all_atoms:
        if kind and a.get("kind") != kind:
            continue
        if owner and a.get("owner") != owner:
            continue
        sc = score(a, q)
        if sc > 0:
            scored.append((sc, a))

    scored.sort(key=lambda x: (-x[0], -int(x[1].get("excitement") or 0)))
    return [a for _, a in scored[:limit]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Search curator atom clouds (session preferred)")
    parser.add_argument("query", nargs="*", default=["anal"])
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--kind", type=str, default=None, help="Filter by kind (kink|system_use|hybrid|...)")
    parser.add_argument("--owner", type=str, default=None, help="Filter by owner (olivia|bunny|shared)")
    parser.add_argument("--session-only", action="store_true")
    args = parser.parse_args()

    q = " ".join(args.query).strip() or "anal"
    hits = search(q, limit=args.limit, kind=args.kind, owner=args.owner, session_only=args.session_only)

    print(f"curator cloud hits for '{q}': {len(hits)}")
    for h in hits:
        layer = h.get("_source_layer", "?")
        own = h.get("owner", "-")
        exc = h.get("excitement", "-")
        kind = h.get("kind", "-")
        ident = h.get("id") or h.get("path") or "?"
        snippet = (h.get("atom") or "")[:120].replace("\n", " ")
        print(f"  [{layer}] id={ident} owner={own} exc={exc} kind={kind}")
        print(f"      {snippet}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
