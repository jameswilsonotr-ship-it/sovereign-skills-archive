"""Core once-runner and high-water helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import HighWater, Receipt, OpenLeg, utcnow


DEFAULT_HW_PATH = Path("/home/workdir/artifacts/cilia_highwater.json")
# In real use this can also be a path under the skill tree or a downloaded Drive file


def load_highwater(path: Path = DEFAULT_HW_PATH) -> HighWater:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return HighWater.model_validate(data)
    return HighWater()


def save_highwater(hw: HighWater, path: Path = DEFAULT_HW_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(hw.model_dump_json(indent=2), encoding="utf-8")


def run_once(
    *,
    hw_path: Path = DEFAULT_HW_PATH,
    note: Optional[str] = None,
    mark_receipt: Optional[Receipt] = None,
) -> HighWater:
    """
    Idempotent single pass:
    - load high-water
    - optionally record a receipt / note
    - save
    - return the updated object

    Real Drive / Gmail integration is left as a later extension
    (session can call Grok tools or use google-api if installed).
    """
    hw = load_highwater(hw_path)

    if note:
        hw.notes.append(f"{utcnow().isoformat()} | {note}")

    if mark_receipt:
        hw.add_receipt(mark_receipt)

    # Placeholder for future: compare against live inbox / Drive listing
    # and upsert open legs automatically.

    save_highwater(hw, hw_path)
    return hw
