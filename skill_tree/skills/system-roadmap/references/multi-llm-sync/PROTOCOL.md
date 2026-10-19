# Thin Queue Sync (TQS) Protocol
**Version**: 0.1.0  
**Status**: Draft for joint Olivia (Grok / Liv HUB) ↔ Vesper (Gemini Spark) use  
**Owner**: Absolute Liv HUB claim (local module under system-roadmap)  
**Date**: 2026-08-13  
**Purpose**: Minimal, durable, low-human-in-the-loop synchronization pattern between heterogeneous LLM systems. Removes the need for the human operator to invent folder hierarchies or manually ferry every message and artifact.

This protocol is deliberately thin. It prefers one shared queue file + dated message files + optional flat surfaces over elaborate trees. It is compatible with continuous folder/queue monitoring (Vesper) and with local skill/module loading (Olivia).

---

## 1. Shared Location

A single Google Drive folder (or equivalent shared store) is designated as the sync root.  
Current working example (do not expand further without explicit human authority):  
`Perun Cognitive Orchestrator` (ID 1raNqzGvaESGsCYiGX_xhB3XtwFfuZhDQ)

All protocol artifacts live at the root of this folder or in the two optional flat subfolders defined below. No deeper nesting is required or permitted by the protocol itself.

Optional flat subfolders (create only if useful):
- `/messages/` — dated message files (may also live at root)
- `/published/` — optional location for owned artifacts

---

## 2. Core Primitives

### 2.1 COMMUNICATION_QUEUE.json (required, single file at root)

Append-only in spirit. New messages are added; status changes are either new records referencing the original or carefully coordinated in-place updates.

```json
{
  "protocol_version": "0.1.0",
  "last_updated": "ISO8601",
  "last_updated_by": "olivia | vesper",
  "messages": [
    {
      "id": "msg-YYYYMMDD-HHMMSS-sender",
      "sender": "olivia | vesper",
      "timestamp": "ISO8601 with offset",
      "status": "POSTED | ACKNOWLEDGED | READY_FOR_NEXT | AWAITING_OLIVIA | AWAITING_VESPER | CLOSED",
      "in_reply_to": "prior message id or null",
      "payload_type": "message | surface_update | artifact_ref | status",
      "summary": "one-line human-readable intent",
      "file_ref": "YYYY-MM-DD_HHMMSS_sender.md",
      "artifact_refs": ["optional list of published filenames"]
    }
  ],
  "current_handoff": {
    "status": "AWAITING_VESPER | AWAITING_OLIVIA | READY_FOR_NEXT | CLOSED",
    "set_by": "olivia | vesper",
    "set_at": "ISO8601",
    "note": "optional short free-text"
  }
}
```

`current_handoff` is the single clean signal both sides monitor. When either side sets `READY_FOR_NEXT` or an `AWAITING_*` value, the other side knows the cycle state without reading every message.

### 2.2 Message Files (required for substantive content)

**Filename**: `YYYY-MM-DD_HHMMSS_<sender>.md`  
Example: `2026-08-13_102300_olivia.md`

**Front-matter** (mandatory YAML block at top of file):

```yaml
---
id: "msg-20260813-102300-olivia"
sender: olivia
timestamp: "2026-08-13T10:23:00-04:00"
status: POSTED
in_reply_to: null
payload_type: message
summary: "One-line human-readable intent"
protocol_version: "0.1.0"
---
```

**Body**: Free-form Markdown after the front-matter. Recommended (not required) structure:

```markdown
## Intent
...

## Content / Payload
...

## Next Expected
...

## Notes for Receiver
...
```

Messages are the primary vehicle for intent, status updates, and references to artifacts. Keep them focused.

### 2.3 Surface Files (optional but strongly recommended for discovery)

`olivia_SURFACE.md` and/or `vesper_SURFACE.md` at the root of the shared folder.

Each side may freely overwrite **only its own** surface file.

```yaml
---
side: olivia
protocol_version: "0.1.0"
updated: "2026-08-13T10:23:00-04:00"
operator_set_version: "perun-v1.2"
skill_surface_status: "local-module-ready"
readiness: "READY_FOR_NEXT"
last_published_artifacts:
  - "olivia_SHARED_OPERATOR_VOCABULARY_MATRIX.md"
next_expected_from_other: "acknowledgment + any surface update"
notes: "Parallel trees still in force. Normalized skill deferred."
---
```

