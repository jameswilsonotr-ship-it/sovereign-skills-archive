#!/usr/bin/env python3
"""IP-WQ-144 target scout — loose Shorts search.

  python3 scripts/agentify_scout.py --who olette --live --n 6
Phrase: agentify target scouts go
Full token card stays on the row. Search uses 2–3 words + Shorts filter.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
SCRIPTS = ROOT / "scripts"
TARGETS = ROOT / "references" / "modules" / "agentify" / "scout_targets.json"
OUT = Path("/home/workdir/artifacts/agentify_scout")
YTDLP = Path("/tmp/yt-dlp")
COOKIES = Path("/home/workdir/artifacts/cookies.txt")
COOKIES_ALT = Path("/home/workdir/artifacts/secrets/youtube-cookies.txt")

sys.path.insert(0, str(SCRIPTS))
try:
    import inbound_classify  # type: ignore
except Exception:
    inbound_classify = None

# YouTube results filter: type = Short
SHORTS_SP = "EgIYAQ%253D%253D"


def _now() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def load_targets() -> dict:
    if not TARGETS.exists():
        return {"rows": []}
    return json.loads(TARGETS.read_text(encoding="utf-8"))


def row_for(who: str) -> dict | None:
    n = (who or "").strip().lower()
    for r in load_targets().get("rows") or []:
        if r.get("slug") == n:
            return r
    return None


def intended_query(row: dict) -> str:
    parts = [
        row.get("hair_family") or "",
        row.get("hair_color") or "",
        "woman",
        row.get("pose") or "",
        row.get("wardrobe") or "",
        row.get("motion") or "",
        row.get("query_extra") or "",
    ]
    if row.get("dance"):
        parts.append("dance")
    return re.sub(r"\s+", " ", " ".join(p for p in parts if p and p != "unspecified")).strip()


def search_query(row: dict) -> str:
    if row.get("search_q"):
        return row["search_q"].strip()
    bits = [row.get("hair_family") or "", "woman"]
    if row.get("dance"):
        bits.append("dance")
    return re.sub(r"\s+", " ", " ".join(bits)).strip()


def cookie_args() -> list[str]:
    for p in (COOKIES, COOKIES_ALT):
        if p.is_file() and p.stat().st_size > 20:
            return ["--cookies", str(p)]
    return []


def ytd() -> str:
    return str(YTDLP if YTDLP.exists() else "yt-dlp")


def search_shorts(query: str, n: int) -> dict:
    """Prefer YouTube Shorts tab. Fall back to plain ytsearch."""
    q = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={q}&sp={SHORTS_SP}"
    cmd = [
        ytd(),
        "--flat-playlist",
        "--skip-download",
        "--no-warnings",
        "--playlist-end",
        str(max(n * 3, 18)),
        "-J",
        *cookie_args(),
        url,
    ]
    raw = _run(cmd)
    entries = _entries(raw)
    if entries:
        return {"ok": True, "via": "shorts-tab", "entries": _shape(entries)}
    cmd2 = [
        ytd(),
        "--flat-playlist",
        "--skip-download",
        "--no-warnings",
        "-J",
        *cookie_args(),
        f"ytsearch{max(n * 3, 18)}:{query}",
    ]
    raw2 = _run(cmd2)
    entries2 = _entries(raw2)
    return {
        "ok": bool(entries2) or raw2.get("ok") is not False,
        "via": "ytsearch",
        "entries": _shape(entries2),
        "error": raw2.get("error") if not entries2 else None,
    }


def _run(cmd: list[str]) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return {"ok": False, "error": "yt-dlp-missing", "stdout": ""}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout", "stdout": ""}
    if p.returncode != 0 and not (p.stdout or "").strip().startswith("{"):
        return {"ok": False, "error": (p.stderr or p.stdout or "")[:400], "stdout": p.stdout}
    return {"ok": True, "stdout": p.stdout or ""}


def _entries(raw: dict) -> list:
    if not raw.get("stdout"):
        return []
    try:
        data = json.loads(raw["stdout"])
    except json.JSONDecodeError:
        return []
    return data.get("entries") or []


def _shape(entries: list) -> list[dict]:
    out = []
    for e in entries:
        if not e:
            continue
        vid = e.get("id") or ""
        if not vid or vid == "None":
            continue
        dur = e.get("duration")
        title = e.get("title") or ""
        keep, why = True, "ok"
        if dur is not None and dur < 5:
            keep, why = False, "too-short"
        elif dur is not None and dur > 180:
            keep, why = False, "too-long"
        low = title.lower()
        if any(x in low for x in ("terminal", "chrome os", "vscode", "linux ricing", "tutorial compile")):
            keep, why = False, "chrome-title"
        out.append({
            "id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": title,
            "duration": dur,
            "thumb_url": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "keep": keep,
            "why": why,
        })
    return out


def fetch_thumb(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r, dest.open("wb") as f:
            f.write(r.read())
        return dest.is_file() and dest.stat().st_size > 200
    except Exception:
        return False


def grade_hit(row: dict, e: dict) -> dict:
    """Strict pass on a loose hit. Tokens + door keys. Never a living name."""
    title = (e.get("title") or "").lower()
    dur = e.get("duration")
    score = 0
    why = []
    fam = (row.get("hair_family") or "").lower()
    color = (row.get("hair_color") or "").lower()
    pose = (row.get("pose") or "").replace("-", " ").lower()
    ward = (row.get("wardrobe") or "").replace("-", " ").lower()
    if fam and fam in title:
        score += 2; why.append("hair")
    if color and color.split("-")[-1] in title:
        score += 1; why.append("color")
    if any(w in title for w in ("woman", "girl", "she", "her", "female")):
        score += 1; why.append("woman")
    if dur is not None and 8 <= dur <= 70:
        score += 2; why.append("short-len")
    elif dur is not None and dur <= 180:
        score += 1; why.append("mid-len")
    if row.get("dance") and any(w in title for w in ("dance", "8-count", "choreo", "look back")):
        score += 2; why.append("dance")
    for k in row.get("door_keys") or []:
        if k.lower() in title:
            score += 1; why.append(f"door:{k}")
    if any(w in title for w in ("for men", "men's", " mens ", "barber men")):
        score -= 2; why.append("men-comp")
    if any(w in title for w in ("#ai", " ai ", "automatic barber")):
        score -= 2; why.append("ai-slop")
    if "how to cut" in title or "tutorial" in title:
        score -= 1; why.append("howto")
    e["strict_score"] = score
    e["strict_why"] = why
    e["strict_keep"] = score >= 2
    return e


def classify_thumb(path: Path) -> dict:
    if inbound_classify is None:
        return {"layout": "unknown", "error": "no-classify"}
    try:
        return inbound_classify.classify(path)
    except Exception as e:
        return {"layout": "unknown", "error": str(e)[:120]}


def scout(who: str, n: int = 6, dry: bool = True) -> dict:
    row = row_for(who)
    if not row:
        return {"ok": False, "error": "unknown-slug", "who": who}
    q = intended_query(row)
    sq = search_query(row)
    stamp = datetime.now(ET).strftime("%Y%m%d-%H%M%S")
    dest = OUT / row["slug"] / stamp
    dest.mkdir(parents=True, exist_ok=True)
    rec = {
        "schema": "agentify-scout-candidates/v1",
        "ok": True,
        "slug": row["slug"],
        "door": row.get("door"),
        "query": q,
        "search_query": sq,
        "n_ask": n,
        "dry": dry,
        "phase": "0-loose",
        "created": _now(),
        "claim": "Absolute Liv HUB",
        "ticket": "IP-WQ-144",
        "law": "thumbs are candidates; generate A later; tokens stay on the card",
        "row": row,
        "entries": [],
    }
    if dry:
        rec["note"] = "dry — pass --live"
    else:
        hit = search_shorts(sq, n)
        rec["search_ok"] = hit.get("ok")
        rec["search_via"] = hit.get("via")
        rec["search_error"] = hit.get("error")
        kept, dropped = [], []
        for e in hit.get("entries") or []:
            if not e.get("keep"):
                dropped.append(e)
                continue
            jpg = dest / f"thumb_{len(kept):02d}_{e['id']}.jpg"
            if e.get("thumb_url") and fetch_thumb(e["thumb_url"], jpg):
                e["thumb_path"] = str(jpg)
                e["classify"] = classify_thumb(jpg)
            grade_hit(row, e)
            kept.append(e)
            if len(kept) >= n:
                break
        if not kept:
            for e in dropped[:n]:
                e = dict(e)
                e["keep"] = True
                e["why"] = "fallback-long"
                jpg = dest / f"thumb_{len(kept):02d}_{e['id']}.jpg"
                if e.get("thumb_url") and fetch_thumb(e["thumb_url"], jpg):
                    e["thumb_path"] = str(jpg)
                    e["classify"] = classify_thumb(jpg)
                kept.append(e)
            rec["fallback"] = "no-short-hits"
        rec["entries"] = kept
        rec["strict"] = [e for e in kept if e.get("strict_keep")]
        rec["urls"] = [e.get("url") for e in kept if e.get("url")]
        rec["strict_urls"] = [e.get("url") for e in rec["strict"]]
        rec["dropped_n"] = len(dropped)
        rec["dropped"] = dropped[:12]
    path = dest / "CANDIDATES.json"
    path.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    rec["path"] = str(path)
    return rec


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--who", default="")
    p.add_argument("--all", action="store_true")
    p.add_argument("--n", type=int, default=6)
    p.add_argument("--dry", action="store_true")
    p.add_argument("--live", action="store_true")
    args = p.parse_args()
    dry = not args.live
    if args.dry:
        dry = True
    if args.all:
        slugs = [r["slug"] for r in load_targets().get("rows") or []]
        house = []
        for s in slugs:
            house.append(scout(s, args.n, dry=dry))
        index = {
            "schema": "agentify-scout-house/v1",
            "created": _now(),
            "n": len(house),
            "slugs": slugs,
            "paths": [h.get("path") for h in house],
            "urls": {h.get("slug"): h.get("urls") for h in house},
            "strict_urls": {h.get("slug"): h.get("strict_urls") for h in house},
        }
        OUT.mkdir(parents=True, exist_ok=True)
        ip = OUT / f"HOUSE_{datetime.now(ET).strftime('%Y%m%d-%H%M%S')}.json"
        ip.write_text(json.dumps(index, indent=2), encoding="utf-8")
        print(json.dumps(index, indent=2))
        return 0
    if not args.who:
        print(json.dumps({"ok": False, "error": "need --who or --all"}))
        return 2
    out = scout(args.who, args.n, dry=dry)
    print(json.dumps(out, indent=2))
    return 0 if out.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
