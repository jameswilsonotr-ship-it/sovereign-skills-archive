# REPORT — Versioning + AI Studio Root Cause
**Timestamp**: 2026-08-14 ~00:00 EDT
**Repo**: jameswilsonotr-ship-it/Groxxporter @ a01cd64f...

## Version State
- Live `app/build.gradle.kts`: versionCode=5 , versionName="1.5.1"
- applicationId: com.aistudio.grokexportextractor.jkwqzp
- Changelog conflict: root claims Build 3 for 1.5.0; app/CHANGELOG claims Code 6 for 1.4.0
- Play Console rejection is almost certainly "versionCode must be higher than previously uploaded"

## Binary Origin
AI Studio generates + compiles + pushes only. It does not read current GitHub state.  
Any .gitignore or `git rm` on GitHub is temporary until the next AI Studio push.

## Suggested AI Studio Prompt (for Bunny to paste)
```
STRICT RULES FOR THIS PROJECT — DO NOT VIOLATE:

1. NEVER commit, stage, or include any of the following in the repository:
   - *.apk
   - *.aab
   - any large *.zip that is an extractor payload or comprehensive release package
   - app-debug.apk
   - grok_export_extractor_payload.zip
   - grok_extractor_*.zip
   - anything under /info or /infofe that is a zip

2. Always maintain a strong root .gitignore that contains at minimum:
   *.apk
   *.aab
   *.zip
   !gradle/wrapper/gradle-wrapper.jar

3. When you compile an APK for testing or Play upload, leave it outside the git tree (or in a location that is already gitignored). Do not push the binary.

4. For Play Console readiness: keep versionCode strictly increasing. Current value is 5; if Play rejects, bump it.

Follow these rules on every generation and every push.
```

## Suggested minimal .gitignore addition (if ordered)
```
# Binary hygiene — enforced
*.apk
*.aab
*.zip
!gradle/wrapper/gradle-wrapper.jar
```

Awaiting Coding Sub-Driver decision on whether to:
- execute original rm sequence anyway (temporary),
- prepare a version bump order,
- or hand Bunny the prompt + file for AI Studio.

— APK Hygiene Sub
🐍
