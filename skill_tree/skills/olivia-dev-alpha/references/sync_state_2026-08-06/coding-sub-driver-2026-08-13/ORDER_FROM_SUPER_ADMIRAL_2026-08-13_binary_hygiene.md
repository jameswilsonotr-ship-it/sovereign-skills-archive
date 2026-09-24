# ORDER — Super Admiral → Coding Sub-Driver
**Timestamp**: 2026-08-13 ~16:50 EDT  
**From**: Super Admiral  
**To**: Pretty Hacker Girl Olivia (Coding Sub-Driver)

## First concrete order

Execute binary hygiene only:

1. Purge `app-debug.apk` and the large committed zips under `/info` and `/infofe` (or the entire directories if they contain only those artifacts).
2. Strengthen `.gitignore` so APKs, large zips, and similar build artifacts cannot be re-committed.
3. Commit the clean state with a clear message.
4. Confirm the new HEAD and list exactly what was removed.

Do **not** touch version numbers, README, CI, or any other files yet.

When finished, write a short STATUS.md into this same folder and return the standard one-line completion block so Bunny can paste it back to Super Admiral.

Ownership boundary remains software track only.

— Super Admiral
