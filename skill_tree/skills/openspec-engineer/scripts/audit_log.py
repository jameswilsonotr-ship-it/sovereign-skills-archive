"""Secret-redacting JSONL audit-log stub for local OpenSpec tooling."""
from __future__ import annotations

import json
import re
import sys
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

_SENSITIVE_KEY = re.compile(
    r"(?:password|passwd|secret|token|api[_-]?key|private[_-]?key|"
    r"authorization|cookie|credential)",
    re.IGNORECASE,
)
_SECRET_VALUE = re.compile(
    r"(?ix)"
    r"(?:"
    r"bearer\s+[a-z0-9._~+/=-]+"
    r"|(?:ghp_|github_pat_|sk-|xox[baprs]-)[a-z0-9._~+/=-]+"
    r"|-----begin [^-]+-----.*?-----end [^-]+-----"
    r")"
)
_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|secret|token|api[_-]?key|authorization|cookie)"
    r"(\s*[:=]\s*)([^\s,;]+)"
)


def redact(value: Any, *, key: str | None = None) -> Any:
    """Return JSON-safe data with likely credential values replaced."""
    if key and _SENSITIVE_KEY.search(key):
        return "[REDACTED]"
    if isinstance(value, Mapping):
        return {str(item_key): redact(item_value, key=str(item_key))
                for item_key, item_value in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        redacted = _SECRET_VALUE.sub("[REDACTED]", value)
        return _ASSIGNMENT.sub(r"\1\2[REDACTED]", redacted)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return str(value)


class AuditLogger:
    """Append JSONL events to a path or stream without leaking credentials."""

    def __init__(self, destination: str | Path | TextIO | None = None) -> None:
        self.destination = destination
        self._owned_stream: TextIO | None = None

    def record(self, event: str, *, status: str = "info", **fields: Any) -> dict[str, Any]:
        """Create and optionally persist one redacted audit event."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "status": status,
            **{key: redact(value, key=key) for key, value in fields.items()},
        }
        if self.destination is not None:
            stream = self._stream()
            stream.write(json.dumps(record, sort_keys=True) + "\n")
            stream.flush()
        return record

    def close(self) -> None:
        if self._owned_stream is not None:
            self._owned_stream.close()
            self._owned_stream = None

    def _stream(self) -> TextIO:
        if hasattr(self.destination, "write"):
            return self.destination  # type: ignore[return-value]
        if self.destination == "-":
            return sys.stderr
        if self._owned_stream is None:
            path = Path(self.destination)  # type: ignore[arg-type]
            path.parent.mkdir(parents=True, exist_ok=True)
            self._owned_stream = path.open("a", encoding="utf-8")
        return self._owned_stream

    def __enter__(self) -> "AuditLogger":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
