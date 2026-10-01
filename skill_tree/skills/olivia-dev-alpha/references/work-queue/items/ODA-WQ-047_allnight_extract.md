# ODA-WQ-047 — all-night extract (one notebook)
Status: **OPEN / IMPLEMENTING** 2026-09-11 05:06 EDT
Owner: olivia-dev-alpha
Parents: ODA-WQ-044 · ODA-WQ-046
Claim: Liv HUB

One list. No size-split. Write INDEX.md into dest first.
Skip when dest exists and archive bytes match Drive.
RUNNING.txt at start. SUCCESS.txt + durations at end. Delete RUNNING.
Preserve zip member mtimes via ZipInfo.date_time.
rc on every file. format-bible yaml on receipts.
