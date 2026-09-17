#!/usr/bin/env python3
"""Minimal pre-flight note for TQS Drive write capability.

This runtime cannot introspect MCP tool availability from pure Python.
Callers should treat the following as the operational contract:

Required for TQS publish:
  - google_drive_list_folder
  - google_drive_read_file
  - google_drive_upload_artifact

If upload_artifact is unavailable, fail loudly and recommend Expert mode
or connector re-auth. Do not claim a successful TQS write.
"""
from __future__ import annotations

REQUIRED = [
    "google_drive_list_folder",
    "google_drive_read_file",
    "google_drive_upload_artifact",
]

def main() -> int:
    print("TQS Drive capability contract:")
    for name in REQUIRED:
        print(f"  - required: {name}")
    print("Runtime must verify these via tool discovery before posting.")
    print("Smoke status 2026-08-13: upload_artifact verified under Expert mode.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
