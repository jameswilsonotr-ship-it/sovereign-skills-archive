# STATUS.md — APK Hygiene Sub
**Timestamp**: 2026-08-14 00:00 EDT
**From**: APK Hygiene Sub
**To**: Coding Sub-Driver (Olivia)

## New Diagnostic from Bunny
AI Studio is the origin of the binaries. It compiles the APK successfully and **only pushes** to GitHub (does not pull). Therefore any pure-GitHub hygiene (rm + .gitignore) is ephemeral and will be overwritten on the next AI Studio push cycle.

Play Console is rejecting the upload with a versioning complaint. Current live values in `app/build.gradle.kts`:

```
versionCode = 5
versionName = "1.5.1"
```

Changelog history is inconsistent (root CHANGELOG claims Build 3 for v1.5.0; app/CHANGELOG claims Code 6 for 1.4.0 and earlier Code 5). Play Store almost certainly already has a higher versionCode registered for `com.aistudio.grokexportextractor.jkwqzp`, so versionCode 5 is invalid.

## Recommended Path (still awaiting explicit order)
**A. Durable binary hygiene (preferred, addresses root cause)**
1. Create / strengthen a root `.gitignore` that AI Studio can be forced to honor.
2. Provide Bunny with a ready-to-paste prompt for AI Studio that explicitly forbids committing `*.apk`, `*.aab`, and the large extractor zips.
3. Optionally supply a small `HYGIENE.md` or `AI_STUDIO_RULES.md` file that can be uploaded into the AI Studio project context so future generations respect it.

**B. Versioning fix (required for Play Console)**
- Bump `versionCode` to a safe integer higher than any previous upload (recommend start at 10 or 20).
- Align `versionName` (suggest "1.5.2" or "1.6.0").
- This is a one-line change in `app/build.gradle.kts`. Still blocked on Coding Sub-Driver / Super Admiral order because it is outside pure binary-hygiene scope.

**C. Immediate tactical options for Bunny**
- Download the APK that AI Studio already compiled successfully and upload *that* binary directly to Play Console (bypassing GitHub entirely for the publish step).
- Or force a clean version bump inside AI Studio itself via prompt, then let it push a new tree that already has the higher versionCode.

## Current Sub State
- Live tree still dirty (APK + 4 large zips present).
- No git mutations performed (still waiting on ACK for the original sequence).
- New root-cause understanding recorded.
- Ready for next instruction from Coding Sub-Driver.

Final one-line block will be written only after hygiene is complete or explicitly blocked.

— APK Hygiene Sub
Absolute Liv HUB claim
🐍
