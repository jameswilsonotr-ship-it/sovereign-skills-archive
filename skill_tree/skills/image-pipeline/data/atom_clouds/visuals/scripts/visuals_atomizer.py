#!/usr/bin/env python3
"""
Cloud C — Visuals Atomizer
IPQ-060 / IPQ-061 support

Turn 2: minimal working core.
- Walks seeds/ for .md / .txt files
- Emits atoms in a schema compatible with existing Cloud A/B (list of dicts)
- Writes a single atoms JSON under atoms/
"""

from __future__ import annotations
import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[1]  # .../visuals/
ATOMS_DIR = ROOT / "atoms"
SEEDS_DIR = ROOT / "seeds"
WORKING_DIR = ROOT / "working"
DOCS_DIR = ROOT / "docs"

CLOUD_NAME = "visuals"
VERSION = "0.2.0-core"
ATOM_FILE = ATOMS_DIR / "visuals_atoms.json"


def ensure_dirs() -> None:
    for d in (ATOMS_DIR, SEEDS_DIR, WORKING_DIR, DOCS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def chunk_text(text: str, max_len: int = 1200) -> List[str]:
    """Simple paragraph-ish chunker for visual assets."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_len:
        return [text]
    chunks = []
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    current = ""
    for p in paragraphs:
        if len(current) + len(p) + 2 <= max_len:
            current = (current + "\n\n" + p).strip()
        else:
            if current:
                chunks.append(current)
            if len(p) > max_len:
                for i in range(0, len(p), max_len):
                    chunks.append(p[i : i + max_len])
                current = ""
            else:
                current = p
    if current:
        chunks.append(current)
    return chunks


def make_atom(home: str, path: str, index: int, text: str, visual_kind: str = "general") -> Dict[str, Any]:
    return {
        "cloud": CLOUD_NAME,
        "home": home,
        "path": path,
        "atom_index": index,
        "atom": text,
        "char_len": len(text),
        "visual_kind": visual_kind,
        "created_ts": now_iso(),
        "promoted_ts": None,
        "geo": None,
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
    }


def infer_visual_kind(path: Path, text: str) -> str:
    name = path.name.lower()
    lower = text.lower()
    if "ls180" in name or "vehicle" in name or "skid" in lower:
        return "vehicle_bible"
    if "split" in name or "merge" in lower or "split-merge" in lower:
        return "split_merge"
    if "outfit" in name or "costume" in name or "dna" in lower:
        return "outfit_dna"
    if "holo" in name or "ear" in lower:
        return "holo_ear"
    if "scope" in name or "cloud c" in lower:
        return "cloud_meta"
    return "general_visual"


def atomize_file(path: Path, start_index: int = 0) -> List[Dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"WARN: could not read {path}: {e}")
        return []
    kind = infer_visual_kind(path, text)
    chunks = chunk_text(text)
    atoms = []
    for i, chunk in enumerate(chunks):
        atoms.append(
            make_atom(
                home="visuals",
                path=str(path.relative_to(ROOT)) if ROOT in path.parents else str(path),
                index=start_index + i,
                text=chunk,
                visual_kind=kind,
            )
        )
    return atoms


def run_atomize() -> Dict[str, Any]:
    ensure_dirs()
    all_atoms: List[Dict[str, Any]] = []
    idx = 0
    seed_files = sorted(SEEDS_DIR.glob("*.md")) + sorted(SEEDS_DIR.glob("*.txt"))
    scope = DOCS_DIR / "CLOUD_C_SCOPE.md"
    if scope.exists():
        seed_files = [scope] + [f for f in seed_files if f.resolve() != scope.resolve()]

    for f in seed_files:
        file_atoms = atomize_file(f, start_index=idx)
        all_atoms.extend(file_atoms)
        idx += len(file_atoms)

    ATOMS_DIR.mkdir(parents=True, exist_ok=True)
    ATOM_FILE.write_text(json.dumps(all_atoms, indent=2, ensure_ascii=False), encoding="utf-8")

    kinds = {}
    for a in all_atoms:
        k = a.get("visual_kind", "unknown")
        kinds[k] = kinds.get(k, 0) + 1

    return {
        "cloud": CLOUD_NAME,
        "version": VERSION,
        "status": "atomized",
        "atom_count": len(all_atoms),
        "atom_file": str(ATOM_FILE),
        "kinds": kinds,
        "seed_files": [str(f) for f in seed_files],
        "timestamp": now_iso(),
    }


def status() -> Dict[str, Any]:
    ensure_dirs()
    atom_count = 0
    if ATOM_FILE.exists():
        try:
            data = json.loads(ATOM_FILE.read_text(encoding="utf-8"))
            atom_count = len(data) if isinstance(data, list) else 0
        except Exception:
            atom_count = -1
    return {
        "cloud": CLOUD_NAME,
        "version": VERSION,
        "status": "ready" if atom_count >= 0 else "error",
        "atom_count": atom_count,
        "atom_file": str(ATOM_FILE) if ATOM_FILE.exists() else None,
        "seeds_dir": str(SEEDS_DIR),
        "timestamp": now_iso(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Cloud C visuals atomizer")
    parser.add_argument("--status", action="store_true", help="Print status")
    parser.add_argument("--atomize", action="store_true", help="Atomize everything currently in seeds/ (+ scope doc)")
    parser.add_argument("--ensure-dirs", action="store_true", help="Create required directories")
    args = parser.parse_args()

    ensure_dirs()

    if args.atomize:
        result = run_atomize()
        print(json.dumps(result, indent=2))
        return

    if args.status or not any(vars(args).values()):
        print(json.dumps(status(), indent=2))
        return

    if args.ensure_dirs:
        print(json.dumps({"ok": True, "dirs": [str(ATOMS_DIR), str(SEEDS_DIR), str(WORKING_DIR)]}, indent=2))


if __name__ == "__main__":
    main()
