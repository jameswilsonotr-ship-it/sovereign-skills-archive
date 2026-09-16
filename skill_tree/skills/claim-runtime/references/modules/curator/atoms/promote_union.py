#!/usr/bin/env python3
"""
Promote / union session overlay → canonical for the porn-curator atom cloud.

Policy (documented, explicit only):
  - Never auto-write the global/canonical file.
  - Load latest (or named) session cloud + current canonical.
  - Merge by stable `id`.
  - Conflict resolution:
      1. Higher excitement wins.
      2. If equal excitement → newer last_interaction wins.
      3. If still tied → session atom wins (session is the working truth).
  - Writes new canonical and updates a small manifest.
  - Leaves original global curator_atom_cloud.json untouched unless --also-legacy is passed.

Usage:
  python3 promote_union.py                  # dry-run report
  python3 promote_union.py --apply          # write canonical + manifest
  python3 promote_union.py --session PATH   # use specific session file
  python3 promote_union.py --apply --also-legacy
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ATOMS_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = ATOMS_DIR / "sessions"
CANONICAL_DIR = ATOMS_DIR / "canonical"
MANIFEST_PATH = ATOMS_DIR / "manifest.json"
LEGACY_GLOBAL = ATOMS_DIR / "curator_atom_cloud.json"

DEFAULT_SESSION_GLOB = "curator_session_atom_cloud_*_v0.4.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def find_latest_session(explicit: Optional[str] = None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_absolute():
            p = SESSIONS_DIR / p
        if not p.exists():
            raise FileNotFoundError(f"Session file not found: {p}")
        return p
    candidates = sorted(SESSIONS_DIR.glob(DEFAULT_SESSION_GLOB), key=lambda x: x.stat().st_mtime, reverse=True)
    if not candidates:
        # fallback to any session
        candidates = sorted(SESSIONS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError("No session clouds found under sessions/")
    return candidates[0]


def atom_map(cloud: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    atoms = cloud.get("atoms", [])
    out: Dict[str, Dict[str, Any]] = {}
    for a in atoms:
        aid = a.get("id")
        if not aid:
            # legacy atoms may only have path
            aid = a.get("path") or a.get("atom", "")[:40]
        if aid:
            out[str(aid)] = a
    return out


def excitement(a: Dict[str, Any]) -> int:
    try:
        return int(a.get("excitement", 0) or 0)
    except (TypeError, ValueError):
        return 0


def last_ts(a: Dict[str, Any]) -> str:
    return str(a.get("last_interaction") or a.get("created_ts") or a.get("updated") or "")


def resolve_conflict(session_atom: Dict[str, Any], canon_atom: Dict[str, Any]) -> Dict[str, Any]:
    se = excitement(session_atom)
    ce = excitement(canon_atom)
    if se > ce:
        return session_atom
    if ce > se:
        return canon_atom
    # equal excitement → newer last_interaction
    st = last_ts(session_atom)
    ct = last_ts(canon_atom)
    if st >= ct:
        return session_atom
    return canon_atom


def merge(session: Dict[str, Any], canonical: Dict[str, Any]) -> Dict[str, Any]:
    s_map = atom_map(session)
    c_map = atom_map(canonical)

    merged: Dict[str, Dict[str, Any]] = {}
    # start with canonical
    for k, v in c_map.items():
        merged[k] = v
    # overlay session with conflict policy
    conflicts = 0
    for k, s_atom in s_map.items():
        if k in merged:
            winner = resolve_conflict(s_atom, merged[k])
            if winner is s_atom:
                conflicts += 1
            merged[k] = winner
        else:
            merged[k] = s_atom

    atoms = list(merged.values())
    # stable sort by id for reproducibility
    atoms.sort(key=lambda a: str(a.get("id") or a.get("path") or ""))

    out = {
        "cloud": "porn_curator",
        "schema_version": session.get("schema_version", "0.4.0-session"),
        "updated": _now_iso(),
        "description": "Canonical porn-curator atom cloud. Produced by explicit promote_union from session overlay.",
        "architecture_notes": session.get("architecture_notes", {}),
        "atom_count": len(atoms),
        "promoted_from_session": str(session.get("updated") or "unknown"),
        "atoms": atoms,
    }
    return out, conflicts, len(s_map), len(c_map)


def write_manifest(session_path: Path, result: Dict[str, Any], conflicts: int, s_count: int, c_count: int) -> None:
    manifest = {
        "schema_version": "0.1.0",
        "last_promoted_ts": _now_iso(),
        "session_source": str(session_path.name),
        "session_atom_count": s_count,
        "prior_canonical_atom_count": c_count,
        "result_atom_count": result["atom_count"],
        "conflicts_resolved": conflicts,
        "canonical_path": str(CANONICAL_DIR / "curator_atom_cloud.json"),
        "legacy_global_untouched": True,
        "policy": "higher excitement wins; equal → newer last_interaction; equal → session wins",
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote manifest → {MANIFEST_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote session curator cloud → canonical (explicit only)")
    parser.add_argument("--apply", action="store_true", help="Actually write canonical + manifest")
    parser.add_argument("--session", type=str, default=None, help="Specific session filename or path")
    parser.add_argument("--also-legacy", action="store_true", help="Also overwrite the old top-level global file (dangerous)")
    args = parser.parse_args()

    session_path = find_latest_session(args.session)
    print(f"Session: {session_path}")
    session = load_json(session_path)
    if not session.get("atoms"):
        print("ERROR: session has no atoms", file=sys.stderr)
        return 1

    canon_path = CANONICAL_DIR / "curator_atom_cloud.json"
    if canon_path.exists():
        canonical = load_json(canon_path)
        print(f"Canonical (existing): {canon_path} ({canonical.get('atom_count', len(canonical.get('atoms', [])))} atoms)")
    else:
        # bootstrap from empty or from legacy if desired
        canonical = {"atoms": []}
        print("Canonical: (none yet — will create)")

    result, conflicts, s_count, c_count = merge(session, canonical)
    print(f"Merge: session={s_count}  prior_canon={c_count}  result={result['atom_count']}  conflicts_resolved={conflicts}")

    if not args.apply:
        print("\n[DRY-RUN] No files written. Re-run with --apply to promote.")
        # show a few sample ids that would be added
        s_ids = set(atom_map(session).keys())
        c_ids = set(atom_map(canonical).keys())
        new_ids = sorted(s_ids - c_ids)[:8]
        print(f"New ids that would be added (sample): {new_ids}")
        return 0

    CANONICAL_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CANONICAL_DIR / "curator_atom_cloud.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote canonical → {out_path}")

    write_manifest(session_path, result, conflicts, s_count, c_count)

    if args.also_legacy:
        LEGACY_GLOBAL.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"ALSO overwrote legacy global → {LEGACY_GLOBAL}")
    else:
        print("Legacy global left untouched (as required).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
