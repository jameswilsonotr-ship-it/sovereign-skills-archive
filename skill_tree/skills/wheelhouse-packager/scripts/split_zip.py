#!/usr/bin/env python3
"""
split_zip.py — deterministic arbitrary-file splitter.

Split any file into zip parts whose *zip file size* is <= max-bytes
(default 10 MiB). Optional base64 sidecars for Colab / text-only transports.

Three-way proof:
  raw file  <->  zip parts (<= max)  <->  .b64 sidecars of those zips

Reassemble is bitwise-identical (SHA-256 of source == SHA-256 of joined).

Usage:
  python split_zip.py split  SRC --out DIR [--max-bytes 10485760] [--b64]
  python split_zip.py join   DIR --out RESTORED
  python split_zip.py verify SRC DIR
  python split_zip.py proof  SRC --out DIR [--max-bytes ...]

Absolute Liv HUB claim. Shared Olivia / Vesper contract.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_MAX = 10 * 1024 * 1024  # 10 MiB
STORED = zipfile.ZIP_STORED
MANIFEST_NAME = "SPLIT_MANIFEST.json"
SCHEMA = "livhub.split-zip.v1"


def sha256_file(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_stem(src: Path) -> str:
    name = src.name
    return name.replace("/", "_").replace("\\", "_")


def _estimate_chunk(max_bytes: int, payload_name: str) -> int:
    """
    ZIP_STORED overhead is small and stable:
      local header ~30 + filename + extra
      central dir  ~46 + filename
      EOCD ~22
    Leave a conservative 4 KiB pad plus filename slack so the *zip*
    never exceeds max_bytes.
    """
    slack = 4096 + 2 * (len(payload_name) + 64)
    chunk = max_bytes - slack
    if chunk < 64 * 1024:
        raise ValueError(
            f"max-bytes={max_bytes} too small after zip overhead slack={slack}"
        )
    return chunk


def split_file(
    src: Path,
    out_dir: Path,
    max_bytes: int = DEFAULT_MAX,
    write_b64: bool = True,
) -> Dict[str, Any]:
    src = src.resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = _safe_stem(src)
    payload_name = f"{stem}.part"
    chunk_size = _estimate_chunk(max_bytes, payload_name)
    source_hash = sha256_file(src)
    source_size = src.stat().st_size

    parts: List[Dict[str, Any]] = []
    index = 0
    with src.open("rb") as f:
        while True:
            raw = f.read(chunk_size)
            if not raw:
                break
            part_id = f"{index:04d}"
            inner_name = f"{stem}.part{part_id}.bin"
            zip_name = f"{stem}.part{part_id}.zip"
            zip_path = out_dir / zip_name

            with zipfile.ZipFile(zip_path, "w", compression=STORED) as zf:
                zf.writestr(inner_name, raw)

            zip_size = zip_path.stat().st_size
            if zip_size > max_bytes:
                raise RuntimeError(
                    f"{zip_name} is {zip_size} bytes > max-bytes {max_bytes}"
                )

            rec: Dict[str, Any] = {
                "index": index,
                "zip": zip_name,
                "inner": inner_name,
                "payload_bytes": len(raw),
                "zip_bytes": zip_size,
                "payload_sha256": sha256_bytes(raw),
                "zip_sha256": sha256_file(zip_path),
            }

            if write_b64:
                b64_name = f"{zip_name}.b64"
                b64_path = out_dir / b64_name
                b64_path.write_text(
                    base64.b64encode(zip_path.read_bytes()).decode("ascii"),
                    encoding="ascii",
                )
                rec["b64"] = b64_name
                rec["b64_bytes"] = b64_path.stat().st_size

            parts.append(rec)
            index += 1

    if index == 0:
        # Empty file still gets one empty zip so join is uniform.
        part_id = "0000"
        inner_name = f"{stem}.part{part_id}.bin"
        zip_name = f"{stem}.part{part_id}.zip"
        zip_path = out_dir / zip_name
        with zipfile.ZipFile(zip_path, "w", compression=STORED) as zf:
            zf.writestr(inner_name, b"")
        rec = {
            "index": 0,
            "zip": zip_name,
            "inner": inner_name,
            "payload_bytes": 0,
            "zip_bytes": zip_path.stat().st_size,
            "payload_sha256": sha256_bytes(b""),
            "zip_sha256": sha256_file(zip_path),
        }
        if write_b64:
            b64_name = f"{zip_name}.b64"
            (out_dir / b64_name).write_text(
                base64.b64encode(zip_path.read_bytes()).decode("ascii"),
                encoding="ascii",
            )
            rec["b64"] = b64_name
            rec["b64_bytes"] = (out_dir / b64_name).stat().st_size
        parts.append(rec)

    manifest: Dict[str, Any] = {
        "schema": SCHEMA,
        "created_utc": utc_now(),
        "source_name": src.name,
        "source_path": str(src),
        "source_bytes": source_size,
        "source_sha256": source_hash,
        "max_bytes": max_bytes,
        "chunk_payload_bytes": chunk_size,
        "compression": "ZIP_STORED",
        "part_count": len(parts),
        "b64_sidecars": write_b64,
        "claim": "Absolute Liv HUB",
        "parts": parts,
    }
    man_path = out_dir / MANIFEST_NAME
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def _load_manifest(part_dir: Path) -> Dict[str, Any]:
    man = part_dir / MANIFEST_NAME
    if not man.is_file():
        raise FileNotFoundError(f"missing {MANIFEST_NAME} in {part_dir}")
    data = json.loads(man.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"unsupported schema {data.get('schema')}")
    return data


def join_parts(part_dir: Path, out_path: Path, prefer_b64: bool = False) -> str:
    part_dir = part_dir.resolve()
    manifest = _load_manifest(part_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    h = hashlib.sha256()
    with out_path.open("wb") as out:
        for rec in sorted(manifest["parts"], key=lambda r: r["index"]):
            zip_path = part_dir / rec["zip"]
            if prefer_b64 and rec.get("b64"):
                b64_path = part_dir / rec["b64"]
                zip_bytes = base64.b64decode(b64_path.read_text(encoding="ascii"))
                tmp = part_dir / f".{rec['zip']}.from_b64"
                tmp.write_bytes(zip_bytes)
                zip_path = tmp
            elif not zip_path.is_file():
                if rec.get("b64"):
                    zip_bytes = base64.b64decode(
                        (part_dir / rec["b64"]).read_text(encoding="ascii")
                    )
                    zip_path.write_bytes(zip_bytes)
                else:
                    raise FileNotFoundError(zip_path)

            with zipfile.ZipFile(zip_path, "r") as zf:
                raw = zf.read(rec["inner"])
            got = sha256_bytes(raw)
            if got != rec["payload_sha256"]:
                raise ValueError(
                    f"payload hash mismatch on part {rec['index']}: {got} != {rec['payload_sha256']}"
                )
            out.write(raw)
            h.update(raw)
            tmp = part_dir / f".{rec['zip']}.from_b64"
            if tmp.exists():
                tmp.unlink()

    digest = h.hexdigest()
    expected = manifest["source_sha256"]
    if digest != expected:
        raise ValueError(f"reassembled hash {digest} != source {expected}")
    if out_path.stat().st_size != manifest["source_bytes"]:
        raise ValueError("reassembled size mismatch")
    return digest


def verify(src: Path, part_dir: Path) -> Dict[str, Any]:
    manifest = _load_manifest(part_dir)
    src_hash = sha256_file(src)
    ok_src = src_hash == manifest["source_sha256"]
    zip_ok = True
    b64_ok = True
    oversize = []
    for rec in manifest["parts"]:
        zp = part_dir / rec["zip"]
        if not zp.is_file() or sha256_file(zp) != rec["zip_sha256"]:
            zip_ok = False
        if zp.is_file() and zp.stat().st_size > manifest["max_bytes"]:
            oversize.append(rec["zip"])
        if rec.get("b64"):
            bp = part_dir / rec["b64"]
            if not bp.is_file():
                b64_ok = False
            else:
                rebuilt = base64.b64decode(bp.read_text(encoding="ascii"))
                if sha256_bytes(rebuilt) != rec["zip_sha256"]:
                    b64_ok = False
    return {
        "source_match": ok_src,
        "zips_match": zip_ok,
        "b64_match": b64_ok,
        "oversize_parts": oversize,
        "part_count": manifest["part_count"],
        "source_sha256": src_hash,
        "manifest_sha256": manifest["source_sha256"],
        "ok": ok_src and zip_ok and b64_ok and not oversize,
    }


def proof(src: Path, out_dir: Path, max_bytes: int) -> Dict[str, Any]:
    """Split, join via zip, join via b64 — three-way identity."""
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = split_file(src, out_dir, max_bytes=max_bytes, write_b64=True)
    restored_zip = out_dir / f"RESTORED_FROM_ZIP_{src.name}"
    restored_b64 = out_dir / f"RESTORED_FROM_B64_{src.name}"
    h_zip = join_parts(out_dir, restored_zip, prefer_b64=False)
    h_b64 = join_parts(out_dir, restored_b64, prefer_b64=True)
    v = verify(src, out_dir)
    result = {
        "ok": h_zip == h_b64 == manifest["source_sha256"] and v["ok"],
        "source_sha256": manifest["source_sha256"],
        "restored_zip_sha256": h_zip,
        "restored_b64_sha256": h_b64,
        "part_count": manifest["part_count"],
        "max_bytes": max_bytes,
        "verify": v,
    }
    (out_dir / "PROOF.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Deterministic 10 MiB zip splitter")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("split")
    s.add_argument("src")
    s.add_argument("--out", required=True)
    s.add_argument("--max-bytes", type=int, default=DEFAULT_MAX)
    s.add_argument("--b64", action="store_true", default=True)
    s.add_argument("--no-b64", action="store_true")

    j = sub.add_parser("join")
    j.add_argument("part_dir")
    j.add_argument("--out", required=True)
    j.add_argument("--from-b64", action="store_true")

    v = sub.add_parser("verify")
    v.add_argument("src")
    v.add_argument("part_dir")

    pr = sub.add_parser("proof")
    pr.add_argument("src")
    pr.add_argument("--out", required=True)
    pr.add_argument("--max-bytes", type=int, default=DEFAULT_MAX)

    args = p.parse_args(argv)

    if args.cmd == "split":
        man = split_file(
            Path(args.src),
            Path(args.out),
            max_bytes=args.max_bytes,
            write_b64=not args.no_b64,
        )
        print(json.dumps({
            "ok": True,
            "part_count": man["part_count"],
            "source_sha256": man["source_sha256"],
            "out": args.out,
        }, indent=2))
        return 0
    if args.cmd == "join":
        digest = join_parts(Path(args.part_dir), Path(args.out), prefer_b64=args.from_b64)
        print(json.dumps({"ok": True, "sha256": digest, "out": args.out}, indent=2))
        return 0
    if args.cmd == "verify":
        report = verify(Path(args.src), Path(args.part_dir))
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1
    if args.cmd == "proof":
        report = proof(Path(args.src), Path(args.out), max_bytes=args.max_bytes)
        print(json.dumps(report, indent=2))
        return 0 if report["ok"] else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
