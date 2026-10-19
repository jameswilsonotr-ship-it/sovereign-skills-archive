#!/usr/bin/env python3
"""Mint a dated Colab notebook that actually does work.

The 03:20 seed only printed a string. This factory writes a notebook that:
  1. Tells you to Runtime → Run all
  2. Mounts Drive
  3. Walks MyDrive for the four phone-first pack names
  4. Prints size + unzip -l when the file is local
  5. Writes a receipt next to the notebook folder
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOBS = HERE / "jobs"


def _stamp() -> str:
    from tui import stamp

    return stamp()


def _nb(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {"provenance": [], "toc_visible": True},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "cells": cells,
    }


def _md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}


def _code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": [text],
    }


def build(job: str, cfg: dict) -> dict:
    packs = json.dumps(cfg["phone_first_packs"], indent=2)
    shelf = cfg["lab_shelf"]
    title = f"ODA-LAB {job}"
    md0 = f"""# {title}

**Runtime → Run all.** Then allow Drive when the popup hits.

This is not a prompt dump. Cell 2 mounts. Cell 3 walks MyDrive for the
four small sunset packs and prints a member list when it can open them.
It will not touch the 416.6 MB grok-five tar.

Shelf: `{shelf}` (`12_ODA-LAB-NOTEBOOKS`)
"""
    code1 = """# Cell 1 — mount
from google.colab import drive
from pathlib import Path
import os, subprocess, json, time

print('=== ODA LAB mount ===')
drive.mount('/content/drive', force_remount=False)
ROOT = Path('/content/drive/MyDrive')
print('mounted', ROOT.exists(), ROOT)
"""
    code2 = (
        "# Cell 2 — find the four small packs and list members\n"
        f"PACKS = {packs}\n"
        f"JOB = {job!r}\n"
        "def find_named(root, name, cap=8000):\n"
        "    hits = []\n"
        "    n = 0\n"
        "    for dirpath, dirnames, filenames in os.walk(root):\n"
        "        n += len(filenames)\n"
        "        if name in filenames:\n"
        "            hits.append(Path(dirpath) / name)\n"
        "        if len(hits) >= 5 or n >= cap:\n"
        "            break\n"
        "    print('  walked', n, 'files')\n"
        "    return hits\n"
        "print('=== ODA LAB pack walk ===')\n"
        "receipt = ['# ODA LAB receipt', 'job=' + JOB, '']\n"
        "for p in PACKS:\n"
        "    name = p['name']\n"
        "    print('---', p['n'], name, 'claimed', p['bytes'])\n"
        "    hits = find_named(ROOT, name) if ROOT.exists() else []\n"
        "    if not hits:\n"
        "        print('  not on this MyDrive walk')\n"
        "        receipt.append('- ' + name + ': NOT FOUND on mount')\n"
        "        continue\n"
        "    for hit in hits:\n"
        "        sz = hit.stat().st_size\n"
        "        print('  hit', hit, 'size', sz)\n"
        "        receipt.append('- ' + name + ': ' + str(hit) + ' size=' + str(sz))\n"
        "        if name.endswith('.zip') and sz < 20_000_000:\n"
        "            r = subprocess.run(['unzip', '-l', str(hit)], capture_output=True, text=True)\n"
        "            print((r.stdout or r.stderr)[:4000])\n"
        "            receipt.append('```')\n"
        "            receipt.append((r.stdout or r.stderr)[:2000])\n"
        "            receipt.append('```')\n"
        "print('=== done walk ===')\n"
        "RECEIPT = '\\n'.join(receipt)\n"
        "print(RECEIPT)\n"
    )
    code3 = (
        "# Cell 3 — write receipt onto Drive if we can see the shelf name\n"
        "out_dir = None\n"
        "for cand in ROOT.rglob('12_ODA-LAB-NOTEBOOKS'):\n"
        "    if cand.is_dir():\n"
        "        out_dir = cand\n"
        "        break\n"
        "if out_dir is None:\n"
        "    out_dir = ROOT / '12_ODA-LAB-NOTEBOOKS_LOCAL'\n"
        "    out_dir.mkdir(exist_ok=True)\n"
        "    print('shelf not found, wrote local fallback', out_dir)\n"
        "else:\n"
        "    print('shelf', out_dir)\n"
        "from datetime import datetime\n"
        f"fn = datetime.now().strftime('%Y%m%d-%H%M') + '_ODA-LAB_{job}.RECEIPT.md'\n"
        "path = out_dir / fn\n"
        "path.write_text(RECEIPT)\n"
        "print('WROTE', path)\n"
    )
    return _nb([_md(md0), _code(code1), _code(code2), _code(code3)])


def mint(job: str, cfg: dict, dest: Path | None = None) -> Path:
    JOBS.mkdir(parents=True, exist_ok=True)
    name = f"{_stamp()}_ODA-LAB_{job}.ipynb"
    dest = dest or (JOBS / name)
    dest.write_text(json.dumps(build(job, cfg), indent=2))
    return dest
