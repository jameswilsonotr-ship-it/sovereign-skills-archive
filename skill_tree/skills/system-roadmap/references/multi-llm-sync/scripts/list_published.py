#!/usr/bin/env python3
"""Thin Queue Sync — list_published.py
Local helper. Lists files matching an ownership prefix (olivia_ / vesper_).
"""

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="List TQS published artifacts by prefix")
    parser.add_argument("--prefix", required=True, help="e.g. olivia_ or vesper_")
    parser.add_argument("--dir", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.dir)
    matches = sorted(root.glob(f"{args.prefix}*"))
    # also check published/ if present
    pub = root / "published"
    if pub.is_dir():
        matches += sorted(pub.glob(f"{args.prefix}*"))

    print(f"=== Published artifacts matching '{args.prefix}' ===")
    if not matches:
        print("  (none found)")
    else:
        for p in matches:
            print(f"  {p}")
    print("[list_published] Done. Local only.")

if __name__ == "__main__":
    main()
