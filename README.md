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
