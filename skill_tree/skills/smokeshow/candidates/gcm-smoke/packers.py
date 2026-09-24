"""Artifact-class packers: imagine / video / plates."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable

CLASSES = ("imagine", "video", "plates")
PLATES_LOCK = "consumption lock: join / production, not a catalog to eat"


def classify(path: Path) -> str | None:
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    if "secret" in name or "secrets" in parts or "cookies" in name or "tskey" in name:
        return "secret"
    if "imagine" in parts or name.startswith("imagine"):
        return "imagine"
    if path.suffix.lower() in {".mp4", ".webm", ".mov"} or "video" in parts:
        return "video"
    if "plates" in parts or "plate" in name:
        return "plates"
    return None


def pack(src_files, dest_root: Path | None = None) -> dict:
    if dest_root is None:
        raise TypeError("dest_root required")
    dest_root = Path(dest_root)
    if isinstance(src_files, Path) and src_files.is_dir():
        files = [p for p in src_files.rglob("*") if p.is_file()]
    else:
        files = list(src_files)
    out: dict = {c: [] for c in CLASSES}
    counts = {"imagine": 0, "video": 0, "plates": 0, "other": 0}
    secrets_omitted = []
    for src in files:
        src = Path(src)
        klass = classify(src)
        if klass == "secret":
            secrets_omitted.append("secrets/" + src.name)
            continue
        if klass not in CLASSES:
            counts["other"] += 1
            continue
        target_dir = dest_root / "sandbox" / klass
        target_dir.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes() if src.is_file() else b""
        dest = target_dir / src.name
        dest.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        card = target_dir / f"{src.stem}.card.md"
        extra = f"\n- {PLATES_LOCK}\n" if klass == "plates" else "\n"
        card.write_text(f"# {klass} card\n- src: {src}\n- sha256: {digest}\n- bytes: {len(data)}{extra}")
        out[klass].append(str(dest))
        counts[klass] += 1
    out["counts"] = counts
    out["secrets_omitted"] = secrets_omitted
    return out
