"""HTTP client for local OpenAI-compatible model servers.

Ollama exposes the OpenAI chat-completions shape under ``/v1``.  Keeping the
client small and transport-injectable makes local development straightforward
and keeps tests completely offline.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from typing import Any

import httpx

DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "llama3.2"


class CoderError(RuntimeError):
    """Raised when the local model cannot produce a valid completion."""


def _normalise_base_url(base_url: str) -> str:
    """Return a versioned API root suitable for an OpenAI-compatible server."""

    value = base_url.rstrip("/")
    if not value.endswith("/v1"):
        value += "/v1"
    return value


def _content_from_message(message: Mapping[str, Any]) -> str:
    content = message.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, Sequence) and not isinstance(content, (bytes, bytearray)):
        parts: list[str] = []
        for part in content:
            if isinstance(part, Mapping) and isinstance(part.get("text"), str):
                parts.append(part["text"])
        return "".join(parts)
    raise CoderError("completion message content is not text")


class OpenAICompatibleClient:
    """Minimal OpenAI chat-completions client.

    ``transport`` is intentionally exposed for tests and local adapters.  A
    caller can pass ``httpx.MockTransport`` without any DNS or network access.
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout: float = 60.0,
        transport: httpx.BaseTransport | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        if http_client is not None and transport is not None:
            raise ValueError("pass either http_client or transport, not both")
        if http_client is not None and base_url is not None:
            # The injected client owns its base URL.  Accepting another one
            # would make requests surprisingly target the wrong server.
            raise ValueError("base_url cannot be used with an injected http_client")

        configured_url = base_url or os.getenv("OLLAMA_BASE_URL", DEFAULT_BASE_URL)
        self.base_url = _normalise_base_url(configured_url)
        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        self._owns_client = http_client is None

        if http_client is not None:
            self._client = http_client
        else:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {api_key or os.getenv('OLLAMA_API_KEY', 'ollama')}",
                    "Content-Type": "application/json",
                },
                timeout=timeout,
                transport=transport,
            )

    def chat(
        self,
        messages: Sequence[Mapping[str, Any]],
        *,
        model: str | None = None,
        temperature: float | None = None,
        **options: Any,
    ) -> str:
        """Send messages to ``/chat/completions`` and return assistant text."""

        payload: dict[str, Any] = {
            "model": model or self.model,
            "messages": [dict(message) for message in messages],
            "stream": False,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        payload.update(options)

        try:
            response = self._client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as exc:
            detail = getattr(exc, "response", None)
            suffix = f": {detail.text}" if detail is not None else ""
            raise CoderError(f"local model request failed{suffix}") from exc
        except ValueError as exc:
            raise CoderError("local model returned invalid JSON") from exc

        try:
            choice = data["choices"][0]
            message = choice["message"]
            if not isinstance(message, Mapping):
                raise TypeError
            return _content_from_message(message)
        except (KeyError, IndexError, TypeError) as exc:
            raise CoderError("local model response did not contain choices[0].message.content") from exc

    # Familiar spelling for callers migrating from the OpenAI SDK.
    chat_completion = chat

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "OpenAICompatibleClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


OllamaClient = OpenAICompatibleClient
