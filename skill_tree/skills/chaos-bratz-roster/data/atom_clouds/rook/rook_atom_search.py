#!/usr/bin/env python3
"""Rook atom cloud searcher."""
import json, sys
from pathlib import Path

CLOUD = Path(__file__).parent / "rook_atom_cloud.json"

def search(query: str, limit: int = 12, interest: str | None = None):
    data = json.loads(CLOUD.read_text())
    q = query.lower().strip()
    hits = []
    for a in data.get("atoms", []):
        if interest and a.get("interest") != interest:
            continue
        if q in a["atom"].lower() or q in a["path"].lower():
            hits.append(a)
            if len(hits) >= limit:
                break
    return hits

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "gear"
    hits = search(q)
    print(f"rook cloud hits for {q!r}: {len(hits)}")
    for h in hits:
        print(f"  [{h['path']}] ({h.get('interest')}) {h['atom'][:160].replace(chr(10), ' ')}...")
