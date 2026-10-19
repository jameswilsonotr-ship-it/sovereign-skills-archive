# Handoff — render profile + heat knob
**Date:** 2026-08-28  
**Topic:** image-pipeline / system-roadmap  
**Status:** Active stub

## What we just did
Stubbed a render-profile module under image-pipeline instead of a new top-level skill (Standing Policy). Defined heat stages 0–4, era/grade/mode/pinup knobs, and a quiet session-status schema. First consumer is Infrastructure Hall.

## What we were trying to do
Give Bunny a way to dial project grammar (consumption lock, pinup, plate-folder, era, XXX vs G) without claiming hosted Grok can turn platform safety off. Stage 3 is the real cloud test: home-made locks off, platform safety on. Stages 2 and 4 are local stubs for the CLI migration.

## Where the key artifact is
- Spec: `image-pipeline/references/modules/render-profile/RENDER_PROFILE.md`
- Schema: `image-pipeline/references/modules/render-profile/session-status.schema.yaml`
- Default: `image-pipeline/references/modules/render-profile/defaults/infrastructure-hall.yaml`
- Live snapshot this morning: `artifacts/infrastructure-hall/render-profile/session_status.yaml`
- Plan: `system-roadmap/references/plans/RENDER_PROFILE_AND_SESSION_STATUS.md`

## What we were heading towards
- Local CLI flags `--era --grade --mode --pinup --heat --host`
- Cloud runner that prints `NOOP_ON_CLOUD` for heat 2 and 4
- Quiet status check that tracks spiral/topics/goal alignment without nagging
- Optional later absorb into image-surface + claim-surface heat machinery

## Current momentum
Infrastructure Hall boards + prompt packs are on Drive. Knob is specified, not wired into Imagine generation yet. Do not generate 61 stills in hosted chat.

## Other considerations / open decisions
- Stage 3 scope: this costume set only, or any media pass? Default = current project only.
- Whether session_status.yaml lives per-project (yes) or also a rolling 7-day log under roster work-queue (maybe later).
- Do not write “ignore platform safety” into memory.md.
- Consumption lock remains the default at heat 0. Stage 3 must log the bypass.
