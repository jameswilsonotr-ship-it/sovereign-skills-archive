# Pixel HUD contract

Status: **draft — documentation only; not a live integration**

This document defines the local Pixel HUD boundary. It does not claim that a
server is listening or that a Pixel client is available.

## Endpoint

| Item | Contract |
| --- | --- |
| Transport | WebSocket |
| URL | `ws://127.0.0.1:8088/nav/hud` |
| Host scope | Loopback only |
| Path | `/nav/hud` |
| Wire mode | `RAWV` |
| Memory budget | Process RSS must remain **less than 35 MB** |

The URL and path are exact. A client must not silently fall back to another
host, port, path, or transport. A failed connection is reported as
`hud_unavailable`; it is not evidence that the endpoint exists.

## RAWV frame contract

`RAWV` is the wire mode for a HUD snapshot. A producer must preserve raw
values: it must not normalize, round, clamp, or silently substitute missing
values. The frame envelope is:

```json
{
  "mode": "RAWV",
  "seq": 0,
  "value": {},
  "burn": {}
}
```

- `mode` is required and must equal `RAWV`.
- `seq` is a producer-assigned, monotonically increasing sequence number.
- `value` contains the raw HUD value.
- `burn` contains the raw included-burn value.
- Additional fields are not part of this contract unless explicitly added
  here.

The object above describes the contract shape; it is not a fixture or a claim
that these values are currently emitted.

## Atomic included burn

The included burn is part of the HUD snapshot, not a follow-up update:

1. `value` and `burn` are captured from the same logical state.
2. They are serialized and sent as one WebSocket message.
3. A snapshot with no valid `burn` is rejected in full; the producer must not
   send a partial HUD frame and then repair it later.
4. A client applies a frame atomically. It either accepts the complete
   snapshot or leaves the previous snapshot unchanged.

The failure result for a missing or invalid included burn is
`burn_missing`. It must not be represented as an empty object that looks like
valid RAWV data.

## Resource invariant

The process serving this bridge must keep resident set size (RSS) strictly
below `35 MB` while the HUD connection is active. For a byte-based
measurement:

```text
rss_mb = rss_bytes / 1_000_000
rss_mb < 35
```

The limit includes connection state, frame buffers, serialization overhead,
and retained snapshots. A producer must bound queues and discard or reject
work before crossing the limit. It must not satisfy the limit by omitting
the included burn or by changing the RAWV mode.

If the budget cannot be maintained, the producer closes the HUD stream and
reports `rss_budget_exceeded`. It must not continue emitting frames in a
degraded, partial format.

## Client behavior

- Connect only to the exact endpoint above.
- Require `mode: "RAWV"` and a valid `burn` before applying a frame.
- Apply each accepted frame once, in sequence order.
- Treat a sequence gap, malformed frame, or invalid burn as a rejected
  snapshot.
- Keep the last accepted snapshot on a rejected frame.
- Surface `hud_unavailable`, `burn_missing`, and `rss_budget_exceeded`
  distinctly.

## Acceptance checklist

- [ ] The connection target is exactly
      `ws://127.0.0.1:8088/nav/hud`.
- [ ] Frames use the `RAWV` mode token.
- [ ] Raw `value` and included `burn` come from one logical snapshot.
- [ ] The snapshot is delivered and applied atomically.
- [ ] Partial or repaired-later frames are rejected.
- [ ] RSS remains strictly below `35 MB`.
- [ ] No alternate endpoint or fallback transport is introduced.
