from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


def _load_matrix_generator():
    script = Path(__file__).parents[2] / "scripts" / "gen_openspec_matrix.py"
    spec = importlib.util.spec_from_file_location("gen_openspec_matrix", script)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_change_id_collision_guard_rejects_case_only_duplicates(tmp_path: Path) -> None:
    generator = _load_matrix_generator()
    (tmp_path / "first.md").write_text(
        "---\nid: T4-08-continuous-included-reload\n---\n# First\n",
        encoding="utf-8",
    )
    (tmp_path / "second.md").write_text(
        "---\nid: t4-08-continuous-included-reload\n---\n# Second\n",
        encoding="utf-8",
    )

    with pytest.raises(generator.ChangeIdCollisionError, match="T4-08"):
        generator.collect_records(tmp_path, root=tmp_path)


def test_change_id_collision_guard_allows_distinct_ids(tmp_path: Path) -> None:
    generator = _load_matrix_generator()
    (tmp_path / "first.md").write_text("# t4-08-continuous-included-reload\n", encoding="utf-8")
    (tmp_path / "second.md").write_text("# t4-09-next-lane\n", encoding="utf-8")

    records = generator.collect_records(tmp_path, root=tmp_path)

    assert [record.id for record in records] == [
        "t4-08-continuous-included-reload",
        "t4-09-next-lane",
    ]
