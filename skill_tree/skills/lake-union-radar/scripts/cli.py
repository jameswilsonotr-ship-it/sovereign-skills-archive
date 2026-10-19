#!/usr/bin/env python3
"""Front door for lake-union-radar verbs."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vendor.bootstrap import load as load_vendor
load_vendor()

HELP = ROOT / "references" / "HELP.md"
PLANES = ROOT / "references" / "PLANES.md"
MODES = ROOT / "references" / "MODES.md"
SCRIPTS = Path(__file__).resolve().parent
NAGS = [
    "Do not slurp KEEP 227 MB, raw/, microchunks/, Letta part bins, or staged_envelopes_nowin.jsonl (360 MB).",
    "Do not claim a live Letta memory manager.",
    "Do not treat Obsidian as the lake.",
    "KLQ-WQ-009 — dated-tree modifiedTime is the 2026-06-18 ingest stamp, not talk time.",
    "Corridor CSV bbox is fat I-80. Radar is the honest geofence.",
    "PAD/NRC floats are not biography. Titles + human MD peek are the truth.",
]

def run(cmd):
    return subprocess.run(cmd, check=False).returncode

def main():
    ap = argparse.ArgumentParser(prog="lake-union-radar")
    sub = ap.add_subparsers(dest="verb")
    for name in ("help", "verbs", "planes", "nags", "modes", "lexicon", "geometry"):
        sub.add_parser(name)
    p = sub.add_parser("canon")
    p.add_argument("which", nargs="?", default="")
    p = sub.add_parser("radar")
    p.add_argument("--file", required=True)
    p.add_argument("--near", default="kenosha")
    p.add_argument("--radii", default="5,15,30")
    p.add_argument("--out", default="")
    p = sub.add_parser("union"); p.add_argument("--build", action="store_true")
    p = sub.add_parser("day"); p.add_argument("date")
    p = sub.add_parser("pad")
    p.add_argument("--hottest", action="store_true")
    p.add_argument("--sourest", action="store_true")
    p = sub.add_parser("sql"); p.add_argument("--q", required=True)
    p = sub.add_parser("embed"); p.add_argument("--q", required=True); p.add_argument("--k", type=int, default=8)
    p = sub.add_parser("peek"); p.add_argument("paths", nargs="+")
    p = sub.add_parser("near"); p.add_argument("city"); p.add_argument("--miles", type=float, default=15)
    p = sub.add_parser("feel"); p.add_argument("emotion"); p.add_argument("--k", type=int, default=8)
    p.add_argument("--min-leaves", type=int, default=20); p.add_argument("--near", default="")
    p = sub.add_parser("human"); p.add_argument("day")
    p = sub.add_parser("hop")
    p.add_argument("kind", nargs="?", default="planes")
    p.add_argument("day", nargs="?")
    args = ap.parse_args()
    verb = args.verb or "help"
    if verb in ("help", "verbs"):
        print(HELP.read_text() if HELP.exists() else "lake-union-radar"); return 0
    if verb == "planes":
        print(PLANES.read_text()); return 0
    if verb == "nags":
        print("\n".join(f"- {n}" for n in NAGS)); return 0
    if verb == "modes":
        print(MODES.read_text() if MODES.exists() else "Expert=query Heavy=rebuild"); return 0
    if verb == "canon":
        mods = ROOT / "references" / "modules"
        which = (getattr(args, "which", "") or "").strip().lower()
        pick = {
            "": mods / "INDEX.md",
            "index": mods / "INDEX.md",
            "arc": mods / "SENTIMENT_ARC.md",
            "sentiment": mods / "SENTIMENT_ARC.md",
            "pad": mods / "pad" / "MODULE.md",
            "haist": mods / "consent-haist" / "MODULE.md",
            "consent": mods / "consent-haist" / "MODULE.md",
            "brat": mods / "brat-tpe" / "MODULE.md",
            "tpe": mods / "brat-tpe" / "MODULE.md",
            "etl": mods / "etl-ingestion" / "MODULE.md",
            "ingestion": mods / "etl-ingestion" / "MODULE.md",
            "blocks": mods / "code-blocks" / "MODULE.md",
            "code": mods / "code-blocks" / "MODULE.md",
        }.get(which)
        if pick is None or not pick.exists():
            print("canon: index | pad | haist | brat | etl | blocks | arc")
            return 2
        print(pick.read_text())
        return 0
    if verb == "lexicon":
        return run([sys.executable, str(SCRIPTS / "triangulate.py"), "lexicon"])
    if verb == "radar":
        cmd = [sys.executable, str(SCRIPTS / "radar.py"), "--file", args.file, "--near", args.near, "--radii", args.radii]
        if args.out: cmd += ["--out", args.out]
        return run(cmd)
    if verb == "union":
        return run([sys.executable, str(SCRIPTS / "union_build.py"), "build"])
    if verb == "day":
        return run([sys.executable, str(SCRIPTS / "triangulate.py"), "day", args.date])
    if verb == "sql":
        return run([sys.executable, str(SCRIPTS / "union_build.py"), "sql", "--q", args.q])
    if verb == "pad":
        q = (
            "SELECT day, AVG(arousal) a, AVG(pleasure) p, COUNT(*) n FROM pad_days GROUP BY day HAVING n >= 20 ORDER BY a DESC LIMIT 8"
            if args.hottest else
            "SELECT day, AVG(pleasure) p, AVG(arousal) a, COUNT(*) n FROM pad_days GROUP BY day HAVING n >= 20 ORDER BY p ASC LIMIT 8"
            if args.sourest else
            "SELECT day, COUNT(*) n, AVG(pleasure), AVG(arousal), AVG(dominance) FROM pad_days GROUP BY day ORDER BY n DESC LIMIT 8"
        )
        return run([sys.executable, str(SCRIPTS / "union_build.py"), "sql", "--q", q])
    if verb == "embed":
        return run([sys.executable, str(SCRIPTS / "embed_tfidf.py"), "--q", args.q, "--k", str(args.k)])
    if verb == "geometry":
        return run([sys.executable, str(SCRIPTS / "tfidf_geometry.py")])
    if verb == "peek":
        return run([sys.executable, str(SCRIPTS / "peek_shards.py"), *args.paths])
    if verb == "near":
        return run([sys.executable, str(SCRIPTS / "triangulate.py"), "near", args.city, "--miles", str(args.miles)])
    if verb == "feel":
        cmd = [sys.executable, str(SCRIPTS / "triangulate.py"), "feel", args.emotion, "--k", str(args.k), "--min-leaves", str(args.min_leaves)]
        if args.near: cmd += ["--near", args.near]
        return run(cmd)
    if verb == "human":
        return run([sys.executable, str(SCRIPTS / "triangulate.py"), "day", args.day])
    if verb == "hop":
        cmd = [sys.executable, str(SCRIPTS / "hop.py"), args.kind]
        if args.day:
            cmd.append(args.day)
        return run(cmd)
    ap.print_help(); return 1

if __name__ == "__main__":
    raise SystemExit(main())
