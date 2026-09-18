#!/usr/bin/env python3
"""Fail when documentation contains common secret-shaped values.

This checker is intentionally local and dependency-free. It is a guard against
accidentally committing credentials to ``docs/``; it is not a replacement for
secret management or a full secret-scanning service.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Pattern


PATTERNS: tuple[tuple[str, Pattern[str]], ...] = (
    (
        "AWS access key ID",
        re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ),
    (
        "GitHub token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    ),
    (
        "Google API key",
        re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ),
    (
        "Slack token",
        re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    ),
    (
        "OpenAI-compatible API key",
        re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    ),
    (
        "Stripe key",
        re.compile(r"\b(?:sk|rk)_(?:live|test)_[0-9A-Za-z]{16,}\b"),
    ),
    (
        "JWT",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
        ),
    ),
    (
        "private key block",
        re.compile(r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----"),
    ),
    (
        "named secret assignment",
        re.compile(
            r"""(?ix)
            \b(?:api[_ -]?key|access[_ -]?key|secret(?:[_ -]?key)?|
            auth(?:entication)?[_ -]?token|bearer|password|passwd|client[_ -]?secret)
            \b\s*[:=]\s*["'`]?[A-Za-z0-9/+_.=-]{16,}
            """
        ),
    ),
    (
        "credential-bearing URL",
        re.compile(
            r"(?i)\b(?:https?|postgres(?:ql)?|mysql|redis)://[^/\s:@]+:[^@\s]+@"
        ),
    ),
)


def iter_document_files(docs_dir: Path) -> Iterable[Path]:
    """Yield regular files under *docs_dir* in deterministic order."""

    yield from sorted(path for path in docs_dir.rglob("*") if path.is_file())


def find_matches(docs_dir: Path) -> list[tuple[Path, int, str]]:
    """Return ``(path, line_number, pattern_name)`` for every finding."""

    findings: list[tuple[Path, int, str]] = []
    for path in iter_document_files(docs_dir):
        try:
            contents = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Documentation should be text, but ignoring undecodable files
            # avoids turning an unrelated binary asset into a false alarm.
            continue

        for line_number, line in enumerate(contents.splitlines(), start=1):
            for pattern_name, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append((path, line_number, pattern_name))
    return findings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail if docs/ contains common secret-shaped values."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs",
        help="directory to scan (default: repository docs/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    docs_dir = args.docs_dir.resolve()
    if not docs_dir.is_dir():
        print(f"error: documentation directory does not exist: {docs_dir}", file=sys.stderr)
        return 2

    findings = find_matches(docs_dir)
    if findings:
        print(f"secret-like patterns found in {len(findings)} location(s):")
        for path, line_number, pattern_name in findings:
            print(f"  {path}:{line_number}: {pattern_name}")
        return 1

    print(f"No secret-like patterns found under {docs_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
