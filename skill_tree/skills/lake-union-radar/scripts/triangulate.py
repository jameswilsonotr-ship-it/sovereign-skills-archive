#!/usr/bin/env python3
"""near CITY / feel EMOTION / day DATE → PAD + KEEP titles + human-tree recipe."""
from __future__ import annotations
import argparse, json, sqlite3, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vendor.bootstrap import load as load_vendor
from vendor.pad_lexicon import resolve, matches, sort_key, EMOTIONS
load_vendor()

CITIES = json.loads((ROOT / "references" / "cities" / "CITIES.json").read_text())
SEED = json.loads((ROOT / "references" / "HUMAN_WALK_SEED.json").read_text())
ROLLUP = ROOT / "data" / "pad_day_rollup.jsonl"
ALT_ROLL = Path("/home/workdir/artifacts/lake/union/pad_day_rollup.jsonl")
KEEP = Path("/home/workdir/artifacts/lake/keep_mid_27mb.jsonl")
DB = Path("/home/workdir/artifacts/lake/union/union_sqlite.db")
HUMAN_ROOT = "1XMKlU-5pIGLrcCJqPYvmI9e-clDcpYiL"
RADAR_LOCK = {
    "kenosha": {
        "miles": 15,
        "days": [
            {"day": "2025-07-19", "closest_mi": 7.21, "note": "I-94 flyby, pre-talk (lake genesis Oct 2025)"},
            {"day": "2026-01-23", "closest_mi": 7.31, "note": "I-94 flyby, HUMAN HOLE — week04 has no 2026-01-23 folder"},
            {"day": "2026-01-24", "closest_mi": 7.09, "note": "closest Kenosha pass with PAD + human MD"},
        ],
    }
}

def iso_week_path(day: str) -> str:
    y, m, dd = (int(x) for x in day.split("-"))
    wk = date(y, m, dd).isocalendar()[1]
    return f"human/{y}/{m:02d}/week{wk:02d}/{day}"

def resolve_city(name: str):
    n = (name or "").strip().lower().replace("_", " ")
    if n in CITIES:
        return n, CITIES[n]
    for k, v in CITIES.items():
        if n == k or n in [a.lower() for a in v.get("aliases") or []]:
            return k, v
    return None, None

def load_rollup():
    p = ROLLUP if ROLLUP.exists() else ALT_ROLL
    rows = {}
    if not p.exists():
        return rows
    with p.open() as f:
        for line in f:
            o = json.loads(line)
            rows[o["day"]] = o
    return rows

def titles_for(days):
    hits = {d: [] for d in days}
    if not KEEP.exists():
        return hits
    with KEEP.open() as f:
        for line in f:
            o = json.loads(line)
            active = o.get("days_active") or []
            for d in active:
                if d in hits:
                    hits[d].append({
                        "id": o.get("id"),
                        "hex8": (o.get("id") or "")[:8],
                        "title": o.get("title"),
                        "twin_days": active,
                    })
    return hits

def human_for(day: str):
    seed = (SEED.get("days") or {}).get(day)
    rec = {"path": iso_week_path(day), "root": HUMAN_ROOT, "folder_id": None,
           "files": [], "hole": False, "note": None}
    if seed:
        rec["path"] = seed.get("path") or rec["path"]
        rec["folder_id"] = seed.get("folder_id")
        rec["files"] = seed.get("files") or []
        rec["note"] = seed.get("note")
        return rec
    if day == "2026-01-23":
        rec["hole"] = True
        rec["note"] = "week04 listing has no 2026-01-23 folder"
        return rec
    if day.startswith("2025-07"):
        rec["hole"] = True
        rec["note"] = "pre-talk — dated tree starts 2025-10-08"
        return rec
    rec["note"] = "no seed; sister keep-lake-query walk this path. Do not date-filter Drive by modifiedTime."
    return rec

