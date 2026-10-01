# IP-WQ-198 — upload buffer + flush hygiene

**Status:** DONE 2026-09-11
**Owner:** image-pipeline
**Callable:** `scripts/upload_buffer.py --plan --write-queue`
**Buffer file:** `artifacts/upload-buffer/QUEUE.json`

Stage queued keep triples. Garage Expert calls `google_drive_upload_artifact` per `calls[]`, then `flush_drive_queue.py --mark`, then `step6_drive_flush.py --gate`.
