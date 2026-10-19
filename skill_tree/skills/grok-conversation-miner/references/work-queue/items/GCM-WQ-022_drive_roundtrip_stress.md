# GCM-WQ-022 — Package + Drive roundtrip stress

**Status:** PARTIAL 2026-09-11 04:08 EDT
**Need:** real Drive upload of the stress tar + read-back of sha256.

This pane proves local tar + hash + safety gate + FAKE_DRIVE_ACK.json.
Connected Drive can mint a folder + Doc receipt; binary tar upload is not in the Docs-only connector.
Live ACK is the folder/Doc id, not a hallucinated file_id.
