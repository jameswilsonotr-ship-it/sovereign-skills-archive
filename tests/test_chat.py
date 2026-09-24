from typing import Any

import pytest

from coder import Coder, MemoryHooks


class RecordingClient:
    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    def chat(self, messages: list[dict[str, Any]], **_: Any) -> str:
        self.messages = messages
        return "local answer"


class RecordingMemory(MemoryHooks):
    def __init__(self) -> None:
        self.before_called = False
        self.after_response = None

    def before_chat(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.before_called = True
        return [{"role": "system", "content": "recalled fact"}, *messages]

    def after_chat(self, messages: list[dict[str, Any]], response: str) -> None:
        self.after_response = response


def test_coder_wires_memory_hooks_and_retains_history() -> None:
    client = RecordingClient()
    memory = RecordingMemory()
    coder = Coder(client, system_prompt="be concise", memory=memory)

    assert coder.send("What changed?") == "local answer"
    assert memory.before_called
    assert memory.after_response == "local answer"
    assert client.messages[0]["content"] == "recalled fact"
    assert coder.history == [
        {"role": "user", "content": "What changed?"},
        {"role": "assistant", "content": "local answer"},
    ]


def test_coder_sends_system_prompt_and_prior_turns() -> None:
    client = RecordingClient()
    coder = Coder(client, system_prompt="be concise")

    coder.send("first")
    coder.send("second")

    assert client.messages == [
        {"role": "system", "content": "be concise"},
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "local answer"},
        {"role": "user", "content": "second"},
    ]


def test_history_is_a_copy_and_reset_clears_it() -> None:
    client = RecordingClient()
    coder = Coder(client)
    coder.send("first")

    history = coder.history
    history[0]["content"] = "mutated outside coder"
    assert coder.history[0]["content"] == "first"

    coder.reset()
    assert coder.history == []


def test_blank_prompt_is_rejected_before_client_or_memory() -> None:
    client = RecordingClient()
    memory = RecordingMemory()
    coder = Coder(client, memory=memory)

    with pytest.raises(ValueError, match="must not be empty"):
        coder.send(" \t\n")

    assert client.messages == []
    assert not memory.before_called