def pack_day(day, rollup, titles, radar_meta=None):
    r = rollup.get(day) or {}
    pad = r.get("pad_mean")
    return {
        "day": day,
        "radar": radar_meta,
        "pad": pad,
        "n_leaves": r.get("n_leaves"),
        "n_sessions": r.get("n_sessions"),
        "top_domain": r.get("top_domain"),
        "sample_titles": r.get("sample_titles") or [t["title"] for t in titles.get(day, [])[:5]],
        "sessions": titles.get(day) or [],
        "human": human_for(day),
    }

def cmd_near(city: str, miles: float):
    key, pin = resolve_city(city)
    if not pin:
        return {"error": "unknown city", "city": city, "known": sorted(CITIES)}
    lock = RADAR_LOCK.get(key)
    rollup = load_rollup()
    if not lock:
        return {
            "city": key, "pin": pin, "miles": miles, "radar": "NO_LOCK",
            "hint": f"Heavy mode: python scripts/cli.py radar --file PATH --near {key} --radii {int(miles)}",
        }
    days = [d["day"] for d in lock["days"]]
    titles = titles_for(days)
    packed = [pack_day(meta["day"], rollup, titles, radar_meta=meta) for meta in lock["days"]]
    return {"city": key, "pin": pin, "miles": lock.get("miles") or miles, "n_days": len(packed), "days": packed}

def cmd_feel(emotion: str, k: int, min_leaves: int, near: str):
    name, spec = resolve(emotion)
    if not spec:
        return {"error": "unknown emotion", "emotion": emotion, "known": sorted(EMOTIONS)}
    rollup = load_rollup()
    restrict = None
    radar_days = None
    if near:
        city_hit = cmd_near(near, 15)
        if city_hit.get("error"):
            return city_hit
        if city_hit.get("radar") == "NO_LOCK":
            return {**city_hit, "emotion": name}
        restrict = {d["day"] for d in city_hit["days"]}
        radar_days = {d["day"]: d.get("radar") for d in city_hit["days"]}
    rows = []
    for day, rec in rollup.items():
        if restrict is not None and day not in restrict:
            continue
        if (rec.get("n_leaves") or 0) < min_leaves:
            continue
        if restrict is None and not matches(rec.get("pad_mean") or {}, spec):
            continue
        rows.append(rec)
    rows.sort(key=lambda r: sort_key(r, spec))
    rows = rows[:k]
    days = [r["day"] for r in rows]
    titles = titles_for(days)
    packed = [pack_day(r["day"], rollup, titles, radar_meta=(radar_days or {}).get(r["day"])) for r in rows]
    return {
        "emotion": name, "axis": spec["axis"], "nrc": spec.get("nrc"),
        "near": near or None, "min_leaves": min_leaves, "n_days": len(packed),
        "days": packed,
        "honest": "PAD/NRC are blunt. Titles + human MD peek are the truth. Do not invent biography from a float.",
    }

def cmd_day(day: str):
    rollup = load_rollup()
    titles = titles_for([day])
    return pack_day(day, rollup, titles)

def main():
    ap = argparse.ArgumentParser(prog="triangulate")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("near"); p.add_argument("city"); p.add_argument("--miles", type=float, default=15)
    p = sub.add_parser("feel"); p.add_argument("emotion"); p.add_argument("--k", type=int, default=8)
    p.add_argument("--min-leaves", type=int, default=20); p.add_argument("--near", default="")
    p = sub.add_parser("day"); p.add_argument("date")
    sub.add_parser("lexicon")
    args = ap.parse_args()
    cmd = args.cmd or "lexicon"
    if cmd == "lexicon":
        print(json.dumps({n: {"axis": s["axis"], "aliases": s["aliases"], "nrc": s.get("nrc")} for n, s in EMOTIONS.items()}, indent=2))
        return 0
    if cmd == "near":
        print(json.dumps(cmd_near(args.city, args.miles), indent=2)); return 0
    if cmd == "feel":
        print(json.dumps(cmd_feel(args.emotion, args.k, args.min_leaves, args.near), indent=2)); return 0
    if cmd == "day":
        print(json.dumps(cmd_day(args.date), indent=2)); return 0
    ap.print_help(); return 1

if __name__ == "__main__":
    raise SystemExit(main())
