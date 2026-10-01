#!/usr/bin/env python3
"""Multi-step hop. Catalog first. Fetch only the small piece the catalog names.

Expert hops:
  hop planes
  hop day YYYY-MM-DD
  hop leaf YYYY-MM-DD          (uses cached leaf_*.json if present)
  hop letta                    (list parts — do not concat)
  hop staged                   (sample seed vs fat blob)
  hop obsidian
  hop enriched YYYY-MM-DD      (daily_enriched id table)

Never download staged_envelopes_nowin (360 MB) or KEEP 227 MB.
Never concat bundle_letta_server.tar.gz.part*.bin — those are a split tarball
of the Letta *server*, not conversation shards.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOPS = ROOT / "data" / "hops"
LEAF_CACHE = HOPS / "leaf_2026-01-24.json"
RAW_DAYS = HOPS / "raw_day_folders.json"
HUMAN_SEED = ROOT / "references" / "HUMAN_WALK_SEED.json"

DAILY_ENRICHED = {
    "folder": "1mrHidOFf-O5rXxQoA-ZEdFjZDo_yofoC",
    "days": {
        "2026-05-15": {"id": "1Y6tjhobQhr6gZ_ixAJ5-swpgUesAH7xc", "bytes": 12200},
        "2026-06-08": {"id": "1kdIe4mzP46drhXl1Vjd4YzOyV-uZgaUf", "bytes": 22292},
        "2026-06-09": {"id": "1t8dnlaNfoOf8Qfz-lppZfyp-Ie1ovO9I", "bytes": 30976},
        "2026-06-10": {"id": "1ya4fsnUfCCfCoaZCcXOX_dcPUF99QRyD", "bytes": 55504},
        "2026-06-11": {"id": "1RPDEcjGNkZDVQm9OsKrDOjqkOF2YbI-3", "bytes": 40469},
        "2026-06-12": {"id": "1922fEMW3xhz-sHsBZaqK799v73PPqnZ6", "bytes": 103843},
        "2026-06-13": {"id": "1eRyOZh2z9GGgCrfh_oR44tcLubzJQ40O", "bytes": 6297},
    },
}

OBSIDIAN = {
    "sieve_lake": "1QAfB5HxkPQEpZ_4zpI_dTCTnWTQVMy9k",
    "hub": "1el2p86IwDbmiRSGwhQ8QZ9Q2I2g8Xi5E",
    "sample_convo": "18rTE09L3-rTLHFcqLVF19eHrYkwd1DSQ",
    "what_can_land": "1b9gB-VldGoMQ_gnhqLY88pPIAkXPJIuk",
    "note": "wiki overlay. 10 MD files. Not the lake. letta_hydrated=false.",
}

STAGED = {
    "seed_1959": "1PHwxrSVCV1nh0PiQymo3NXqHZb333w0R",
    "seed_1542": "1jVTQ628MC7HbJIBsKoAze513hLKY4LDv",
    "seed_6841": "1y3mBDSOPX7-Tp_lv_oRbai1ND938yfna",
    "paused_331mb": "1G5dKrT7WSdiluoa0XPGL_15siv26HAHJ",
    "nowin_360mb": "15Nz1UrOT_OmjV6Q0lW61Pgmx971DKZ1-",
    "hopable": False,
    "why": "Seeds are pipeline test leaves. Fat files are single JSONL blobs with no byte-offset index. Cannot hop a session out of 360 MB without scanning.",
}

LETTA = {
    "kind": "split tarball of Letta server, not conversation shards",
    "pattern": "bundle_letta_server.tar.gz.partNNNN.bin",
    "parts_seen": "0001–0022",
    "part_bytes": 10481474,
    "last_part_bytes": 6944083,
    "hopable": False,
    "usable_plane": "daily_enriched (letta_compat_v1), 7 day files",
}

LEAF_INDEX_FOLDER = "17ClGCkm-G61on46K4iy0cvvUvutxPVPm"


def planes():
    return {
        "hop_order": [
            "1. day (PAD / radar / feel)",
            "2. raw_day_folders.json or fleet_run → raw folder_id",
            "3. leaf_YYYY-MM-DD.json (~0.3–3 KB) → file ids",
            "4. download ONE raw json OR peek human MD by hex8",
            "5. daily_enriched only if day is 2026-05-15 or 2026-06-08..13",
        ],
        "do_not_hop": ["KEEP 227 MB", "staged_envelopes_nowin 360 MB", "letta part bins", "microchunks"],
        "obsidian": OBSIDIAN,
        "staged": STAGED,
        "letta": LETTA,
        "daily_enriched": DAILY_ENRICHED,
        "leaf_index_folder": LEAF_INDEX_FOLDER,
    }


def day_hop(day: str):
    out = {"day": day, "steps": []}
    if RAW_DAYS.exists():
        cat = json.loads(RAW_DAYS.read_text())
        rec = (cat.get("days") or {}).get(day)
        out["steps"].append(
            {
                "step": 2,
                "plane": "raw",
                "from": "data/hops/raw_day_folders.json",
                "hit": rec,
                "next": f"list folder {rec['raw_folder_id']}" if rec else "hole in fleet catalog",
            }
        )
    if day == "2026-01-24" and LEAF_CACHE.exists():
        leaf = json.loads(LEAF_CACHE.read_text())
        out["steps"].append(
            {
                "step": 3,
                "plane": "leaf_indexes",
                "from": str(LEAF_CACHE.name),
                "folder_id": leaf.get("folder_id"),
                "files": leaf.get("files"),
                "next": "download the small raw json (26 KB MisID), not the 925 KB Intimate Road Trip, unless asked",
            }
        )
    else:
        out["steps"].append(
            {
                "step": 3,
                "plane": "leaf_indexes",
                "search": f"leaf_{day}.json inside {LEAF_INDEX_FOLDER}",
                "cached": False,
            }
        )
    if HUMAN_SEED.exists():
        seed = json.loads(HUMAN_SEED.read_text())
        h = (seed.get("days") or {}).get(day)
        out["steps"].append({"step": 4, "plane": "human", "seed": h or "no seed — sister keep-lake-query walk"})
    enr = DAILY_ENRICHED["days"].get(day)
    out["steps"].append(
        {
            "step": 5,
            "plane": "daily_enriched",
            "hit": enr,
            "note": "GPS names live here when present. Thin dates only.",
        }
    )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", nargs="?", default="planes")
    ap.add_argument("day", nargs="?")
    args = ap.parse_args()
    kind = args.kind
    day = args.day
    if kind in ("planes", "help"):
        print(json.dumps(planes(), indent=2))
        return 0
    if kind in ("day", "leaf"):
        if not day:
            raise SystemExit("hop day YYYY-MM-DD")
        print(json.dumps(day_hop(day), indent=2))
        return 0
    if kind == "letta":
        print(json.dumps(LETTA, indent=2))
        return 0
    if kind == "staged":
        print(json.dumps(STAGED, indent=2))
        return 0
    if kind == "obsidian":
        print(json.dumps(OBSIDIAN, indent=2))
        return 0
    if kind == "enriched":
        if day:
            print(json.dumps({"day": day, "file": DAILY_ENRICHED["days"].get(day)}, indent=2))
        else:
            print(json.dumps(DAILY_ENRICHED, indent=2))
        return 0
    raise SystemExit(f"unknown hop {kind}")


if __name__ == "__main__":
    raise SystemExit(main())
