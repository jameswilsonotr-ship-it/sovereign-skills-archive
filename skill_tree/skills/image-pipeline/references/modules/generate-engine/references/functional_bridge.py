#!/usr/bin/env python3
"""
functional_bridge.py — style_chain → plan application → healing/event logs.

Phase-1 surface for grok-imagine-generate-engine. Does not call the image API directly;
returns structured plans the agent/runtime can execute with generate_image / overlay.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "references" / "dual-engine" / "artifacts" / "bridge_events.jsonl"


def _log(event: Dict[str, Any]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event["ts"] = datetime.now(timezone.utc).isoformat()
    with LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")


def handle_style_chain_generation(
    style_chain: List[str],
    base_prompt: str = "",
    heat: int = 5,
    presentable_reframe: bool = True,
) -> Dict[str, Any]:
    """
    Build an ordered generation plan from a style_chain.
    Each step is a prompt fragment the runtime can feed to generate_image.
    """
    heat = max(0, min(10, int(heat)))
    steps = []
    for i, style in enumerate(style_chain):
        steps.append({
            "index": i,
            "style": style,
            "prompt": f"{base_prompt} | style:{style} | heat:H{heat} | "
                      f"presentable_reframe={'on' if presentable_reframe else 'off'} | "
                      f"DNA: see references/liv-bunny-dna-lock.md",
        })
    plan = {
        "ok": True,
        "heat": heat,
        "presentable_reframe": presentable_reframe,
        "steps": steps,
        "dna_lock_path": "references/liv-bunny-dna-lock.md",
    }
    _log({"event": "style_chain_plan", "n_steps": len(steps), "heat": heat})
    return plan


def bridge(mode: str = "generate", payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = payload or {}
    if "style_chain" in payload:
        return handle_style_chain_generation(
            list(payload["style_chain"]),
            base_prompt=str(payload.get("base_prompt", "")),
            heat=int(payload.get("heat", 5)),
            presentable_reframe=bool(payload.get("presentable_reframe", True)),
        )
    out = {"ok": True, "mode": mode, "payload": payload}
    _log({"event": "bridge_passthrough", "mode": mode})
    return out


def health() -> Dict[str, Any]:
    dna = ROOT / "references" / "liv-bunny-dna-lock.md"
    return {
        "functional_bridge": "ok",
        "dna_lock_present": dna.exists(),
        "log_path": str(LOG),
    }


def self_test() -> None:
    h = health()
    assert h["functional_bridge"] == "ok"
    plan = handle_style_chain_generation(["clean", "heat_gradient"], base_prompt="test bunny", heat=6)
    assert plan["ok"] and len(plan["steps"]) == 2
    print("SELF_TEST_PASS")
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    if "--test" in sys.argv or len(sys.argv) == 1:
        self_test()
    else:
        print(json.dumps(health(), indent=2))
