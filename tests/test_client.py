import httpx
import pytest

from coder import CoderError, OpenAICompatibleClient


def test_chat_posts_openai_shape_without_network() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers["authorization"]
        seen["json"] = request.read()
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"role": "assistant", "content": "Use a local test."}}
                ]
            },
            request=request,
        )

    transport = httpx.MockTransport(handler)
    with OpenAICompatibleClient(
        base_url="http://ollama.test",
        model="qwen2.5-coder",
        transport=transport,
    ) as client:
        answer = client.chat([{"role": "user", "content": "hello"}], temperature=0.2)

    assert answer == "Use a local test."
    assert seen["url"] == "http://ollama.test/v1/chat/completions"
    assert seen["authorization"] == "Bearer ollama"
    assert b'"model":"qwen2.5-coder"' in seen["json"]  # type: ignore[operator]
    assert b'"stream":false' in seen["json"]  # type: ignore[operator]


def test_http_error_is_wrapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="Ollama is not running", request=request)

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CoderError, match="Ollama is not running"):
            client.chat([{"role": "user", "content": "hello"}])

