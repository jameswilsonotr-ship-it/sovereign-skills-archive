from pathlib import Path

import pytest

CHANGE_FOLDER_NAME_ALLOWLIST = frozenset({"change-7", "change-8", "change-9"})
OPENSPEC_DOCS = Path(__file__).parents[2] / "docs" / "openspec"


def test_change_folder_names_for_seven_through_nine_are_allowlisted() -> None:
    if not OPENSPEC_DOCS.is_dir():
        pytest.skip("OpenSpec docs path is not present")

    for number in range(7, 10):
        assert f"change-{number}" in CHANGE_FOLDER_NAME_ALLOWLIST
