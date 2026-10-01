#!/usr/bin/env python3
"""SR-WQ-038b — walk work-queue items, check IDs / prefixes / reverse links."""
from __future__ import annotations

import argparse
import json
import sys

from wq_hygiene_lib import skills_root, surface_dir, validate, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = skills_root()
    report = validate(root, strict=args.strict)
    out = surface_dir(root) / "HYGIENE_REPORT.json"
    write_json(out, report)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"ok={report['ok']} errors={report['error_count']} warns={report['warn_count']} items={report['item_count']}")
        for issue in report["issues"][:40]:
            print(f"  [{issue['level']}] {issue['code']}: {issue['msg']}")
        if len(report["issues"]) > 40:
            print(f"  … {len(report['issues']) - 40} more")
        print(f"wrote {out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
