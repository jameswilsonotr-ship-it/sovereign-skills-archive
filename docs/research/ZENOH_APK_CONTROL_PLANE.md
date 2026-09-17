# `zenoh.apk` as a Burner Control Plane

Research and integration brief for the Android system-bus cockpit, an Android
Intent adapter, and the companion APKs that may sit behind it.

**Repository:** [`jameswilsonotr-ship-it/zenoh.apk`](https://github.com/jameswilsonotr-ship-it/zenoh.apk)
**Related repositories:** [`Groxxporter`](https://github.com/jameswilsonotr-ship-it/Groxxporter) and
[`kokoro-speaker-cloner.apk`](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk)
**Research date:** 2026-09-17
**Status:** architecture/research note; the MCP and Intent contracts below are proposed
interfaces, not claims that those interfaces already exist in the APK.

## Executive summary

`zenoh.apk` is a useful shape for a disposable Android control-plane node:

1. A human or automation client attaches to a short-lived Android node.
2. The node opens a Zenoh session, or a clearly labelled simulation session while
   native bindings are unavailable.
3. The node exposes a narrow set of allowlisted operations: status, connect,
   publish, subscribe, query, and disconnect.
4. Results are correlated with a request ID and emitted as structured events.
5. The node is torn down, its session is closed, and its identity is not reused.

The important qualification is that the current repository does **not** yet
implement the production data plane implied by its README. Its Gradle file
comments out the Zenoh Kotlin dependency and bundles local classes under
`org.eclipse.zenoh` as compile-time stubs. The `ZenohViewModel` therefore
supports a real-looking UI, a simulated fallback, and a future native session,
but the checked-in source is not evidence of a working remote Zenoh transport.
The same qualification applies to MCP: there is no MCP server, tool schema, or
Android Intent contract in the current `zenoh.apk` tree.

This brief defines the smallest safe seam to add those capabilities without
turning a burner node into a permanent credential store or an arbitrary remote
code launcher.

## 1. What was verified

The following observations are anchored to the public default branches of the
three application repositories as they existed on the research date.

| Surface | Observed implementation | Consequence |
| --- | --- | --- |
| Zenoh client UI | `ZenohViewModel` exposes endpoint, `client`/`peer` mode, a subscription expression, a publish topic/payload, heartbeat, logs, and diagnostics. | A useful control-plane cockpit already exists. |
| Connection path | The view model builds a `Config`, inserts `connect/endpoints` and `mode`, then opens a `Session`. | This is the intended native seam, but it must not be described as live until the binding is real. |
| Native dependency | `app/build.gradle.kts` comments out `org.eclipse.zenoh:zenoh-kotlin`; local `Config`, `Session`, `Sample`, `KeyExpr`, and `Value` classes are checked in under `org.eclipse.zenoh`. | Current builds compile against no-op stubs. |
| Fallback | If native loading fails, the view model marks the node as simulated and generates sample swarm traffic locally. | Every external caller must be able to distinguish `native`, `simulated`, and `error`. |
| Existing topics | The UI defaults to `swarm/bus/**` and publishes a heartbeat at `swarm/bus/heartbeat`. | Preserve these as compatibility/demo topics; use a versioned control namespace for automation. |
| Android entry point | The manifest exports only a launcher activity with `MAIN`/`LAUNCHER`; it has no custom command action, receiver, service, or deep-link contract. | “Android intent MCP” is a design target, not a current feature. |
| Groxxporter | The app is an offline Grok export extractor with a `FileProvider`. Its manifest currently exposes a launcher activity and keeps the provider non-exported while granting URI permissions. | Hand off content URIs with explicit grants; do not pass filesystem paths. |
| Kokoro | The app performs speaker diarization, style extraction, and voice-packaging. It also declares an exported Android TTS service for the system `TTS_SERVICE` action. | The TTS service is a platform integration point, not a general-purpose MCP command bus. |

The primary source anchors are:

- [`ZenohViewModel.kt`](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/app/src/main/java/com/example/ZenohViewModel.kt)
- [`ZenohStubs.kt`](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/app/src/main/java/org/eclipse/zenoh/ZenohStubs.kt)
- [`zenoh.apk` Gradle dependencies](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/app/build.gradle.kts)
- [`zenoh.apk` manifest](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/app/src/main/AndroidManifest.xml)
- [`Groxxporter` README](https://github.com/jameswilsonotr-ship-it/Groxxporter/blob/main/README.md)
- [`Groxxporter` manifest](https://github.com/jameswilsonotr-ship-it/Groxxporter/blob/main/app/src/main/AndroidManifest.xml)
- [`kokoro-speaker-cloner.apk` README](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk/blob/main/README.md)
- [`kokoro-speaker-cloner.apk` manifest](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk/blob/main/app/src/main/AndroidManifest.xml)

## 2. Meaning of “burner control plane”

“Burner” describes the lifecycle and trust posture, not a special Zenoh
protocol mode.

A burner node is:

- **short-lived:** created for one task, session, or test window;
- **scoped:** allowed to reach only an explicitly configured endpoint and
  namespace;
- **stateless by default:** no long-lived credentials, conversation archive, or
  voice material is stored merely because a command was received;
- **observable:** every accepted, rejected, simulated, and failed operation has
  a correlation ID and outcome;
- **revocable:** disconnect and teardown invalidate the session and any local
  capability token;
- **disposable:** the node can be uninstalled, cleared, or replaced without
  migrating identity.

It is not:

- a permanent broker;
- an authentication system;
- a general Android automation bridge;
- a place to put private keys in the APK or in Intent extras;
- permission to execute arbitrary shell commands, components, URLs, or
  Java/Kotlin class names;
- proof that a message was acted on by a physical device when the app is in
  simulation mode.

The burner boundary is especially important because Zenoh can unify pub/sub,
queries, storage, and computation under related key expressions. A convenient
data path can otherwise become an overly powerful remote-execution path.

## 3. Reference architecture

```text
 MCP client / agent
        |
        | MCP JSON-RPC tool call
        v
  MCP adapter
  (in-process or companion bridge)
        |
        | validated, explicit Android Intent
        v
  zenoh.apk control receiver/service
        |
        +--> capability + namespace policy
        |        |
        |        +--> native Zenoh Session
        |        |       (when the real binding is present)
        |        |
        |        +--> simulation adapter
        |                (clearly labelled, local only)
        |
        +--> structured result/event
                  |
                  +--> MCP tool result
                  +--> Zenoh event topic
                  +--> bounded local diagnostics

  Companion paths:
    Groxxporter  -- content URI --> import/extract job
    Kokoro       -- content URI --> diarize/package/TTS job
```

There are two viable MCP placements:

### Option A: in-process MCP surface

The MCP server runs in the same application process as the control-plane
adapter. A tool call is decoded into a typed command and passed to the same
command handler used by the UI. This has the best security story because no
other application receives privileged Intents. It also requires an MCP
transport that can run on Android and a deliberate lifecycle policy for the
server.

### Option B: external MCP-to-Intent bridge

An MCP server runs on a workstation, local server, or another trusted Android
process. It validates the tool call, resolves the destination package
explicitly, and sends a typed Intent to `zenoh.apk`. This is useful for an
ADB-connected burner or a device-local automation hub.

The bridge must not treat an arbitrary `action`, `component`, or `data` value
from an MCP caller as executable input. The destination package, action set,
extra names, and value types are policy, not caller-controlled routing.

MCP is the structured tool protocol at the edge. Android Intent is the local
component-delivery mechanism. Zenoh is the optional node-to-node data plane.
They are complementary layers and should not be presented as interchangeable
protocols.

## 4. Proposed Android Intent contract

The contract below is intentionally explicit and versioned. The package name is
shown as a placeholder because the current application ID is generated and
should not become a public compatibility promise until the app is renamed.

```text
Package: com.aistudio.zenohbus.<stable-id>
Action prefix: com.aistudio.zenohbus.control.v1
```

### 4.1 Command actions

| Action | Required extras | Result |
| --- | --- | --- |
| `...STATUS` | `request_id` | Current lifecycle, transport mode, native/simulation state, policy version, and counters. |
| `...CONNECT` | `request_id`, `endpoint`, `mode` | Session ID and effective policy. |
| `...DISCONNECT` | `request_id` | Closed session or already-disconnected result. |
| `...PUBLISH` | `request_id`, `key_expr`, `payload`, `encoding` | Accepted/rejected plus publication status. |
| `...SUBSCRIBE` | `request_id`, `key_expr` | Subscription ID and bounded event stream metadata. |
| `...UNSUBSCRIBE` | `request_id`, `subscription_id` | Subscription close status. |
| `...QUERY` | `request_id`, `key_expr`, optional `selector` | Bounded query replies, only when the native implementation supports queries. |
| `...CAPABILITIES` | `request_id` | Version, supported operations, limits, and simulation flag. |

The receiver should return one immediate acknowledgement and publish or
deliver later results by the same `request_id`. A result must include:

```json
{
  "protocol": "zenoh-android-control/v1",
  "request_id": "req-01J...",
  "node_id": "burner-7f2e",
  "operation": "publish",
  "status": "accepted",
  "transport": "simulated",
  "created_at": "2026-09-17T03:58:00Z"
}
```

`transport` is mandatory. Valid values are `native`, `simulated`, `offline`,
and `error`. A simulated publish must never be reported as a network delivery.

### 4.2 Extra and payload rules

- `request_id`: opaque UTF-8 string, 1–96 bytes, supplied by the caller or
  generated by the adapter.
- `endpoint`: one configured endpoint, not an arbitrary URI scheme. The policy
  should normally allow `tcp/host:port` and a local test endpoint only.
- `mode`: enum `client` or `peer`; default to `client` for a burner.
- `key_expr`: validate as a Zenoh key expression before opening a session or
  sending a packet. Do not silently rewrite caller input.
- `payload`: bounded text or bytes. The first version should cap a single
  Intent payload well below Android Binder’s transaction limit; large artifacts
  move through a `content://` URI.
- `encoding`: enum `utf8`, `json`, or `base64`; JSON must be parsed before a
  JSON-specific command is accepted.
- `timeout_ms`: bounded by the app policy, not an untrusted unbounded sleep.
- unknown extras: reject in strict mode and report their names without logging
  their values.

For a file handoff, use:

```text
Intent data: content://...
Flags: FLAG_GRANT_READ_URI_PERMISSION
Extra: display_name (optional, non-authoritative)
```

The receiving app must read the URI through `ContentResolver`. A display name
is presentation metadata and must not be used as a filesystem path.

### 4.3 Component and permission posture

The preferred design is a non-exported internal command handler when the MCP
surface is in-process. If an external bridge is required, expose a dedicated
receiver or service with all of the following:

1. explicit component delivery (`setComponent` or `setPackage`);
2. a signature-level permission owned by `zenoh.apk`;
3. strict action and extra allowlists;
4. request authentication or a short-lived capability established out of band;
5. replay protection using request ID plus expiry;
6. bounded result and event buffers;
7. no generic “run intent” action.

The launcher activity should not be repurposed as a command endpoint. A
launcher is user-facing and is not a reliable background execution surface.
Likewise, a custom URI scheme or an implicit Intent may be useful for discovery
or a user-confirmed handoff, but it is not an adequate authorization boundary
for control commands.

The Android documentation covers the distinction between explicit and implicit
Intents and the risks of implicit Intent interception. See:

- [Intent and Intent filters](https://developer.android.com/guide/components/intents-filters)
- [Implicit Intent hijacking](https://developer.android.com/privacy-and-security/risks/implicit-intent-hijacking)
- [Content URI permissions](https://developer.android.com/training/secure-file-sharing)

## 5. Proposed MCP tool surface

The MCP adapter should expose named tools rather than a single
`android_send_intent` escape hatch.

| Tool | Inputs | Side effect | Default policy |
| --- | --- | --- | --- |
| `zenoh_capabilities` | none | none | allowed |
| `zenoh_status` | none | none | allowed |
| `zenoh_connect` | endpoint, mode, expiry | opens a session | explicit approval or session capability |
| `zenoh_disconnect` | session ID | closes a session | allowed for the owning request |
| `zenoh_publish` | session ID, key expression, payload | sends data | namespace allowlist and size limit |
| `zenoh_subscribe` | session ID, key expression, duration | receives data | bounded duration and buffer |
| `zenoh_unsubscribe` | subscription ID | closes a subscription | allowed for the owning request |
| `zenoh_query` | session ID, key expression, selector, timeout | reads remote state | opt-in; no arbitrary storage access |
| `companion_open` | companion enum, content URI, operation | launches a known handoff | explicit app/action allowlist |

The MCP tool names are intentionally narrower than the Android primitive. The
adapter may internally build an Intent, but the caller never chooses a
component class, action string, package, or arbitrary extra key.

A minimal `zenoh_publish` input schema should look conceptually like:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["session_id", "key_expr", "payload"],
  "properties": {
    "session_id": { "type": "string", "minLength": 1, "maxLength": 96 },
    "key_expr": { "type": "string", "minLength": 1, "maxLength": 256 },
    "payload": { "type": "string", "maxLength": 65536 },
    "encoding": {
      "type": "string",
      "enum": ["utf8", "json", "base64"]
    },
    "request_id": { "type": "string", "maxLength": 96 }
  }
}
```

The tool result should return the structured acknowledgement, not a prose
claim that the packet arrived. For subscriptions, use a bounded stream or
polling tool result with an explicit expiry. Do not leave a subscription
running indefinitely because an MCP client disconnected.

The MCP tools specification defines tools as named operations with an input
schema, and the protocol uses JSON-RPC messages at the protocol boundary. The
adapter should follow the current specification rather than inventing an
Intent-shaped MCP tool:

- [MCP server tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [MCP transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

## 6. Zenoh namespace proposal

The current UI uses `swarm/bus/**`. Keep that namespace for compatibility with
the existing demo and swarm experiments. Put burner control traffic under a
versioned namespace so automation does not accidentally publish a command as
telemetry.

```text
burner/v1/{node_id}/status
burner/v1/{node_id}/capabilities
burner/v1/{node_id}/event/{request_id}
burner/v1/{node_id}/telemetry
burner/v1/{node_id}/command/{request_id}
burner/v1/{node_id}/companion/{request_id}
```

Suggested envelope:

```json
{
  "protocol": "zenoh-android-control/v1",
  "request_id": "req-01J...",
  "node_id": "burner-7f2e",
  "operation": "publish",
  "issued_at": "2026-09-17T03:58:00Z",
  "expires_at": "2026-09-17T03:59:00Z",
  "payload": {
    "topic": "swarm/bus/heartbeat",
    "value": {
      "status": "nominal"
    }
  }
}
```

The following rules keep the namespace useful:

- command paths are not telemetry paths;
- node IDs are generated per burner lifecycle and are not permanent user IDs;
- `request_id` is unique within the capability lifetime;
- timestamps are informational unless the device has a trusted clock;
- the receiver acknowledges admission and reports delivery/processing
  separately;
- binary artifacts and audio never travel through a routine control topic;
- remote query and storage paths need a separate allowlist from publish paths.

Zenoh’s own project describes the protocol as unifying pub/sub, storage/query,
and computation, with router and language bindings around the core. For the
intended protocol model, consult:

- [Eclipse Zenoh](https://github.com/eclipse-zenoh/zenoh)
- [Zenoh Kotlin bindings](https://github.com/eclipse-zenoh/zenoh-kotlin)
- [Zenoh Android demo](https://github.com/eclipse-zenoh/zenoh-demos/tree/main/zenoh-android)
- [`zenoh.apk`’s checked-in protocol notes](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/RESEARCH.md)

The last link is project-local research. It is useful for mapping the intended
API, but the local stubs and commented dependency mean it cannot by itself
establish native transport support.

## 7. Companion APK integration

### 7.1 Groxxporter

[`Groxxporter`](https://github.com/jameswilsonotr-ship-it/Groxxporter) is an
offline-first Android export extractor and integrity utility. Its README
describes local parsing, chunking, format compilation, attachment decoding, and
optional integrity verification. Its current manifest exposes:

- a launcher activity;
- a non-exported `FileProvider` with URI grants;
- no custom MCP action;
- no general command receiver.

The safe control-plane relationship is therefore a **content handoff**, not
remote UI driving:

```text
zenoh.apk / MCP adapter
  -> create or select a content:// export URI
  -> explicit Groxxporter import action (future contract)
  -> Groxxporter reads the granted URI locally
  -> result URI + digest returned as a bounded event
```

Proposed future action:

```text
Action: com.jameswilsonotr.groxxporter.control.v1.IMPORT
Data:   content://...
Extras: request_id, format_hint, sha256 (optional verification hint)
Flags:  FLAG_GRANT_READ_URI_PERMISSION
```

The `format_hint` is advisory. Groxxporter should inspect the content and
report the detected format; it must not trust a caller-provided extension.
Results should be addressed by content URI and digest. Do not put a full
conversation export, attachment bytes, or bearer credentials in an Intent
extra or Zenoh log.

### 7.2 Kokoro Speaker Cloner

[`kokoro-speaker-cloner.apk`](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk)
describes a local audio pipeline:

1. ingest denoised audio;
2. identify or diarize speakers;
3. extract a Kokoro style representation;
4. package a voice profile as `.bin` plus JSON metadata and a reference WAV;
5. provide an offline TTS service.

The current manifest declares `PocketTtsEngineService` as an exported service
for Android’s `android.intent.action.TTS_SERVICE`. That is a platform TTS
provider surface. It should not be overloaded as an arbitrary “synthesize this
remote command” endpoint. A future burner integration should use a separate,
explicit, permissioned action for a content-URI job:

```text
Action: com.jameswilsonotr.kokoro.control.v1.PACK_VOICE
Data:   content://.../audio
Extras: request_id, voice_id, output_uri (optional)
Flags:  FLAG_GRANT_READ_URI_PERMISSION
```

The control plane should return metadata such as `voice_id`, tensor shape,
sample rate, output URI, and digest. It should not mirror raw audio or voice
latents into Zenoh telemetry. Audio is sensitive biometric-adjacent material;
retention, export, and deletion must be explicit.

If the only goal is system TTS, use Android’s normal TTS engine selection and
request path. An MCP tool named `kokoro_synthesize` should not pretend that
the exported TTS service is a general network API.

## 8. Lifecycle and state machine

The control plane should make the burner lifecycle explicit:

```text
NEW
  -> READY
  -> CONNECTING
  -> CONNECTED_NATIVE
  -> CONNECTED_SIMULATED
  -> DISCONNECTING
  -> CLOSED

Any active state -> ERROR
ERROR -> DISCONNECTING -> CLOSED
```

Rules:

1. `READY` may answer capabilities and status, but cannot publish.
2. `CONNECTING` rejects duplicate connects unless the request is idempotent.
3. `CONNECTED_SIMULATED` can exercise UI and schema paths but cannot claim
   remote side effects.
4. Every subscription has a TTL and an owner request/session.
5. `DISCONNECTING` cancels heartbeat, subscriptions, query callbacks, and
   companion jobs owned by the burner.
6. `CLOSED` rejects all commands except a diagnostic status that reports the
   terminal state.

Idempotency keys should be honored for connect, disconnect, and companion job
creation. A repeated publish is not automatically idempotent; callers should
provide their own event ID when duplicate delivery matters.

## 9. Security and failure model

### Threats

| Threat | Failure mode | Mitigation |
| --- | --- | --- |
| Implicit Intent interception | Another app receives a command or URI. | Explicit component, signature permission, and URI grant. |
| Intent injection | Caller supplies an arbitrary action/component/extra. | Named MCP tools and a fixed action registry. |
| Replay | Old publish or companion job runs again. | Expiry, capability ID, request ID replay cache. |
| Endpoint pivot | Caller connects the burner to an unintended host. | Endpoint allowlist, no arbitrary schemes, visible effective config. |
| Payload exfiltration | Audio/export data appears in logs or topics. | Content URIs, digests, redaction, size limits, no raw payload logging. |
| Simulation confusion | Local fake event is treated as remote success. | Mandatory `transport` field and visible `SIMULATED` state. |
| Native binding drift | Stub API diverges from the real binding. | Contract tests against the real dependency and a compile-time adapter. |
| Runaway subscription | Device or MCP client leaks a live stream. | TTL, max events, cancellation on disconnect, backpressure. |
| Package confusion | A similarly named app receives a handoff. | Fully qualified package/component and package signature verification where available. |
| Sensitive voice retention | Speaker audio/profile persists unexpectedly. | Explicit retention policy, user confirmation, deletion acknowledgement. |

### Burner defaults

- default mode: `client`;
- default session expiry: short and visible;
- default control namespace: only `burner/v1/{node_id}/...`;
- default publish allowlist: no command paths unless explicitly enabled;
- default query access: disabled;
- default companion access: disabled until a known package and contract are
  selected;
- default logging: metadata only, with payload redaction;
- default transport: fail closed if native availability is ambiguous;
- developer/demo mode: simulation is allowed, but every result says
  `transport=simulated`.

“Fail closed” here means that a caller cannot accidentally turn a failed native
load into a remote-looking success. A local demo may opt into simulation, but
that choice should be visible in the capability response and UI.

## 10. Implementation sequence

The work should land in narrow seams even if the overall integration is a
large effort.

### Phase 0: truth-in-advertising

- Rename or clearly label the local classes as stubs.
- Add a `TransportMode` enum instead of inferring native availability from a
  successful no-op `Config.defaultConfig()`.
- Make `status` report `native`, `simulated`, or `unavailable`.
- Keep the existing `swarm/bus/**` demo behavior behind an explicit demo flag.

### Phase 1: typed command core

- Extract a platform-neutral command model from `ZenohViewModel`.
- Define the action registry and JSON schemas in one place.
- Add validation for endpoints, modes, key expressions, payload size, expiry,
  and request IDs.
- Add deterministic result envelopes and a bounded event buffer.
- Add unit tests for acceptance, rejection, replay, expiry, and simulation
  labelling.

### Phase 2: Android adapter

- Add a dedicated receiver/service; do not route commands through the launcher.
- Use explicit component delivery.
- Add a signature-level permission for external mode.
- Require a short-lived capability for privileged actions.
- Use `content://` URIs for files and audio with one-shot or narrowly scoped
  grants.
- Add instrumentation tests that attempt implicit delivery, unknown actions,
  malformed extras, and oversized payloads.

### Phase 3: native Zenoh adapter

- Replace local stubs with the supported `zenoh-kotlin` Android dependency or
  a versioned internal wrapper.
- Verify Android ABI packaging, minimum SDK, session close behavior, and
  callback threading on a real device/emulator.
- Test client and peer modes separately.
- Verify that QoS configuration is actually supported by the chosen binding;
  do not preserve a UI toggle that silently does nothing.
- Add an integration test against a controlled `zenohd` router.

### Phase 4: MCP adapter

- Expose named tools with strict input schemas.
- Map tool calls to typed commands, never to arbitrary Intents.
- Return the structured acknowledgement and transport state.
- Cancel subscriptions when the MCP client or capability expires.
- Add an audit record containing request ID, tool, outcome, and digest—not raw
  secrets or full payloads.

### Phase 5: companion handoffs

- Define separate versioned action contracts for Groxxporter and Kokoro.
- Verify package identity and grant only the required URI permission.
- Return job state and content digests.
- Add explicit deletion/retention operations for extracted exports and voice
  artifacts.
- Keep TTS provider registration separate from MCP job control.

## 11. Verification checklist

### Repository and build truth

- [ ] A build with the real Zenoh dependency does not resolve the local stubs.
- [ ] A stub/simulation build is labelled as such in the APK and every result.
- [ ] Native library load failure is distinguishable from a successful session.
- [ ] Android ABIs used by the APK are listed and tested.
- [ ] No secret appears in `.env.example`, an Intent extra, a topic, or a log.

### Intent boundary

- [ ] Commands use an explicit package/component.
- [ ] External mode requires the signature-level permission.
- [ ] Unknown actions, components, extras, and encodings are rejected.
- [ ] A caller cannot select an arbitrary activity, service, receiver, or URI
      scheme.
- [ ] File handoffs use `content://` plus narrowly scoped grant flags.
- [ ] The receiver expires or cancels abandoned requests.
- [ ] Binder-sized payloads are rejected before dispatch.

### MCP behavior

- [ ] Tool schemas set `additionalProperties: false`.
- [ ] Tool results distinguish accepted, completed, failed, expired, and
      simulated.
- [ ] Subscription duration and event count are bounded.
- [ ] Repeated request IDs are handled deterministically.
- [ ] Disconnect closes the Zenoh session and companion jobs.
- [ ] A dropped MCP client cannot leave an unbounded background operation.

### Zenoh behavior

- [ ] Control and telemetry key expressions are separate.
- [ ] The endpoint and mode shown in status are the effective values.
- [ ] `client` and `peer` behavior is tested against the intended topology.
- [ ] Publish acknowledgement is not confused with remote processing.
- [ ] Query access is separately authorized from publish access.
- [ ] Router/device logs do not record sensitive export or audio content.

### Companion behavior

- [ ] Groxxporter receives a content URI and verifies the detected format.
- [ ] Groxxporter returns a digest and output URI rather than a raw path.
- [ ] Kokoro jobs state retention and deletion behavior.
- [ ] Kokoro’s system TTS service is not used as an arbitrary command endpoint.
- [ ] Voice artifacts and references are never copied to a telemetry topic.

## 12. Short operator runbook

1. Install a fresh burner APK on a test device or emulator.
2. Open **Capabilities** and verify `transport`, app version, policy version,
   allowed endpoint, and supported actions.
3. Connect only to the controlled router or local simulator.
4. Confirm status reports a new burner `node_id` and a session expiry.
5. Publish a harmless test event under `burner/v1/{node_id}/...`.
6. Confirm the acknowledgement and the observed event have the same
   `request_id`.
7. If testing simulation, verify no remote router receives the event.
8. For a companion handoff, use a test content URI and verify the digest.
9. Disconnect, confirm subscriptions and heartbeat stop, and clear app data or
   uninstall the burner when the test is complete.

## 13. Bottom line

`zenoh.apk` is a strong candidate for a burner control-plane **shell** because
its UI and view model already express the right operational concepts:
session lifecycle, client/peer mode, key expressions, publish/subscribe,
heartbeat, diagnostics, and a visible fallback path.

It is not yet a production control plane. The checked-in Zenoh classes are
stubs, the native dependency is commented out, and no Android Intent MCP
surface exists. The safe path is to add a typed command core, an explicit and
permissioned Android adapter, and a named MCP tool layer while preserving the
simulation/native distinction.

Groxxporter should remain the offline export/content-processing companion.
Kokoro should remain the local audio/voice-processing companion and system TTS
provider. `zenoh.apk` should coordinate bounded jobs and report state, not
absorb their private artifacts or become a generic launcher for every Android
component.

