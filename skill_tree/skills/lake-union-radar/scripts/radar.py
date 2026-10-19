#!/usr/bin/env python3
"""Stream-scan a Timeline.json for points near a pin. No ijson required."""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

def _pins():
    import json
    cities = json.loads((Path(__file__).resolve().parents[1] / "references" / "cities" / "CITIES.json").read_text())
    out = {k: (v["lat"], v["lon"]) for k, v in cities.items()}
    for k, v in list(cities.items()):
        for a in v.get("aliases") or []:
            out[a.lower()] = (v["lat"], v["lon"])
    return out
PIN = _pins()
POINT_RE = re.compile(
    r"""(?P<lat>-?\d+(?:\.\d+)?)°\s*,\s*(?P<lon>-?\d+(?:\.\d+)?)°"""
)
TIME_RE = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?[+-]\d{2}:\d{2})")


def haversine_mi(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 3958.7613 * 2 * math.asin(min(1.0, math.sqrt(h)))


def parse_when(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def scan(path: Path, pin, radii):
    hits = {r: [] for r in radii}
    total = 0
    first = last = None
    # carry last seen time on nearby lines
    last_time = None
    with path.open("r", errors="ignore") as fh:
        for line in fh:
            tm = TIME_RE.search(line)
            if tm:
                last_time = parse_when(tm.group(1))
            m = POINT_RE.search(line)
            if not m:
                continue
            total += 1
            lat, lon = float(m.group("lat")), float(m.group("lon"))
            if last_time:
                first = last_time if first is None or last_time < first else first
                last = last_time if last is None or last_time > last else last
            mi = haversine_mi(pin, (lat, lon))
            rec = {"lat": lat, "lon": lon, "when": last_time, "miles": mi}
            for r in radii:
                if mi <= r:
                    hits[r].append(rec)
    return total, first, last, hits


def cluster(recs, gap_hours=6.0):
    recs = sorted(recs, key=lambda x: x["when"] or datetime.min)
    if not recs:
        return []
    groups, cur = [], [recs[0]]
    for h in recs[1:]:
        prev, now = cur[-1]["when"], h["when"]
        if prev and now and (now - prev) <= timedelta(hours=gap_hours):
            cur.append(h)
        else:
            groups.append(cur)
            cur = [h]
    groups.append(cur)
    out = []
    for g in groups:
        times = [h["when"] for h in g if h["when"]]
        out.append(
            {
                "start": min(times).isoformat() if times else None,
                "end": max(times).isoformat() if times else None,
                "points": len(g),
                "closest_mi": round(min(h["miles"] for h in g), 2),
                "sample": [g[0]["lat"], g[0]["lon"]],
            }
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--near", default="kenosha")
    ap.add_argument("--radii", default="5,15,30")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    if "," in args.near and args.near[0].isdigit() or args.near.startswith("-"):
        parts = [float(x) for x in args.near.split(",")]
        pin = (parts[0], parts[1])
        pin_name = "custom"
    else:
        pin = PIN[args.near.lower()]
        pin_name = args.near.lower()
    radii = [float(x) for x in args.radii.split(",")]
    path = Path(args.file)
    total, first, last, hits = scan(path, pin, radii)
    report = {
        "file": str(path),
        "pin": {"name": pin_name, "lat": pin[0], "lon": pin[1]},
        "points_scanned": total,
        "span": {
            "first": first.isoformat() if first else None,
            "last": last.isoformat() if last else None,
        },
        "radii_miles": {},
    }
    for r in radii:
        groups = cluster(hits[r])
        days = sorted({(h["when"].date().isoformat()) for h in hits[r] if h["when"]})
        report["radii_miles"][str(r)] = {
            "points": len(hits[r]),
            "passes": len(groups),
            "unique_days": days,
            "pass_summaries": groups,
        }
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text)


if __name__ == "__main__":
    main()
