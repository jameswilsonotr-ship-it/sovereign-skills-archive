#!/usr/bin/env python3
"""Generate CSV and Markdown matrices from ``docs/openspec/*.md``.

The parser intentionally uses only the Python standard library.  Each Markdown
file produces one row with the following fields:

``id, title, status, owner, priority, summary, tags, dependencies,
requirements, acceptance, checklist_total, checklist_done, source``

Metadata is read from an optional YAML-like front matter block.  For the
fields commonly used in a spec, a matching second-level heading is accepted as
a fallback.  This makes the format useful for both front-matter-first and
human-written Markdown documents without requiring PyYAML.
"""

from __future__ import annotations

import argparse
import ast
import csv
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


MATRIX_COLUMNS = (
    "id",
    "title",
    "status",
    "owner",
    "priority",
    "summary",
    "tags",
    "dependencies",
    "requirements",
    "acceptance",
    "checklist_total",
    "checklist_done",
    "source",
)

_KEY_ALIASES = {
    "spec_id": "id",
    "identifier": "id",
    "description": "summary",
    "depends_on": "dependencies",
    "depends-on": "dependencies",
}
_CHECKBOX_RE = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+", re.MULTILINE)
_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*#*\s*$", re.MULTILINE)
_LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class SpecRecord:
    """Normalized data extracted from one OpenSpec document."""

    id: str
    title: str
    status: str
    owner: str
    priority: str
    summary: str
    tags: str
    dependencies: str
    requirements: int
    acceptance: int
    checklist_total: int
    checklist_done: int
    source: str

    def as_row(self) -> dict[str, object]:
        return {column: getattr(self, column) for column in MATRIX_COLUMNS}


def _normalize_key(key: str) -> str:
    normalized = re.sub(r"[\s-]+", "_", key.strip().lower())
    return _KEY_ALIASES.get(normalized, normalized)


def _split_inline_list(value: str) -> list[str]:
    """Split a simple ``[one, "two"]`` value without a YAML dependency."""

    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        parsed = None
    if isinstance(parsed, (list, tuple)):
        return [str(item).strip() for item in parsed if str(item).strip()]

    return [
        item.strip().strip("\"'")
        for item in re.split(r"\s*,\s*", inner)
        if item.strip()
    ]


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        return _split_inline_list(value)
    if value[:1] in {"'", '"'} and value[-1:] == value[:1]:
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if value.lower() in {"null", "none", "~"}:
        return ""
    return value


