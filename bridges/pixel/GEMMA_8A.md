# Pixel 8a first-target runbook

Goal: bring `pixel-8a` online as a local-first Gemma node, expose only the
small control endpoint needed by the bridge, and prove the Tailscale path
before attempting an on-device model.

This runbook assumes an 8 GB Pixel 8a. It starts with Gemma 3 1B or Gemma 3n
E2B in a supported 4-bit runtime. Do not start with Gemma 12B or 27B.

See [`README.md`](README.md) for model/runtime tradeoffs, thermal limits, and
the phone → Vultr → Gemini/Spark (Vesper) escalation contract.

## 0. Safety and prerequisites

- Use Termux from one trusted distribution source (F-Droid or the official
  Termux release channel); do not mix Termux package sources.
- Install the official Tailscale Android app separately. This script does not
  create, print, or store a Tailscale auth key.
- Keep at least several GB of free storage for a model artifact and temporary
  runtime files. Model files stay on the phone and are not checked into this
  repository.
- Set the Android battery mode for **Tailscale** and **Termux** to
  unrestricted/allowed for background use. Start with the phone cool and
  unplugged.

## 1. Install the bridge files

From Termux:

```sh
pkg update -y
pkg install -y git
mkdir -p "$HOME/src"
git clone https://github.com/jameswilsonotr-ship-it/sovereign-skills-archive \
  "$HOME/src/sovereign-skills-archive"
cd "$HOME/src/sovereign-skills-archive"
chmod 700 bridges/pixel/termux-setup.sh
./bridges/pixel/termux-setup.sh
```

The setup is repeatable. It installs small control-plane packages, creates an
Ed25519 SFTP key in `~/.config/pixel-bridge/ssh/`, prints the public-key path,
and starts a localhost-only `/health` stub on port 8081. It does not install
model weights or a binary runner.

Confirm the local endpoint:

```sh
curl --fail --silent --show-error http://127.0.0.1:8081/health
```

Expected shape:

```json
{"status": "ok", "service": "pixel-mcp-health-stub"}
```

That response proves process liveness only; the stub is not an MCP protocol
implementation. Replace it with a tested server using `MCP_COMMAND` only after
the network path is healthy:

```sh
MCP_COMMAND='python "$HOME/bin/pixel_mcp.py" --host 0.0.0.0 --port 8081' \
MCP_BIND_ADDRESS=0.0.0.0 \
./bridges/pixel/termux-setup.sh
```

Use the actual server's documented health route if it is not `/health`.

## 2. Bring `pixel-8a` online in Tailscale

1. Open the Tailscale Android app on the phone.
2. Turn the VPN on, sign in to the intended tailnet, and use the device name
   `pixel-8a` if the app permits it.
3. Approve the Android VPN prompt.
4. In Android settings, allow background activity and disable battery
   optimization for Tailscale. Do the same for Termux if Termux must serve the
   endpoint while the screen is off.
5. Confirm the device appears online in the tailnet admin/device view.

The Termux script reports a local `tailscale` CLI only when one happens to be
installed; the Android app is the source of truth on a normal phone. Do not
paste a Tailscale auth key into Termux, this repository, or an SFTP command.

If the device is currently shown as often offline:

- open Tailscale and toggle the VPN off/on once;
- check Wi-Fi/mobile data and the Android VPN indicator;
- remove battery restrictions before testing screen-off behavior;
- check that the tailnet has not expired or disabled the device;
- reboot only after recording the current Tailscale device state; and
- rerun the local health check before diagnosing the remote path.

Do not use an infinite reconnect loop. A phone may be offline and should then
be treated as an unavailable worker.

## 3. Prove the mesh path

Keep the first test local-only. When local health is green, deliberately bind
the tested server to all interfaces so the Android VPN can reach it:

```sh
cd "$HOME/src/sovereign-skills-archive"
MCP_BIND_ADDRESS=0.0.0.0 \
./bridges/pixel/termux-setup.sh
```

From an already-authorized Vultr mesh peer, replace the hostname with the
MagicDNS name or tailnet IP shown by the Tailscale admin:

```sh
curl --fail --silent --show-error http://pixel-8a:8081/health
```

If MagicDNS is not enabled:

