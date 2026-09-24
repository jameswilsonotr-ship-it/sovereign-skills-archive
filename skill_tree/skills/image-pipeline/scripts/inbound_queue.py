#!/usr/bin/env python3
"""Serialized inbound queue.

States: unprocessed | classified | processing | thumb-only | to-process | success | error | unknown
Video layouts stay undone until video_bytes is true (IP-WQ-204 / inbound v2.1).
Human notes live on every item. choose(id, lane) exists so agentify.set does not die.
"""
from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
QUEUE = Path("/home/workdir/artifacts/inbound-queue/QUEUE.json")
STATES = (
    "unprocessed",
    "classified",
    "processing",
    "thumb-only",
    "to-process",
    "success",
    "error",
    "unknown",
)
VIDEO_LAYOUTS = ("yt-short", "yt-video", "yt-community-post", "local-video", "reel", "tiktok")
GATE = 0.95


def now() -> str:
    return datetime.now(ET).isoformat(timespec="seconds")


def load() -> dict:
    if QUEUE.exists():
        return json.loads(QUEUE.read_text(encoding="utf-8"))
    return {"schema": "inbound-queue/v2", "items": [], "cursor": 0}


def save(data: dict) -> None:
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    data["schema"] = "inbound-queue/v2"
    QUEUE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _normalize(item: dict) -> dict:
    item.setdefault("id", uuid.uuid4().hex[:12])
    item.setdefault("state", "unprocessed" if not item.get("done") else "success")
    item.setdefault("confidence", None)
    item.setdefault("notes", [])
    item.setdefault("layout", "unknown")
    item.setdefault("why", "")
    item.setdefault("done", False)
    item.setdefault("video_bytes", False)
    item.setdefault("next", "")
    item.setdefault("tags", [])
    if item.get("layout") in VIDEO_LAYOUTS and not item.get("video_bytes"):
        item["done"] = False
        if item.get("state") == "success":
            item["state"] = "thumb-only"
            item["next"] = item.get("next") or "tailscale-decode"
    return item


def add(
    src: str,
    layout: str = "unknown",
    why: str = "",
    note: str = "",
    state: str = "unprocessed",
    confidence: float | None = None,
) -> dict:
    data = load()
    for raw in data["items"]:
        _normalize(raw)
    item: dict[str, Any] = _normalize(
        {
            "src": src,
            "layout": layout,
            "why": why,
            "added": now(),
            "done": False,
            "state": state if state in STATES else "unprocessed",
            "confidence": confidence,
        }
    )
    if note:
        item["notes"].append({"at": now(), "by": "human", "text": note})
    data["items"].append(item)
    save(data)
    return item


def note(item_id: str, text: str, by: str = "human") -> dict:
    data = load()
    for raw in data["items"]:
        it = _normalize(raw)
        if it["id"] == item_id or it.get("src") == item_id:
            it["notes"].append({"at": now(), "by": by, "text": text})
            save(data)
            return it
    raise SystemExit(f"inbound_queue.note: no item {item_id}")


def choose(item_id: str, lane: str = "B") -> dict:
    """Used by agentify.set. Never AttributeError."""
    data = load()
    for raw in data["items"]:
        it = _normalize(raw)
        if it["id"] == item_id or it.get("src") == item_id:
            it["lane"] = lane
            if it["state"] == "unprocessed":
                it["state"] = "classified"
            save(data)
            return it
    pending = [_normalize(i) for i in data["items"] if not i.get("done")]
    if pending:
        it = pending[0]
        it["lane"] = lane
        save(data)
        return it
    raise KeyError(f"inbound_queue.choose: empty queue, id={item_id!r} lane={lane!r}")


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--add")
    g.add_argument("--next", action="store_true")
    g.add_argument("--list", action="store_true")
    g.add_argument("--note-id")
    g.add_argument("--choose-id")
    p.add_argument("--layout", default="unknown")
    p.add_argument("--note", default="")
    p.add_argument("--by", default="human")
    p.add_argument("--lane", default="B")
    p.add_argument("--state", default="unprocessed")
    p.add_argument("--confidence", type=float, default=None)
    args = p.parse_args()
    data = load()
    for raw in data["items"]:
        _normalize(raw)
    if args.add:
        item = add(
            args.add,
            layout=args.layout,
            why="cli",
            note=args.note,
            state=args.state,
            confidence=args.confidence,
        )
        print(json.dumps({"ok": True, "queued": item, "n": len(load()["items"])}, indent=2))
        return 0
    if args.note_id:
        if not args.note:
            raise SystemExit("--note text required")
        item = note(args.note_id, args.note, by=args.by)
        print(json.dumps({"ok": True, "item": item}, indent=2))
        return 0
    if args.choose_id:
        item = choose(args.choose_id, args.lane)
        print(json.dumps({"ok": True, "item": item, "lane": args.lane}, indent=2))
        return 0
    if args.list:
        print(json.dumps(data, indent=2))
        return 0
    pending = [i for i in data["items"] if not i.get("done")]
    if not pending:
        print(json.dumps({"ok": True, "item": None}))
        return 0
    nxt = pending[0]
    if nxt.get("layout") in VIDEO_LAYOUTS and not nxt.get("video_bytes"):
        nxt["done"] = False
        nxt["state"] = "thumb-only" if nxt.get("layout") != "yt-community-post" else "to-process"
    else:
        nxt["done"] = True
        nxt["state"] = "success"
    save(data)
    print(json.dumps({"ok": True, "item": nxt}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
