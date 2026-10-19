"""Conversation orchestration for the local coder."""

from __future__ import annotations

from typing import Any

from .client import OpenAICompatibleClient
from .memory import MemoryHooks, NoOpMemoryHooks


class Coder:
    """Maintain a short in-process conversation around a model client."""

    def __init__(
        self,
        client: OpenAICompatibleClient,
        *,
        system_prompt: str | None = None,
        memory: MemoryHooks | None = None,
    ) -> None:
        self.client = client
        self.system_prompt = system_prompt
        self.memory = memory or NoOpMemoryHooks()
        self._history: list[dict[str, Any]] = []

    @property
    def history(self) -> list[dict[str, Any]]:
        """Return a copy of the conversation history."""

        return [dict(message) for message in self._history]

    def send(self, prompt: str, **options: Any) -> str:
        if not prompt.strip():
            raise ValueError("prompt must not be empty")

        messages: list[dict[str, Any]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(self._history)
        messages.append({"role": "user", "content": prompt})
        prepared = self.memory.before_chat(messages)
        response = self.client.chat(prepared, **options)
        self._history.extend(
            [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response},
            ]
        )
        self.memory.after_chat(prepared, response)
        return response

    ask = send

    def reset(self) -> None:
        self._history.clear()

