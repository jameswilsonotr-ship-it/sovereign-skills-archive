#!/usr/bin/env python3
"""
web_search_wrapper.py — dual-search wrapper for the porn curator.

Payload policy (important):
  - Atom-cloud side receives CLEAN search terms only.
    Domain operators (site:xvideos.com, site:rule34video.com, etc.) are stripped.
  - Web / remote side receives the FULL original query, including any site: filters.

Returns a JSON envelope with origination tags so local and live results stay distinct.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ATOMS = Path(__file__).resolve().parents[1] / "atoms" / "curator_atom_cloud.json"
ORIGINATION = "porn_curator.web_search_wrapper"

def clean_terms(query: str) -> str:
    """Strip site:/domain operators; keep the actual porn search terms."""
    q = query.strip()
    # remove site:domain and bare domain-style filters
    q = re.sub(r'\bsite:\S+', '', q, flags=re.I)
    q = re.sub(r'\b(https?://\S+)', '', q, flags=re.I)
    q = re.sub(r'\s+', ' ', q).strip()
    return q

def atom_search(query: str, limit: int = 8):
    if not ATOMS.exists():
        return []
    data = json.loads(ATOMS.read_text())
    q = query.lower().strip()
    if not q:
        return []
    hits = []
    for a in data.get("atoms", []):
        if q in a.get("atom", "").lower() or q in a.get("path", "").lower():
            hits.append({
                "path": a.get("path"),
                "atom": a.get("atom", "")[:300],
                "origination": "porn_curator.atom_cloud"
            })
            if len(hits) >= limit:
                break
    return hits

def main():
    full_query = " ".join(sys.argv[1:]).strip() or "anal first"
    clean = clean_terms(full_query)
    payload = {
        "origination": ORIGINATION,
        "full_query": full_query,
        "clean_terms_for_atom_cloud": clean,
        "atom_hits": atom_search(clean),
        "web_results": {
            "origination": "web_search",
            "query_to_use": full_query,
            "status": "pending_or_merged_by_caller",
            "note": "Caller issues real web_search with full_query (including site: operators). Atom cloud already ran on clean_terms only."
        }
    }
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
