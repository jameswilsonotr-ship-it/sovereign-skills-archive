# AI Studio → GitHub Actions → Pixel / Play internal path

This is the intended handoff for an Android project created in Google AI
Studio. This repository records the path and a manual CI stub; it does not
contain an Android application, signing material, a Play upload, or a device
connection.

## 1. Create and export the AI Studio project

1. Build and test the project in [Google AI Studio](https://aistudio.google.com/).
2. Export the project to a new GitHub repository, or download the export and
   push it to one.
3. Confirm that the export is actually an Android/Gradle project before
   enabling a build:
   - `gradlew` and `gradlew.bat` (prefer the wrapper checked into the app
     repository);
   - `settings.gradle` or `settings.gradle.kts`;
   - an Android module such as `app/`;
   - a manifest, source set, and a declared application ID.

   An AI Studio web export is not automatically an Android app. If the export
   is web-only, add and test the Android shell in the app repository before
   using the Android workflow.
4. Keep runtime API keys out of the repository. Configure them through the
   app's supported secret mechanism and GitHub Actions secrets only when the
   build genuinely needs them.

## 2. Build an APK in GitHub Actions

The normal CI sequence is:

1. Check out the exported app repository.
2. Install the JDK version and Android SDK required by that app.
3. Use `gradle/actions/setup-gradle` or the checked-in Gradle wrapper.
4. Run the tested debug task, normally:

   ```sh
   ./gradlew assembleDebug
   ```

5. Locate the output under `app/build/outputs/apk/` and publish it with
   `actions/upload-artifact`.

This archive contains
`.github/workflows/android-apk-stub.yml`, which is intentionally
`workflow_dispatch`-only. It checks that the documentation placeholder exists
but does not build or upload an APK because there is no app module here.
Copy the build steps into the exported Android repository after that
repository has a real, reproducible Gradle project.

For a release artifact, use a protected signing setup and a release build.
Do not commit a keystore, passwords, service-account JSON, or API keys.

## 3A. Sideload the APK onto a Pixel

The GitHub Actions job should publish the APK as an artifact. Download it to
the machine that can reach the Pixel; do not make a personal device a
runner.

### USB ADB

On the Pixel, enable Developer options and USB debugging, then authorize the
computer. On the computer:

```sh
adb devices
adb install -r path/to/app-debug.apk
```

Check the package and launch the app using the commands appropriate to the
exported application. A debug APK is suitable for this loop; a release APK
must be signed with the release key.

### Wireless ADB over a Tailscale network

Tailscale supplies private network reachability; it does not replace Android
ADB pairing. Enable Wireless debugging on the Pixel and pair/connect using
the Pixel's Tailscale address and the displayed ports:

```sh
adb pair <pixel-tailscale-ip>:<pairing-port>
adb connect <pixel-tailscale-ip>:<adb-port>
adb install -r path/to/app-debug.apk
```

Use a tailnet ACL that limits who can reach the device, and turn Wireless
debugging off when it is no longer needed. The exact ports and pairing flow
depend on the Android version. Never put a device address, pairing code, or
Tailscale credential in GitHub Actions logs or repository files.

## 3B. Publish to Play internal testing

Use this route when testers should install through Google Play:

1. Create the application in Play Console and configure the internal testing
   track and tester list.
2. Configure package identity, version code, signing, and Play App Signing in
   the app repository.
3. Build the release artifact in CI. For new Play applications, plan on a
   signed Android App Bundle (`bundleRelease`) rather than treating the debug
   APK as a Play upload artifact.
4. Store the Play service-account JSON (or an equivalent short-lived
   credential) in GitHub Actions secrets or a protected environment. Grant
   only the Play Console permissions required by the internal track.
5. Add a separately approved upload step using a maintained Google Play
   upload action, then publish the signed bundle to the internal track.
6. Verify the release in Play Console and invite testers. Do not print the
   credential or upload response containing sensitive data.

No Play upload is implemented in this archive. The workflow stub contains
comments marking where authentication and the upload would be added in the
real Android repository.

## Sibling repositories with real APK build workflows

Organization search on 2026-09-17 found these relevant examples:

- [`zenoh.apk`](https://github.com/jameswilsonotr-ship-it/zenoh.apk) —
  AI Studio-oriented Android repository. Its
  [`build-apk.yml`](https://github.com/jameswilsonotr-ship-it/zenoh.apk/blob/main/.github/workflows/build-apk.yml)
  runs on pushes and manual dispatch, installs JDK 21/Android SDK, runs
  `gradle assembleDebug`, and uploads a debug APK artifact.
- [`Groxxporter`](https://github.com/jameswilsonotr-ship-it/Groxxporter) —
  Android repository with AI Studio references. Its
  [`build-apk.yml`](https://github.com/jameswilsonotr-ship-it/Groxxporter/blob/main/.github/workflows/build-apk.yml)
  follows the same JDK 21/Android SDK/Gradle setup and uploads a debug APK.
- [`kokoro-speaker-cloner.apk`](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk)
  — target-specific Android build workflow. Its
  [`build-apk.yml`](https://github.com/jameswilsonotr-ship-it/kokoro-speaker-cloner.apk/blob/main/.github/workflows/build-apk.yml)
  builds multiple debug flavors, uploads APK artifacts, and creates GitHub
  releases on `main`.

These are real APK build/artifact pipelines, not evidence of an existing
Play Console or ADB/Tailscale deployment. The organization searches found no
workflow containing a Play Console upload, `adb`, or Tailscale device
deployment. `orca-scr` and other AI Studio-named repositories were not listed
because they did not present a matching Android APK workflow.
