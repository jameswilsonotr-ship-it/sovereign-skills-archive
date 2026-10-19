#!/usr/bin/env python3
"""
keep_path.py — IPQ-078

Session receipt → serialized keep record (jpeg + prompt.md + keep.json)
  local A: /home/workdir/artifacts/rendered/
  local B: skill tree references/visuals/keeps/YYYY/MM/
  drive:   Liv-HUB/image-pipeline-keeps  (native upload, agent flushes)

Auto slug: --slug wins if given. Else built from agent + prompt tokens.

Usage:
  python scripts/keep_path.py --src receipt.jpg --auto-slug --agent olivia \\
      --prompt "exact tool prompt..."
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from PIL import Image

ET = ZoneInfo("America/New_York")
DEFAULT_RENDERED = Path("/home/workdir/artifacts/rendered")
SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_KEEPS = SKILL_ROOT / "references" / "visuals" / "keeps"
CONNECTOR_CFG = SKILL_ROOT / "connectors" / "google-drive" / "config.json"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
JPEG_QUALITY = 92
STOP = {
    "a", "an", "the", "of", "and", "or", "to", "in", "on", "at", "for", "with",
    "from", "by", "as", "is", "are", "be", "this", "that", "her", "his", "she",
    "he", "woman", "man", "photo", "photograph", "image", "portrait", "shot",
    "studio", "professional", "photoreal", "photorealistic", "id", "card",
}
KNOWN_AGENTS = (
    "olivia", "valerie", "eve", "rachel", "root", "miss-root", "gabriella",
    "jane", "crystal", "bunny", "vesper", "rook", "echo", "mira", "nyxelle",
    "pearl", "rusla", "dana", "stikla", "shauna", "shelby",
)


def slugify(raw: str) -> str:
    s = raw.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        raise SystemExit("keep_path: empty slug")
    if not SLUG_RE.match(s):
        raise SystemExit(f"keep_path: bad slug {s!r}")
    return s


def auto_slug(prompt: str, agent: str = "", heat: str = "") -> str:
    text = prompt.lower()
    found_agent = slugify(agent) if agent else ""
    if not found_agent:
        for name in KNOWN_AGENTS:
            if re.search(rf"\b{re.escape(name.replace('-', ' '))}\b", text) or name in text:
                found_agent = name
                break
    words: List[str] = []
    for w in re.findall(r"[a-z0-9]+", text):
        if w in STOP or len(w) < 3:
            continue
        if w == found_agent or w in words:
            continue
        words.append(w)
        if len(words) >= 4:
            break
    parts = [p for p in (found_agent, *words, f"h{heat}" if heat else "") if p]
    if not parts:
        parts = ["keep"]
    return slugify("-".join(parts))[:80]


def stamp_now() -> tuple[str, str, datetime]:
    now = datetime.now(ET)
    return now.strftime("%Y%m%d-%H%M%S"), now.isoformat(timespec="seconds"), now


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def to_jpeg_bytes(src: Path) -> bytes:
    if not src.exists() or not src.is_file():
        raise SystemExit(f"keep_path: source missing: {src}")
    if src.stat().st_size <= 0:
        raise SystemExit(f"keep_path: source empty: {src}")
    from io import BytesIO

    with Image.open(src) as im:
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            converted = im.convert("RGBA")
            bg.paste(converted, mask=converted.split()[-1])
            rgb = bg
        else:
            rgb = im.convert("RGB")
        buf = BytesIO()
        rgb.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True, subsampling=1)
        data = buf.getvalue()
    if not data:
        raise SystemExit("keep_path: jpeg encode produced empty bytes")
    return data


def write_prompt_md(
    path: Path,
    *,
    basename: str,
    slug: str,
    stamp: str,
    created: str,
    engine: str,
    orientation: str,
    source_receipt: str,
    digest: str,
    prompt: str,
    drive: str,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    extra = extra or {}
    lines = [
        "---",
        f"asset: {basename}",
        f"image: {basename}.jpg",
        f"keep: {basename}.keep.json",
        f"slug: {slug}",
        f"stamp: {stamp}",
        f"created: {created}",
        f"engine: {engine}",
        f"orientation: {orientation}",
        f"source_receipt: {source_receipt}",
        f"sha256: {digest}",
        f"drive: {drive}",
        "drive_id:",
    ]
    for k, v in extra.items():
        if v is None or v == "":
            continue
        lines.append(f"{k}: {v}")
    lines += ["---", "", "# Prompt used", "", "```", prompt.rstrip("\n"), "```", ""]
    text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")
    return text


def append_jsonl(jsonl_path: Path, row: Dict[str, str]) -> None:
    """Append-only ledger. EIO on the markdown index must not kill the keep."""
    line = json.dumps(row, separators=(",", ":")) + "\n"
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()


def append_index(index_path: Path, row: Dict[str, str]) -> None:
    """Markdown render of the index. Never raise into keep().

    IP-WQ-115: KEEP_INDEX.md EIO (2026-09-04) used to abort after the
    triple was already written. JSONL is the durable row; MD is best-effort.
    """
    header = (
        "# KEEP_INDEX — IPQ-078\n\n"
        "| stamp | slug | jpeg | prompt | keep | sha256 | drive |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    line = (
        f"| {row['stamp']} | {row['slug']} | `{row['jpeg']}` | "
        f"`{row['prompt']}` | `{row['keep']}` | `{row['sha256'][:12]}` | {row['drive']} |\n"
    )
    jsonl_path = index_path.with_suffix(".jsonl")
    try:
        append_jsonl(jsonl_path, row)
    except OSError as exc:
        sys.stderr.write(f"keep_path: KEEP_INDEX.jsonl append failed: {exc}\n")
    try:
        if not index_path.exists():
            index_path.write_text(header + line, encoding="utf-8")
            return
        text = index_path.read_text(encoding="utf-8")
        if line not in text:
            if not text.endswith("\n"):
                text += "\n"
            index_path.write_text(text + line, encoding="utf-8")
    except OSError as exc:
        partial = index_path.with_name("KEEP_INDEX.partial.md")
        try:
            partial.write_text(header + line, encoding="utf-8")
        except OSError:
            pass
        sys.stderr.write(
            f"keep_path: KEEP_INDEX.md write failed ({exc}); "
            f"triple still valid; jsonl={jsonl_path}\n"
        )


def load_connector() -> Dict[str, Any]:
    if not CONNECTOR_CFG.exists():
        return {"enabled": False}
    try:
        return json.loads(CONNECTOR_CFG.read_text(encoding="utf-8"))
    except Exception:
        return {"enabled": False}


def drive_status(cfg: Dict[str, Any]) -> str:
    return "queued" if cfg.get("enabled") and cfg.get("folder_id") else "skipped"


def keep(
    src: Path,
    slug: str,
    prompt: str,
    *,
    dest_dir: Path,
    engine: str,
    orientation: str,
    tag: str,
    extra: Dict[str, Any],
    auto: bool,
) -> Dict[str, Any]:
    if not prompt.strip():
        raise SystemExit("keep_path: prompt is required (the exact tool string)")
    if auto or not slug:
        slug = auto_slug(prompt, extra.get("agent", ""), extra.get("heat", ""))
    else:
        slug = slugify(slug)
    stamp, created, now = stamp_now()
    dest_dir.mkdir(parents=True, exist_ok=True)
    basename = f"{slug}_{stamp}" + (f"_{slugify(tag)}" if tag else "")
    jpeg_path = dest_dir / f"{basename}.jpg"
    md_path = dest_dir / f"{basename}.prompt.md"
    keep_path = dest_dir / f"{basename}.keep.json"
    jpeg_bytes = to_jpeg_bytes(src)
    digest = sha256_bytes(jpeg_bytes)
    jpeg_path.write_bytes(jpeg_bytes)
    cfg = load_connector()
    drive = drive_status(cfg)
    prompt_text = write_prompt_md(
        md_path,
        basename=basename,
        slug=slug,
        stamp=stamp,
        created=created,
        engine=engine,
        orientation=orientation,
        source_receipt=str(src.resolve()),
        digest=digest,
        prompt=prompt,
        drive=drive,
        extra=extra,
    )
    skill_month = SKILL_KEEPS / now.strftime("%Y") / now.strftime("%m")
    skill_month.mkdir(parents=True, exist_ok=True)
    skill_jpeg = skill_month / jpeg_path.name
    skill_md = skill_month / md_path.name
    skill_keep = skill_month / keep_path.name
    shutil.copy2(jpeg_path, skill_jpeg)
    shutil.copy2(md_path, skill_md)

    record = {
        "schema": "ipq-078-keep/v1",
        "basename": basename,
        "slug": slug,
        "slug_mode": "auto" if auto or extra.get("slug_mode") == "auto" else "explicit",
        "stamp": stamp,
        "created": created,
        "engine": engine,
        "orientation": orientation,
        "agent": extra.get("agent", ""),
        "heat": extra.get("heat", ""),
        "files": {
            "jpeg": jpeg_path.name,
            "prompt": md_path.name,
            "keep": keep_path.name,
        },
        "sha256": {
            "jpeg": digest,
            "prompt": sha256_text(prompt_text),
        },
        "prompt": prompt,
        "source_receipt": str(src.resolve()),
        "local": {
            "artifacts": str(dest_dir),
            "jpeg": str(jpeg_path),
            "prompt_md": str(md_path),
            "keep_json": str(keep_path),
            "skill_tree": str(skill_month),
        },
        "drive": {
            "status": drive,
            "folder_id": cfg.get("folder_id"),
            "folder_url": cfg.get("folder_url"),
            "native_tool": cfg.get("native_tool", "google_drive_upload_artifact"),
            "jpeg_id": None,
            "prompt_id": None,
            "keep_id": None,
            "uploads": [
                {
                    "artifact_path": f"/rendered/{jpeg_path.name}",
                    "file_name": jpeg_path.name,
                    "folder_id": cfg.get("folder_id"),
                    "mime_type": "image/jpeg",
                },
                {
                    "artifact_path": f"/rendered/{md_path.name}",
                    "file_name": md_path.name,
                    "folder_id": cfg.get("folder_id"),
                    "mime_type": "text/markdown",
                },
                {
                    "artifact_path": f"/rendered/{keep_path.name}",
                    "file_name": keep_path.name,
                    "folder_id": cfg.get("folder_id"),
                    "mime_type": "application/json",
                },
            ] if drive == "queued" else [],
        },
        "claim": "Absolute Liv HUB",
        "ipq": "IPQ-078",
        "step6": (
            {
                "required": True,
                "protocol": "IPQ-078-S6",
                "command": f"python3 /home/workdir/.grok/skills/image-pipeline/scripts/step6_drive_flush.py --from-keep {keep_path}",
                "gate": "python3 /home/workdir/.grok/skills/image-pipeline/scripts/step6_drive_flush.py --gate",
                "native_tool": cfg.get("native_tool", "google_drive_upload_artifact"),
                "rule": "Same turn. Call google_drive_upload_artifact for each drive.uploads row, flush_drive_queue.py --mark ids, then --gate must exit 0 BEFORE render_file or any Drive-saved claim.",
            }
            if drive == "queued"
            else {"required": False, "protocol": "IPQ-078-S6", "reason": drive}
        ),
    }
    keep_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(keep_path, skill_keep)
    append_index(
        dest_dir / "KEEP_INDEX.md",
        {
            "stamp": stamp,
            "slug": slug,
            "jpeg": jpeg_path.name,
            "prompt": md_path.name,
            "keep": keep_path.name,
            "sha256": digest,
            "drive": drive,
        },
    )
    append_index(
        SKILL_KEEPS / "KEEP_INDEX.md",
        {
            "stamp": stamp,
            "slug": slug,
            "jpeg": str(skill_jpeg.relative_to(SKILL_KEEPS)),
            "prompt": str(skill_md.relative_to(SKILL_KEEPS)),
            "keep": str(skill_keep.relative_to(SKILL_KEEPS)),
            "sha256": digest,
            "drive": drive,
        },
    )
    record["ok"] = True
    record["render_file"] = str(jpeg_path)
    record["bytes"] = len(jpeg_bytes)
    return record


def main() -> int:
    p = argparse.ArgumentParser(description="IPQ-078 keep path")
    p.add_argument("--src", required=True)
    p.add_argument("--slug", default="", help="explicit slug; omit to auto-build")
    p.add_argument("--auto-slug", action="store_true", help="force slug from agent+prompt")
    p.add_argument("--prompt", default="")
    p.add_argument("--prompt-file", default="")
    p.add_argument("--engine", default="generate_image")
    p.add_argument("--orientation", default="portrait")
    p.add_argument("--tag", default="")
    p.add_argument("--agent", default="")
    p.add_argument("--heat", default="")
    p.add_argument("--dest", default=str(DEFAULT_RENDERED))
    args = p.parse_args()
    prompt = args.prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    extra = {}
    if args.agent:
        extra["agent"] = args.agent
    if args.heat:
        extra["heat"] = args.heat
    extra["slug_mode"] = "auto" if (args.auto_slug or not args.slug) else "explicit"
    result = keep(
        Path(args.src),
        args.slug,
        prompt,
        dest_dir=Path(args.dest),
        engine=args.engine,
        orientation=args.orientation,
        tag=args.tag,
        extra=extra,
        auto=args.auto_slug or not args.slug,
    )
    print(json.dumps(result, indent=2))
    step6 = result.get("step6") or {}
    if step6.get("required"):
        print(
            "IPQ-078-S6 FLUSH REQUIRED — do not speak or render_file until "
            "step6_drive_flush.py --gate exits 0",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
