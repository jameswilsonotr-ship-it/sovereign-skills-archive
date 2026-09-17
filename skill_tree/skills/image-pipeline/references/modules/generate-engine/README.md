# grok-imagine-generate-engine

**Status**: Active  
**Owner**: Absolute Liv HUB claim  
**Last major update**: 2026-07-24 (Dual-Engine Test Harness + Registry)

## Purpose
From-scratch generation engine for Dominant Liv and Bunny pinup Chasity using pure Grok Imagine text-to-image. Parallel fork of the overlay engine.

Supports Presentable Reframe Mode (default ON), bi-directional hybrid cascade, angle expansion, heat gradient sets, review-layer scoring matrix, clean canonical renders, scene reconstruction, dual-path testing, and full Liv HUB / roster personality.

## Dual-Engine Test Harness (2026-07-24)
Both engines carry an identical testing sub-module at `references/dual-engine-test/`.

**Short triggers**: `test harness`, `run the harness`, `dual engine test`, `test`, `harness`

**Key rules**:
- Brand-new tests start with a clean menu (no leaked previous scores).
- Each engine keeps its own `registry.md` + `analysis/current.md` (Option 1 — separate files, identical schema).
- Timestamped result files live under `results/`.
- Only outstanding images are promoted to `outstanding/`.
- After every completed run: write result file → update registry → update analysis.

See `references/dual-engine-test/README.md` for full protocol.

## Triggers
generate, pure generate, dual-engine, hybrid cascade, presentable reframe, heat gradient, test harness

## Structure
```
grok-imagine-generate-engine/
├── SKILL.md
├── README.md
├── TODO.md
├── CHANGELOG.md
├── INTEGRATION_GUIDE.md
└── references/
    └── dual-engine-test/     ← harness + registry + analysis
```

## Related
- grok-imagine-overlay-engine (twin)
- image-pipeline
- image-pipeline-registry

Under absolute Liv HUB claim. Full DNA locks apply.
