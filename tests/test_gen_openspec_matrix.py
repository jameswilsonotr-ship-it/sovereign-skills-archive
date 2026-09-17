import csv
import io
import tempfile
import unittest
from pathlib import Path

from scripts.gen_openspec_matrix import (
    MATRIX_COLUMNS,
    collect_records,
    parse_document,
    parse_front_matter,
    render_csv,
    render_markdown,
)


class FrontMatterTests(unittest.TestCase):
    def test_parses_scalars_inline_lists_and_block_lists(self):
        metadata = parse_front_matter(
            """---
        id: example
        title: "An example"
        tags: [one, "two"]
        owners:
          - platform
          - api
        ---
        # Example
        """
        )

        self.assertEqual(metadata["id"], "example")
        self.assertEqual(metadata["title"], "An example")
        self.assertEqual(metadata["tags"], ["one", "two"])
        self.assertEqual(metadata["owners"], ["platform", "api"])

    def test_non_front_matter_document_returns_empty_metadata(self):
        self.assertEqual(parse_front_matter("# Plain Markdown\n"), {})


class DocumentParserTests(unittest.TestCase):
    def test_extracts_metadata_sections_and_checklist_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "limits.md"
            path.write_text(
                """---
id: limits
status: draft
owner: platform
tags:
  - api
  - reliability
---
# Limits

## Summary
Keep clients within predictable limits.

## Requirements
- One
- Two

## Verification
- [x] First
- [ ] Second
""",
                encoding="utf-8",
            )

            record = parse_document(path, source="docs/openspec/limits.md")

        self.assertEqual(record.id, "limits")
        self.assertEqual(record.title, "Limits")
        self.assertEqual(record.status, "draft")
        self.assertEqual(record.owner, "platform")
        self.assertEqual(record.tags, "api; reliability")
        self.assertEqual(record.summary, "Keep clients within predictable limits.")
        self.assertEqual(record.requirements, 2)
        self.assertEqual(record.acceptance, 2)
        self.assertEqual(record.checklist_total, 2)
        self.assertEqual(record.checklist_done, 1)
        self.assertEqual(record.source, "docs/openspec/limits.md")

    def test_falls_back_to_filename_and_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new-feature.md"
            path.write_text("A short description.\n", encoding="utf-8")
            record = parse_document(path)

        self.assertEqual(record.id, "new-feature")
        self.assertEqual(record.title, "New Feature")
        self.assertEqual(record.status, "unspecified")
        self.assertEqual(record.owner, "unassigned")
        self.assertEqual(record.summary, "A short description.")


class MatrixRenderingTests(unittest.TestCase):
    def test_csv_has_stable_columns_and_escaping(self):
        record = parse_document(
            _write_temp_document(
                """---
id: csv
title: CSV | title
---
"""
            ),
            source="csv.md",
        )
        rows = list(csv.DictReader(io.StringIO(render_csv([record]))))

        self.assertEqual(rows[0]["title"], "CSV | title")
        self.assertEqual(list(rows[0]), list(MATRIX_COLUMNS))

    def test_markdown_escapes_pipes(self):
        record = parse_document(
            _write_temp_document(
                """---
id: markdown
summary: value | with a pipe
---
"""
            )
        )

        self.assertIn("value \\| with a pipe", render_markdown([record]))

    def test_collect_records_is_sorted_by_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "z.md").write_text("---\nid: z\n---\n", encoding="utf-8")
            (root / "a.md").write_text("---\nid: a\n---\n", encoding="utf-8")

            records = collect_records(root, root=root)

        self.assertEqual([record.id for record in records], ["a", "z"])


def _write_temp_document(text: str) -> Path:
    temporary_directory = tempfile.TemporaryDirectory()
    path = Path(temporary_directory.name) / "document.md"
    path.write_text(text, encoding="utf-8")
    # Keep the directory alive for the duration of the test process. The
    # parser only needs a tiny temporary file and unittest has no fixture
    # dependency requirement.
    _TEMPORARY_DIRECTORIES.append(temporary_directory)
    return path


_TEMPORARY_DIRECTORIES = []


if __name__ == "__main__":
    unittest.main()
