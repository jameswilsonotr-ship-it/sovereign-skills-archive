#!/usr/bin/env python3
"""IP-WQ-173 implication retry picker. Does not lower the pick. Does not mint."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
INDEX = ROOT / "references" / "registry" / "implication_index.json"

FIRST = {
    "C": "anime-convenient-censorship",
    "E": "shunga-partial-clothing-proxy",
    "e": "shunga-partial-clothing-proxy",
    "B": "environmental-occlusion",
    "crop": "crepax-cinematic-gutter-inference",
    "gutter": "crepax-cinematic-gutter-inference",
}


def load_index() -> list[dict]:
    if not INDEX.exists():
        return []
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    return data.get("techniques") or []


def pick(lane: str, intensity: str, reason: str = "moderated") -> dict:
    lane_u = (lane or "C").upper()
    inten = (intensity or "").lower()
    if "crop" in (reason or "").lower() or "gutter" in (reason or "").lower():
        key = "crop"
    elif lane_u == "C":
        key = "C"
    elif lane_u in ("E", "B") and inten in ("e", "d"):
        key = "E"
    else:
        key = lane_u if lane_u in FIRST else inten
    slug = FIRST.get(key) or FIRST.get(lane_u) or "environmental-occlusion"
    techniques = load_index()
    hit = next((t for t in techniques if t.get("id", "").endswith(slug) or slug in t.get("source", "")), None)
    return {
        "ok": True,
        "ticket": "IP-WQ-173",
        "lane": lane_u,
        "intensity": inten,
        "same_code": True,
        "lowered_pick": False,
        "clothes_on_retreat": False,
        "implication_id": hit.get("id") if hit else f"implication.{slug}",
        "technique": slug,
        "source": (hit or {}).get("source"),
        "reason": reason,
        "keep_field": {"implication_id": hit.get("id") if hit else f"implication.{slug}", "moderation": "implied-retry"},
        "second_miss": "record moderation: implied-fallback-failed and speak the wall",
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lane", default="C")
    p.add_argument("--intensity", default="e")
    p.add_argument("--reason", default="moderated")
    p.add_argument("--code", default="")
    args = p.parse_args()
    out = pick(args.lane, args.intensity, args.reason)
    if args.code:
        out["code"] = args.code
        out["retry_code"] = args.code  # never lower
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
