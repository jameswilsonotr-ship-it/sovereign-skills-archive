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


def test_base_url_does_not_duplicate_v1() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "http://ollama.test/v1/chat/completions"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "ok"}}]},
            request=request,
        )

    with OpenAICompatibleClient(
        base_url="http://ollama.test/v1/",
        transport=httpx.MockTransport(handler),
    ) as client:
        assert client.chat([{"role": "user", "content": "hello"}]) == "ok"


def test_environment_configuration_is_used(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://configured.test/")
    monkeypatch.setenv("OLLAMA_MODEL", "configured-model")
    monkeypatch.setenv("OLLAMA_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "http://configured.test/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.read()
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "configured"}}]},
            request=request,
        )

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        assert client.base_url == "http://configured.test/v1"
        assert client.model == "configured-model"
        assert client.chat([{"role": "user", "content": "hello"}]) == "configured"


def test_explicit_api_key_and_options_are_serialized() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = request.read()
        assert b'"temperature":0.4' in payload
        assert b'"top_p":0.8' in payload
        assert request.headers["authorization"] == "Bearer explicit-key"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "options"}}]},
            request=request,
        )

    with OpenAICompatibleClient(
        api_key="explicit-key",
        transport=httpx.MockTransport(handler),
    ) as client:
        assert (
            client.chat(
                [{"role": "user", "content": "hello"}],
                temperature=0.4,
                top_p=0.8,
            )
            == "options"
        )


def test_multimodal_message_content_is_joined() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": [
                                {"type": "text", "text": "first"},
                                {"type": "image_url", "image_url": {}},
                                {"type": "text", "text": " second"},
                            ]
                        }
                    }
                ]
            },
            request=request,
        )

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        assert client.chat([{"role": "user", "content": "hello"}]) == "first second"


@pytest.mark.parametrize(
    ("response", "message"),
    [
        ({}, "choices[0].message.content"),
        ({"choices": []}, "choices[0].message.content"),
        ({"choices": [{}]}, "choices[0].message.content"),
        ({"choices": [{"message": {"content": 42}}]}, "content is not text"),
    ],
)
def test_malformed_completion_is_wrapped(
    response: object, message: str
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=response, request=request)

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CoderError, match=message):
            client.chat([{"role": "user", "content": "hello"}])


def test_invalid_json_is_wrapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="not-json", request=request)

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CoderError, match="invalid JSON"):
            client.chat([{"role": "user", "content": "hello"}])


def test_transport_failure_is_wrapped_without_network() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("simulated offline failure", request=request)

    with OpenAICompatibleClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(CoderError, match="local model request failed"):
            client.chat([{"role": "user", "content": "hello"}])


def test_injected_http_client_owns_its_base_url_and_is_not_closed() -> None:
    http_client = httpx.Client(
        base_url="http://injected.test/v1",
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                json={"choices": [{"message": {"content": "injected"}}]},
                request=request,
            )
        ),
    )
    client = OpenAICompatibleClient(http_client=http_client)

    assert client.chat_completion([{"role": "user", "content": "hello"}]) == "injected"
    client.close()
    assert not http_client.is_closed
    http_client.close()

