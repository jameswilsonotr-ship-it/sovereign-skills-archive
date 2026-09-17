# Pixel / Termux bridge notes

This directory is an operator note and configuration stub for Pixel 8a, 9a,
and the upcoming Pixel 11 Pro. It does not contain an APK, model weights,
Tailscale key, Gemini key, or a live `SKILL.md`.

## Termux/MCP baseline

The proven transport is Tailscale plus SFTP. The phone-side MCP bridge should
remain a small adapter around the local runner:

```text
Termux MCP -> 127.0.0.1:8081/health
           -> local Gemma runner (LiteRT-LM/MediaPipe or llama.cpp)
           -> optional Tailscale calls to Vultr :8000/v1
           -> SFTP drops to olette-box 100.115.0.111:22
```

Start with `127.0.0.1:8081`. If another tailnet node must reach the bridge,
bind explicitly to the Tailscale interface/IP and enforce a Tailscale ACL;
never bind the MCP port to all public interfaces.

The offline contract already present in this branch is:

[`harness/src/sovereign_harness/phone_mcp.py`](../../harness/src/sovereign_harness/phone_mcp.py)

The real Termux process should preserve the same health and cancellation
semantics. A healthy result must identify the phone, runner, model, and
readiness state without returning a secret.

## Termux setup outline

The following is an operator checklist, not an executable installer:

1. Install Termux from a trusted source and grant only required storage and
   notification permissions.
2. Install the Tailscale client path approved for the device and enroll the
   phone using a short-lived, scoped auth flow.
3. Install Python/Node only if the selected MCP bridge needs them; keep the
   runner and bridge processes bounded by Android battery/thermal policy.
4. Copy a secret-managed environment file from
   [`termux-mcp.env.example`](termux-mcp.env.example) to the Termux private
   directory. Never put it in the Git checkout.
5. Start the bridge and check `http://127.0.0.1:8081/health`.
6. From an authorized tailnet peer, verify only the intended endpoint is
   reachable. Then run the offline smoke/cancellation tests before allowing
   Tier B or SFTP traffic.

Pin the `olette-box` host key before the first SFTP drop. Use an atomic
`.part` upload followed by rename and a bounded retention policy.

## Optional local Gemma runner

Use one runner per phone; the MCP bridge should not care which one is chosen:

| Device | Starting point | Promotion rule |
| --- | --- | --- |
| Pixel 8a, 8 GB | Gemma 3 1B or Gemma 2 2B int4 with LiteRT-LM/MediaPipe LLM Inference | Promote only after cold-start, cancellation, and thermal tests. |
| Pixel 9a, 8 GB | Same baseline; test Gemma 3 4B int4 experimentally | Keep 1B/2B as the guaranteed fallback if 4B thrashes or overheats. |
| Pixel 11 Pro | Confirm final SKU/RAM first; plan for 12 GB-class only provisionally | Test Gemma 3 4B int4; do not assume 8B is viable without measurement. |

`llama.cpp` Android/JNI is the fallback when the Google AI Edge path does not
support the selected quantization. Android AI Core/Gemini Nano is optional
system capability, not a generic Gemma runtime. Model files belong in
device-private storage and must be fetched from an approved source at
enrollment time.

The runner should expose a local `/health` and a bounded chat operation. It
must support cancellation and return a structured “insufficient memory /
thermal / unavailable” result so the router can try Tier B without guessing.

## Do not ship from this scaffold

- No real `TS_AUTHKEY`, Gemini key, Composio token, or SFTP private key.
- No APK/AAB or large archive in Git.
- No public MCP listener.
- No automatic Gemini escalation for private or unapproved data.
- No Cursor process in the phone's runtime dependency graph.