def parse_front_matter(text: str) -> dict[str, object]:
    """Parse the small front-matter subset needed by the matrix.

    Supported values are scalars, inline lists, and lists written as indented
    ``- item`` lines. Unknown keys are retained, so callers can extend the
    parser without changing the file format.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if end is None:
        return {}

    result: dict[str, object] = {}
    current_key: str | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s*-\s+(.*)$", line)
        if list_match and current_key:
            existing = result.setdefault(current_key, [])
            if not isinstance(existing, list):
                existing = [] if existing == "" else [str(existing)]
                result[current_key] = existing
            existing.append(str(_parse_scalar(list_match.group(1))))
            continue

        key_match = re.match(r"^([A-Za-z0-9_. -]+):\s*(.*)$", line)
        if not key_match:
            continue
        current_key = _normalize_key(key_match.group(1))
        result[current_key] = _parse_scalar(key_match.group(2))
    return result


def _as_text(value: object) -> str:
    if isinstance(value, (list, tuple)):
        return "; ".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip() if value is not None else ""


def _headings(text: str) -> list[tuple[int, str, str]]:
    matches = list(_HEADING_RE.finditer(text))
    sections: list[tuple[int, str, str]] = []
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((len(match.group(1)), match.group(2).strip(), text[body_start:body_end].strip()))
    return sections


def _section_body(sections: Sequence[tuple[int, str, str]], *names: str) -> str:
    normalized_names = {name.casefold() for name in names}
    normalized_names.update(f"{name}s" for name in tuple(normalized_names))
    for level, heading, body in sections:
        if level >= 2 and heading.casefold() in normalized_names:
            return body
    return ""


def _section_value(sections: Sequence[tuple[int, str, str]], *names: str) -> str:
    for name in names:
        body = _section_body(sections, name)
        if body:
            first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
            return re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", first_line).strip()
    return ""


def _first_paragraph(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("#") or stripped.startswith("---"):
            continue
        if re.match(r"^(?:[-*+]|\d+[.)])\s+", stripped):
            if lines:
                break
            continue
        lines.append(stripped)
    return " ".join(lines)


def _count_list_items(body: str) -> int:
    return len(_LIST_ITEM_RE.findall(body))


def _metadata_value(metadata: Mapping[str, object], sections: Sequence[tuple[int, str, str]], *keys: str) -> str:
    for key in keys:
        normalized = _normalize_key(key)
        if normalized in metadata:
            value = _as_text(metadata[normalized])
            if value:
                return value
    return _section_value(sections, *keys)


def parse_document(path: Path, source: str | None = None) -> SpecRecord:
    """Parse one Markdown OpenSpec document into a normalized record."""

    text = path.read_text(encoding="utf-8")
    metadata = parse_front_matter(text)
    sections = _headings(text)
    h1_title = next((heading for level, heading, _ in sections if level == 1), "")
    title = _metadata_value(metadata, sections, "title") or h1_title or path.stem.replace("_", " ").replace("-", " ").title()
    identifier = _metadata_value(metadata, sections, "id") or path.stem
    summary = _metadata_value(metadata, sections, "summary") or _section_value(sections, "summary") or _first_paragraph(text)

    requirements_body = _section_body(sections, "requirement")
    acceptance_body = _section_body(sections, "acceptance", "verification", "test")
    checklist = _CHECKBOX_RE.findall(text)
    done = sum(mark.lower() == "x" for mark in checklist)

    return SpecRecord(
        id=identifier,
        title=title,
        status=_metadata_value(metadata, sections, "status") or "unspecified",
        owner=_metadata_value(metadata, sections, "owner") or "unassigned",
        priority=_metadata_value(metadata, sections, "priority") or "unspecified",
        summary=summary,
        tags=_metadata_value(metadata, sections, "tags", "tag"),
        dependencies=_metadata_value(metadata, sections, "dependencies", "dependency"),
        requirements=_count_list_items(requirements_body),
        acceptance=_count_list_items(acceptance_body),
        checklist_total=len(checklist),
        checklist_done=done,
        source=source or path.as_posix(),
    )


def collect_documents(input_dir: Path) -> list[Path]:
    """Return the non-hidden Markdown files directly under ``input_dir``."""

    return sorted(
        (path for path in input_dir.glob("*.md") if not path.name.startswith(".")),
        key=lambda path: path.name.casefold(),
    )


def collect_records(input_dir: Path, root: Path | None = None) -> list[SpecRecord]:
    root = root or Path.cwd()
    records = []
    for path in collect_documents(input_dir):
        try:
            source = path.relative_to(root).as_posix()
        except ValueError:
            source = path.as_posix()
        records.append(parse_document(path, source=source))
    return sorted(records, key=lambda record: (record.id.casefold(), record.source.casefold()))


def render_csv(records: Iterable[SpecRecord]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=MATRIX_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(record.as_row())
    return output.getvalue()


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", " ").strip()


def render_markdown(records: Iterable[SpecRecord]) -> str:
    records = list(records)
    lines = [
        "# OpenSpec matrix",
        "",
        "Generated from `docs/openspec/*.md` by `scripts/gen_openspec_matrix.py`.",
        "",
        "| " + " | ".join(MATRIX_COLUMNS) + " |",
        "| " + " | ".join("---" for _ in MATRIX_COLUMNS) + " |",
    ]
    for record in records:
        lines.append("| " + " | ".join(_markdown_cell(record.as_row()[column]) for column in MATRIX_COLUMNS) + " |")
    return "\n".join(lines) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("docs/openspec"))
    parser.add_argument("--csv", dest="csv_output", type=Path, default=Path("docs/openspec-matrix.csv"))
    parser.add_argument("--md", "--markdown", dest="markdown_output", type=Path, default=Path("docs/openspec-matrix.md"))
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate existing outputs instead of writing them",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    records = collect_records(args.input_dir)
    csv_text = render_csv(records)
    markdown_text = render_markdown(records)

    if args.check:
        mismatches = []
        for output_path, expected in (
            (args.csv_output, csv_text),
            (args.markdown_output, markdown_text),
        ):
            actual = output_path.read_text(encoding="utf-8") if output_path.exists() else None
            if actual != expected:
                mismatches.append(str(output_path))
        if mismatches:
            print("Generated output is stale: " + ", ".join(mismatches), file=sys.stderr)
            return 1
        return 0

    args.csv_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.csv_output.write_text(csv_text, encoding="utf-8")
    args.markdown_output.write_text(markdown_text, encoding="utf-8")
    print(f"Wrote {len(records)} records to {args.csv_output} and {args.markdown_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
