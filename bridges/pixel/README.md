# Pixel Gemma bridge

This bridge is a **local-first node**, not a replacement for a phone app or a
cloud model. The first supported target is the Pixel 8a; the Pixel 9a is the
next practical target, and the Pixel 11 Pro entry is deliberately provisional
until Google publishes its hardware and runtime support.

## Read-aloud summary

- **8a:** 8 GB RAM. Start with Gemma 3 1B or Gemma 3n E2B, 4-bit.
- **9a:** 8 GB RAM. Use the same baseline; a 4B 4-bit model is an experiment,
  not the default service.
- **11 Pro (soon):** do not size a deployment from rumors. Record actual RAM,
  storage, thermals, and supported accelerator APIs after launch.
- Termux is the control plane. An Android app is the better home for a
  long-running LiteRT/MediaPipe inference process.
- A phone Gemma answer can defer to Vultr over the Tailscale mesh, then to
  **Gemini/Spark (Vesper)**. The phone should not need a direct Gemini key.

## Model size versus phone RAM

The figures below are planning ranges, not promises. They include approximate
weights for a quantized artifact but **not** the full Android process, KV cache,
allocator overhead, or the model's maximum context. Leave several GB free for
Android and other apps.

| Model choice | Rough Q4/Q5 weight footprint | Pixel 8a / 9a | Guidance |
| --- | ---: | --- | --- |
| Gemma 2 2B | ~1.5–2.0 GB | Good baseline | Text-first, short context |
| Gemma 3 1B | ~0.7–1.2 GB | Recommended | Lowest heat and fastest recovery |
| Gemma 3n E2B | mobile-optimized; artifact varies | Recommended if the chosen runtime supports it | Check the model card and runtime build |
| Gemma 3 4B | ~2.5–3.5 GB | Conditional | 4-bit, short context, foreground use |
| Gemma 3 12B | ~7–9 GB before generous runtime headroom | Not a target | It competes with Android for the whole 8 GB |
| Gemma 2/3 27B | far beyond phone-class RAM | No | Route to Vultr or Gemini |

The Pixel 8a and Pixel 9a are treated here as 8 GB devices. A future Pixel 11
Pro may make a larger model plausible, but the decision must use the retail
RAM SKU and a measured cold-start/thermal test. Even with 12 or 16 GB, a
larger model is not automatically a good always-on service: memory pressure,
context length, and sustained heat still dominate.

For every candidate, measure:

1. cold start time and peak RSS;
2. tokens/second at the intended context length;
3. ten minutes of representative traffic while unplugged; and
4. whether Android kills the process after screen-off or backgrounding.

## Choose the runtime

### Android app: preferred inference path

Use an Android app when the phone is meant to run Gemma continuously or use
the device accelerator:

- **LiteRT** (the current TensorFlow Lite family) is the low-level on-device
  runtime. Use the exact Gemma model format and delegate supported by the
  model documentation.
- **MediaPipe LLM Inference** provides a higher-level Android integration
  around supported on-device language models. It is a good first app path
  when its model/runtime matrix includes the selected Gemma build.
- Store downloaded model files in app storage or another explicitly provisioned
  device location. Model files are artifacts, not source files for this repo.
- Let the app observe Android thermal and lifecycle signals and stop or reduce
  work when the device is hot or backgrounded.

### Termux: preferred control and bridge path

Termux is useful for SSH/SFTP, Tailscale-adjacent operations, health checks,
queues, and an MCP HTTP adapter. It is less reliable as the home of Android
accelerator APIs. The supplied `termux-setup.sh` therefore starts a small
`/health` liveness stub by default; set `MCP_COMMAND` to an already-tested
server when one is available.

### llama.cpp / llama.cpp-android: flexible fallback

`llama.cpp` is a useful GGUF/CPU-oriented fallback and can be built from
source for Android or a Termux-compatible environment. The Android NDK/JNI
route is generally more maintainable for an app; a Termux build is useful for
experiments and headless control. Build from an upstream checkout on the
device or in a build system, and download a permitted GGUF model at runtime.
Do not commit a prebuilt executable, GGUF, APK, NDK output, or model weights.

Do not mix runtime assumptions: a LiteRT model is not automatically a GGUF
model, and a `llama.cpp` build is not automatically an Android accelerator
integration.

## Battery and thermal guardrails

- Start with 1B/E2B, Q4, batch 1, and a 2k–4k context.
- Cap output tokens and queue work rather than keeping a hot inference loop.
- Keep the device ventilated. Stop the runner if Android reports a serious
  thermal state or the chassis is uncomfortable to hold.
- Test unplugged and screen-off; charging can hide a bad power profile.
- Request a Termux wake lock only while a deliberate job is running, then
  release it. Do not make an always-on wake lock the default.
- Tailscale's VPN and periodic health checks consume less power than inference,
  but they still need battery-unrestricted/background permission on Android.
- Treat the phone as intermittently available. A missed heartbeat is a normal
  routing event, not a reason to spin-retry forever.

## Off-cloud mesh and escalation

The intended path is:

```text
phone Gemma (local)
  └─ uncertain / too large / needs shared context
       └─ Tailscale mesh → Vultr MCP or inference node
            └─ still unresolved or needs Gemini capability
                 └─ Gemini / Spark (Vesper) → signed result back through Vultr
```

The escalation envelope should contain a correlation ID, task class, concise
redacted context, local confidence/deferral reason, timeout, and requested
return format. It must not contain Tailscale keys, SSH private keys, provider
tokens, or an unbounded conversation dump. Keep the cloud hop opt-in and
auditable; if the mesh is unavailable, queue or answer locally rather than
claiming that a remote escalation succeeded.

`GEMMA_8A.md` turns this architecture into a first-boot checklist. The shell
stub is intentionally offline-friendly and has no binary payloads.

## Olivia → James checklist

- [ ] Pixel is identified as `pixel-8a`, has battery-unrestricted permission,
      and is online in the Tailscale app.
- [ ] Termux came from one trusted distribution source and has storage access.
- [ ] `termux-setup.sh` completed without putting a secret in the repository.
- [ ] `curl http://127.0.0.1:8081/health` returns `{"status":"ok",...}`.
- [ ] The same `/health` endpoint is reachable from an authorized mesh peer
      only if remote binding was intentionally enabled.
- [ ] The SFTP public key was installed on the intended Vultr account; the
      private key stayed on the phone.
- [ ] The first model is Gemma 3 1B or Gemma 3n E2B, not a 12B/27B model.
- [ ] Escalation is phone → Vultr → Gemini/Spark (Vesper), with redaction and
      a timeout.
- [ ] Offline behavior is defined: local answer, queue, or explicit defer.
