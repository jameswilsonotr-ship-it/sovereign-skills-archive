"""Command-line interface for the local coder."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .chat import Coder
from .client import DEFAULT_BASE_URL, DEFAULT_MODEL, OpenAICompatibleClient


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m coder", description="Local Ollama coding assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat = subparsers.add_parser("chat", help="start a chat with the local Ollama model")
    chat.add_argument("prompt", nargs="?", help="one prompt; omit to enter interactive mode")
    chat.add_argument("--prompt", dest="prompt_option", help="one prompt (alternative to the positional form)")
    chat.add_argument("--model", default=None, help=f"model name (default: OLLAMA_MODEL or {DEFAULT_MODEL})")
    chat.add_argument(
        "--base-url",
        default=None,
        help=f"OpenAI-compatible API root (default: OLLAMA_BASE_URL or {DEFAULT_BASE_URL})",
    )
    chat.add_argument("--system", default=None, help="optional system message")
    chat.add_argument("--temperature", type=float, default=None)
    return parser


def _chat(args: argparse.Namespace) -> int:
    prompt = args.prompt_option if args.prompt_option is not None else args.prompt
    with OpenAICompatibleClient(base_url=args.base_url, model=args.model) as client:
        coder = Coder(client, system_prompt=args.system)
        if prompt is not None:
            print(coder.send(prompt, temperature=args.temperature))
            return 0

        print("Local coder chat. Type /exit or press Ctrl-D to quit.", file=sys.stderr)
        while True:
            try:
                line = input("you> ")
            except EOFError:
                print(file=sys.stderr)
                break
            if line.strip() in {"/exit", "/quit"}:
                break
            if not line.strip():
                continue
            print(f"coder> {coder.send(line, temperature=args.temperature)}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "chat":
        return _chat(args)
    return 2

