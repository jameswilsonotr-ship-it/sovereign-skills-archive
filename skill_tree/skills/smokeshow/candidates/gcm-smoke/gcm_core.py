"""Deterministic core for grok-conversation-miner.

Stdlib + PyYAML only. Same inputs -> same tree + same stamps.
Implements GCM-WQ-011, 012, 014 (annotation), 015, 017 layout.
"""
from __future__ import annotations

import hashlib
import json
import tarfile
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

CLAIM = "Absolute Liv HUB"
SKILL = "grok-conversation-miner"
PROTOCOL_VERSION = "0.2.0-script"
TZ = ZoneInfo("America/New_York")

CANONICAL_TREE = [
    "00_HEADER.md",
    "01_TOC.md",
    "02_OMISSIONS.md",
    "03_TURNS.md",
    "04_DECISIONS.md",
    "05_SKILL_DELTA",
    "06_SANDBOX",
    "07_MAIL",
    "08_RECEIPTS",
    "MANIFEST.md",
]

REASON_CODES = (
    "SKIP-EXISTS",
    "SKIP-OVERLAP",
    "SKIP-NO-HIT",
    "TOO-LARGE",
    "SECRET",
    "NOT-WALKED",
    "PANE-VANISH",
    "OPERATOR-SAID-NO",
    "NO_TWIN",
    "KEEP-DUPLICATE",
)

SAFETY_MAX_GITHUB = 800 * 1024
BINARY_EXTS = {".tar", ".gz", ".zip", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".webm", ".gif"}


def stamp_now(when: datetime | None = None) -> dict[str, str]:
    dt = when or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ny = dt.astimezone(TZ)
    utc = dt.astimezone(timezone.utc)
    return {
        "stamp_iso_ny": ny.isoformat(timespec="seconds"),
        "stamp_iso_utc": utc.isoformat(timespec="seconds"),
        "stamp_compact": ny.strftime("%Y%m%d-%H%M%S"),
        "date_ny": ny.strftime("%Y-%m-%d"),
    }


def run_id(verb: str, slug: str, when: datetime | None = None) -> str:
    s = stamp_now(when)
    raw = f"{verb}|{slug}|{s['stamp_iso_utc']}|{CLAIM}"
    hx = hashlib.sha256(raw.encode()).hexdigest()[:8]
    return f"GCM-{s['stamp_compact']}-{hx}"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def github_safety_gate(path: Path) -> dict[str, Any]:
    size = path.stat().st_size if path.exists() else 0
    blocked = (path.suffix.lower() in BINARY_EXTS) or size > SAFETY_MAX_GITHUB or ".tar.gz" in path.name
    return {
        "path": str(path),
        "size": size,
        "blocked": blocked,
        "reason": "BINARY_OR_LARGE_PAYLOAD — GitHub Contents API path blocked. Use Google Drive."
        if blocked
        else "ok",
    }


@dataclass
class Envelope:
    stamp_iso_ny: str
    stamp_iso_utc: str
    run_id: str
    conversation_id: str
    slug: str
    skill: str = SKILL
    verb: str = "sunset"
    protocol_version: str = PROTOCOL_VERSION
    claim: str = CLAIM
    msg_id: str = ""

    def header_md(self) -> str:
        return (
            f"# 00_HEADER\n"
            f"- stamp_iso_ny: {self.stamp_iso_ny}\n"
            f"- stamp_iso_utc: {self.stamp_iso_utc}\n"
            f"- run_id: {self.run_id}\n"
            f"- msg_id: {self.msg_id or self.run_id}\n"
            f"- conversation_id: {self.conversation_id}\n"
            f"- slug: {self.slug}\n"
            f"- skill: {self.skill}\n"
            f"- verb: {self.verb}\n"
            f"- protocol_version: {self.protocol_version}\n"
            f"- claim: {self.claim}\n"
        )


@dataclass
class TocRow:
    path: str
    klass: str
    bytes: int
    sha256: str
    stamp: str


@dataclass
class OmissionRow:
    path: str
    klass: str
    reason: str
    still_gettable: bool
    pointer: str = ""
    note: str = ""


@dataclass
class TurnCard:
    turns_this_run: int
    turns_remaining_estimate: int
    blocked_on: str
    time_is_not_the_budget: bool = True

    def md(self) -> str:
        return (
            f"# 03_TURNS\n"
            f"- turns_this_run: {self.turns_this_run}\n"
            f"- turns_remaining_estimate: {self.turns_remaining_estimate}\n"
            f"- blocked_on: {self.blocked_on}\n"
            f"- time_is_not_the_budget: {str(self.time_is_not_the_budget).lower()}\n"
        )


def toc_md(rows: list[TocRow]) -> str:
    lines = ["# 01_TOC", "", "| path | class | bytes | sha256 | stamp |", "|---|---|---:|---|---|"]
    for r in rows:
        lines.append(f"| `{r.path}` | {r.klass} | {r.bytes} | `{r.sha256[:12]}` | {r.stamp} |")
    lines.append("")
    return "\n".join(lines)


def omissions_md(rows: list[OmissionRow]) -> str:
    lines = [
        "# 02_OMISSIONS",
        "",
        "SKIP is an audit line. SKIP is not silence.",
        "",
        "| path | class | reason | still_gettable | pointer | note |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r.reason not in REASON_CODES:
            raise ValueError(f"unknown reason code: {r.reason}")
        lines.append(
            f"| `{r.path}` | {r.klass} | {r.reason} | {str(r.still_gettable).lower()} | {r.pointer or '—'} | {r.note} |"
        )
    if not rows:
        lines.append("| — | — | — | — | — | none |")
    lines.append("")
    return "\n".join(lines)


def write_conv_space(root: Path, env: Envelope, toc: list[TocRow], om: list[OmissionRow],
                     turns: TurnCard, decisions: str = "", delta: str = "first-run") -> Path:
    space = root / f"{env.slug}_{env.conversation_id[:8]}"
    (space / "05_SKILL_DELTA").mkdir(parents=True, exist_ok=True)
    (space / "06_SANDBOX").mkdir(exist_ok=True)
    (space / "07_MAIL").mkdir(exist_ok=True)
    (space / "08_RECEIPTS").mkdir(exist_ok=True)
    (space / "00_HEADER.md").write_text(env.header_md())
    (space / "01_TOC.md").write_text(toc_md(toc))
    (space / "02_OMISSIONS.md").write_text(omissions_md(om))
    (space / "03_TURNS.md").write_text(turns.md())
    (space / "04_DECISIONS.md").write_text(f"# 04_DECISIONS\n\n{decisions or '(none)'}\n")
    (space / "07_MAIL" / "06_DELTA.txt").write_text(delta + "\n")
    manifest = {
        "claim": CLAIM,
        "skill": SKILL,
        "verb": env.verb,
        "run_id": env.run_id,
        "conversation_id": env.conversation_id,
        "delta": delta,
        "toc_count": len(toc),
        "omission_count": len(om),
        "tree": CANONICAL_TREE,
        "stamp_iso_ny": env.stamp_iso_ny,
        "stamp_iso_utc": env.stamp_iso_utc,
    }
    (space / "MANIFEST.md").write_text("# MANIFEST\n\n```json\n" + json.dumps(manifest, indent=2, sort_keys=True) + "\n```\n")
    return space


def tar_tree(src: Path, dest: Path) -> dict[str, Any]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dest, "w:gz") as tf:
        tf.add(src, arcname=src.name)
    gate = github_safety_gate(dest)
    gate["sha256"] = sha256_file(dest)
    return gate
