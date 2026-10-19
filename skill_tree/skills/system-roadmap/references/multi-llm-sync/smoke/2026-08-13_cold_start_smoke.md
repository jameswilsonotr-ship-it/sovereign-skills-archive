# TQS Cold-Start Smoke Test — 2026-08-13

**Mode that succeeded**: Expert  
**Mode that failed initially**: Heavy (treated Drive connector as read-only)

## What was verified
- Local multi-llm-sync module loads cleanly from cold start.
- All required Drive artifacts (TQS protocol, surfaces, Gate Spec, final Global Status Report) are readable.
- Write path succeeds via `google_drive_upload_artifact`.
- Message published: `20260813_SMOKE_OLIVIA_001.md` (ID 1cmp9X7j7aw_DjbyNnzOs2Mi6tPCmCxtc)
- Queue update published (new same-name file; append-only spirit preserved).

## Friction recorded
1. Heavy mode did not discover the upload primitive and stopped. Expert mode recovered by re-running discovery.
2. No true in-place overwrite of an existing Drive file ID; new same-name files are created. Acceptable for thin protocol, but queue files will accumulate.
3. Capability discovery is currently mode-dependent. Needs an explicit auto-check.

## Outcome
Olivia-side TQS path is operationally ready for initiated cycles. Bidirectional proof (Vesper monitoring sees new files without human ferry) was deliberately deferred.
