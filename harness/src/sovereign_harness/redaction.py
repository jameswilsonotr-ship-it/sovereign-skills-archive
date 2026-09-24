"""Offline secret and PII checks for the checked-in fixture set.

The checker reports rule names and line numbers only. It never includes the
matched value in a finding, receipt, or command-line result.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RedactionFinding:
    """A location and rule name, without the sensitive value."""

    source: str
    rule: str
    line: int


_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "email",
        re.compile(
            r"(?<![\w.+-])[\w.!#$%&'*+/=?^_`{|}~-]+@[\w-]+(?:\.[\w-]+)+(?![\w-])"
        ),
    ),
    (
        "phone",
        re.compile(
            r"(?<!\d)(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-])\d{3}[\s.-]\d{4}(?!\d)"
        ),
    ),
    (
        "credential-assignment",
        re.compile(
            r"""(?ix)
            \b(?:api[_ -]?key|access[_ -]?token|client[_ -]?secret|password)\b
            \s*["']?\s*[:=]\s*["']?[A-Za-z0-9][A-Za-z0-9._~-]{11,}
            """
        ),
    ),
    (
        "private-key",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    ),
    (
        "bearer-token",
        re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b"),
    ),
)


def scan_text(text: str, source: str = "<memory>") -> tuple[RedactionFinding, ...]:
    """Return redaction findings without returning matched content."""

    findings: list[RedactionFinding] = []
    for rule, pattern in _RULES:
        for match in pattern.finditer(text):
            findings.append(
                RedactionFinding(
                    source=source,
                    rule=rule,
                    line=text.count("\n", 0, match.start()) + 1,
                )
            )
    return tuple(sorted(findings, key=lambda finding: (finding.source, finding.line, finding.rule)))


def check_fixture_directory(fixture_dir: Path | str) -> tuple[RedactionFinding, ...]:
    """Scan local JSON fixtures recursively for secret or PII patterns."""

    root = Path(fixture_dir)
    findings: list[RedactionFinding] = []
    for path in sorted(root.rglob("*.json")):
        findings.extend(scan_text(path.read_text(encoding="utf-8"), str(path)))
    return tuple(findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "fixture_dir",
        nargs="?",
        type=Path,
        default=Path("harness/src/sovereign_harness/fixtures"),
    )
    args = parser.parse_args()

    findings = check_fixture_directory(args.fixture_dir)
    if not findings:
        print(f"redaction check: PASS ({args.fixture_dir})")
        return 0

    print(f"redaction check: FAIL ({args.fixture_dir})")
    for finding in findings:
        print(f"- {finding.source}:{finding.line}: {finding.rule}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
