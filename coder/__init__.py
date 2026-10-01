"""Small local coding assistant package backed by an OpenAI-compatible API."""

from .client import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    CoderError,
    OllamaClient,
    OpenAICompatibleClient,
)
from .chat import Coder
from .memory import LettaMemoryHooks, MemoryHooks, NoOpMemoryHooks

__all__ = [
    "Coder",
    "CoderError",
    "DEFAULT_BASE_URL",
    "DEFAULT_MODEL",
    "LettaMemoryHooks",
    "MemoryHooks",
    "NoOpMemoryHooks",
    "OllamaClient",
    "OpenAICompatibleClient",
]
