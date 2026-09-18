#!/usr/bin/env python3
"""Stream-peek JSONL / JSON shards. Treats Drive 'octet-stream' as text until proven binary."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def peek(path: Path, n=3):
    raw = path.open("rb").read(8)
    kind = "json-text" if raw[:1] in (b"{", b"[") else "maybe-binary"
    out = {"path": str(path), "magic": raw[:8].hex(), "kind": kind, "samples": []}
    if kind != "json-text":
        return out
    with path.open() as f:
        first = f.read(1)
        f.seek(0)
        if first == "[":
            # array JSON — do not json.load whole file
            out["shape"] = "json-array"
            out["note"] = "use ijson.items(file, 'item') when ijson is present; do not slurp"
            return out
        out["shape"] = "jsonl"
        keys = Counter()
        for i, line in enumerate(f):
            if i >= n:
                break
            o = json.loads(line)
            keys.update(o.keys())
            out["samples"].append({"keys": list(o.keys()), "id": o.get("id") or o.get("session_id"), "title": (o.get("title") or "")[:80]})
        out["key_union_first_n"] = list(keys)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("-n", type=int, default=2)
    args = ap.parse_args()
    print(json.dumps([peek(Path(p), args.n) for p in args.paths], indent=2))


if __name__ == "__main__":
    main()
