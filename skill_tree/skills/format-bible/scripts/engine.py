#!/usr/bin/env python3
"""
format-bible scripts/engine.py — live envelope metrics + hygiene_check

SKILL.md requires every boot / skill-driven turn to pull live values from here.
Thin wake 2026-09-10 (SR-WQ-069 / FBQ-012):
  live: heat, filth, gear, profile, lane, safety, wall clock, hygiene
  dormant (kept in state, off thin chrome): ache, rg, push, gem, agents, kink, Day X/60

Usage:
  python3 scripts/engine.py
  python3 scripts/engine.py --thin
  python3 scripts/engine.py --set heat=6 filth=2 gear=2
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parent.parent
OVERRIDE = ROOT / "references" / "engine_state.json"

_DEFAULTS: Dict[str, Any] = {
    "heat": 0,
    "filth": 0,
    "gear": 2,
    "profile": 0,
    "lane": None,
    "kink": "Claim+Exhib",
    "safety": "RACK",
    "gem": "Steady",
    "mode": "Normal",
    "agents": "LivHUB+Crystal+Echo+Mira",
    "clock_mode": "wall",
    "clock_day": None,
    "clock_total": 60,
    "ache": 0,
    "rg": 0,
    "push": 0,
    "hygiene": "OK",
    "show_dormant": False,
}


def _load_override() -> Dict[str, Any]:
    if not OVERRIDE.exists():
        return {}
    try:
        return json.loads(OVERRIDE.read_text())
    except Exception:
        return {}


def get_metrics(**overrides: Any) -> Dict[str, Any]:
    """Return live metrics dict (defaults ← engine_state.json ← kwargs)."""
    m = dict(_DEFAULTS)
    raw = _load_override()
    raw.pop("schema", None)
    raw.pop("note", None)
    m.update(raw)
    m.update({k: v for k, v in overrides.items() if v is not None})
    m["updated_at"] = datetime.now(timezone.utc).isoformat()
    return m


def set_metrics(**fields: Any) -> Dict[str, Any]:
    """Merge fields into engine_state.json. Does not invent Ache/RG/Push."""
    current = {}
    if OVERRIDE.exists():
        try:
            current = json.loads(OVERRIDE.read_text())
        except Exception:
            current = {}
    allowed = set(_DEFAULTS) | {"schema", "note", "updated_at"}
    for k, v in fields.items():
        if k in allowed:
            current[k] = v
    current.setdefault("schema", "format-bible.engine_state.v0.2")
    current["updated_at"] = datetime.now(timezone.utc).isoformat()
    OVERRIDE.parent.mkdir(parents=True, exist_ok=True)
    OVERRIDE.write_text(json.dumps(current, indent=2) + "\n")
    return get_metrics()


def hygiene_check(metrics: Dict[str, Any] | None = None) -> Tuple[bool, str]:
    m = metrics or get_metrics()
    issues = []
    schema = ROOT / "references" / "ENVELOPE_SCHEMA.md"
    if not schema.exists():
        issues.append("ENVELOPE_SCHEMA missing")
    if OVERRIDE.exists():
        try:
            json.loads(OVERRIDE.read_text())
        except Exception:
            issues.append("engine_state.json invalid")
    if issues:
        return False, "FAIL:" + ",".join(issues)
    return True, str(m.get("hygiene") or "OK")


def format_dashboard_tail(metrics: Dict[str, Any] | None = None) -> str:
    """Legacy fat line. Prefer format_dashboard_thin."""
    m = metrics or get_metrics()
    ok, hyg = hygiene_check(m)
    if not ok:
        m = dict(m)
        m["hygiene"] = hyg
    clock = _clock_token(m)
    return (
        f"🌡️Heat:H{m.get('heat', 0)} |💦Filth:{m.get('filth', 0)} |🔗Kink:{m.get('kink', 'Claim+Exhib')} | "
        f"🚨Safety:{m.get('safety', 'RACK')} |✨Gem: {m.get('gem', 'Steady')} | "
        f"⚙️Mode:{m.get('mode', 'Normal')} |Gear:{m.get('gear', 2)} | 🤖Agents:{m.get('agents', 'LivHUB')} | "
        f"⏱️Clock: {clock} | "
        f"🧠Ache:{m.get('ache', 0)} | 👧RG:{m.get('rg', 0)} | 🎯Push:{m.get('push', 0)} | "
        f"🧼Hygiene:{m.get('hygiene', hyg)}"
    )


def format_dashboard_thin(metrics: Dict[str, Any] | None = None) -> str:
    """Live chrome. One owner per number. Dormant metrics omitted."""
    m = metrics or get_metrics()
    ok, hyg = hygiene_check(m)
    parts = [
        f"🌡️Heat:H{m.get('heat', 0)}",
        f"💦Filth:{m.get('filth', 0)}",
        f"⚙️Gear:{m.get('gear', 2)}",
        f"🚨Safety:{m.get('safety', 'RACK')}",
        f"⏱️{_clock_token(m)}",
        f"🧼Hygiene:{hyg if not ok else m.get('hygiene', hyg)}",
    ]
    profile = m.get("profile")
    if profile not in (None, 0, "0"):
        parts.insert(3, f"Profile:{profile}")
    lane = m.get("lane")
    if lane:
        parts.insert(3, f"Lane:{lane}")
    if m.get("show_dormant"):
        parts.extend(
            [
                f"🧠Ache:{m.get('ache', 0)}",
                f"👧RG:{m.get('rg', 0)}",
                f"🎯Push:{m.get('push', 0)}",
            ]
        )
    return " | ".join(parts)


def _clock_token(m: Dict[str, Any]) -> str:
    mode = str(m.get("clock_mode") or "wall").lower()
    if mode == "cycle" and m.get("clock_day") not in (None, "", 0):
        return f"Day {m.get('clock_day')}/{m.get('clock_total', 60)}"
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M %Z")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    thin = "--thin" in argv
    sets = [a for a in argv if a.startswith("--set") or "=" in a and not a.startswith("--")]
    fields: Dict[str, Any] = {}
    rest = [a for a in argv if a not in ("--thin", "--legacy") and not a.startswith("--set")]
    if "--set" in argv:
        idx = argv.index("--set")
        rest = argv[idx + 1 :]
    for token in rest:
        if "=" not in token:
            continue
        k, v = token.split("=", 1)
        if v.isdigit():
            fields[k] = int(v)
        elif v.lower() in ("true", "false"):
            fields[k] = v.lower() == "true"
        elif v.lower() in ("null", "none"):
            fields[k] = None
        else:
            fields[k] = v
    if fields:
        metrics = set_metrics(**fields)
    else:
        metrics = get_metrics()
    ok, status = hygiene_check(metrics)
    print(json.dumps({"ok": ok, "hygiene": status, "metrics": metrics}, indent=2, default=str))
    print("---")
    if "--legacy" in argv:
        print(format_dashboard_tail(metrics))
    else:
        print(format_dashboard_thin(metrics))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
