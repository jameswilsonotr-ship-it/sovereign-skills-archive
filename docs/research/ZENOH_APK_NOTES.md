# `zenoh.apk` notes for a phone MCP mesh

Research snapshot: 2026-09-17 UTC. Source examined:
[jameswilsonotr-ship-it/zenoh.apk](https://github.com/jameswilsonotr-ship-it/zenoh.apk).
No APK or native binary is copied into this archive.

## What the existing app actually is

The repository is a Kotlin/Compose Android project for a Zenoh bus explorer
and swarm-node cockpit. Its README describes:

* Android minimum SDK 30, with `INTERNET` and
  `ACCESS_NETWORK_STATE` permissions.
* Client/router and peer modes.
* Configurable Zenoh endpoint and wildcard Key Expressions such as
  `swarm/bus/**`.
* A coroutine heartbeat publisher, subscriber log, throughput diagnostics, and
  a developer-mode console.
* A GitHub Actions workflow that builds a debug APK with JDK 21, Gradle 9.3.1,
  and a generated debug keystore.

The repository is a useful **shape/pattern**, but it is not evidence that a
native Zenoh data plane is currently shipped. The app module comments out its
`org.eclipse.zenoh` dependency and includes local `org.eclipse.zenoh` stubs.
`Session.open`, `put`, and subscription close are no-ops in those stubs. The
view model detects missing JNI and intentionally enters a simulated protocol
flow. In other words, its current green build proves UI and simulation
plumbing, not a live Zenoh connection.

The repository metadata did not surface a root `LICENSE` file in the examined
tree. Resolve licensing before copying code or publishing a derived app. The
Gradle project also includes a secrets plugin and environment-based release
signing configuration; a mesh fork should keep signing material out of source
and use debug-only builds until a separate release process exists.

## Upstream Zenoh pattern

The relevant upstream pieces are:

* [eclipse-zenoh/zenoh-kotlin](https://github.com/eclipse-zenoh/zenoh-kotlin):
  Kotlin API over Rust/JNI. Its current Android README documents
  `org.eclipse.zenoh:zenoh-kotlin-android`, minimum SDK 30, and the two
  network permissions. The repository had commits on 2026-09-15 and reports
  33 GitHub stars in this snapshot. The GitHub API did not map its dual
  EPL-2.0/Apache-2.0 licensing badge to a single SPDX value; read the
  repository license before redistribution.
* [eclipse-zenoh/zenoh-flat-jni](https://github.com/eclipse-zenoh/zenoh-flat-jni):
  the generated/native JNI layer and Android ABI artifacts consumed by the
  Kotlin wrapper. It is the reason a normal consumer build need not compile
  Rust or install the NDK when published artifacts are available. Its current
  main branch was also synced on 2026-09-15.
* [Zenoh Android demo](https://github.com/eclipse-zenoh/zenoh-demos/tree/main/zenoh-android/ZenohApp):
  the upstream demo link called out by `zenoh-kotlin`; use it to validate
  actual Android session setup rather than relying on the local stubs.

There is a version drift worth recording: the org app README mentions
`zenoh-kotlin-android:1.1.0`, while the current upstream README shows `1.1.1`
for its release example and a newer snapshot coordinate in its build notes.
Do not copy a version from prose into a mesh app without checking Maven
Central, the upstream release, and the matching `zenoh-flat-jni` artifact.

## What to steal for an MCP mesh

### 1. Keep Zenoh as the event/data plane, MCP as the command plane

Use Zenoh for low-rate control-plane events and status fan-out, for example:

```text
phone/<node-id>/presence
phone/<node-id>/capabilities
phone/<node-id>/events
phone/<node-id>/audit
phone/<node-id>/command-result/<request-id>
```

An MCP server should remain the authenticated request boundary. It can publish
a command envelope to a phone-specific Key Expression and await a
correlated result. It should not expose a wildcard publisher or turn
arbitrary user text into a Zenoh key.

### 2. Reuse the explicit session state machine

The view model's `DISCONNECTED → CONNECTING → CONNECTED → ERROR` states,
session cleanup, subscriber handles, bounded log history, and diagnostic
counters are good operational patterns for a phone daemon. Add:

* a request ID, origin, capability, and expiry to every command;
* an explicit `DENIED`/`EXPIRED` result;
* replay protection for command IDs;
* bounded payload sizes and per-capability rate limits;
* audit records that do not include SMS bodies or notification text by
  default.

### 3. Prefer routed client mode on a burner

The existing app already models client/router and peer modes. A burner phone
should normally be a Zenoh client to a router on the tailnet. Peer mode and
multicast scouting should be an explicitly enabled lab profile. This limits
discovery and makes the router/Tailscale ACL the place to reason about
reachability.

### 4. Make capability advertisement policy-aware

Publish only the capabilities enabled on that device, not a static list of all
possible tools. A useful record is:

```json
{
  "node": "burner-01",
  "transport": "zenoh-client",
  "capabilities": ["torch", "notify"],
  "sms": "disabled",
  "ui_automation": "disabled",
  "expires_at": "2026-09-17T04:00:00Z"
}
```

MCP tool descriptions and Zenoh capability records must agree. An agent should
not be able to infer an unavailable capability and then fall back to shell or
arbitrary Intent execution.

### 5. Preserve the safe fallback boundary

The org app's simulation mode is useful for CI and UI tests, provided it is
unmistakably labeled. Keep a fake Zenoh transport for tests, but make
production code fail closed when the native session is missing. A simulated
“connected” state must never be allowed to imply that a phone command was
delivered.

### 6. Build native libraries; do not vendor them here

The upstream split between `zenoh-kotlin` and `zenoh-flat-jni` is the pattern to
keep: application code consumes a versioned artifact, while native ABI
packaging happens upstream. Do not commit `lib*.so`, an APK, a model, or a
generated Gradle cache to this research/archive repository. Pin and verify the
artifact in a future application repository.

## Proposed next-agent handoff

1. Start with a no-side-effect capability: phone presence or torch state.
2. Build a fake Zenoh router test around request/result correlation.
3. Add the MCP-to-Zenoh adapter only after the allowlist and audit schema are
   fixed.
4. Keep SMS, notification reads/replies, camera, location, contacts, and UI
   automation disabled in the default profile.
5. Compare the broker transport against
   [`khimaros/mimic`](https://github.com/khimaros/mimic) and the typed modules
   in [`stixez/droid-mcp`](https://github.com/stixez/droid-mcp), but do not
   mix their code or licenses without review.
