# Zenoh Android control-plane research

Status: research and architecture notes only. This change does not add an MCP
server, an Android service, an intent receiver, or a network control channel.

## Source reviewed

- Repository: [jameswilsonotr-ship-it/zenoh.apk](https://github.com/jameswilsonotr-ship-it/zenoh.apk)
- Reviewed revision: `ee4213dca6c86ed47ea0491133eb7f305823fc6e` (`ci: upgrade Gradle to 9.3.1 and JDK to 21 for AGP 9.1.1 compatibility`)
- Relevant files: `README.md`, `RESEARCH.md`, `app/build.gradle.kts`,
  `app/src/main/AndroidManifest.xml`, `MainActivity.kt`,
  `ZenohViewModel.kt`, and `org/eclipse/zenoh/*` stubs

## Finding: the current APK is not yet a control plane

The repository is a Compose dashboard/prototype with a Zenoh-shaped API. It
does not currently implement MCP or Android-intent control:

| Surface | What the source actually provides |
| --- | --- |
| Android entry point | An exported launcher `MainActivity`; the only intent filter is `MAIN` + `LAUNCHER`. |
| Android background execution | A `viewModelScope` heartbeat coroutine, tied to the ViewModel lifecycle; no service or receiver is declared. |
| MCP | No MCP dependency, server, tool schema, or MCP transport is present. |
| Zenoh transport | `app/build.gradle.kts` comments out the real Zenoh dependency and includes local `ZenohStubs.kt`, whose session, subscriber, and publish methods are no-ops. |
| Simulation | The ViewModel has a fallback traffic generator and local publish logging when native JNI is unavailable. |
| Network permissions | `INTERNET` and `ACCESS_NETWORK_STATE` only; no transport authentication or device identity is configured. |

The README describes the intended native `zenoh-kotlin-android` integration,
but the checked-in build is not evidence that the native library is active.
That distinction must remain explicit in any deployment or security review.

## Target role: a phone-side edge adapter

The useful decomposition is to keep MCP as the tool/control interface on a
trusted host and use Zenoh as the phone-facing data plane:

```text
MCP client
   |
   v
MCP server + policy/authorization
   |
   | validated command envelope over an authenticated Zenoh session
   v
Android foreground service
   |
   | allowlisted, explicit Android Intent
   v
capability component (activity/service/receiver)
   |
   v
result envelope -> Zenoh -> MCP server -> MCP client
```

This avoids treating an Android APK as an unauthenticated, remotely callable
MCP server. The phone should expose only narrowly scoped capabilities; the
host MCP server should own tool descriptions, user authorization, audit
context, and policy decisions.

### Suggested Zenoh namespaces

Use a per-device namespace and separate commands from observations. These are
design names, not existing topics in the source repository:

```text
control/phone/{device_id}/command/{request_id}
control/phone/{device_id}/result/{request_id}
control/phone/{device_id}/event/{event_id}
control/phone/{device_id}/presence
```

Zenoh ACLs should allow a device to consume only its own command namespace and
publish only its own results/events. Do not reuse a broad wildcard such as
`swarm/bus/**` for privileged actions.

### Command envelope

The bridge should accept a small, versioned envelope rather than arbitrary
intent names or arbitrary extras:

```json
{
  "schema": "phone-command.v1",
  "request_id": "opaque-request-id",
  "capability": "approved.capability",
  "args": {},
  "issued_at": "2026-09-17T00:00:00Z",
  "expires_at": "2026-09-17T00:00:30Z",
  "nonce": "single-use-value",
  "reply_to": "control/phone/device-01/result/opaque-request-id"
}
```

The actual implementation must validate schema, capability, argument types,
expiry, nonce/replay state, request size, and authorization before dispatch.
Responses should carry the request ID, a bounded error code, and a
sanitized result. Never pass an MCP payload directly to `Intent` extras.

## Android intent boundary

Android intents are an internal dispatch mechanism here, not a security
boundary by themselves.

1. Default capability components to `android:exported="false"`.
2. Resolve capabilities from a fixed registry owned by the app; do not accept
   a component class, package name, URI, or shell command from the network.
3. Construct explicit intents with fixed actions and typed, size-bounded
   extras.
4. If a separate broker app is required, protect its entry point with a
   signature-level permission, verify the calling UID/package, and still
   apply the envelope authorization and replay checks.
5. Keep sensitive actions behind a visible, user-consented foreground-service
   flow. Android background-execution and runtime-permission rules still
   apply; Zenoh connectivity does not bypass them.
6. Return an explicit denial when a capability is unavailable, permission is
   missing, the request is expired, or the user has not approved the action.

The manifest should not grow a generic exported receiver such as “run any
intent.” A generic receiver would turn the phone into a remote code/action
dispatcher and would make the MCP authorization layer ineffective.

## Lifecycle and transport changes needed

To turn this prototype into a usable phone-side adapter, a future
implementation would need to:

1. Replace the local Zenoh stubs with a pinned, verified Android binding and
   test the exact ABIs shipped in the APK. Do not claim native transport while
   the stub dependency remains active.
2. Move session ownership from `ZenohViewModel` into a lifecycle-aware
   foreground service. Bind the UI to service state instead of using the UI
   ViewModel as the daemon.
3. Add authenticated session/bootstrap configuration, device identity, router
   ACLs, reconnect/backoff, bounded queues, and orderly shutdown.
4. Add a narrow intent gateway with a capability registry, schema validation,
   replay protection, and result publication.
5. Implement the host-side MCP adapter that maps declared tools to the
   allowlisted envelope. Keep tool descriptions and authorization policy on
   the host; keep phone-side execution minimal.
6. Add instrumentation tests for denied callers, expired/replayed requests,
   malformed arguments, missing Android permissions, service restarts, and
   loss of the Zenoh route.

The sample `0.0.0.0:7447` router command in the upstream README should not be
used as a production default. Bind only where required, authenticate the
router/session, and enforce network and Zenoh ACLs. A “burner” device is not
an authorization mechanism and must not be treated as permission to expose an
open listener.

## Capability examples

These names illustrate the intended granularity and are not implemented by
the source repository:

| MCP-facing capability | Android dispatch shape | Default |
| --- | --- | --- |
| `phone.status.read` | Internal service operation; no external intent | Allow with authenticated session |
| `phone.notification.show` | Explicit app-owned activity/service with typed text | Require local policy |
| `phone.audio.play-approved` | Explicit app-owned service with an asset/reference ID | Require user permission and policy |
| `phone.settings.open` | Explicit activity intent to a fixed settings screen | User confirmation |

Avoid capabilities such as arbitrary shell execution, arbitrary URI
navigation, arbitrary package launching, unrestricted file access, or
silent microphone/camera control. Those do not belong in a general-purpose
MCP-to-phone bridge.

## Security and operational checklist

- Pair each device deliberately and rotate/revoke credentials.
- Store device keys in Android Keystore; never place them in intent extras,
  `.env.example`, logs, or the APK source.
- Use TLS/transport authentication as appropriate for the Zenoh deployment and
  restrict router ACLs by device and namespace.
- Enforce short expirations, single-use nonces, request-size limits, and
  idempotency for every command.
- Redact payloads and audio/text content from logs; retain only the minimum
  audit metadata needed for debugging.
- Make the foreground notification and active-control state visible to the
  device user.
- Treat the current simulated telemetry and sample `override_route` payload as
  fixtures only, not as a safe command contract.
- Verify the built APK, manifest, dependency graph, and signing identity before
  installing on a device.

## Scope of this archive change

This archive change records the source study and a future architecture. It
does not add executable Android, Zenoh, MCP, intent, audio, or device-control
code. Related repositories are linked as documentation-only stubs:

- [Groxxporter](./GROXXPORTER.md)
- [kokoro-speaker-cloner.apk](./KOKORO_SPEAKER_CLONER.md)
