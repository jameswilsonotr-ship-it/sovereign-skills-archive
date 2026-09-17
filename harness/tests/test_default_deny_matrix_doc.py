"""Offline regression check for the optional default-deny matrix document."""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DENY_MATRIX = REPOSITORY_ROOT / "DEFAULT_DENY_MATRIX.md"


def test_default_deny_matrix_exists_when_present() -> None:
    """A checked-in deny matrix must be a file when this checkout includes it."""
    if DEFAULT_DENY_MATRIX.exists():
        assert DEFAULT_DENY_MATRIX.is_file()
