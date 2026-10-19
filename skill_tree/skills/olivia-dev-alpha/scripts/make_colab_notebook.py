#!/usr/bin/env python3
"""Write a Colab-ready .ipynb into artifacts/. Liv HUB. No secrets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def notebook(title: str, folder_id: str, prompt: str) -> dict:
    md = (
        f"# {title}\n\n"
        "Paste the prompt in cell 3. Run all. Drive mounts first.\n\n"
        f"Default folder id: `{folder_id}`\n"
    )
    mount = (
        "from google.colab import drive\n"
        "import os\n"
        "drive.mount('/content/drive')\n"
        "print('mounted', os.path.exists('/content/drive/MyDrive'))\n"
    )
    body = (
        f"PROMPT = '''{prompt}'''\n"
        f"FOLDER_ID = '{folder_id}'\n"
        "print(PROMPT)\n"
        "print('folder', FOLDER_ID)\n"
        "# next: list Drive via pydrive2 / files API if token present\n"
    )
    return {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "language_info": {"name": "python"},
        },
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [md]},
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": [mount],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": [body],
            },
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--title", default="Liv HUB Colab seed")
    p.add_argument("--folder-id", default="14ZusAV3UP6RbqcrFZ6t_fCO0BZwgG0vg")
    p.add_argument("--prompt", default="Index packed sunset archives. Do not explode 416 MB.")
    p.add_argument("--out", default="/home/workdir/artifacts/LivHUB_Colab_Seed.ipynb")
    args = p.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(notebook(args.title, args.folder_id, args.prompt), indent=2))
    print(out)


if __name__ == "__main__":
    main()
