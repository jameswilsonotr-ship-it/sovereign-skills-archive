from __future__ import annotations

from typing import Any

import pytest

from coder import cli


class FakeClient:
    instances: list["FakeClient"] = []

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.prompts: list[tuple[str, dict[str, Any]]] = []
        self.__class__.instances.append(self)

    def __enter__(self) -> "FakeClient":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def chat(self, messages: Any, **options: Any) -> str:
        self.prompts.append((messages[-1]["content"], options))
        return f"answer for {messages[-1]['content']}"


@pytest.fixture(autouse=True)
def clear_fake_clients() -> None:
    FakeClient.instances.clear()


def test_one_shot_chat_passes_cli_configuration(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "OpenAICompatibleClient", FakeClient)

    assert (
        cli.main(
            [
                "chat",
                "review this",
                "--model",
                "qwen2.5-coder",
                "--base-url",
                "http://ollama.test",
                "--system",
                "be precise",
                "--temperature",
                "0.2",
            ]
        )
        == 0
    )

    client = FakeClient.instances[0]
    assert client.kwargs == {
        "base_url": "http://ollama.test",
        "model": "qwen2.5-coder",
    }
    assert client.prompts == [
        ("review this", {"temperature": 0.2}),
    ]
    assert capsys.readouterr().out == "answer for review this\n"


def test_prompt_option_is_supported(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(cli, "OpenAICompatibleClient", FakeClient)

    assert cli.main(["chat", "--prompt", "from option"]) == 0

    assert FakeClient.instances[0].prompts[0][0] == "from option"
    assert capsys.readouterr().out == "answer for from option\n"


def test_interactive_chat_skips_blank_lines_and_stops_at_exit(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(cli, "OpenAICompatibleClient", FakeClient)
    inputs = iter(["", "first", "/quit"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))

    assert cli.main(["chat"]) == 0

    assert FakeClient.instances[0].prompts == [("first", {"temperature": None})]
    captured = capsys.readouterr()
    assert "Local coder chat." in captured.err
    assert "coder> answer for first" in captured.out
