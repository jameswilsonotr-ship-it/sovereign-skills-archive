# Local coder architecture

The `coder/` package is intentionally a thin local client. It has three
runtime layers:

```text
python -m coder
       │
       ▼
  cli.main ─────────────── parses one-shot or interactive chat options
       │
       ▼
  Coder.send ───────────── owns conversation history and memory hooks
       │
       ├── MemoryHooks.before_chat / after_chat
       │
       ▼
  OpenAICompatibleClient ─ posts one non-streaming request
       │
       ▼
  Ollama /v1/chat/completions on localhost
```

## Boundaries

- `coder/cli.py` is the process boundary. It selects the model, API root,
  system prompt, and temperature, then prints the result.
- `coder/chat.py` is orchestration only. It validates prompts, prepends the
  optional system message, retains user/assistant turns, and delegates memory
  lifecycle hooks.
- `coder/client.py` owns HTTP details. It normalizes the API root to `/v1`,
  sends the OpenAI-compatible payload with `stream: false`, extracts
  `choices[0].message.content`, and converts transport/protocol failures to
  `CoderError`.
- `coder/memory.py` is an offline extension seam. The default hooks are no-op;
  `LettaMemoryHooks` is only a placeholder and imports no Letta client.

The client accepts either an `httpx` transport or an injected `httpx.Client`.
That seam is the reason the test suite can exercise request construction,
response parsing, failures, and CLI orchestration without DNS, Ollama, model
downloads, or hosted APIs.

## Configuration

| Input | Default | Used by |
| --- | --- | --- |
| `--base-url` / `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | HTTP client |
| `--model` / `OLLAMA_MODEL` | `llama3.2` | request payload |
| `OLLAMA_API_KEY` | `ollama` | bearer header |
| `--system` | unset | conversation history |

The API key is retained for compatibility with OpenAI-shaped local servers.
Ollama itself does not require a real credential for the default local setup.

## Test map

- `tests/test_client.py`: URL and environment configuration, request options,
  content extraction, malformed responses, invalid JSON, and simulated
  transport failures.
- `tests/test_chat.py`: memory lifecycle, system/history ordering, defensive
  history copies, reset, and prompt validation.
- `tests/test_cli.py`: one-shot, `--prompt`, and interactive command handling
  using a fake client.

No test opens a socket. A test that needs an HTTP response uses
`httpx.MockTransport`.

