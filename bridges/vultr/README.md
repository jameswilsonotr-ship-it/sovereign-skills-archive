# Vultr inference bridge templates

These files are dry-run scaffolds for a Tailscale-joined, headless inference
VPS. They do not call the Vultr API, create/destroy an instance, enroll a
tailnet node, download a model, or contain secrets.

## Files

- [`cloud-init.yaml`](cloud-init.yaml): host bootstrap template for Docker,
  Tailscale, firewall rules, and Compose.
- [`docker-compose.yml`](docker-compose.yml): OpenAI-compatible vLLM service
  template with a model placeholder.
- [`.env.example`](.env.example): names and placeholders only; copy into a
  secret-managed deployment directory, never into Git as `.env`.

## Dry-run sequence

1. Pick a Vultr GPU or CPU plan and estimate compute, storage, egress, and
   model-cache cost against the `$250` credit.
2. Create a short-lived Tailscale auth key and store it outside the repo.
3. Supply a secret-managed `TS_AUTHKEY`; keep `VULTR_API_KEY` in the
   provisioning operator only. The running VPS does not need the Vultr API
   key.
4. Render the cloud-init template and inspect it. Do not paste a real key into
   this repository or a ticket.
5. Provision only after an explicit MIS-7/operator approval.
6. Verify the host is reachable on the tailnet and that port `8000` is not
   reachable from the public interface.

The default command assumes a GPU-capable vLLM image. For a CPU plan, select a
tested Ollama or `llama.cpp` server image and update the command, memory
limits, model, and health check as one reviewed change. Do not use `latest` in
a production deployment record; pin an image digest there.

## Runtime boundary

The service is OpenAI-compatible at `/v1`, but this is not a Gemini credential
proxy. Spark/Vesper requests belong to the explicit Gemini API path described
in [`../../docs/SPARK_GEMINI.md`](../../docs/SPARK_GEMINI.md). Tailscale is
the only intended network path to this bridge.
