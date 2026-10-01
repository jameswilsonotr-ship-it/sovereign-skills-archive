#!/usr/bin/env python3
"""Named YouTube Short → multi-frame Agentify SOURCE (not plate A).

The short is a reel. We pull several frames as inspiration.
Plate A is a regenerated photoreal cousin. B heat. C anime. D rig.
Raw frames never publish as A.

Video bytes may 403/SABR from this sandbox. Then we fall back to official
thumbs and say so. Next box that can fetch googlevideo uses the same path.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
INBOUND = Path("/home/workdir/artifacts/agentify_inbound")
AGENTIFY = ROOT / "scripts" / "agentify.py"
YTDLP = Path("/tmp/yt-dlp")
COOKIES = Path("/home/workdir/artifacts/cookies.txt")
COOKIES_ALT = Path("/home/workdir/artifacts/secrets/youtube-cookies.txt")
NODE = Path("/usr/bin/node")


def video_id(url: str) -> str:
    m = re.search(r"(?:shorts/|v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not m:
        raise SystemExit("no youtube id in url")
    return m.group(1)


def fetch_thumbs(vid: str, dest: Path) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    for n in ("maxresdefault", "sddefault", "hq720", "hqdefault"):
        p = dest / f"thumb_{n}.jpg"
        r = subprocess.run(
            ["curl", "-fsSL", "-o", str(p), f"https://i.ytimg.com/vi/{vid}/{n}.jpg"],
            capture_output=True,
        )
        if r.returncode == 0 and p.exists() and p.stat().st_size > 8000:
            out.append(p)
    return out


def crop_center_third(src: Path, dest: Path) -> Path:
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(src)],
        text=True,
    ).strip()
    w, h = map(int, probe.split(","))
    if w < h * 1.4:
        shutil.copy2(src, dest)
        return dest
    cw = max(w // 3, 1)
    subprocess.check_call(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-vf", f"crop={cw}:{h}:{cw}:0", str(dest)]
    )
    return dest


def cookie_file() -> Path | None:
    for p in (COOKIES_ALT, COOKIES):
        if p.exists() and p.stat().st_size > 100:
            return p
    return None


def try_download_video(url: str, dest: Path) -> Path | None:
    if not YTDLP.exists():
        return None
    out = dest / "source.mp4"
    cookies = cookie_file()
    cmd = [
        str(YTDLP),
        "-f", "18/134/160/best[height<=480]",
        "-o", str(out),
        "--no-playlist",
        url,
    ]
    if cookies:
        cmd[1:1] = ["--cookies", str(cookies)]
    if NODE.exists():
        cmd[1:1] = ["--js-runtimes", f"node:{NODE}"]
    subprocess.run(cmd, capture_output=True, text=True)
    if out.exists() and out.stat().st_size > 50_000:
        return out
    return None


def extract_frames(video: Path, dest: Path, n: int = 8) -> list[Path]:
    """Even-interval stills across the whole short."""
    dest.mkdir(parents=True, exist_ok=True)
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(video)],
        text=True,
    ).strip()
    try:
        dur = float(probe)
    except ValueError:
        dur = 8.0
    if dur <= 0:
        dur = 8.0
    frames: list[Path] = []
    # skip first/last 4% so we are not stuck on title card / end slate
    usable = max(dur * 0.92, 0.5)
    start = dur * 0.04
    for i in range(n):
        t = start + (usable * i / max(n - 1, 1))
        p = dest / f"frame_{i:02d}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}",
             "-i", str(video), "-frames:v", "1", "-q:v", "3", str(p)],
            check=False,
        )
        if p.exists() and p.stat().st_size > 4000:
            frames.append(p)
    return frames


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: yt_short_ingest.py URL [--who SLUG] [--frames N]", file=sys.stderr)
        return 2
    url = argv[1]
    who = "cand-yt-short"
    n_frames = 8
    if "--who" in argv:
        who = argv[argv.index("--who") + 1]
    if "--frames" in argv:
        n_frames = int(argv[argv.index("--frames") + 1])
    vid = video_id(url)
    dest = INBOUND / f"yt-{vid}"
    dest.mkdir(parents=True, exist_ok=True)
    frame_dir = dest / "frames"
    frame_dir.mkdir(exist_ok=True)

    video = try_download_video(url, dest)
    source_kind = "video-frames"
    frames: list[Path] = []
    if video:
        frames = extract_frames(video, frame_dir, n_frames)
    if not frames:
        source_kind = "thumb-fallback-403"
        thumbs = fetch_thumbs(vid, dest)
        if thumbs:
            hero = dest / "still_hero.jpg"
            crop_center_third(thumbs[0], hero)
            frames = [hero] + thumbs[:3]

    if not frames:
        print(json.dumps({"ok": False, "error": "no frames"}))
        return 1

    # first frame = hero SOURCE, rest = pose refs. none of these are plate A.
    hero = str(frames[0])
    frame_args = [f"{frames[0]}:hero"]
    for i, p in enumerate(frames[1:], start=1):
        role = "ref"
        frame_args.append(f"{p}:{role}")

    desc = (
        f"yt-short {vid} MULTI-FRAME source reel. "
        f"kind={source_kind}. frames are inspiration. "
        f"plate A is a regenerated cousin. no mint. source={url}"
    )
    cmd = [
        sys.executable, str(AGENTIFY), "set",
        "--who", who,
        "--desc", desc,
        "--hero", hero,
        "--slug", f"yt-{vid}",
    ]
    for spec in frame_args:
        cmd.extend(["--frame", spec])
    set_path = ""
    scrape = None
    set_error = None
    try:
        set_out = subprocess.check_output(cmd, text=True)
        data = json.loads(set_out)
        set_path = data.get("path") or ""
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        set_error = str(exc)[:400]
    if set_path and Path(set_path).exists():
        try:
            scrape_raw = subprocess.check_output([
                sys.executable, str(AGENTIFY), "scrape",
                "--from-set", set_path,
                "--feed", "yt-still",
                "--locale", "en",
                "--family", "short-reel",
            ], text=True)
            scrape = json.loads(scrape_raw)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            set_error = (set_error or "") + " scrape:" + str(exc)[:200]

    meta = {
        "ok": True,
        "vid": vid,
        "url": url,
        "who": who,
        "source_kind": source_kind,
        "n_frames": len(frames),
        "frames": [str(p) for p in frames],
        "video": str(video) if video else None,
        "set": set_path or None,
        "set_error": set_error,
        "scrape": (scrape or {}).get("path"),
        "plate_recipe": {
            "inbound_frames": "source / inspiration — never plate A",
            "A": "regenerated photoreal cousin",
            "B": "heat",
            "C": "anime",
            "D": "rig",
        },
        "promote": False,
        "at": datetime.now(ET).isoformat(timespec="seconds"),
    }
    (dest / "INGEST.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
