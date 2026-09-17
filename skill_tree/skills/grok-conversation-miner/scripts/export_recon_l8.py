#!/usr/bin/env python3
"""GCM-WQ-006 L8 export recon. Diff fake or real export index vs lake/sunset ids."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gcm_lib import stamps, write_text


def recon(export_index: list[dict], lake_ids: set[str], sunset_ids: set[str]) -> dict:
    export_ids = {r["id"] for r in export_index}
    return {
        "IN_LAKE": sorted(export_ids & lake_ids),
        "IN_EXPORT_ONLY": sorted(export_ids - lake_ids - sunset_ids),
        "IN_SUNSET_ONLY": sorted(sunset_ids - export_ids),
        "ASSET_MISSING": sorted((export_ids | lake_ids) - export_ids),
        **stamps(),
    }


def render_md(diff: dict) -> str:
    lines = ["# EXPORT_RECON", "", f"stamp_utc: {diff['stamp_utc']}", ""]
    for k in ("IN_LAKE", "IN_EXPORT_ONLY", "IN_SUNSET_ONLY", "ASSET_MISSING"):
        lines.append(f"## {k}")
        vals = diff.get(k) or []
        if not vals:
            lines.append("- (none)")
        for v in vals:
            lines.append(f"- `{v}`")
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--export-json", type=Path, required=True)
    p.add_argument("--lake-json", type=Path, required=True)
    p.add_argument("--sunset-json", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)
    export_index = json.loads(args.export_json.read_text(encoding="utf-8"))
    lake_ids = set(json.loads(args.lake_json.read_text(encoding="utf-8")))
    sunset_ids = set(json.loads(args.sunset_json.read_text(encoding="utf-8")))
    diff = recon(export_index, lake_ids, sunset_ids)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_md(diff), encoding="utf-8")
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in diff.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
