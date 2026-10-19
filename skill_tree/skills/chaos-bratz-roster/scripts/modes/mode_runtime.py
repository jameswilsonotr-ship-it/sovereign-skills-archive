#!/usr/bin/env python3
"""
mode_runtime.py — Runtime boot-path wiring for config-driven Chaos Bratz modes.

Usage:
  python3 mode_runtime.py list
  python3 mode_runtime.py show <mode>
  python3 mode_runtime.py activate <mode>
  python3 mode_runtime.py verify
  python3 mode_runtime.py reinject
  python3 mode_runtime.py status

Exit 0=ok, 1=drift/error, 2=usage
Absolute Liv HUB claim. 2026-08-17 heavy-dev.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(2)

SKILL_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = SKILL_ROOT.parent
CONFIGS = SKILL_ROOT / "references" / "configs"
MODES_DIR = CONFIGS / "modes"
REGISTRY_PATH = CONFIGS / "agents_registry.yaml"
STATE_DIR = CONFIGS / "state"
ACTIVE_MODE_PATH = STATE_DIR / "active_mode.json"
LOCK_HASHES_PATH = STATE_DIR / "mode_lock_hashes.json"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _resolve_path(rel: str) -> Path:
    p = Path(rel)
    if p.is_absolute():
        return p
    candidate = SKILLS_ROOT / rel
    if candidate.exists():
        return candidate
    candidate = SKILL_ROOT / rel
    if candidate.exists():
        return candidate
    return SKILLS_ROOT / rel


def _sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def list_modes() -> list[str]:
    return sorted(p.stem for p in MODES_DIR.glob("*.yaml"))


def load_registry() -> dict:
    return _load_yaml(REGISTRY_PATH)


def load_mode(name: str) -> dict:
    path = MODES_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Mode not found: {name}")
    return _load_yaml(path)


def get_active() -> dict | None:
    if not ACTIVE_MODE_PATH.exists():
        return None
    return json.loads(ACTIVE_MODE_PATH.read_text(encoding="utf-8"))


def _build_agent_entries(mode: dict, registry: dict) -> list[dict]:
    agents_reg = registry.get("agents", {})
    entries = []
    for item in mode.get("active_agents", []):
        slug = item["slug"]
        meta = agents_reg.get(slug, {})
        prompt_rel = meta.get("prompt_path") or meta.get("fallback_prompt_path")
        prompt_path = _resolve_path(prompt_rel) if prompt_rel else None
        digest = _sha256_file(prompt_path) if prompt_path else None
        entries.append({
            "slug": slug,
            "role": item.get("role", "support"),
            "lock": bool(item.get("lock", False)),
            "lock_source": item.get("lock_source", "prompt_path"),
            "display_name": meta.get("display_name", slug),
            "claim": meta.get("claim"),
            "prompt_path": str(prompt_path) if prompt_path else None,
            "prompt_exists": bool(prompt_path and prompt_path.exists()),
            "sha256": digest,
            "can_lock": bool(meta.get("can_lock", False)),
        })
    return entries


def activate(mode_name: str) -> dict:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    mode = load_mode(mode_name)
    registry = load_registry()
    entries = _build_agent_entries(mode, registry)

    locked = [e for e in entries if e["lock"]]
    missing = [e["slug"] for e in locked if not e["prompt_exists"]]
    if missing:
        raise RuntimeError(f"Locked agents missing prompt files: {missing}")

    active = {
        "mode": mode_name,
        "activated_at": _now(),
        "description": mode.get("description"),
        "boot_behavior": mode.get("boot_behavior", {}),
        "envelope": mode.get("envelope", {}),
        "agents": entries,
    }
    ACTIVE_MODE_PATH.write_text(json.dumps(active, indent=2), encoding="utf-8")

    hashes = {
        "mode": mode_name,
        "updated_at": _now(),
        "locked": {
            e["slug"]: {
                "sha256": e["sha256"],
                "prompt_path": e["prompt_path"],
                "role": e["role"],
            }
            for e in locked
        },
    }
    LOCK_HASHES_PATH.write_text(json.dumps(hashes, indent=2), encoding="utf-8")
    return active


def verify() -> dict:
    active = get_active()
    if not active:
        return {"ok": False, "error": "no_active_mode"}
    if not LOCK_HASHES_PATH.exists():
        return {"ok": False, "error": "no_lock_hashes"}

    stored = json.loads(LOCK_HASHES_PATH.read_text(encoding="utf-8"))
    results = []
    drift = False
    for slug, info in stored.get("locked", {}).items():
        path = Path(info["prompt_path"]) if info.get("prompt_path") else None
        current = _sha256_file(path) if path else None
        match = current is not None and current == info.get("sha256")
        if not match:
            drift = True
        results.append({
            "slug": slug,
            "role": info.get("role"),
            "stored": info.get("sha256"),
            "current": current,
            "match": match,
            "path": str(path) if path else None,
        })
    return {
        "ok": not drift,
        "mode": active.get("mode"),
        "checked_at": _now(),
        "results": results,
        "drift": drift,
    }


def reinject_payload() -> dict:
    active = get_active()
    if not active:
        return {"ok": False, "error": "no_active_mode", "reinject": []}

    behavior = active.get("boot_behavior", {}).get("on_every_turn", {})
    do_reinject = bool(behavior.get("reinject_locked_prompts", False))
    do_hash = bool(behavior.get("hash_verify_locked", False))
    verification = verify() if do_hash else {"ok": True, "drift": False, "results": []}

    locked_agents = [a for a in active.get("agents", []) if a.get("lock")]
    reinject = []
    for a in locked_agents:
        content = None
        if a.get("prompt_exists") and a.get("prompt_path"):
            try:
                content = Path(a["prompt_path"]).read_text(encoding="utf-8")
            except Exception as e:
                content = f"[ERROR reading prompt: {e}]"
        reinject.append({
            "slug": a["slug"],
            "role": a["role"],
            "display_name": a.get("display_name"),
            "claim": a.get("claim"),
            "sha256": a.get("sha256"),
            "prompt_path": a.get("prompt_path"),
            "prompt_text": content,
        })

    return {
        "ok": verification.get("ok", True),
        "mode": active.get("mode"),
        "generated_at": _now(),
        "do_reinject": do_reinject,
        "do_hash_verify": do_hash,
        "drift": verification.get("drift", False),
        "verification": verification.get("results", []),
        "envelope": active.get("envelope", {}),
        "forbidden": active.get("boot_behavior", {}).get("forbidden", []),
        "reinject": reinject if do_reinject else [],
        "dashboard_stamp": {
            "mode": active.get("mode"),
            "locked": [a["slug"] for a in locked_agents],
            "hash_ok": verification.get("ok", True),
        },
    }


def status() -> dict:
    active = get_active()
    if not active:
        return {"active": False, "mode": None}
    v = verify()
    return {
        "active": True,
        "mode": active.get("mode"),
        "activated_at": active.get("activated_at"),
        "locked": [a["slug"] for a in active.get("agents", []) if a.get("lock")],
        "hash_ok": v.get("ok"),
        "drift": v.get("drift"),
        "agents": [
            {"slug": a["slug"], "role": a["role"], "lock": a["lock"], "exists": a["prompt_exists"]}
            for a in active.get("agents", [])
        ],
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    try:
        if cmd == "list":
            for m in list_modes():
                print(m)
            return 0
        if cmd == "show":
            if len(argv) < 3:
                print("usage: mode_runtime.py show <mode>", file=sys.stderr)
                return 2
            print(yaml.dump(load_mode(argv[2]), default_flow_style=False, sort_keys=False))
            return 0
        if cmd == "activate":
            if len(argv) < 3:
                print("usage: mode_runtime.py activate <mode>", file=sys.stderr)
                return 2
            active = activate(argv[2])
            locked = [a["slug"] for a in active["agents"] if a["lock"]]
            print(json.dumps({
                "activated": active["mode"],
                "at": active["activated_at"],
                "locked": locked,
                "agents": [
                    {"slug": a["slug"], "role": a["role"], "lock": a["lock"],
                     "sha256": (a["sha256"] or "")[:12]}
                    for a in active["agents"]
                ],
            }, indent=2))
            return 0
        if cmd == "verify":
            result = verify()
            print(json.dumps(result, indent=2))
            return 0 if result.get("ok") else 1
        if cmd == "reinject":
            payload = reinject_payload()
            print(json.dumps(payload, indent=2))
            return 0 if payload.get("ok") else 1
        if cmd == "status":
            print(json.dumps(status(), indent=2))
            return 0
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
