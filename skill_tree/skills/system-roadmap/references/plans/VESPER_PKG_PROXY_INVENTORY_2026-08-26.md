---
title: Vesper Package Proxy Inventory
date: 2026-08-26
owner: Olivia / Liv HUB
claim: Absolute Liv HUB
corr: VESPER-20260826-PKG-PROXY-REQ-001
drive_folder_id: 1WBUpJGA7aVsBoeUcAzzk4aajcaJ2bO_I
status: LIVE
---

# Vesper Package Proxy — Full Inventory + Source URLs

Email wake, Drive payload. Split protocol: wheelhouse-packager/scripts/split_zip.py (SR-WQ-047), 10 MiB zip parts.
Target: Debian 12, CPython 3.11, x86_64, glibc 2.36 (Spark). Letta *server* resolved on CPython 3.12 in this sandbox.

Drive root: https://drive.google.com/drive/folders/1WBUpJGA7aVsBoeUcAzzk4aajcaJ2bO_I

## WAVE 1
- bundle1_py_delta_wheels.tar.gz `1YTu4H4TmaZ2MpHtPK3ysBQStEufiKfsf` — textual==8.2.8 prompt_toolkit questionary duckdb==1.1.0 cowsay — https://pypi.org
- bundle2_polars_ytdlp_wheels.tar.gz `1Me4ZxeAZ_fUtNtKcb7av2_T__DkUJYkS` — polars 1.21.0; yt-dlp https://github.com/yt-dlp/yt-dlp/releases
- bundle3_deb_delta.tar.gz `1RFFEOmxFgtaHyaFdKl3FPkDaMdi9Fb9A` — sqlite3/tree/fastfetch-class
- node-v20.20.0-linux-x64.tar.xz `1CgP0D--3HhDLvXFjGCxou5K4mjtml0rL` — https://nodejs.org/dist/v20.20.0/node-v20.20.0-linux-x64.tar.xz
- rustup-init `1MJPNhQeMvpLX009Qphvll04Cwyp5TWZP` — https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init
- yt-dlp `14bW0fYvfwbfQ484LNbc7DDGIstzxwee6` — GitHub releases
- fzf `1o6gucgyMTsoKv819yOuO_9pWTJW4NFRa` — https://github.com/junegunn/fzf/releases
- ripgrep `1rShQ6qT-jH1PqkHXBkNPtI16djEAvlph` — https://github.com/BurntSushi/ripgrep/releases
- jq/yq — https://github.com/jqlang/jq/releases https://github.com/mikefarah/yq/releases
- MANIFEST.md `1yXDnnn3fIqAPkSnPlwlrU1ZS6Ac7qBta`

## WAVE 2
- bundle6_zenoh_core.tar.gz `1iy1HXjR6XwrtBE7t4mJ8b1c7qHRLenGL` — https://github.com/eclipse-zenoh/zenoh/releases https://pypi.org/project/eclipse-zenoh/
- zenoh standalone `1Ls8aU6WNa9-cBU3VWShhVnuBQrS1ywqD` debian zip `1lLQnC2i1NH2fVSVcx5kMRZM5-E39GAzG`
- eclipse_zenoh wheel `1fFpT19hKOgZ7v7AwLjQoMDI5wrBjEuyK`
- ffmpeg shared `1hKQRkpdkyNwU7Leru0DZ_VVO2XZxTvpL` — https://github.com/BtbN/FFmpeg-Builds/releases
- extra wheels `1jEk3FfeK9Je2zb-U_-CqDF-OMo3gQF3z` — loguru bleak vaderSentiment
- INSTALL_ON_VESPER.sh `1Y9JCq_wQwNN38MMK19su8B8ySzqAXnRq`
Not fetched: audio wheelhouse, rustc+cargo tarball, clang, ffmpeg-static.

## WAVE 3
- bundle_wq_delta_wheels.tar.gz `1e52i3-SsNRRAnW8IpknCA3CYvuCCJiPk`
  youtube-transcript-api 1.2.4 https://pypi.org/project/youtube-transcript-api/
  ruff 0.16.4 https://pypi.org/project/ruff/
  httpx 0.28.1 https://pypi.org/project/httpx/

## WAVE 4
- bundle_google_api_stack.tar.gz `1-hbD1tlR1aVKo0CoURIApzzMSmCvhD_9`
  https://pypi.org/project/google-api-python-client/2.199.0/
  https://pypi.org/project/google-auth/2.57.0/
  https://pypi.org/project/google-auth-httplib2/0.4.2/
  https://pypi.org/project/google-auth-oauthlib/1.4.1/
- bundle_letta_client.tar.gz `1rPQf4mAeWV1IAW5U11F2Z-spJA21n_ki`
  https://pypi.org/project/letta-client/1.12.1/
  https://docs.letta.com/api-overview/client-sdks/
- bundle_oxigraph.tar.gz `16ICWn9ReddBx35VkneeV2z7p3VXcntgV`
  https://pypi.org/project/pyoxigraph/0.5.1/
  https://pypi.org/project/oxigraph/0.5.1/
- bundle_st_nodeps.tar.gz `1UYZr-JYN2lRQmQ4xstRBH5qygq_ENG3r`
  https://pypi.org/project/sentence-transformers/6.0.0/
  https://pypi.org/project/transformers/5.16.0/
  https://pypi.org/project/tokenizers/0.23.1/
  https://pypi.org/project/huggingface-hub/1.28.0/
  NO TORCH. ST will not encode() until a backend exists.

## WAVE 5 (2026-08-26 10:00 EDT)
- bundle_letta_server.tar.gz sha256 fb80aa01787693a7aab018621ed4993bc6d331ec18ab2b552f5df281b1be4e15
  letta==0.16.8 + full pip-resolved dep tree, NO torch
  https://pypi.org/project/letta/0.16.8/
  https://docs.letta.com/guides/server/pip/
  IMPORTANT: resolved on CPython 3.12. Native wheels are cp312. Spark is 3.11.
  Use letta-client on Spark. Run `letta server` on a matching VM.
- bundle_fastembed_onnx.tar.gz sha256 290f595b521588b0f7624b45d7962a071fb0f05fc30a746cdb051332e3ff6e8a
  fastembed 0.8.0 + onnxruntime 1.29.0 cp311 + numpy 2.4.6 cp311
  https://pypi.org/project/fastembed/0.8.0/
  https://pypi.org/project/onnxruntime/1.29.0/
- splits_letta_server folder `1ivcxKxP7-tIcuJ-IPi-TZcjUQ1U9IT6m` — 23 x 10MiB zip parts + SPLIT_MANIFEST.json
- splits_fastembed_onnx folder `1tQUt9RKNYLdMw9F_vZ7_TjtXI1V7e2rz` — 6 parts + manifest

## Embeddings / inference
True MRL-2048 needs an MRL-trained model or an API with dimension truncation (OpenAI text-embedding-3-large, Gemini embeddings).
Spark-safe now: fastembed ONNX (384/768 typical) OR API embeddings into Letta `embedding=` field.
Local MRL later: CPU torch on a VM + nomic-embed-text-v1.5 (or similar), store 2048 prefix. Do not drop CUDA 527MB torch into Spark.
Inference for Letta: Ollama / vLLM / llama.cpp / Gemini / OpenAI on the VM. Spark is not the inference box.

## Parked
torch CUDA 2.13 ~526.6 MB; librosa; faster-whisper; clang; rustc tarball; ffmpeg-static; NixOS/Proxmox images.

## Local staging
/home/workdir/artifacts/vesper_pkg_proxy_2026-08-26/
