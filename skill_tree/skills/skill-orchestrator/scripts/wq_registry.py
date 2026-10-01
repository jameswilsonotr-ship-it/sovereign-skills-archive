#!/usr/bin/env python3
"""SR-WQ-038a — generate MASTER_REGISTRY.md + .json from the live skill tree."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from wq_hygiene_lib import (
    build_registry,
    render_registry_md,
    skills_root,
    surface_dir,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()
    root = skills_root()
    reg = build_registry(root)
    out_dir = surface_dir(root)
    md_path = out_dir / "MASTER_REGISTRY.md"
    json_path = out_dir / "MASTER_REGISTRY.json"
    md_path.write_text(render_registry_md(reg), encoding="utf-8")
    write_json(json_path, reg)
    print(f"skills_root={root}")
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")
    print(f"queues={len(reg['queues'])} items={reg['item_count']} unregistered={len(reg['unregistered_ids'])}")
    if args.print:
        print(md_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
