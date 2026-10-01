#!/usr/bin/env python3
"""agentify.py — image-pipeline subscale verb (menu B).

Single still or multi-frame set of the SAME person.
Not a top-level skill. Not a merge engine.

Usage:
  python3 agentify.py route "agentify these"
  python3 agentify.py veto --who eve
  python3 agentify.py plan --who NAME --desc "..."
  python3 agentify.py card --who NAME --desc "..."
  python3 agentify.py set --who NAME --desc "..." --hero FILE --frame FILE:role [--frame FILE:role]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
MOD = ROOT / "references" / "modules" / "agentify"
VETO_PATH = MOD / "VETO.json"
CARD_DIR = Path("/home/workdir/artifacts/inbound-queue")
SET_DIR = Path("/home/workdir/artifacts/inbound")

HIT_PATTERNS = [
    r"\bagentify\b",
    r"\bmake an agent\b",
    r"\bdraft a candidate agent\b",
    r"\bb agent\b",
    r"\bmenu b\b",
    r"\bidentify as (an? )?agent\b",
    r"\bidentify (this|her|him|them|it|these) as (an? )?agent\b",
]

# IP-WQ-168 — STT turns "identify as agent" into bare "identify".
# Media/person nouns in the same utterance promote it. Silent miss is the bug.
IDENTIFY_MEDIA_HINTS = (
    r"\b(still|stills|short|shorts|frame|frames|photo|photos|picture|pictures|"
    r"jpeg|jpg|png|webp|image|images|reel|clip|clips|video|mp4|webm)\b",
    r"youtu\.be|youtube\.com",
    r"\bthis woman\b",
    r"\bthese two\b",
    r"\bthis girl\b",
    r"\bthis person\b",
    r"\bthese (women|girls|people|frames|stills)\b",
)
LEGAL_TAGS = ("a-id", "b-heat", "c-anime", "d-rig")
LEGAL_EXTRAS = ("pose", "wardrobe", "face", "hip")


def _now() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def load_veto() -> dict:
    if VETO_PATH.exists():
        return json.loads(VETO_PATH.read_text(encoding="utf-8"))
    return {"hard_names": ["eve"], "already_core": []}


def normalize_who(who: str) -> str:
    return re.sub(r"\s+", " ", (who or "").strip().lower())


def veto_who(who: str) -> dict:
    v = load_veto()
    n = normalize_who(who)
    if not n:
        return {"ok": True, "veto": None, "class": None}
    for name in v.get("hard_names") or []:
        if n == name or n.startswith(name + " "):
            return {"ok": False, "veto": f"hard-veto:{name}", "class": "eve"}
    for name in v.get("already_core") or []:
        if n == name or n.startswith(name + " "):
            return {
                "ok": True,
                "veto": None,
                "class": "already-core",
                "kind": "core-refresh",
            }
    return {"ok": True, "veto": None, "class": None}


def _identify_has_media_or_person(t: str, has_media: bool = False) -> bool:
    if has_media:
        return True
    return any(re.search(p, t) for p in IDENTIFY_MEDIA_HINTS)


def route(text: str, has_media: bool = False) -> dict:
    t = (text or "").strip().lower()
    hit = any(re.search(p, t) for p in HIT_PATTERNS)
    identify_word = bool(re.search(r"\bidentify\b", t))
    mediaish = _identify_has_media_or_person(t, has_media)
    stt_promote = bool(identify_word and mediaish and not hit)
    if stt_promote:
        hit = True
    bare_identify = bool(identify_word and not hit)
    wants_merge = bool(re.search(r"\b(m2|m3|merge|twister)\b", t))
    multi = bool(re.search(r"\b(these|frames|set|stills|clips)\b", t))
    who = None
    m = re.search(r"\bagentify\s+(eve|olivia|liv|bunny|valerie|crystal)\b", t)
    if m:
        who = m.group(1)
    v = veto_who(who or "")
    out = {
        "ok": True,
        "hit": hit,
        "module": "agentify" if hit else None,
        "parent": "image-pipeline",
        "menu": "B" if hit else None,
        "kind": "candidate" if hit else None,
        "four_plates": bool(hit),
        "set_mode": bool(hit and multi),
        "merge": bool(hit and wants_merge),
        "bare_identify": bare_identify,
        "stt_promote": stt_promote,
        "has_media": bool(has_media or mediaish),
        "who_guess": who,
        "veto": None if v["ok"] else v["veto"],
        "note": None,
        "ticket": "IP-WQ-168",
    }
    if not hit and bare_identify:
        out["note"] = (
            "identify what — a still, a Short, this woman, these two? "
            "Say agentify if that was the verb. Do not mint."
        )
    if stt_promote:
        out["note"] = "IP-WQ-168 STT: identify + media/person entered agentify. Do not mint."
    if hit and not v["ok"]:
        out["ok"] = False
        out["veto"] = v["veto"]
    if hit and v.get("class") == "already-core":
        out["kind"] = "core-refresh"
    return out


def plan(who: str, desc: str, src: str = "", merge: bool = False, pose_refs: list | None = None) -> dict:
    v = veto_who(who)
    if not v["ok"]:
        return {"ok": False, "veto": v["veto"]}
    sys.path.insert(0, str(SCRIPTS))
    import split_plan  # type: ignore

    body = split_plan.plan(who, desc, "generate", merge)
    extra = ""
    if pose_refs:
        extra = " Pose vocabulary from the set: " + "; ".join(pose_refs) + "."
        slots = body.get("slots") or {}
        body["slots"] = {k: (val.rstrip(".") + "." + extra).strip() for k, val in slots.items()}
    body["ok"] = True
    body["module"] = "agentify"
    body["menu"] = "B"
    body["kind"] = "core-refresh" if v.get("class") == "already-core" else "candidate"
    body["src"] = src
    body["pose_refs"] = pose_refs or []
    body["merge_requested"] = bool(merge)
    return body


def card(who: str, desc: str, src: str = "", slug: str = "", frames: list | None = None) -> dict:
    v = veto_who(who)
    if not v["ok"]:
        return {"ok": False, "veto": v["veto"]}
    stamp = datetime.now(ET).strftime("%Y%m%d-%H%M%S")
    slug = slug or re.sub(r"[^a-z0-9]+", "-", normalize_who(who) or "unnamed").strip("-")
    rec = {
        "schema": "agentify-candidate/v1",
        "ok": True,
        "slug": slug,
        "who": who,
        "kind": "core-refresh" if v.get("class") == "already-core" else "candidate",
        "status": "draft",
        "desc": desc,
        "src": src,
        "frames": frames or [],
        "menu": "B",
        "plates": ["0_source", "A_realistic", "B_heat", "C_anime", "D_rig"],
        "plate_recipe": {
            "0_source": "actual inbound still / official thumb. emit first. never call this A.",
            "inbound": "same as 0_source — never publish raw still as A",
            "A_realistic": "regenerated photoreal ID card",
            "B_heat": "same identity, heat",
            "C_anime": "same identity, anime",
            "D_rig": "same identity, turnaround",
            "default_emit": ["0", "A", "B", "C", "D"],
            "ticket": "IP-WQ-204",
            "promote": False,
        },
        "promote": "CONFIRM AGENT FOR " + slug.upper(),
        "created": _now(),
        "claim": "Absolute Liv HUB",
        "ticket": "IP-WQ-094",
    }
    CARD_DIR.mkdir(parents=True, exist_ok=True)
    path = CARD_DIR / f"CANDIDATE_{slug}_{stamp}.json"
    path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    rec["path"] = str(path)
    return rec


def parse_frame(spec: str) -> dict:
    # FILE:role[:pose_slug[:wardrobe_slug]]
    parts = spec.split(":")
    path = parts[0] if parts else spec
    role = parts[1] if len(parts) > 1 and parts[1] else "ref"
    pose = parts[2] if len(parts) > 2 and parts[2] else ""
    wardrobe = parts[3] if len(parts) > 3 and parts[3] else ""
    p = Path(path).expanduser().resolve()
    return {
        "path": str(p),
        "role": role,
        "pose_slug": pose,
        "wardrobe_slug": wardrobe,
        "exists": p.is_file(),
    }


PACKS_ROOT = ROOT / "references" / "packs"
INDEX_PATH = ROOT / "references" / "registry" / "packs.index.json"
CATALOG_PATH = MOD / "ROLE_CATALOG.json"


def load_catalog() -> dict:
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {"roles": {}, "wardrobe_default": {"slug": "unspecified-wardrobe", "name": "Unspecified Wardrobe", "terms": []}}


def slugify_pack(raw: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (raw or "").strip().lower()).strip("-")
    return s or "unnamed"


def wardrobe_from_hint(hint: str) -> dict:
    t = (hint or "").lower()
    if "arena" in t or ("one-piece" in t or "onepiece" in t or "swimsuit" in t):
        return {
            "slug": "black-arena-cutout-onepiece",
            "name": "Black Arena Cutout One-Piece",
            "terms": [
                "black competitive one-piece swimsuit",
                "high-cut legs and deep side cutouts",
                "small pink arena chest logo",
            ],
        }
    cat = load_catalog().get("wardrobe_default") or {}
    return {
        "slug": slugify_pack(cat.get("slug") or "unspecified-wardrobe"),
        "name": cat.get("name") or "Unspecified Wardrobe",
        "terms": list(cat.get("terms") or ["wardrobe as seen on the still"]),
    }


def pose_from_role(role: str, explicit: str = "") -> dict:
    cat = load_catalog().get("roles") or {}
    if explicit:
        key = slugify_pack(explicit)
        row = cat.get(explicit) or cat.get(key) or {}
        return {
            "slug": key,
            "name": row.get("pose_name") or key.replace("-", " ").title(),
            "terms": list(row.get("pose_terms") or [key.replace("-", " ")]),
        }
    row = cat.get(role) or {}
    if row:
        return {
            "slug": slugify_pack(row.get("pose") or role),
            "name": row.get("pose_name") or role.replace("_", " ").title(),
            "terms": list(row.get("pose_terms") or [role.replace("_", " ")]),
        }
    return {
        "slug": slugify_pack(role or "unspecified-pose"),
        "name": (role or "unspecified").replace("_", " ").title(),
        "terms": [f"{role.replace('_', ' ')} as seen on the still"],
    }


def _write_pack_file(kind: str, slug: str, name: str, terms: list, instance: dict) -> dict:
    folder = PACKS_ROOT / kind
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{slug}.json"
    pid = f"{kind}.{slug}"
    if path.exists():
        pack = json.loads(path.read_text(encoding="utf-8"))
        inst = list(pack.get("instances") or [])
        src = instance.get("src")
        already = bool(src and any(i.get("src") == src for i in inst))
        created = False
        if not already:
            inst.append(instance)
            ver = str(pack.get("version") or "0.1.0").split(".")
            if len(ver) == 3:
                try:
                    pack["version"] = f"{ver[0]}.{ver[1]}.{int(ver[2]) + 1}"
                except Exception:
                    pack["version"] = "0.1.1"
        pack["instances"] = inst
        pack["n"] = len(inst)
        pack["updated"] = _now()
    else:
        pack = {
            "id": pid,
            "kind": kind,
            "name": name,
            "version": "0.1.0",
            "status": "draft",
            "source": "agentify-scrape",
            "ticket": "IP-WQ-094",
            "tags": [kind, "agentify", slug],
            "prompt_terms": [
                {"term": t, "variance": 0.25 if i == 0 else 0.4, "weight": 1.0 if i == 0 else 0.8}
                for i, t in enumerate(terms[:6])
            ],
            "instances": [instance],
            "n": 1,
            "created": _now(),
            "updated": _now(),
            "content": {"taxonomy": "structural" if kind == "pose" else "wardrobe", "origin": "inbound still scrape"},
        }
        created = True
    path.write_text(json.dumps(pack, indent=2) + "\n", encoding="utf-8")
    _index_pack(pack, f"packs/{kind}/{slug}.json")
    pack["path"] = str(path)
    pack["created_now"] = created
    return pack


def _index_pack(pack: dict, rel: str) -> None:
    idx = {"version": "1.6.1", "updated": _now(), "count": 0, "packs": []}
    if INDEX_PATH.exists():
        try:
            idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    packs = list(idx.get("packs") or [])
    pid = pack.get("id")
    row = {"id": pid, "kind": pack.get("kind"), "name": pack.get("name"), "path": rel, "tags": pack.get("tags") or []}
    packs = [p for p in packs if p.get("id") != pid] + [row]
    idx["packs"] = packs
    idx["count"] = len(packs)
    idx["updated"] = _now()
    INDEX_PATH.write_text(json.dumps(idx, indent=2) + "\n", encoding="utf-8")


def scrape_set(
    frames: list,
    who: str = "",
    slug: str = "",
    wardrobe_hint: str = "",
    dest: Path | None = None,
    tone: str = "",
    culture: str = "",
    feed: str = "",
    locale: str = "",
    family: str = "",
    continent: str = "",
    region: str = "",
) -> dict:
    """Mint or extend pose + wardrobe packs from inbound frames.

    Same pose on two stills → one pose pack with two instances.
    Same wardrobe across the set → one wardrobe pack with N instances.
    """
    default_w = wardrobe_from_hint(wardrobe_hint)
    pose_packs: dict[str, dict] = {}
    wardrobe_packs: dict[str, dict] = {}
    per_frame = []
    for fr in frames:
        role = fr.get("role") or "ref"
        pose = pose_from_role(role, fr.get("pose_slug") or "")
        wslug = fr.get("wardrobe_slug") or ""
        ward = wardrobe_from_hint(wslug) if wslug else default_w
        inst = {
            "who": who,
            "set": slug,
            "role": role,
            "src": fr.get("inbound") or fr.get("path"),
            "at": _now(),
        }
        pp = _write_pack_file("pose", pose["slug"], pose["name"], pose["terms"], inst)
        wp = _write_pack_file("wardrobe", ward["slug"], ward["name"], ward["terms"], inst)
        pose_packs[pp["id"]] = {"id": pp["id"], "n": pp.get("n"), "path": pp.get("path"), "name": pp.get("name")}
        wardrobe_packs[wp["id"]] = {"id": wp["id"], "n": wp.get("n"), "path": wp.get("path"), "name": wp.get("name")}
        row = {
            "role": role,
            "src": inst["src"],
            "pose": pp["id"],
            "wardrobe": wp["id"],
            "skin": {
                "tone": tone or "unspecified",
                "undertone": "unspecified",
                "observed": bool(tone),
                "ipq070": True,
            },
            "culture": {
                "tags": [t.strip() for t in culture.split(",") if t.strip()],
                "influence": ["wardrobe", "persona-style"] if culture else [],
                "notes": "",
            },
            "feed": {
                "platform": feed or "dump",
                "locale": locale,
                "aesthetic_family": family,
            },
            "coverage": {
                "continent": continent,
                "region": region,
                "slot": "unspecified" if not (continent or region) else "observed",
                "observed": bool(continent or region),
            },
        }
        per_frame.append(row)
        fr["pose_pack"] = pp["id"]
        fr["wardrobe_pack"] = wp["id"]
    out = {
        "ok": True,
        "schema": "agentify-scrape/v1.1",
        "pose_packs": list(pose_packs.values()),
        "wardrobe_packs": list(wardrobe_packs.values()),
        "frames": per_frame,
        "rule": "duplicate pose or wardrobe across stills extends instances on one pack",
    }
    if dest:
        p = Path(dest) / "SCRAPE.json"
        p.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        out["path"] = str(p)
    return out


def scrape_from_set_file(
    set_path: str,
    wardrobe_hint: str = "",
    tone: str = "",
    culture: str = "",
    feed: str = "",
    locale: str = "",
    family: str = "",
    continent: str = "",
    region: str = "",
) -> dict:
    data = json.loads(Path(set_path).read_text(encoding="utf-8"))
    dest = Path(data.get("dir") or Path(set_path).parent)
    frames = data.get("frames") or []
    hint = wardrobe_hint or (data.get("card") or {}).get("desc") or ""
    out = scrape_set(
        frames,
        who=data.get("who") or "",
        slug=data.get("slug") or "",
        wardrobe_hint=hint,
        dest=dest,
        tone=tone,
        culture=culture,
        feed=feed,
        locale=locale,
        family=family,
        continent=continent,
        region=region,
    )
    data["scrape"] = out
    Path(set_path).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    out["set"] = set_path
    return out


def build_set(who: str, desc: str, hero: str, frames: list[str], slug: str = "") -> dict:
    v = veto_who(who)
    if not v["ok"]:
        return {"ok": False, "veto": v["veto"]}
    slug = slug or re.sub(r"[^a-z0-9]+", "-", normalize_who(who) or "set").strip("-")
    stamp = datetime.now(ET).strftime("%Y%m%d-%H%M%S")
    dest = SET_DIR / f"{slug}_{stamp}"
    dest.mkdir(parents=True, exist_ok=True)

    parsed = [parse_frame(f) for f in frames]
    hero_p = parse_frame(hero if ":" in hero else f"{hero}:hero")
    if hero_p not in parsed:
        parsed = [hero_p] + [f for f in parsed if f["path"] != hero_p["path"]]

    copied = []
    sys.path.insert(0, str(SCRIPTS))
    import inbound_classify  # may fail if no main API
    import inbound_queue  # type: ignore

    for i, fr in enumerate(parsed):
        src = Path(fr["path"])
        if not src.is_file():
            fr["error"] = "missing"
            continue
        target = dest / f"{i:02d}_{fr['role']}{src.suffix.lower() or '.png'}"
        shutil.copy2(src, target)
        fr["inbound"] = str(target)
        try:
            cls = inbound_classify.classify(target) if hasattr(inbound_classify, "classify") else None
        except Exception:
            cls = None
        if cls is None:
            import subprocess

            p = subprocess.run(
                [sys.executable, str(SCRIPTS / "inbound_classify.py"), "--src", str(target)],
                text=True,
                capture_output=True,
            )
            try:
                cls = json.loads(p.stdout) if p.returncode == 0 else {"error": p.stderr}
            except Exception:
                cls = {"error": "classify-parse"}
        fr["classify"] = cls
        try:
            item = inbound_queue.add(str(target), layout=str((cls or {}).get("layout") or ""), why="agentify-set")
            chosen = inbound_queue.choose(item["id"], "B")
            fr["queue_id"] = chosen.get("id")
            fr["choice"] = chosen.get("choice")
        except (OSError, KeyError) as exc:
            fr["queue_error"] = str(exc)
            fr["choice"] = "B"
        copied.append(fr)

    pose_refs = [f"{f.get('role')}:{Path(f.get('inbound') or f['path']).name}" for f in copied]
    pl = plan(who, desc, hero_p.get("inbound") or hero_p["path"], False, pose_refs)
    cd = card(who, desc, pl.get("src") or "", slug, copied)
    rec = {
        "ok": True,
        "schema": "agentify-set/v1",
        "slug": slug,
        "who": who,
        "kind": pl.get("kind"),
        "hero": hero_p,
        "frames": copied,
        "n_frames": len(copied),
        "plates": 4,
        "rule": "one candidate per set; default emit 0+A+B+C+D; frames are pose refs; 0 is source",
        "plan": pl,
        "card": cd,
        "dir": str(dest),
        "created": _now(),
        "ticket": "IP-WQ-094",
    }
    rec["scrape"] = scrape_set(copied, who=who, slug=slug, wardrobe_hint=desc, dest=dest)
    rec["plan"] = plan(
        who,
        desc,
        hero_p.get("inbound") or hero_p["path"],
        False,
        [f"{x['id']} x{x['n']}" for x in rec["scrape"].get("pose_packs") or []],
    )
    set_path = dest / "SET.json"
    set_path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    rec["path"] = str(set_path)
    return rec


INTENSITY = {
    "c": {
        "key": "c",
        "outfit": "hotter cut, fabric stays fabric",
        "skip_if": "already-max-cling",
    },
    "d": {
        "key": "d",
        "outfit": "same cut, sheer / mesh of that garment",
        "skip_if": None,
    },
    "e": {
        "key": "e",
        "outfit": "hotter cut AND sheer",
        "skip_if": None,
        "hops": ["d", "crop"],
    },
}

LANES = {
    "A": "photoreal cousin / ID",
    "B": "heat photoreal",
    "C": "anime canvas",
    "D": "rig / turnaround",
    "E": "high heat of B. Same woman, same wardrobe lock. Cut and cling follow the pick. No clothes-on ceiling.",
}


def parse_code(code: str) -> dict:
    """Parse I-n-LANE-intensity or messy '1cde' / 'I1Be' / 'sheer on the look-back'."""
    raw = (code or "").strip()
    out = {
        "ok": False,
        "raw": raw,
        "character": "I",
        "pose": None,
        "lane": None,
        "intensity": None,
        "outfit": None,
        "english": False,
    }
    if not raw:
        return out
    low = raw.lower()
    if any(w in low for w in ("sit", "stop", "done")):
        out.update({"ok": True, "command": "sit"})
        return out
    if "sheer" in low and "hotter" in low:
        out.update({"ok": True, "english": True, "intensity": "e", "outfit": INTENSITY["e"]["outfit"]})
        return out
    if "sheer" in low:
        out.update({"ok": True, "english": True, "intensity": "d", "outfit": INTENSITY["d"]["outfit"]})
        return out
    if "hotter" in low or "window" in low or "crop" in low:
        out.update({"ok": True, "english": True, "intensity": "c", "outfit": INTENSITY["c"]["outfit"]})
        return out
    m = re.search(r"\b([IVX]+)\s*[- ]?\s*(\d+)\s*[- ]?\s*([A-Ea-e])\s*[- ]?\s*([cdeCDE])?\b", raw)
    if m:
        lane = m.group(3).upper()
        inten = (m.group(4) or "").lower() or None
        out.update(
            {
                "ok": True,
                "character": m.group(1).upper(),
                "pose": int(m.group(2)),
                "lane": lane if lane in LANES else None,
                "intensity": inten if inten in INTENSITY else None,
            }
        )
        if out["intensity"]:
            out["outfit"] = INTENSITY[out["intensity"]]["outfit"]
        return out
    # compact 1cde / 2c / IE / I1Be — case-sensitive lane vs intensity
    compact = raw.replace(" ", "")
    m2 = re.fullmatch(r"([IVXivx]+)?(\d+)?([A-E])?([cde]+)?", compact)
    if m2 and any(m2.group(i) for i in range(1, 5)):
        letter = m2.group(3) or ""
        tail = m2.group(4) or ""
        out.update(
            {
                "ok": True,
                "character": (m2.group(1) or "I").upper(),
                "pose": int(m2.group(2)) if m2.group(2) else None,
                "lane": letter if letter else "C",
                "intensities": list(tail),
            }
        )
        if tail == "cde":
            out["intensity"] = "cde"
            out["outfit"] = "c then d then e"
        elif tail:
            out["intensity"] = tail[0]
            out["outfit"] = INTENSITY.get(out["intensity"], {}).get("outfit")
        return out
    return out


def hop_plan(intensity: str, lane: str = "C", cling: str = "unknown") -> dict:
    """IP-WQ-116 / 117. Print before pixels."""
    inten = (intensity or "").lower()
    lane = (lane or "C").upper()
    plan = {
        "lane": lane,
        "intensity": inten,
        "hops": [],
        "skip": False,
        "reason": None,
        "refuse_policy": "card, not shrug",
    }
    if inten in ("c", "cde") and cling in ("max", "already-max-cling", "painted-on", "unitard-tight"):
        if inten == "c":
            plan.update({"skip": True, "reason": "c skipped, already tight"})
            return plan
        plan["hops"] = [
            {"from": "C-clean", "do": "SKIP c — already tight"},
            {"from": "C-clean", "do": "d — same cut sheer"},
            {"from": "C-d", "do": "e — crop, keep sheer"},
        ]
        plan["reason"] = "c no-op; still run d then e"
        return plan
    if inten == "cde":
        plan["hops"] = [
            {"from": "C-clean", "do": "c — hotter cut, cloth stays cloth"},
            {"from": "C-c", "do": "d — same original cut, sheer"},
            {"from": "C-d", "do": "e — crop, keep sheer"},
        ]
        plan["reason"] = "three printers; e is two hops after d"
        return plan
    if inten == "c":
        plan["hops"] = [{"from": "C-clean", "do": "hotter cut, cloth stays cloth"}]
    elif inten == "d":
        plan["hops"] = [{"from": "C-clean", "do": "same cut, sheer garment"}]
    elif inten == "e":
        plan["hops"] = [
            {"from": "C-clean", "do": "d — same cut sheer"},
            {"from": "C-d", "do": "crop / hotter cut, keep sheer"},
        ]
        plan["reason"] = "never single-hop photoreal+e"
    elif lane == "E":
        plan["hops"] = [{"from": "B", "do": "hot photoreal of the same woman; cut/cling follow the pick"}]
        plan["reason"] = "E is B turned up. Implication pack on moderate. Not a clothes-on retreat."
    else:
        plan["reason"] = "unknown intensity"
    return plan


def picker_card(
    candidate: str = "CANDIDATE",
    outfit: str = "outfit",
    pose1: str = "pose 1",
    pose2: str = "pose 2",
    others: str = "",
) -> str:
    """IP-WQ-118. Eight lines. English and codes both parse."""
    extra = f"\nII/III {others}" if others else ""
    return (
        f"{candidate} live. {outfit}.\n"
        f"1 {pose1}   2 {pose2}\n"
        "c hotter cloth   d same-cut sheer   e both\n"
        "E photoreal hot"
        f"{extra}\n"
        "\n"
        "reply: 1cde 2cde E\n"
        "   or: sheer on the look-back\n"
        "   or: sit\n"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("route")
    r.add_argument("text")
    r.add_argument("--media", action="store_true", help="inbound still/short attached (IP-WQ-168)")

    v = sub.add_parser("veto")
    v.add_argument("--who", required=True)

    pl = sub.add_parser("plan")
    pl.add_argument("--who", required=True)
    pl.add_argument("--desc", required=True)
    pl.add_argument("--src", default="")
    pl.add_argument("--merge", action="store_true")

    c = sub.add_parser("card")
    c.add_argument("--who", required=True)
    c.add_argument("--desc", required=True)
    c.add_argument("--src", default="")
    c.add_argument("--slug", default="")

    s = sub.add_parser("set")
    s.add_argument("--who", required=True)
    s.add_argument("--desc", required=True)
    s.add_argument("--hero", required=True)
    s.add_argument("--frame", action="append", default=[])
    s.add_argument("--slug", default="")

    sc = sub.add_parser("scrape")
    sc.add_argument("--from-set", required=True)
    sc.add_argument("--wardrobe", default="")
    sc.add_argument("--tone", default="")
    sc.add_argument("--culture", default="")
    sc.add_argument("--feed", default="")
    sc.add_argument("--locale", default="")
    sc.add_argument("--family", default="")
    sc.add_argument("--continent", default="")
    sc.add_argument("--region", default="")

    ra = sub.add_parser("reel-analyze")
    ra.add_argument("--inbound", required=True)
    ra.add_argument("--n-characters", type=int, default=1)
    ra.add_argument("--slug", default="cand-reel")

    mn = sub.add_parser("menu")
    mn.add_argument("--inbound", required=True)
    pk = sub.add_parser("pick")
    pk.add_argument("--inbound", required=True)
    pk.add_argument("--who", default="")
    pk.add_argument("--pose", default="")
    pk.add_argument("--wardrobe", default="")
    pk.add_argument("--code", default="")

    sz = sub.add_parser("serialize")
    sz.add_argument("--src", required=True)
    sz.add_argument("--slug", required=True)
    sz.add_argument("--prompt", default="")
    sz.add_argument("--tag", default="", help="a-id|b-heat|c-anime|d-rig only")
    sz.add_argument("--extra", default="", help="pose|wardrobe|face|hip — not a lane")

    ht = sub.add_parser("heat")
    ht.add_argument("--code", required=True)
    ht.add_argument("--cling", default="unknown")
    ht.add_argument("--lane", default="")

    pkc = sub.add_parser("picker")
    pkc.add_argument("--candidate", default="CANDIDATE")
    pkc.add_argument("--outfit", default="outfit")
    pkc.add_argument("--pose1", default="pose 1")
    pkc.add_argument("--pose2", default="pose 2")
    pkc.add_argument("--others", default="")

    args = p.parse_args()
    if args.cmd == "route":
        out = route(args.text, has_media=bool(getattr(args, "media", False)))
        print(json.dumps(out, indent=2))
        return 0
    if args.cmd == "veto":
        out = veto_who(args.who)
        print(json.dumps(out, indent=2))
        return 0 if out["ok"] else 2
    if args.cmd == "plan":
        out = plan(args.who, args.desc, args.src, args.merge)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 2
    if args.cmd == "card":
        out = card(args.who, args.desc, args.src, args.slug)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 2
    if args.cmd == "set":
        frames = list(args.frame or [])
        if args.hero not in frames and not any(f.startswith(args.hero) for f in frames):
            frames = [args.hero + ":hero"] + frames
        out = build_set(args.who, args.desc, args.hero, frames, args.slug)
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 2
    if args.cmd == "scrape":
        out = scrape_from_set_file(
            args.from_set,
            args.wardrobe,
            getattr(args, "tone", ""),
            getattr(args, "culture", ""),
            getattr(args, "feed", ""),
            getattr(args, "locale", ""),
            getattr(args, "family", ""),
            getattr(args, "continent", ""),
            getattr(args, "region", ""),
        )
        print(json.dumps(out, indent=2))
        return 0 if out.get("ok") else 2
    if args.cmd == "reel-analyze":
        cmd = [
            sys.executable,
            str(SCRIPTS / "reel_analyze.py"),
            "--inbound",
            args.inbound,
            "--n-characters",
            str(args.n_characters),
            "--slug",
            args.slug,
        ]
        proc = subprocess.run(cmd)
        return proc.returncode
    if args.cmd == "menu":
        proc = subprocess.run([
            sys.executable, str(SCRIPTS / "reel_menu.py"), "menu",
            "--inbound", args.inbound,
        ])
        return proc.returncode
    if args.cmd == "pick":
        cmd = [
            sys.executable, str(SCRIPTS / "reel_menu.py"), "pick",
            "--inbound", args.inbound,
            "--who", args.who or "",
            "--pose", args.pose or "",
            "--wardrobe", args.wardrobe or "",
        ]
        if args.code:
            cmd.extend(["--code", args.code])
        proc = subprocess.run(cmd)
        return proc.returncode
    if args.cmd == "heat":
        parsed = parse_code(args.code)
        lane = args.lane or parsed.get("lane") or "C"
        inten = parsed.get("intensity") or (parsed.get("intensities") or [None])[0]
        hops = hop_plan(inten or "", lane, args.cling)
        print(json.dumps({"parsed": parsed, "hop": hops}, indent=2))
        return 0 if parsed.get("ok") or hops.get("hops") or hops.get("skip") else 2
    if args.cmd == "picker":
        print(
            picker_card(
                args.candidate,
                args.outfit,
                args.pose1,
                args.pose2,
                args.others,
            )
        )
        return 0
    if args.cmd == "serialize":
        tag = (args.tag or "").strip().lower()
        extra = (getattr(args, "extra", "") or "").strip().lower()
        if tag and tag not in LEGAL_TAGS:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "illegal serialize tag",
                        "tag": tag,
                        "legal": list(LEGAL_TAGS),
                        "note": "E is heat-of-B, not a tag. pose/wardrobe/face/hip use --extra.",
                    }
                )
            )
            return 2
        if extra and extra not in LEGAL_EXTRAS:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "error": "illegal serialize extra",
                        "extra": extra,
                        "legal": list(LEGAL_EXTRAS),
                    }
                )
            )
            return 2
        keep_tag = tag
        if extra:
            keep_tag = f"extra-{extra}-not-lane" if not tag else f"{tag}-extra-{extra}"
        cmd = [
            sys.executable,
            str(SCRIPTS / "keep_path.py"),
            "--src",
            args.src,
            "--slug",
            args.slug,
            "--prompt",
            args.prompt or f"agentify plate {args.slug}",
            "--agent",
            "agentify",
        ]
        if keep_tag:
            cmd.extend(["--tag", keep_tag])
        proc = subprocess.run(cmd, text=True)
        return proc.returncode
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
