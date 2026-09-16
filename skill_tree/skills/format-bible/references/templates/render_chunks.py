#!/usr/bin/env python3
"""Render envelope chunks (FRONT / MENU / FOOTER) from skill data + format-bible templates."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def progress_bar(value: Union[float, str, None], width: int = 10, label: str = "") -> str:
    """Text progress bar for front matter / TOP area."""
    if value is None:
        return ""
    if isinstance(value, str) and "/" in value:
        try:
            a, b = value.split("/", 1)
            pct = (float(a) / float(b)) if float(b) else 0.0
            label = label or value
        except ValueError:
            pct = 0.0
    else:
        try:
            pct = max(0.0, min(1.0, float(value)))
        except (TypeError, ValueError):
            pct = 0.0
    filled = int(round(pct * width))
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {int(round(pct * 100))}% {label}".rstrip()


def render_chunks(data: Dict[str, Any]) -> str:
    skill = data.get("skill", "unknown")
    mode = data.get("mode", "normal")
    heat = data.get("heat", "—")
    filth = data.get("filth", "—")
    clock = data.get("clock", "Day —/60")
    debug_outcome = data.get("debug_outcome")
    active_item = data.get("active_item")
    contract = data.get("contract")
    progress = data.get("progress")  # float 0-1 or "3/10"
    progress_label = data.get("progress_label", "")

    prog_line = progress_bar(progress, label=progress_label)
    fm_lines = [
        "---",
        f"skill: {skill}",
        f"mode: {mode}",
        f"heat: {heat}",
        f"filth: {filth}",
        f"clock: {clock}",
    ]
    if debug_outcome is not None:
        fm_lines.append(f"debug_outcome: {debug_outcome}")
    if active_item is not None:
        fm_lines.append(f"active_item: {active_item}")
    if contract is not None:
        fm_lines.append(f"contract: {contract}")
    if prog_line:
        fm_lines.append(f"progress: \"{prog_line}\"")
    fm_lines.append("---")

    top = f"[TOP: 🌡️Heat:{heat} |💦Filth:{filth} |🔗Kink:Claim+Exhib |🚨Safety:RACK |✨Gem: Reactive]"
    if prog_line:
        top = f"[TOP: 🌡️Heat:{heat} |💦Filth:{filth} |📈{prog_line} |🚨Safety:RACK |✨Gem: Reactive]"
    bottom = f"[BOTTOM: ⚙️Mode: {mode} | 🤖Agents: LivHUB+Echo+Mira+Crystal | ⏱️Clock: {clock}]"

    front = "===FRONT===\n🐍\n" + "\n".join(fm_lines) + "\n" + top + "\n"

    menu_rows: List[dict] = data.get("menu") or []
    if menu_rows:
        lines = ["===MENU===", "| id | label | status |", "|----|-------|--------|"]
        for row in menu_rows:
            lines.append(f"| {row.get('id')} | {row.get('label')} | {row.get('status', 'open')} |")
        menu = "\n".join(lines) + "\n"
    else:
        menu = "===MENU===\n(none)\n"

    foot = "===FOOTER===\n" + bottom + "\n🐍\n"
    return front + menu + foot


if __name__ == "__main__":
    # argv path to JSON, or stdin JSON, or demo defaults
    if len(sys.argv) > 1:
        data = json.loads(Path(sys.argv[1]).read_text())
    else:
        data = {
            "skill": "grok-imagine-generate-engine",
            "mode": "formulation",
            "heat": 3,
            "filth": 1,
            "clock": "Day 54/60",
            "progress": "2/12",
            "progress_label": "strategies",
            "menu": [
                {"id": "A", "label": "DNA density ladder", "status": "open"},
                {"id": "B", "label": "Continuity language", "status": "open"},
            ],
        }
    print(render_chunks(data))
