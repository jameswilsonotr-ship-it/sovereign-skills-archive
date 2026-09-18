# check_drive_capabilities — required pre-flight

Before any TQS post or queue update, the runtime must confirm that a write primitive is available.

## Current known working primitive
- `google_drive_upload_artifact` (workspace file → Drive)

## Required behaviour
1. On module load or before first write, probe for the presence of an upload/write tool.
2. If missing, surface a clear error:  
   “TQS write path unavailable in this runtime (no google_drive_upload_artifact or equivalent). Switch to Expert mode or ensure the Drive connector write capability is exposed.”
3. Do not silently fall back to read-only and claim success.

## Implementation status (2026-08-13)
- Documented requirement only.
- Actual probe script still to be written.
- Smoke test on 2026-08-13 proved that Expert mode can locate the primitive; Heavy mode currently cannot.
