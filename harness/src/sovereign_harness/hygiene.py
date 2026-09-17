"""Repository safety checks for the KEEP lake surface."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pathspec import PathSpec


KEEP_ROOT = Path("skill_tree/skills/keep-lake-query")
KEEP_MARKERS = (
    "Do not slurp KEEP",
    "Drive root is always no",
    "Copy, do not overwrite",
    "Do not mint a fifth mouth",
    "Folder path is the date",
)
SKILL_PATHSPEC = PathSpec.from_lines("gitwildmatch", ["skill_tree/**/SKILL.md"])


@dataclass(frozen=True)
class GateReport:
    """A small machine- and human-readable gate result."""

    issues: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.issues


def _changed_paths(repo_root: Path, base_ref: str) -> set[str]:
    """Collect committed and uncommitted paths without modifying the checkout."""

    paths: set[str] = set()
    commands = [
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
    ]
    for command in commands:
        result = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            paths.update(line for line in result.stdout.splitlines() if line)
    return paths


def check_keep_lake_query(repo_root: Path, base_ref: str = "origin/skill-tree-intake") -> GateReport:
    """Validate KEEP's safety contract and reject live skill edits."""

    issues: list[str] = []
    keep_root = repo_root / KEEP_ROOT
    skill_path = keep_root / "SKILL.md"
    help_path = keep_root / "HELP.md"

    if not skill_path.is_file():
        issues.append(f"missing {KEEP_ROOT / 'SKILL.md'}")
    else:
        content = skill_path.read_text(encoding="utf-8")
        for marker in KEEP_MARKERS:
            if marker.casefold() not in content.casefold():
                issues.append(f"KEEP marker missing: {marker}")

    if not help_path.is_file():
        issues.append(f"missing {KEEP_ROOT / 'HELP.md'}")

    changed_skill_paths = sorted(
        path for path in _changed_paths(repo_root, base_ref) if SKILL_PATHSPEC.match_file(path)
    )
    if changed_skill_paths:
        issues.append("live SKILL.md writes are locked: " + ", ".join(changed_skill_paths))

    return GateReport(tuple(issues))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", default="origin/skill-tree-intake")
    args = parser.parse_args()

    report = check_keep_lake_query(args.repo_root.resolve(), args.base_ref)
    if report.passed:
        print("keep-lake-query hygiene: PASS")
        return 0

    print("keep-lake-query hygiene: FAIL")
    for issue in report.issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
