# sovereign-skills-archive

Receipt + index repo for the daily skill-library vacuum.

- Payload bytes: Google Drive parent `1Lw83CBcRcouf1nQYQtrVHtQjZhoeysE0`
- Receipts / manifests / inventory: `snapshots/YYYY-MM-DD/`
- Policy: `MASTER-INDEX.md`
- Claim: Liv HUB

## Local coder

The root `coder/` package is a small, local-first coding assistant client for
Ollama's OpenAI-compatible API. It does not call a hosted model by default.

```bash
python3 -m pip install -e '.[test]'
ollama serve
ollama pull llama3.2
python3 -m coder chat
```

Use `--model`, `--base-url`, or `--system` to override the defaults. The
client defaults to `http://localhost:11434/v1`; `OLLAMA_BASE_URL` and
`OLLAMA_MODEL` are also supported. See `docs/grok-cli.md` for optional Grok
CLI notes.

Do not expect the 132M full tarball in git. Point at Drive file IDs instead.

## Coder architecture

The CLI is a deliberately small three-layer path:

```text
python -m coder
  -> cli.main
  -> Coder (history + memory hooks)
  -> OpenAICompatibleClient
  -> Ollama /v1/chat/completions
```

`coder/client.py` owns URL normalization, request serialization, response
validation, and `CoderError` conversion. `coder/chat.py` owns conversation
state. `coder/memory.py` provides no-op hooks and a future integration seam;
it does not import or contact Letta. The HTTP transport is injectable, so the
test suite uses `httpx.MockTransport` and never opens a socket. See
[the architecture notes](docs/coder-architecture.md) for the boundary and
test map.

## Local Docker Compose

`docker-compose.yml` is an optional local wrapper around the same two
components:

```bash
docker compose up --build
# In another terminal, download the model into the named volume:
docker compose exec ollama ollama pull llama3.2
```

The Ollama model is downloaded into the named `ollama` volume. The `coder`
container talks to the service name `ollama`, not `localhost`. Set
`OLLAMA_MODEL` before `docker compose up` to use another model. The compose
setup is for local development; it is not used by the offline tests.

## Specification tracking

There is currently no `SPEC-001` or OpenSpec artifact in this checkout.
[docs/openspec-mapping.md](docs/openspec-mapping.md) records that absence and
the evidence inventory to reconcile when the canonical specification is
available. It intentionally does not invent a normative mapping.
