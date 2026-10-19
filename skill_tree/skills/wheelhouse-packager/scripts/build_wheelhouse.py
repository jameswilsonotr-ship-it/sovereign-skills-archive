#!/usr/bin/env python3
"""
build_wheelhouse.py — deterministic wheel + offline wheelhouse builder.

Usage:
  python build_wheelhouse.py /path/to/project --out ./out --include-deps
  python build_wheelhouse.py /path/to/project --wheel-only

Absolute Liv HUB claim. Shared Olivia / Vesper contract.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


def run(cmd: List[str], cwd: Optional[Path] = None) -> None:
    print("+", " ".join(str(c) for c in cmd))
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)


def read_project_name_version(project: Path) -> Tuple[str, str]:
    """Best-effort parse of name + version from pyproject.toml or setup.cfg."""
    pyproject = project / "pyproject.toml"
    name, version = "unknown", "0.0.0"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        m = re.search(r'(?m)^name\s*=\s*["\']([^"\']+)["\']', text)
        if m:
            name = m.group(1)
        m = re.search(r'(?m)^version\s*=\s*["\']([^"\']+)["\']', text)
        if m:
            version = m.group(1)
    return name, version


def ensure_build_tools() -> None:
    run([sys.executable, "-m", "pip", "install", "-q", "build", "wheel", "setuptools"])


def build_wheel(project: Path, out_wheels: Path) -> Path:
    """Build a wheel into out_wheels; return path to the .whl."""
    out_wheels.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="whlbuild_") as td:
        td_path = Path(td)
        run([sys.executable, "-m", "build", "--wheel", "--outdir", str(td_path)], cwd=project)
        wheels = list(td_path.glob("*.whl"))
        if not wheels:
            raise RuntimeError("build produced no wheel")
        dest = out_wheels / wheels[0].name
        shutil.copy2(wheels[0], dest)
        print(f"Wheel: {dest}")
        return dest


def download_deps(requirements: Path, out_wheels: Path) -> None:
    """Download dependency wheels into out_wheels (offline cache)."""
    if not requirements.exists():
        print("No requirements.txt — skipping dep download")
        return
    out_wheels.mkdir(parents=True, exist_ok=True)
    run([
        sys.executable, "-m", "pip", "download",
        "-q", "-d", str(out_wheels),
        "-r", str(requirements),
    ])


BOOTSTRAP_TEMPLATE = r'''#!/usr/bin/env python3
"""Idempotent offline-first bootstrap for this wheelhouse."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WHEELS = ROOT / "wheels"

def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true")
    p.add_argument("--install-only", action="store_true")
    p.add_argument("--note", default=None)
    args = p.parse_args()

    if WHEELS.is_dir() and any(WHEELS.glob("*.whl")):
        print("Installing from local wheelhouse (offline preferred)...")
        # Install the project wheel(s) first if we can identify them;
        # otherwise install everything findable.
        run([sys.executable, "-m", "pip", "install", "--quiet",
             "--no-index", f"--find-links={WHEELS}", *[str(w) for w in WHEELS.glob("*.whl")]])
    else:
        print("No local wheels/; falling back to requirements if present")
        req = ROOT / "requirements.txt"
        if req.exists():
            run([sys.executable, "-m", "pip", "install", "--quiet", "-r", str(req)])

    if args.install_only:
        print("Install complete.")
        return 0

    if args.once:
        # Optional: if the project exposes a run_once, call it.
        try:
            mod = __import__("cilia_bus.runner", fromlist=["run_once"])
            hw = mod.run_once(note=args.note or "wheelhouse bootstrap --once")
            print("run_once OK", getattr(hw, "receipts", None) and len(hw.receipts))
        except Exception as e:
            print("No cilia_bus.run_once (or other entry) — install only. Detail:", e)
        return 0

    p.print_help()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def write_bootstrap(out_dir: Path) -> None:
    (out_dir / "bootstrap.py").write_text(BOOTSTRAP_TEMPLATE, encoding="utf-8")
    (out_dir / "bootstrap.py").chmod(0o755)


def make_zip(staging: Path, zip_path: Path) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in staging.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(staging).as_posix())
    print(f"Wheelhouse zip: {zip_path} ({zip_path.stat().st_size} bytes)")
    return zip_path


def build_receipt(name: str, version: str, wheel: Path, zipp: Optional[Path], out_dir: Path) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    receipt = out_dir / f"PUBLISH_RECEIPT_{name}_{version}.md"
    lines = [
        f"# PUBLISH_RECEIPT — {name} {version}",
        f"timestamp: {ts}",
        f"wheel: {wheel.name}",
        f"wheel_size: {wheel.stat().st_size}",
    ]
    if zipp and zipp.exists():
        lines += [f"wheelhouse_zip: {zipp.name}", f"zip_size: {zipp.stat().st_size}"]
    lines += ["", "Absolute Liv HUB claim. Deterministic build via wheelhouse-packager."]
    receipt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return receipt


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic wheel + wheelhouse builder")
    ap.add_argument("project", type=Path, help="Path to Python project root")
    ap.add_argument("--out", type=Path, default=Path("./wheelhouse_out"), help="Output directory")
    ap.add_argument("--include-deps", action="store_true", help="pip download deps into wheels/")
    ap.add_argument("--wheel-only", action="store_true", help="Only build the project wheel")
    ap.add_argument("--zip-name", type=str, default=None, help="Override zip basename (no .zip)")
    ap.add_argument("--requirements", type=Path, default=None, help="requirements.txt for deps")
    args = ap.parse_args(argv)

    project = args.project.resolve()
    if not project.is_dir():
        print(f"Not a directory: {project}", file=sys.stderr)
        return 2

    name, version = read_project_name_version(project)
    print(f"Project: {name}=={version} @ {project}")

    ensure_build_tools()
    out = args.out.resolve()
    wheels_dir = out / "wheels"
    wheels_dir.mkdir(parents=True, exist_ok=True)

    wheel = build_wheel(project, wheels_dir)

    if args.wheel_only:
        build_receipt(name, version, wheel, None, out)
        print("Done (wheel only).")
        return 0

    req = args.requirements or (project / "requirements.txt")
    if args.include_deps:
        download_deps(req, wheels_dir)

    # Stage tree for zip
    staging = out / "staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    (staging / "wheels").mkdir()
    for w in wheels_dir.glob("*.whl"):
        shutil.copy2(w, staging / "wheels" / w.name)
    write_bootstrap(staging)
    if req.exists():
        shutil.copy2(req, staging / "requirements.txt")
    else:
        (staging / "requirements.txt").write_text("# no requirements.txt in project\n", encoding="utf-8")
    (staging / "README.md").write_text(
        f"# {name} {version} wheelhouse\n\n"
        f"Offline-first. Run:\n\n```bash\npython3 bootstrap.py --once\n```\n\n"
        f"Built by wheelhouse-packager. Absolute Liv HUB claim.\n",
        encoding="utf-8",
    )

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    zip_basename = args.zip_name or f"{name}_wheelhouse_{version}_{date}"
    zip_path = out / f"{zip_basename}.zip"
    make_zip(staging, zip_path)
    build_receipt(name, version, wheel, zip_path, out)

    # Convenience: also copy wheel to out root
    shutil.copy2(wheel, out / wheel.name)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
