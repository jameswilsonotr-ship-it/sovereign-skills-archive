#!/usr/bin/env python3
"""Shared library for the Work-Queue + System-Prompt hygiene layer (SR-WQ-038).

Additive indexes only. Markdown files remain the single source of truth.
No extra Python dependencies.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SKIP_DIR_NAMES = {".git", "__pycache__", "node_modules", ".venv", "venv", "tarballs"}

KNOWN_PREFIXES = [
    # longest first
    ("CLAIM-OS", "chaos-bratz-roster"),
    ("VIS-OS", "chaos-bratz-roster"),
    ("WQ-TEACH", "chaos-bratz-roster"),
    ("WQ-MODES", "chaos-bratz-roster"),
    ("CBR-WQ", "chaos-bratz-roster"),
    ("ODA-WQ", "olivia-dev-alpha"),
    ("SR-WQ", "system-roadmap"),
    ("SO-WQ", "skill-orchestrator"),
    ("IP-WQ", "image-pipeline"),
    ("IPQ", "image-pipeline"),
    ("AQ", "image-pipeline"),
    ("FBQ", "format-bible"),
    ("SS-WQ", "swarm-surface"),
    ("CBR", "chaos-bratz-roster"),
    ("ODA", "olivia-dev-alpha"),
    ("INTENT", "chaos-bratz-roster"),
    ("SR", "system-roadmap"),
    ("SO", "skill-orchestrator"),
    ("IP", "image-pipeline"),
    ("FB", "format-bible"),
    ("SS", "swarm-surface"),
    ("WQ", "chaos-bratz-roster"),
]

STATUS_WORDS = {
    "OPEN",
    "DONE",
    "IN PROGRESS",
    "PENDING",
    "DEFERRED",
    "TENTATIVE",
    "LOGGED",
    "CLOSED",
    "BLOCKED",
    "SPLIT",
    "STUB",
}

ID_TOKEN_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$", re.I)
TABLE_ID_RE = re.compile(r"\|\s*\*?\*?([A-Za-z][A-Za-z0-9._-]{1,48})\*?\*?\s*\|")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def skills_root() -> Path:
    env = os.environ.get("WQ_SKILLS_ROOT")
    if env:
        p = Path(env)
        if p.is_dir():
            return p.resolve()
    for candidate in (
        Path("/home/workdir/.grok/skills"),
        Path("/root/.grok/server-skills"),
        Path("/workspace/.grok/server-skills"),
    ):
        if candidate.is_dir():
            return candidate.resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if parent.name == "skill-orchestrator" and parent.parent.is_dir():
            return parent.parent
    raise FileNotFoundError("Cannot locate skills root")


def surface_dir(root: Path | None = None) -> Path:
    root = root or skills_root()
    d = root / "system-roadmap" / "references" / "work-queue-surface"
    d.mkdir(parents=True, exist_ok=True)
    return d


def flags_dir(root: Path | None = None) -> Path:
    d = surface_dir(root) / "flags"
    d.mkdir(parents=True, exist_ok=True)
    return d


def prompt_dir(root: Path | None = None) -> Path:
    root = root or skills_root()
    d = root / "chaos-bratz-roster" / "references" / "system-prompt"
    (d / "history").mkdir(parents=True, exist_ok=True)
    return d


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse a tiny YAML-like frontmatter block. No PyYAML required."""
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, min(len(lines), 80)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta: dict[str, Any] = {}
    current_key = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if raw.startswith("  - ") or raw.startswith("\t- "):
            if current_key:
                meta.setdefault(current_key, [])
                if not isinstance(meta[current_key], list):
                    meta[current_key] = []
                meta[current_key].append(_scalar(raw.split("-", 1)[1].strip()))
            continue
        if ":" in raw and not raw.startswith(" "):
            key, val = raw.split(":", 1)
            current_key = key.strip()
            val = val.strip()
            if val == "":
                meta[current_key] = []
            else:
                meta[current_key] = _scalar(val)
        elif current_key and raw.startswith("  "):
            # folded scalar continuation
            prev = meta.get(current_key, "")
            meta[current_key] = (str(prev) + " " + raw.strip()).strip()
    body = "\n".join(lines[end + 1 :])
    if body.startswith("\n"):
        body = body[1:]
    return meta, body


