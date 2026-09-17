"""Small, dependency-free text coding helper for the local Ollama endpoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send a coding prompt to a local OpenAI-compatible endpoint."
    )
    parser.add_argument("-p", "--prompt", help="Text prompt. Reads stdin when omitted.")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Include a UTF-8 text file in the prompt (repeatable).",
    )
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "gemma3:4b"))
    parser.add_argument(
        "--base-url",
        default=os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/v1"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = args.prompt
    if prompt is None:
        prompt = sys.stdin.read().strip()
    if not prompt:
        print("Provide --prompt or pipe a prompt on stdin.", file=sys.stderr)
        return 2

    attachments: list[str] = []
    for file_name in args.file:
        path = Path(file_name)
        attachments.append(f"\n\n--- {path} ---\n{path.read_text(encoding='utf-8')}")

    request_body = json.dumps(
        {
            "model": args.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a local, text-only coding assistant. "
                        "Return concise, actionable answers. Do not claim to have "
                        "edited files or run commands."
                    ),
                },
                {"role": "user", "content": prompt + "".join(attachments)},
            ],
            "stream": False,
        }
    ).encode("utf-8")
    endpoint = args.base_url.rstrip("/") + "/chat/completions"
    request = urllib.request.Request(
        endpoint,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer ollama",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.load(response)
    except (OSError, ValueError) as exc:
        print(f"local inference request failed: {exc}", file=sys.stderr)
        return 1

    try:
        print(result["choices"][0]["message"]["content"])
    except (KeyError, IndexError, TypeError):
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
