#!/usr/bin/env python3
"""Live deterministic atom_search — Cloud A + B + C (Heavy restore 2026-08-13)"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import List, Dict, Any, Optional

CLOUD_A = Path("/home/workdir/.grok/skills/chaos-bratz-roster/data/atom_clouds/canonical/memory_atomizer.json")
CLOUD_B = Path("/home/workdir/.grok/skills/chaos-bratz-roster/data/atom_clouds/canonical/skill_surface_atomizer.json")
CLOUD_C = Path("/home/workdir/.grok/skills/image-pipeline/data/atom_clouds/visuals/atoms/visuals_atoms.json")
CLOUD_MAP = {"memory": CLOUD_A, "skill_surface": CLOUD_B, "visuals": CLOUD_C}
VISUAL_TOKENS = {"visual","dna","outfit","holo","ear","ears","split-merge","split","merge","ls180","vehicle","bible","reference","plate","implication","character","lock","costume","holo-ear","core mark","pixie","tattoo","harness","strappy","bondage"}

def load_cloud(name: str) -> List[Dict[str, Any]]:
    path = CLOUD_MAP.get(name)
    if not path or not path.exists(): return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list): return []
        for a in data: a.setdefault("cloud", name)
        return data
    except Exception as e:
        print(f"WARN: failed to load {name}: {e}", flush=True)
        return []

def should_prefer_visual(query: str) -> bool:
    q = query.lower()
    return any(tok in q for tok in VISUAL_TOKENS)

def score_atom(atom: Dict[str, Any], terms: List[str]) -> int:
    text = (atom.get("atom") or "").lower()
    path = (atom.get("path") or "").lower()
    kind = (atom.get("visual_kind") or "").lower()
    blob = text + " " + path + " " + kind
    return sum(1 for t in terms if t in blob)

def atom_search(query: str, clouds: Optional[List[str]] = None, prefer_visual: bool = True,
                owner: Optional[str] = None, path_prefix: Optional[str] = None,
                kind: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    if clouds is None: clouds = ["memory", "skill_surface", "visuals"]
    if prefer_visual and should_prefer_visual(query):
        ordered = [c for c in ["visuals"] if c in clouds] + [c for c in clouds if c != "visuals"]
        clouds = ordered
    terms = [t for t in re.split(r"\s+", query.lower().strip()) if t]
    results: List[tuple] = []
    for cname in clouds:
        for a in load_cloud(cname):
            if owner and a.get("owner") != owner and a.get("home") != owner: continue
            if path_prefix and not (a.get("path") or "").startswith(path_prefix): continue
            if kind and a.get("visual_kind") != kind: continue
            sc = score_atom(a, terms) if terms else 1
            if sc > 0 or not terms: results.append((sc, a))
    results.sort(key=lambda x: (-x[0], x[1].get("atom_index", 0)))
    return [a for _, a in results[:limit]]

def context_lookup(query: str, clouds: Optional[List[str]] = None, limit: int = 8) -> Dict[str, Any]:
    prefer = should_prefer_visual(query)
    res = atom_search(query, clouds=clouds, prefer_visual=prefer, limit=limit)
    return {"query": query, "results": res, "clouds_searched": clouds or ["memory","skill_surface","visuals"], "prefer_visual": prefer, "count": len(res)}

def main():
    p = argparse.ArgumentParser(description="Union atom search A+B+C")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--cloud", action="append", dest="clouds")
    p.add_argument("--limit", type=int, default=8)
    p.add_argument("--kind", default=None)
    p.add_argument("--owner", default=None)
    p.add_argument("--path-prefix", default=None)
    p.add_argument("--no-prefer-visual", action="store_true")
    p.add_argument("--status", action="store_true")
    args = p.parse_args()
    if args.status:
        status = {n: {"path": str(p), "exists": p.exists(), "atom_count": len(load_cloud(n))} for n,p in CLOUD_MAP.items()}
        print(json.dumps(status, indent=2)); return
    results = atom_search(args.query, clouds=args.clouds, prefer_visual=not args.no_prefer_visual,
                          owner=args.owner, path_prefix=args.path_prefix, kind=args.kind, limit=args.limit)
    print(json.dumps({"query": args.query, "count": len(results), "prefer_visual": should_prefer_visual(args.query) and not args.no_prefer_visual, "results": results}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
