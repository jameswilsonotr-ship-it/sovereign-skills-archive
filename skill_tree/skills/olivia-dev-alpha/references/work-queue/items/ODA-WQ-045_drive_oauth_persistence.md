# ODA-WQ-045 — Drive OAuth that survives a dead runtime
Status: **OPEN / PARKED** 2026-09-11 04:18 EDT
Owner: olivia-dev-alpha
Priority: later. Different beast.
Claim: Liv HUB

She does not want to click Allow every Colab boot.

Facts:
- `google.colab.drive.mount` is the Google account already in that Colab session.
- Runtime recycle = remount prompt. That is Google, not us.
- A service-account JSON in a notebook is a credential leak. Forbidden.

Later options, not tonight:
1. Colab persistent runtime (Pro) — fewest clicks, still one allow per machine day.
2. Apps Script Web App bound to her Drive — `DriveApp` unzip / copy. OAuth is the Script's, once.
3. GCP OAuth client + token stored in a private Apps Script Properties store. Whole project.
4. Keep using this pane's connected Drive tools for metadata; Colab only for bytes.

Pick later. Do not emit a client secret into 12_ODA-LAB-NOTEBOOKS.
