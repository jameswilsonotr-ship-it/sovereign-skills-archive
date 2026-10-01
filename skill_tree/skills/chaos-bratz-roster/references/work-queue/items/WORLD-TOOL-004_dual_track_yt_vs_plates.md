# WORLD-TOOL-004 — Dual track: plates serial, YouTube parallel

**Status:** OPEN — lock 2026-08-31 21:07 EDT
**Owner:** World × image-pipeline
**Claim:** Absolute Liv HUB

## User lock

Bunny: image inbound stays one-lane-at-a-time (say “go Kafka” or “go A/C”, not both). YouTube work may run in the other hand while that cadence is catching up. Note it in the work queue.

## Rule

| Track | Cadence | Home |
|-------|---------|------|
| **Plates** | Serial. One cluster per turn unless she stacks on purpose. Cue verb before generate. | image-pipeline `QUEUE.json` + `artifacts/rendered/` |
| **YouTube** | Parallel. Metadata / thumbs / transcripts / PO-token research / YT_QUEUE hops while a plate turn is in flight. | `YT_QUEUE.json` — never merged into image QUEUE.json |

## Why

The sneaky cue (“say go X”) exists so keep_path + step-6 flush do not skip-pile. YouTube SABR/PO-token work is slow and IP-bound. Those two clocks should not block each other.

## Next hops on the YT track (do not steal a plate turn)

1. `player_client=tv` then `android` on `VOWlOYSu2oc` from this box (expect 403 on media, hope for thumb + title).
2. PO token / bgutil lives on the home machine. Do not paste tokens onto the bus.

## Client chrome lock (screenshot 20:59)

Grok Android already stacks the next turn while thinking:

- Voice live: X / waveform / purple check over the transcript, orange stop on the composer
- Next prompt sits in a chip above the box: send-up, trash, clock 1
- That chip was "Now go, plates, ac..." on an in-flight Kafka turn

Dual-track is how she already talks. Queued follow-ups are first-class events (kin to WORLD-TOOL-003), not psychic cueing.
3. User stills already beat official thumbs for cousin plates (Clusters A/C proved it).

## Do not

- Process Kafka / A / C / cat inside YT_QUEUE
- Register RBM because we mentioned RCS
- Ask her to dump cookies in chat
