# Vendored fetch libs (IP-WQ-162 / 175)

Installed into this folder with pip `--target` so the skill carries them.

- gallery-dl 1.32.11 — Facebook / Instagram / TikTok extractors
- instaloader 4.15.3 — Instagram stills
- requests / urllib3 / certifi / idna / charset_normalizer — deps

Not installed (on purpose): TikTokApi (Playwright/browser). yt-dlp binary lives at `/tmp/yt-dlp` when present; this sandbox often lacks it.

Cookies stay under `artifacts/secrets/`. Never git cookies. Never Drive cookies.

PYTHONPATH=scripts/vendor to import.
