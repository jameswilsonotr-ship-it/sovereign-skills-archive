#!/usr/bin/env python3
"""
transcript_acquire.py — Video Strategy Debrief library

Acquire a complete continuous transcript from a YouTube video using yt-dlp
auto-captions, clean it into a usable timestamped document, and archive it
under the skill's references/transcripts/ tree.

Usage:
    python3 transcript_acquire.py <youtube_url_or_id> [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def get_video_id(url_or_id: str) -> str:
    if re.match(r"^[\w-]{11}$", url_or_id):
        return url_or_id
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", url_or_id)
    if m:
        return m.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def download_vtt(video_id: str, work_dir: Path) -> Path:
    out_tmpl = str(work_dir / f"{video_id}.%(ext)s")
    cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "--sub-format", "vtt",
        "-o", out_tmpl,
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    print(f"[acquire] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("yt-dlp failed")
    vtt = work_dir / f"{video_id}.en.vtt"
    if not vtt.exists():
        # fallback name patterns
        candidates = list(work_dir.glob(f"{video_id}*.vtt"))
        if not candidates:
            raise FileNotFoundError("No VTT produced")
        vtt = candidates[0]
    return vtt


def clean_vtt(vtt_path: Path) -> list[tuple[str, str]]:
    """Return list of (MM:SS, text) with progressive deduplication."""
    content = vtt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\n+", content)
    entries: list[tuple[str, str]] = []

    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue
        ts_match = None
        text_parts = []
        for l in lines:
            if re.match(r"^\d{2}:\d{2}:\d{2}", l):
                ts_match = l
            else:
                cleaned = re.sub(r"<[^>]+>", "", l)
                if cleaned and "<c>" not in l:  # prefer non-cue lines
                    text_parts.append(cleaned)
                elif not text_parts:
                    text_parts.append(cleaned)
        if ts_match and text_parts:
            start = ts_match.split(" --> ")[0]
            h, m, s = start.split(":")
            s = s.split(".")[0]
            mmss = f"{int(h) * 60 + int(m):02d}:{s}"
            text = re.sub(r"\s+", " ", " ".join(text_parts)).strip()
            if text and len(text) > 3:
                entries.append((mmss, text))

    # Progressive merge / dedup
    final: list[tuple[str, str]] = []
    buffer = ""
    last_ts = "00:00"
    for ts, txt in entries:
        if buffer and (
            txt.startswith(buffer[-50:])
            or buffer.endswith(txt[:40])
            or txt in buffer
            or buffer in txt
        ):
            if len(txt) > len(buffer):
                buffer = txt
                last_ts = ts
            continue
        else:
            if buffer:
                final.append((last_ts, buffer))
            buffer = txt
            last_ts = ts
    if buffer:
        final.append((last_ts, buffer))

    # Sentence-level merge of short fragments
    merged: list[tuple[str, str]] = []
    cur_ts, cur = None, ""
    for ts, txt in final:
        if not cur:
            cur_ts, cur = ts, txt
            continue
        if len(txt) < 55 or (txt and not txt[0].isupper() and not txt.startswith('"')):
            cur = cur.rstrip() + " " + txt
        else:
            merged.append((cur_ts, cur.strip()))
            cur_ts, cur = ts, txt
    if cur:
        merged.append((cur_ts, cur.strip()))
    return merged


def write_transcript(
    entries: list[tuple[str, str]],
    out_path: Path,
    meta: dict,
) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# {meta.get('title', 'Unknown Title')}\n")
        f.write(f"# Channel: {meta.get('channel', 'Unknown')}\n")
        f.write(f"# Video ID: {meta.get('video_id')}\n")
        f.write(f"# Source: auto-generated English captions (cleaned continuous)\n")
        f.write("# Purpose: decision-process extraction for agentic orchestration mapping\n\n")
        for ts, txt in entries:
            f.write(f"[{ts}] {txt}\n")
    print(f"[acquire] Wrote {len(entries)} blocks → {out_path} ({out_path.stat().st_size} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Acquire + clean YouTube strategy transcript")
    parser.add_argument("url_or_id")
    parser.add_argument("--out-dir", default=".", type=Path)
    parser.add_argument("--title", default="")
    parser.add_argument("--channel", default="")
    args = parser.parse_args()

    video_id = get_video_id(args.url_or_id)
    work = args.out_dir
    work.mkdir(parents=True, exist_ok=True)

    vtt = download_vtt(video_id, work)
    entries = clean_vtt(vtt)

    meta = {
        "video_id": video_id,
        "title": args.title or f"video_{video_id}",
        "channel": args.channel or "unknown",
    }
    out = work / f"{video_id}_full_transcript.txt"
    write_transcript(entries, out, meta)
    print(f"[acquire] Done. Primary artifact: {out}")


if __name__ == "__main__":
    main()
