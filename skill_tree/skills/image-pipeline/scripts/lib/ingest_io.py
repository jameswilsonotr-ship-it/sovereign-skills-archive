#!/usr/bin/env python3
"""Inbound dir + vendor runners. No mint."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

ROOT = Path("/home/workdir/.grok/skills/image-pipeline")
INBOUND = Path("/home/workdir/artifacts/agentify_inbound")
VENDOR = ROOT / "scripts" / "vendor"
GDL = VENDOR / "bin" / "gallery-dl"
INSTA = VENDOR / "bin" / "instaloader"
COOKIES = [
    Path("/home/workdir/artifacts/secrets/youtube-cookies.txt"),
    Path("/home/workdir/artifacts/cookies.txt"),
    Path("/home/workdir/artifacts/secrets/ig-cookies.txt"),
    Path("/home/workdir/artifacts/secrets/fb-cookies.txt"),
]


def inbound_dir(prefix: str, ident: str) -> Path:
    slug = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in f"{prefix}-{ident}")[:80]
    dest = INBOUND / slug
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "frames").mkdir(exist_ok=True)
    (dest / "stills").mkdir(exist_ok=True)
    return dest


def cookie_file() -> Path | None:
    for p in COOKIES:
        if p.exists() and p.stat().st_size > 100:
            return p
    return None


def write_ingest(dest: Path, meta: dict) -> Path:
    path = dest / "INGEST.json"
    path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return path


def _vendor_env() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(VENDOR) + os.pathsep + env.get("PYTHONPATH", "")
    return env


def try_gallery_dl(url: str, dest: Path, extractor: str = "") -> tuple[list[str], str | None]:
    dest.mkdir(parents=True, exist_ok=True)
    if not GDL.exists():
        return [], "gallery-dl missing"
    cmd = [str(GDL), "--no-mtime", "-D", str(dest), url]
    ck = cookie_file()
    if ck:
        cmd[1:1] = ["--cookies", str(ck)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=40, env=_vendor_env())
    except Exception as exc:
        return [], str(exc)[:300]
    saved = [str(p) for p in dest.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4"}]
    if saved:
        return saved, None
    err = (proc.stderr or proc.stdout or "no-stills")[-400:]
    return [], err


def try_instaloader(url: str, dest: Path) -> tuple[list[str], str | None]:
    dest.mkdir(parents=True, exist_ok=True)
    if not INSTA.exists():
        return [], "instaloader missing"
    cmd = [str(INSTA), "--dirname-pattern", str(dest), "--no-videos", "--", url]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=40, env=_vendor_env())
    except Exception as exc:
        return [], str(exc)[:300]
    saved = [str(p) for p in dest.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    if saved:
        return saved, None
    return [], (proc.stderr or proc.stdout or "no-stills")[-400:]
