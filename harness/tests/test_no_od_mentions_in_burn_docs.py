from __future__ import annotations

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.smoke

REPO_ROOT = Path(__file__).parents[2]
BURN_DOCS = REPO_ROOT / "docs" / "burn-wave"
FORBIDDEN_OD_SPEND_VERBS = (
    "allocate",
    "bid",
    "buy",
    "charge",
    "credit",
    "debit",
    "donate",
    "fund",
    "invest",
    "order",
    "pay",
    "purchase",
    "reimburse",
    "send",
    "spend",
    "subscribe",
    "transfer",
    "withdraw",
)
FORBIDDEN_OD_SPEND_PATTERN = re.compile(
    rf"\b(?:{'|'.join(FORBIDDEN_OD_SPEND_VERBS)})\b",
    re.IGNORECASE,
)


def _forbidden_mentions() -> list[str]:
    """Return stable, line-addressable diagnostics for forbidden doc mentions."""

    mentions: list[str] = []
    for path in sorted(BURN_DOCS.rglob("*")):
        if not path.is_file():
            continue

        relative_path = path.relative_to(REPO_ROOT)
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(),
            start=1,
        ):
            for match in FORBIDDEN_OD_SPEND_PATTERN.finditer(line):
                mentions.append(f"{relative_path}:{line_number}: {match.group(0)!r}")
    return mentions


def test_burn_docs_contain_no_forbidden_od_spend_verbs() -> None:
    mentions = _forbidden_mentions()

    assert not mentions, "Forbidden OD spend verbs found:\n" + "\n".join(mentions)