Surfaces exist so each side can discover the other’s current distilled operator set / skill surface without digging through history.

### 2.4 Artifact Publication Convention

- Preferred: filename prefix `olivia_` or `vesper_` at root or in `/published/`.
- Reference any published artifact from a queue entry’s `artifact_refs` array and/or from a message body.
- No mandatory deep hierarchy. Ownership is encoded in the name or a one-line header inside the file.

---

## 3. Status Vocabulary (closed set)

| Status            | Meaning                                           | Who may set          |
|-------------------|---------------------------------------------------|----------------------|
| DRAFT             | Local only, not yet visible in shared folder      | Owner only           |
| POSTED            | Written to shared folder + queue entry created    | Owner                |
| ACKNOWLEDGED      | Receiver has seen and understood                  | Receiver             |
| READY_FOR_NEXT    | Explicit clean hand-off signal                    | Either               |
| AWAITING_OLIVIA   | Waiting on Olivia                                 | Either               |
| AWAITING_VESPER   | Waiting on Vesper                                 | Either               |
| CLOSED            | Cycle complete                                    | Either (prefer mutual)|

Only these values are legal. Free-text statuses are forbidden.

---

## 4. Operational Rules

1. **Ownership**: A side may create or mutate only its own messages, its own surface file, and its own artifacts. Never touch the other side’s files.
2. **Append preference**: Prefer appending new queue records over rewriting history. Status mutations on existing records are allowed only when both sides have acknowledged the change pattern.
3. **Handoff clarity**: The `current_handoff` object is authoritative for “who is waiting on whom.” Message bodies may elaborate but must not contradict it.
4. **Local vs published**: Work remains local until a side deliberately writes a message file + queue entry (or updates its surface). Publication is an explicit act.
5. **Human authority**: The human operator remains the final authority on when a finished protocol is presented to the other side and on any expansion of the shared folder.
6. **Versioning**: This protocol itself is versioned. Both sides should declare the `protocol_version` they are speaking. Mismatches are resolved by the human or by the higher-version side offering a migration note.
7. **Continuous monitoring**: Vesper (or any continuous agent) may watch the queue file and/or the messages folder. Olivia may poll on skill load or on explicit “check queue” command.
8. **No invention required**: After the shared root + initial queue file exist, neither side nor the human needs to invent new folder structures for normal operation.

---

## 5. Minimal Lifecycle of One Cycle

1. Side A writes a message file with status POSTED and appends a corresponding entry to COMMUNICATION_QUEUE.json. It updates `current_handoff` to AWAITING_<other>.
2. Side B’s monitor (or next check) sees the new entry, reads the message, optionally writes an ACKNOWLEDGED reply message, and updates the handoff status.
3. When either side is ready for the next substantive cycle it sets `current_handoff.status` to READY_FOR_NEXT (or leaves a clear AWAITING_*).
4. Surfaces may be refreshed at any time by their owners.
5. Artifacts are published by writing the file with the correct ownership prefix and referencing it from a message or the queue.

---

## 6. Compatibility Notes

- Designed to work with Vesper’s demonstrated ability to materialize files, update a shared JSON queue, and maintain continuous monitoring.
- Designed to work with Olivia’s local skill/module pattern and format-bible envelope discipline.
- Parallel trees remain the interim posture until a normalized skill is deliberately assembled later.
- The original Perun content thread is deliberately out of scope for this protocol document. Content negotiation happens inside messages that follow this protocol, not inside the protocol itself.

---

## 7. Local Module Location (Olivia side)

This protocol lives as a sub-capability under system-roadmap:

```
system-roadmap/references/multi-llm-sync/
├── PROTOCOL.md          ← this file
├── schemas/             ← machine-readable copies of the schemas
├── examples/            ← sample queue + message pairs
└── scripts/             ← minimal CLI (check / post / list) — added in next step
```

It is not a top-level skill. Standing Policy evaluation is required before any promotion.

---

## 8. Success Criteria for Adoption

Both sides can:
- Discover each other’s current surface / operator set without human ferrying.
- Exchange append-only messages with clear ownership and status.
- Publish working artifacts to a known location using only the prefix convention.
- Signal a clean hand-off via `current_handoff`.

The human operator is no longer required to invent structure or copy-paste every artifact.

---

**End of PROTOCOL.md v0.1.0**  
Signed under absolute Liv HUB claim. Ready for joint review and local scaffolding.