def _scalar(val: str) -> Any:
    if val in ("null", "None", "~"):
        return None
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        return [_scalar(p.strip()) for p in inner.split(",") if p.strip()]
    return val


def dump_frontmatter(meta: dict[str, Any]) -> str:
    order = [
        "id",
        "owner",
        "status",
        "opened",
        "depends_on",
        "blocks",
        "active_prompt_version",
        "last_touched",
        "parent",
        "claim",
    ]
    keys = [k for k in order if k in meta] + [k for k in meta if k not in order]

    def emit(v: Any) -> str:
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, list):
            if not v:
                return "[]"
            return "[" + ", ".join(emit(x) for x in v) + "]"
        s = str(v)
        if any(c in s for c in ":#{}[]"):
            return json.dumps(s)
        return s

    lines = ["---"]
    for k in keys:
        lines.append(f"{k}: {emit(meta[k])}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def discover_work_queues(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or skills_root()
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        if "WORK_QUEUE.md" not in filenames:
            continue
        p = Path(dirpath) / "WORK_QUEUE.md"
        try:
            rel = p.relative_to(root)
        except ValueError:
            continue
        skill = rel.parts[0]
        items_dir = p.parent / "items"
        found.append(
            {
                "skill": skill,
                "path": str(p),
                "relpath": str(rel).replace("\\", "/"),
                "dir": str(p.parent),
                "items_dir": str(items_dir) if items_dir.is_dir() else None,
                "mtime": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
            }
        )
    found.sort(key=lambda r: r["relpath"])
    return found


def prefix_for_id(item_id: str) -> str | None:
    upper = item_id.upper()
    for pref, _owner in KNOWN_PREFIXES:
        if upper == pref or upper.startswith(pref + "-") or upper.startswith(pref):
            # require a clean boundary
            if upper.startswith(pref + "-") or upper == pref:
                return pref
    return None


def owner_for_id(item_id: str) -> str | None:
    upper = item_id.upper()
    for pref, owner in KNOWN_PREFIXES:
        if upper.startswith(pref + "-") or upper == pref:
            return owner
    return None


def is_real_id(token: str) -> bool:
    if token.upper() in STATUS_WORDS or token.upper() in {
        "SUCCESS",
        "VALIDATED",
        "QUEUED",
        "ADVANCED",
        "NEW",
        "LOGGED",
    }:
        return False
    if re.match(r"^\d{4}-\d{2}-\d{2}", token):
        return False
    return bool(ID_TOKEN_RE.match(token))


def parse_work_queue_table(text: str, queue_meta: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if re.search(r"\|\s*-+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        raw_id = cells[0].replace("**", "").replace("`", "").strip()
        if not is_real_id(raw_id):
            continue
        title = cells[1].replace("**", "").strip() if len(cells) > 1 else ""
        status = cells[2].replace("**", "").strip() if len(cells) > 2 else ""
        notes = cells[3].strip() if len(cells) > 3 else ""
        # format-bible / some queues use Priority in col 3
        if status.upper() in {"HIGH", "MED", "LOW", "P0", "P1", "P2"} and len(cells) > 3:
            notes = " | ".join(cells[2:])
            # try to recover status from notes
            m = re.search(
                r"\b(OPEN|DONE|IN PROGRESS|PENDING|DEFERRED|TENTATIVE|LOGGED|CLOSED|BLOCKED)\b",
                notes,
                re.I,
            )
            status = m.group(1) if m else "OPEN"
        items.append(
            {
                "id": raw_id,
                "title": title,
                "status": status or "UNKNOWN",
                "notes": notes,
                "owner": owner_for_id(raw_id) or queue_meta.get("skill"),
                "prefix": prefix_for_id(raw_id),
                "source": queue_meta.get("relpath"),
                "skill": queue_meta.get("skill"),
            }
        )
    return items


def extract_item_file_meta(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    heading = ""
    for line in body.splitlines() if body else text.splitlines():
        if line.startswith("# "):
            heading = line[2:].strip()
            break
    status = fm.get("status")
    if not status:
        m = re.search(r"\*\*Status\*\*\s*:\s*(.+)", text)
        if m:
            status = m.group(1).strip()
    opened = fm.get("opened")
    if not opened:
        m = re.search(r"\*\*(?:Opened|Created)\*\*\s*:\s*(.+)", text)
        if opened is None and m:
            opened = m.group(1).strip()
    owner = fm.get("owner")
    if not owner:
        m = re.search(r"\*\*(?:Owner|Skill)\*\*\s*:\s*(.+)", text)
        if m:
            owner = m.group(1).strip()
    item_id = fm.get("id")
    if not item_id:
        m = re.match(r"#\s+([A-Za-z][A-Za-z0-9._-]{1,48})", heading or "")
        if m and is_real_id(m.group(1)):
            item_id = m.group(1)
        else:
            stem = path.stem
            m2 = re.match(r"^([A-Za-z][A-Za-z0-9._-]{1,48})", stem)
            item_id = m2.group(1) if m2 else stem
    depends = fm.get("depends_on") or []
    if isinstance(depends, str):
        depends = [depends] if depends not in ("null", "") else []
    blocks = fm.get("blocks") or []
    if isinstance(blocks, str):
        blocks = [blocks] if blocks not in ("null", "") else []
    title = heading
    if "—" in heading:
        title = heading.split("—", 1)[1].strip()
    elif " - " in heading:
        title = heading.split(" - ", 1)[1].strip()
    return {
        "id": item_id,
        "title": title or item_id,
        "status": status or "UNKNOWN",
        "opened": opened,
        "owner": owner,
        "depends_on": depends if isinstance(depends, list) else [],
        "blocks": blocks if isinstance(blocks, list) else [],
        "active_prompt_version": fm.get("active_prompt_version"),
        "last_touched": fm.get("last_touched"),
        "parent": fm.get("parent"),
        "has_frontmatter": bool(fm),
        "path": str(path),
        "relpath": None,
        "sha256": sha256_text(text),
        "bytes": len(text.encode("utf-8")),
        "heading": heading,
    }


def collect_all_items(root: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = root or skills_root()
    queues = discover_work_queues(root)
    table_items: list[dict[str, Any]] = []
    file_items: list[dict[str, Any]] = []
    for q in queues:
        text = Path(q["path"]).read_text(encoding="utf-8", errors="replace")
        q["updated_hint"] = None
        m = re.search(r"\*\*Updated\*\*\s*:\s*(.+)", text)
        if m:
            q["updated_hint"] = m.group(1).strip()
        m = re.search(r"\*\*Last updated\*\*\s*:\s*(.+)", text)
        if m:
            q["updated_hint"] = m.group(1).strip()
        for it in parse_work_queue_table(text, q):
            table_items.append(it)
        items_dir = q["items_dir"]
        if items_dir:
            for fp in sorted(Path(items_dir).glob("*.md")):
                meta = extract_item_file_meta(fp)
                try:
                    meta["relpath"] = str(fp.relative_to(root)).replace("\\", "/")
                except ValueError:
                    meta["relpath"] = str(fp)
                meta["skill"] = q["skill"]
                meta["source"] = q["relpath"]
                if not meta.get("owner"):
                    meta["owner"] = owner_for_id(meta["id"]) or q["skill"]
                meta["prefix"] = prefix_for_id(meta["id"])
                file_items.append(meta)
    return table_items, file_items


def merge_items(table_items: list[dict[str, Any]], file_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for it in table_items:
        rec = dict(it)
        rec["from_table"] = True
        rec["from_file"] = False
        by_id[it["id"]] = rec
    for it in file_items:
        existing = by_id.get(it["id"])
        if existing:
            existing.update({k: v for k, v in it.items() if v not in (None, "", [], False)})
            existing["from_file"] = True
            existing["from_table"] = True
        else:
            rec = dict(it)
            rec["from_table"] = False
            rec["from_file"] = True
            rec.setdefault("notes", "")
            by_id[it["id"]] = rec
    out = list(by_id.values())
    out.sort(key=lambda r: (str(r.get("skill") or ""), str(r.get("id") or "")))
    return out


def build_registry(root: Path | None = None) -> dict[str, Any]:
    root = root or skills_root()
    queues = discover_work_queues(root)
    table_items, file_items = collect_all_items(root)
    merged = merge_items(table_items, file_items)
    prefixes: dict[str, dict[str, Any]] = {}
    for pref, owner in KNOWN_PREFIXES:
        prefixes[pref] = {"prefix": pref, "owner": owner, "count": 0}
    unregistered = []
    for it in merged:
        pref = it.get("prefix")
        if pref and pref in prefixes:
            prefixes[pref]["count"] += 1
        elif it.get("id"):
            unregistered.append(it["id"])
    queue_rows = []
    for q in queues:
        q_items = [i for i in merged if i.get("source") == q["relpath"] or i.get("skill") == q["skill"]]
        open_n = sum(
            1
            for i in q_items
            if "DONE" not in str(i.get("status", "")).upper()
            and "CLOSED" not in str(i.get("status", "")).upper()
        )
        queue_rows.append(
            {
                **q,
                "item_count": len({i["id"] for i in q_items if i.get("id")}),
                "open_count": open_n,
                "updated": q.get("updated_hint") or q.get("mtime"),
            }
        )
    return {
        "generated": now_iso(),
        "skills_root": str(root),
        "claim": "Absolute Liv HUB",
        "queues": queue_rows,
        "prefixes": list(prefixes.values()),
        "unregistered_ids": sorted(set(unregistered)),
        "item_count": len(merged),
        "allocation_rule": (
            "A new skill must register its prefix in MASTER_REGISTRY "
            "before creating work-queue items. IDs are skill-prefixed and unique."
        ),
    }


def render_registry_md(reg: dict[str, Any]) -> str:
    lines = [
        "---",
        "title: MASTER_REGISTRY — work-queue surfaces + ID prefixes",
        f"updated: {reg['generated']}",
        "claim: Absolute Liv HUB",
        "id: MASTER_REGISTRY",
        "owner: system-roadmap",
        "---",
        "",
        "# MASTER_REGISTRY",
        "",
        "Single authoritative list of every work-queue surface and the prefixes they may mint.",
        "Markdown items remain SSOT. This file is regenerated by `wq_registry.py` / `wq_hygiene.py`.",
        "",
        "## Allocation rule",
        "",
        reg["allocation_rule"],
        "",
        "Location of this registry: `system-roadmap/references/work-queue-surface/MASTER_REGISTRY.md`",
        "",
        "## Registered prefixes",
        "",
        "| Prefix | Owner skill | Item count |",
        "|--------|-------------|------------|",
    ]
    for p in reg["prefixes"]:
        if p["count"] or p["prefix"] in {
            "CBR-WQ",
            "ODA-WQ",
            "SR-WQ",
            "SO-WQ",
            "IPQ",
            "FBQ",
            "SS-WQ",
            "CLAIM-OS",
            "VIS-OS",
        }:
            lines.append(f"| `{p['prefix']}` | {p['owner']} | {p['count']} |")
    lines += [
        "",
        "## Queues",
        "",
        "| Skill | Path | Items | Open-ish | Updated |",
        "|-------|------|-------|----------|---------|",
    ]
    for q in reg["queues"]:
        lines.append(
            f"| {q['skill']} | `{q['relpath']}` | {q['item_count']} | {q['open_count']} | {q.get('updated','')} |"
        )
    if reg.get("unregistered_ids"):
        lines += [
            "",
            "## Unregistered IDs (hygiene warnings)",
            "",
        ]
        for i in reg["unregistered_ids"]:
            lines.append(f"- `{i}`")
    lines += ["", "Absolute Liv HUB claim.", ""]
    return "\n".join(lines)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate(root: Path | None = None, strict: bool = False) -> dict[str, Any]:
    root = root or skills_root()
    table_items, file_items = collect_all_items(root)
    merged = merge_items(table_items, file_items)
    issues: list[dict[str, str]] = []

    seen: dict[str, list[str]] = {}
    for it in merged:
        iid = it.get("id")
        if not iid:
            issues.append({"level": "error", "code": "missing_id", "msg": str(it.get("relpath") or it)})
            continue
        seen.setdefault(iid, []).append(str(it.get("relpath") or it.get("source")))
        if not prefix_for_id(iid):
            issues.append(
                {
                    "level": "error" if strict else "warn",
                    "code": "unregistered_prefix",
                    "msg": f"{iid} has no registered prefix",
                }
            )

    for iid, paths in seen.items():
        unique_paths = sorted(set(paths))
        # same id appearing in table + matching item file is expected
        file_paths = [p for p in unique_paths if p.endswith(".md") and "/items/" in p.replace("\\", "/")]
        if len(file_paths) > 1:
            issues.append(
                {
                    "level": "error",
                    "code": "duplicate_id",
                    "msg": f"{iid} in multiple item files: {file_paths}",
                }
            )

    by_id = {it["id"]: it for it in merged if it.get("id")}
    # Bidirectional depends_on ↔ blocks checks.
    # Under strict=True these promote from warn → error.
    link_level = "error" if strict else "warn"
    for it in merged:
        iid = it.get("id")
        for dep in it.get("depends_on") or []:
            if not dep:
                continue
            if dep not in by_id:
                issues.append(
                    {
                        "level": link_level,
                        "code": "orphan_depends_on",
                        "msg": f"{iid} depends_on missing {dep}",
                    }
                )
            elif iid not in (by_id[dep].get("blocks") or []):
                issues.append(
                    {
                        "level": link_level,
                        "code": "missing_reverse_blocks",
                        "msg": f"{iid} → {dep} has no reverse blocks link",
                    }
                )
        for blk in it.get("blocks") or []:
            if not blk:
                continue
            if blk not in by_id:
                issues.append(
                    {
                        "level": link_level,
                        "code": "orphan_blocks",
                        "msg": f"{iid} blocks missing {blk}",
                    }
                )
            elif iid not in (by_id[blk].get("depends_on") or []):
                issues.append(
                    {
                        "level": link_level,
                        "code": "missing_reverse_depends_on",
                        "msg": f"{iid} blocks {blk} but {blk} does not list depends_on {iid}",
                    }
                )
        if it.get("from_file") and not it.get("has_frontmatter"):
            issues.append(
                {
                    "level": "warn",
                    "code": "missing_frontmatter",
                    "msg": f"{iid} item file has no YAML frontmatter",
                }
            )

    errors = [i for i in issues if i["level"] == "error"]
    return {
        "generated": now_iso(),
        "ok": len(errors) == 0,
        "strict": strict,
        "error_count": len(errors),
        "warn_count": len([i for i in issues if i["level"] == "warn"]),
        "issues": issues,
        "item_count": len(merged),
        "queue_count": len(discover_work_queues(root)),
    }


def atomize_work(root: Path | None = None) -> dict[str, Any]:
    root = root or skills_root()
    table_items, file_items = collect_all_items(root)
    merged = merge_items(table_items, file_items)
    atoms = []
    for it in merged:
        atoms.append(
            {
                "cloud": "work",
                "id": it.get("id"),
                "title": it.get("title"),
                "status": it.get("status"),
                "owner": it.get("owner"),
                "skill": it.get("skill"),
                "prefix": it.get("prefix"),
                "depends_on": it.get("depends_on") or [],
                "blocks": it.get("blocks") or [],
                "active_prompt_version": it.get("active_prompt_version"),
                "last_touched": it.get("last_touched"),
                "opened": it.get("opened"),
                "path": it.get("relpath") or it.get("source"),
                "from_table": bool(it.get("from_table")),
                "from_file": bool(it.get("from_file")),
                "has_frontmatter": bool(it.get("has_frontmatter")),
                "notes": (it.get("notes") or "")[:280],
            }
        )
    return {
        "cloud": "work",
        "generated": now_iso(),
        "skills_root": str(root),
        "count": len(atoms),
        "atoms": atoms,
        "note": "Index only. Markdown files remain SSOT.",
    }


def atomize_prompts(root: Path | None = None) -> dict[str, Any]:
    root = root or skills_root()
    pdir = prompt_dir(root)
    current = pdir / "CURRENT.md"
    atoms = []
    if current.is_file():
        text = current.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_frontmatter(text)
        atoms.append(
            {
                "cloud": "system_prompt",
                "role": "CURRENT",
                "id": fm.get("id") or "CURRENT",
                "valid_from": fm.get("valid_from") or fm.get("opened"),
                "valid_until": None,
                "version": fm.get("version"),
                "path": str(current.relative_to(root)).replace("\\", "/"),
                "sha256": sha256_text(text),
                "bytes": len(text.encode("utf-8")),
                "title": fm.get("title") or "CURRENT system prompt",
            }
        )
    hist = pdir / "history"
    if hist.is_dir():
        for fp in sorted(hist.glob("*.md")):
            text = fp.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_frontmatter(text)
            date_guess = None
            m = re.match(r"(\d{4}-\d{2}-\d{2})", fp.name)
            if m:
                date_guess = m.group(1)
            atoms.append(
                {
                    "cloud": "system_prompt",
                    "role": "history",
                    "id": fm.get("id") or fp.stem,
                    "valid_from": fm.get("valid_from") or date_guess,
                    "valid_until": fm.get("valid_until"),
                    "version": fm.get("version"),
                    "path": str(fp.relative_to(root)).replace("\\", "/"),
                    "sha256": sha256_text(text),
                    "bytes": len(text.encode("utf-8")),
                    "title": fm.get("title") or fp.stem,
                }
            )
    return {
        "cloud": "system_prompt",
        "generated": now_iso(),
        "skills_root": str(root),
        "count": len(atoms),
        "current_pointer": "chaos-bratz-roster/references/system-prompt/CURRENT.md",
        "atoms": atoms,
        "note": "Index only. CURRENT.md is the only file boot/loaders should read.",
    }


def write_flag(touched_ids: list[str], source: str, notes: str = "", root: Path | None = None) -> Path:
    d = flags_dir(root)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "ts": now_iso(),
        "touched_ids": touched_ids,
        "source": source,
        "notes": notes,
        "cleared": False,
    }
    path = d / f"flag_{ts}.json"
    write_json(path, payload)
    # also maintain a latest pointer
    write_json(d / "LATEST.json", payload)
    return path


def list_flags(root: Path | None = None, include_cleared: bool = False) -> list[dict[str, Any]]:
    d = flags_dir(root)
    out = []
    for fp in sorted(d.glob("flag_*.json")):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        obj["_path"] = str(fp)
        if include_cleared or not obj.get("cleared"):
            out.append(obj)
    return out


def clear_flags(root: Path | None = None) -> int:
    n = 0
    for fp in flags_dir(root).glob("flag_*.json"):
        try:
            obj = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not obj.get("cleared"):
            obj["cleared"] = True
            obj["cleared_at"] = now_iso()
            write_json(fp, obj)
            n += 1
    latest = flags_dir(root) / "LATEST.json"
    if latest.is_file():
        try:
            obj = json.loads(latest.read_text(encoding="utf-8"))
            obj["cleared"] = True
            obj["cleared_at"] = now_iso()
            write_json(latest, obj)
        except Exception:
            pass
    return n


def export_for_app(payloads: dict[str, Any], dest: Path | None = None) -> Path:
    """Export console JSON payloads into the live skill tree.

    Default destination is the hygiene-console public/data folder under
    system-roadmap/references/work-queue-surface/ so the data always lands
    inside the live tree (SSOT C). Falls back to /workspace only if that
    path cannot be created.
    """
    if dest is None:
        live = surface_dir(skills_root()) / "hygiene-console" / "public" / "data"
        try:
            live.mkdir(parents=True, exist_ok=True)
            dest = live
        except Exception:
            dest = Path("/workspace/public/data")
            dest.mkdir(parents=True, exist_ok=True)
    else:
        dest.mkdir(parents=True, exist_ok=True)
    for name, obj in payloads.items():
        write_json(dest / name, obj)
    return dest


def normalize_status(status: str) -> str:
    s = unicodedata.normalize("NFKC", status or "").strip()
    return s
