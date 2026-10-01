"""Memory extension points.

The default implementation deliberately does nothing.  These hooks provide a
stable seam for a future Letta integration without making Letta a runtime or
test dependency today.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

Message = Mapping[str, Any]


class MemoryHooks:
    """No-op lifecycle hooks for memory-aware chat implementations.

    Override ``before_chat`` to add recalled context and ``after_chat`` to
    persist a completed turn.  ``recall`` and ``remember`` are convenience
    stubs for integrations that prefer explicit memory operations.
    """

    def before_chat(self, messages: Sequence[Message]) -> list[dict[str, Any]]:
        return [dict(message) for message in messages]

    def after_chat(self, messages: Sequence[Message], response: str) -> None:
        return None

    def recall(self, query: str) -> list[dict[str, Any]]:
        return []

    def remember(self, content: str, *, metadata: Mapping[str, Any] | None = None) -> None:
        return None


class NoOpMemoryHooks(MemoryHooks):
    """Explicit name for the local default memory behavior."""


class LettaMemoryHooks(MemoryHooks):
    """Placeholder for a future Letta-backed implementation.

    No Letta import or network call happens here.  Subclass this type and
    implement the four methods when a Letta server and agent identity are
    available.
    """

