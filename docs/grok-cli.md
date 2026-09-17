# Grok CLI install notes

The local `coder` package does not require, install, or invoke a Grok CLI.
Its runtime path is Ollama on `localhost`, so `pytest` stays offline and does
not need an xAI account or API key.

If you also use a Grok CLI:

1. Install the CLI from the current official xAI distribution instructions
   for your platform. The package name and supported install method are
   subject to change; do not add an unverified `grok-cli` package to this
   repository's dependencies.
2. Verify the executable before using it:

   ```bash
   command -v grok
   grok --version
   ```

3. Configure credentials using the CLI's documented environment-variable or
   login flow. Keep any xAI key outside the repository (for example in a
   local shell profile or an ignored `.env` file).
4. Keep Grok CLI setup separate from the local coder setup. A working local
   coder only needs:

   ```bash
   ollama serve
   python3 -m coder chat --model llama3.2
   ```

CI should not install or call Grok. The tests use `httpx.MockTransport`, so
they exercise request and response handling without DNS, Ollama, xAI, or any
other network access.
