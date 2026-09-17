#!/usr/bin/env python3
"""Verify the offline THIRD_SALVO T3-21 fixture and its checksum."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/third-salvo/t3-21-ultra-included.json"
CHECKSUMS = ROOT / "fixtures/third-salvo/checksums.sha256"
EXPECTED = {
    "availability": "included",
    "on_demand": False,
    "salvo": "THIRD_SALVO",
    "slot": "T3-21",
    "tier": "Ultra",
}


def main() -> None:
    fixture_bytes = FIXTURE.read_bytes()
    checksum_lines = [
        line.strip()
        for line in CHECKSUMS.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(checksum_lines) != 1:
        raise SystemExit("expected exactly one active checksum record")

    recorded_digest, recorded_path = checksum_lines[0].split(maxsplit=1)
    if recorded_path != "fixtures/third-salvo/t3-21-ultra-included.json":
        raise SystemExit(f"unexpected checksum path: {recorded_path}")

    actual_digest = hashlib.sha256(fixture_bytes).hexdigest()
    if actual_digest != recorded_digest:
        raise SystemExit(
            f"checksum mismatch: expected {recorded_digest}, got {actual_digest}"
        )

    payload = json.loads(fixture_bytes)
    if payload != EXPECTED:
        raise SystemExit(f"fixture policy mismatch: {payload!r}")
    if payload["on_demand"]:
        raise SystemExit("T3-21 must never be On-Demand")

    print(f"verified {recorded_path} sha256={actual_digest}")


if __name__ == "__main__":
    main()
