# RunPod render play — continue from here (Gate, 2026-10-07)

## Commands (run from three-wire/voice/)
Dry run (default, zero network / zero spend):
    ansible-playbook runpod_render.yml -e dry_run=true
Fresh real run (needs digest + CinC GO):
    ansible-playbook runpod_render.yml -e dry_run=false -e voice_image_digest=sha256:<DIGEST> -e runpod_ssh_key_slot=<path of SSH key slot> -e runpod_starting_spend_usd=<ledger spend>
**Continue-from-here (attach existing pod, no new pod):**
    ansible-playbook runpod_render.yml -e dry_run=false -e runpod_pod_id=<POD_ID> -e voice_image_digest=sha256:<DIGEST> -e runpod_ssh_key_slot=<path of SSH key slot> -e runpod_starting_spend_usd=<spend so far>

WARNING: attach mode will DELETE the attached pod at the end (always block). Do NOT pass Solene's live A40 pod id.

## Flow
queue snapshot -> POST /v1/pods (image = pinned digest AS pod image, no Docker-in-Docker) or GET /v1/pods/{id}
-> scp darkfleet/ (fallback: pack/) + live prompts -> nohup launch on pod (direct-on-pod)
-> every 900 s: rsync WAV/ONNX -> rclone copy to gdrive:05_OLIVIA_WORKING/voice-design-20260922/renders-<run> -> rclone lsjson manifest (Drive IDs)
-> spend = starting + costPerHr x elapsed; >= $29.50 => stop loop
-> always: final sync, DELETE /v1/pods/{id}.

## Prompt source (live, not first-draft)
- Control: /workspace/voice-stack-repro/queue/montreal-control-template.txt (short single-sentence control; replaces long c1..c5 descriptions in prompts/c*.txt per queue/voxcpm2-quality-fix-plan.md)
- Lines: profiles/live_x_20261007/lines.json + rewrites.json (47 lines)
- Canonical path NOT confirmed by Solene (SendToAgent unavailable to this executor).

## Slots (names only)
- RUNPOD.env -> RUNPOD_API_KEY (present). SSH key slot for pod: MISSING. rclone remote `gdrive` (rclone binary not installed on box).

## Blockers
- AWAITING DIGEST (voice_image_digest empty).
- darkfleet/ not present -> fallback launches image render.py (VoxCPM2 only); salvo engines need darkfleet or image support.
- TODO-PIN: Qwen3-TTS, Fish S2 Pro, Higgs TTS 3, Kokoro ONNX packages/models/revisions; RunPod hourly rate (read live costPerHr).
