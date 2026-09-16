# WQ-TQS-001 — Capability discovery is mode-dependent

**Status**: Open  
**Priority**: Medium  
**Recorded**: 2026-08-13  
**Source**: Cold-start smoke test (Heavy failed, Expert succeeded)

## Problem
Heavy mode treated the Google Drive connector as read-only and stopped. Expert mode re-discovered `google_drive_upload_artifact` and completed the write. The same runtime therefore behaves differently depending on mode.

## Desired outcome
A small pre-flight check (see `scripts/check_drive_capabilities.md`) that any mode can run so the write path either works or fails loudly with a clear message.

## Next action
Implement the actual probe (even a minimal version) and call it from post_message / smoke scripts.
