"""Keep OpenSpec documentation independent from local skill-file paths."""

from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
OPENSPEC_DOCS = REPO_ROOT / "docs" / "openspec"
SKILL_PATH = re.compile(
    r"""(?ix)
    (?<![\w.-])
    [^\s<>"'`()\[\],;:]*skill\.md
    (?=$|[\s<>"'`()\[\],;:])
    """
)


def test_openspec_docs_do_not_reference_skill_paths() -> None:
    """OpenSpec docs must not depend on machine- or skill-tree-specific paths."""
    violations: list[str] = []

    if OPENSPEC_DOCS.is_dir():
        for path in sorted(OPENSPEC_DOCS.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue

            relative_path = path.relative_to(REPO_ROOT)
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                for match in SKILL_PATH.finditer(line):
                    violations.append(
                        f"{relative_path}:{line_number}: {match.group(0)!r}"
                    )

    assert not violations, (
        "docs/openspec must not reference SKILL.md paths:\n"
        + "\n".join(violations)
    )
