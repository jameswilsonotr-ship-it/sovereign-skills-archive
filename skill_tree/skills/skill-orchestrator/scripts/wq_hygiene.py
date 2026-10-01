#!/usr/bin/env python3
"""SR-WQ-038 umbrella runner.

Regenerates MASTER_REGISTRY, work + prompt atom clouds, validation report,
checks flags, optionally clears them. Export snapshots for the console app.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from wq_hygiene_lib import (
    atomize_prompts,
    atomize_work,
    build_registry,
    clear_flags,
    export_for_app,
    list_flags,
    render_registry_md,
    skills_root,
    surface_dir,
    validate,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--clear-flags", action="store_true")
    parser.add_argument("--export-app", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = skills_root()
    out = surface_dir(root)
    flags = list_flags(root)

    if args.check_only:
        report = validate(root, strict=args.strict)
        print(f"flags_open={len(flags)} ok={report['ok']} errors={report['error_count']} warns={report['warn_count']}")
        for f in flags:
            print(f"  FLAG {f.get('ts')} ids={f.get('touched_ids')} source={f.get('source')}")
        return 0 if report["ok"] else 1

    reg = build_registry(root)
    (out / "MASTER_REGISTRY.md").write_text(render_registry_md(reg), encoding="utf-8")
    write_json(out / "MASTER_REGISTRY.json", reg)

    work = atomize_work(root)
    write_json(out / "work_atomizer.json", work)

    prompts = atomize_prompts(root)
    write_json(out / "prompt_atomizer.json", prompts)

    report = validate(root, strict=args.strict)
    write_json(out / "HYGIENE_REPORT.json", report)

    snapshot = {
        "generated": report["generated"],
        "skills_root": str(root),
        "flags": flags,
        "registry": {
            "queue_count": len(reg["queues"]),
            "item_count": reg["item_count"],
            "unregistered": reg["unregistered_ids"],
        },
        "work_count": work["count"],
        "prompt_count": prompts["count"],
        "hygiene": {
            "ok": report["ok"],
            "error_count": report["error_count"],
            "warn_count": report["warn_count"],
            "issues": report["issues"][:80],
        },
    }
    write_json(out / "SNAPSHOT.json", snapshot)

    if args.export_app:
        dest = export_for_app(
            {
                "registry.json": reg,
                "work_atoms.json": work,
                "prompt_atoms.json": prompts,
                "hygiene_report.json": report,
                "flags.json": {"flags": flags, "generated": report["generated"]},
                "snapshot.json": snapshot,
            }
        )
        print(f"exported {dest}")

    if args.clear_flags:
        n = clear_flags(root)
        print(f"cleared_flags={n}")

    print(
        f"hygiene queues={len(reg['queues'])} items={reg['item_count']} "
        f"work_atoms={work['count']} prompts={prompts['count']} "
        f"ok={report['ok']} errors={report['error_count']} warns={report['warn_count']} "
        f"flags={len(flags)}"
    )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
