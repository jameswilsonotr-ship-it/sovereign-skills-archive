#!/usr/bin/env python3
"""reel_analyze.py — Agentify foreplay on an inbound frame dir.

  python3 scripts/reel_analyze.py --inbound DIR --n-characters N --slug SLUG

Writes FOREPLAY.json + CHARACTERS.json on the inbound dir.
Also seeds CHARACTER / WARDROBE / POSE / FACE / BEAT / PHRASE stubs.
Does not mint. Does not invent tattoos. Crowd is ignored.
Human still counts mouths; --n-characters is that count.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
FACE_BINS = (
    "focus",
    "smile",
    "talk",
    "look-down",
    "neutral",
    "smirk",
    "open-mouth",
    "bite",
    "flushed",
    "averted",
    "direct",
)
FRAME_RE = re.compile(r"\.(jpe?g|png|webp)$", re.I)


def now() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def list_frames(inbound: Path) -> list[Path]:
    frames_dir = inbound / "frames" if (inbound / "frames").is_dir() else inbound
    files = [p for p in sorted(frames_dir.iterdir()) if p.is_file() and FRAME_RE.search(p.name)]
    return files


def roman(i: int) -> str:
    return ROMAN[i] if 0 <= i < len(ROMAN) else str(i + 1)


def analyze(inbound: Path, n_characters: int, slug: str) -> dict:
    inbound = inbound.resolve()
    frames = list_frames(inbound)
    n_characters = max(1, int(n_characters or 1))
    characters = []
    for i in range(n_characters):
        rid = roman(i)
        ch_slug = slug if n_characters == 1 else f"{slug}-{rid.lower()}"
        characters.append(
            {
                "id": f"char-{rid.lower()}",
                "roman": rid,
                "slug": ch_slug,
                "kind": "candidate",
                "adult": True,
                "notes": "featured mouth. crowd ignored. human-counted.",
                "marks": [],
                "skin": {"tone": "unspecified", "undertone": "unspecified", "observed": False},
                "hair": {"family": "unspecified", "color": "unspecified"},
                "pose_ids": [],
                "wardrobe_ids": [],
                "status": "draft",
            }
        )
    pose_rows = []
    beats = []
    for i, frame in enumerate(frames):
        pose_id = f"pose-{i+1:02d}"
        pose_rows.append(
            {
                "id": pose_id,
                "n": i + 1,
                "src": str(frame),
                "name": f"frame {i+1}",
                "weight": "unspecified",
                "joints": "stub",
            }
        )
        beats.append(
            {
                "t": i,
                "code": f"I-{i+1}-A",
                "pose": pose_id,
                "face": "unspecified",
                "wardrobe": "unspecified",
                "src": str(frame),
            }
        )
    if characters and pose_rows:
        characters[0]["pose_ids"] = [p["id"] for p in pose_rows]
    foreplay = {
        "schema": "agentify-foreplay/v1",
        "ok": True,
        "slug": slug,
        "inbound": str(inbound),
        "n_characters": n_characters,
        "n_frames": len(frames),
        "frames": [str(p) for p in frames],
        "characters": [{"roman": c["roman"], "slug": c["slug"], "kind": "candidate"} for c in characters],
        "poses": pose_rows,
        "wardrobes": [{"id": "wardrobe-unspecified", "name": "as seen on the still"}],
        "face_bins_legal": list(FACE_BINS),
        "rule": "frames are SOURCE. never plate A. no mint. no invented marks.",
        "created": now(),
        "ticket": "IP-WQ-101",
        "reconstructed": "2026-09-11 — missing from Vesper bags and LIV_PANE archive",
        "claim": "Absolute Liv HUB",
    }
    chars_doc = {
        "schema": "agentify-characters/v1",
        "slug": slug,
        "n": n_characters,
        "characters": characters,
        "ignored": "crowd / extras",
        "updated": now(),
    }
    (inbound / "FOREPLAY.json").write_text(json.dumps(foreplay, indent=2) + "\n", encoding="utf-8")
    (inbound / "CHARACTERS.json").write_text(json.dumps(chars_doc, indent=2) + "\n", encoding="utf-8")
    if characters:
        (inbound / "CHARACTER.json").write_text(json.dumps(characters[0], indent=2) + "\n", encoding="utf-8")
    (inbound / "WARDROBE.json").write_text(
        json.dumps({"id": "wardrobe-unspecified", "look": "as seen", "pieces": []}, indent=2) + "\n",
        encoding="utf-8",
    )
    (inbound / "POSE.json").write_text(
        json.dumps(pose_rows[0] if pose_rows else {"id": "pose-00"}, indent=2) + "\n",
        encoding="utf-8",
    )
    (inbound / "FACE.json").write_text(
        json.dumps({"bin": "unspecified", "dims": {}}, indent=2) + "\n",
        encoding="utf-8",
    )
    (inbound / "BEAT.json").write_text(
        json.dumps(beats[0] if beats else {"t": 0}, indent=2) + "\n",
        encoding="utf-8",
    )
    (inbound / "PHRASE.json").write_text(
        json.dumps({"beats": beats}, indent=2) + "\n",
        encoding="utf-8",
    )
    return foreplay


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--inbound", required=True)
    p.add_argument("--n-characters", type=int, default=1)
    p.add_argument("--slug", default="cand-reel")
    args = p.parse_args()
    inbound = Path(args.inbound)
    if not inbound.exists():
        print(json.dumps({"ok": False, "error": f"missing inbound {inbound}"}))
        return 2
    out = analyze(inbound, args.n_characters, args.slug)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
