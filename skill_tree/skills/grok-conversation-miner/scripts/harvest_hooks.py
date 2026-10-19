#!/usr/bin/env python3
"""Wire every sunset/harvest lane into EXPORT_LOG.jsonl (GCM-WQ-020)."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from export_log import DEFAULT, append_row, cite, log_lanes as _log_lanes_core, write_mirror

LANES = ("L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8")


def run_id(prefix: str = "HOOK") -> str:
    from gcm_lib import stamps
    return f"{prefix}-{stamps()['date_ny'].replace('-','')}"


def log_lanes(run_id: str, verb: str, slug: str, lanes: list[dict], log_path: Path | None = None) -> dict:
    path = Path(log_path or DEFAULT)
    _log_lanes_core(path, run_id=run_id, verb=verb, conversation_key=slug, lanes=lanes, dry_run=True)
    write_mirror(path)
    c = cite(path)
    c["row_count"] = c.get("count", 0)
    return c
