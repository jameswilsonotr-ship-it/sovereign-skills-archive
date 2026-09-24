#!/usr/bin/env python3
"""DEPRECATED thin search — prefer search.py (session → canonical → legacy).

Search the porn_curator atom cloud. Intended to be run in parallel with web searches.
"""

import json, sys
from pathlib import Path

CLOUD = Path(__file__).parent / "curator_atom_cloud.json"

def search(query: str, limit: int = 8):
    data = json.loads(CLOUD.read_text())
    q = query.lower().strip()
    hits = []
    for a in data.get("atoms", []):
        if q in a["atom"].lower() or q in a["path"].lower():
            hits.append(a)
            if len(hits) >= limit:
                break
    return hits

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "anal"
    hits = search(q)
    print(f"porn_curator cloud hits for '{q}': {len(hits)}")
    for h in hits:
        print(f"  [{h['path']}] {h['atom'][:140]}...")