```sh
curl --fail --silent --show-error http://<pixel-8a-tailscale-ip>:8081/health
```

If local health passes but remote health fails, check in this order:

1. Tailscale shows `pixel-8a` online and the peer is authorized.
2. The process is listening on `0.0.0.0:8081`, not only `127.0.0.1`.
3. Android's VPN and battery policy has not suspended Termux.
4. The peer is using the Tailscale address, not a LAN address.
5. Any host-side MCP allowlist permits this device and port.

Do not expose port 8081 to the public internet. The intended access boundary
is the tailnet plus the MCP server's own authentication/allowlist.

## 4. Add the SFTP key slot

The setup script prints the public key location. Inspect only the public half:

```sh
cat "$HOME/.config/pixel-bridge/ssh/id_ed25519.pub"
```

Install that line in the intended Vultr account's `authorized_keys` through
the approved account-access path. Keep the private half at:

```text
$HOME/.config/pixel-bridge/ssh/id_ed25519
```

Test with a narrow, non-secret path:

```sh
sftp -i "$HOME/.config/pixel-bridge/ssh/id_ed25519" \
  vultr-user@<vultr-tailscale-host>
```

The SFTP key is a separate SSH credential. It is not a Tailscale key and must
not be reused as one.

## 5. Choose and test Gemma

### Android app path (recommended)

Use an Android app built around LiteRT or MediaPipe LLM Inference when the
selected Gemma model is in that runtime's supported model matrix. Download
the model on-device through the app's documented flow. Start with:

- Gemma 3 1B, 4-bit; or
- Gemma 3n E2B, if the app/runtime explicitly supports that artifact.

Run a fixed offline prompt and record cold start, peak memory, output speed,
and temperature. Keep the first context at 2k–4k tokens and cap output.

### Termux / llama.cpp experiment

Only if an Android-compatible build is needed, install build tools and compile
from source on the device:

```sh
cd "$HOME/src/sovereign-skills-archive"
INSTALL_LLAMA_CPP=1 \
./bridges/pixel/termux-setup.sh
```

This clones source and builds a local executable; it does not download a GGUF.
Validate the current upstream `llama-server` flags before wiring it to
`MCP_COMMAND`. Download a permitted GGUF at runtime into a device-only
directory, and never add it, its checksum-bearing private URL, or the
executable to this repository.

If the build is slow, hot, or incompatible with the current Termux/Android
ABI, stop. Use the Android app path or defer inference to Vultr.

## 6. Exercise local-first escalation

Use a harmless, redacted test request with a correlation ID:

```json
{
  "correlation_id": "pixel-8a-smoke-001",
  "task": "classify",
  "input": "redacted smoke-test text",
  "local_model": "gemma-3-1b-q4",
  "decision": "defer_if_uncertain",
  "timeout_ms": 8000
}
```

Routing rules:

1. Gemma answers locally when the task fits its context and confidence gate.
2. If it defers, the bridge sends only the redacted envelope over Tailscale to
   Vultr.
3. Vultr handles the stronger/longer operation. If it cannot resolve the
   request or explicitly needs Gemini capability, Vultr escalates to **Gemini,
   also called Spark/Vesper**, then returns a result and correlation ID.
4. The phone displays the result and records whether it was local, Vultr, or
   Gemini/Spark. If the mesh is down, it reports `deferred_offline`; it does
   not claim a successful escalation.

Never include private keys, Tailscale material, provider tokens, or a full
conversation history in the smoke test. Human approval is required before
enabling broad cloud forwarding.

## 7. Acceptance checklist

- [ ] Tailscale app is on and `pixel-8a` is online.
- [ ] Local `127.0.0.1:8081/health` passes twice, including after restarting
      the script.
- [ ] Remote `/health` passes from one authorized Vultr tailnet peer.
- [ ] The listener is not reachable from an untrusted/public interface.
- [ ] SFTP public key is installed; the private key never left the phone.
- [ ] A 1B/E2B offline prompt completes without a thermal warning.
- [ ] The model artifact and native executable are device-only.
- [ ] A redacted defer reaches Vultr, and the Gemini/Spark (Vesper) fallback
      is clearly labeled when used.
- [ ] Offline mode returns `deferred_offline` or a local answer.
