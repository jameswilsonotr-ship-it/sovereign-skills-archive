# image-pipeline modules

Former top-level image engines live **only** under this folder. No top-level stubs.

**Render route (2026-08-28 lock):** from-scratch = `generate_image`. Overlay = `edit_image`. Display = `render_file` on a persisted path. SSOT: `shared/RENDER_ROUTE_LOCK.md`. Imagine component tags are demoted. Gamma is spare-door only.

| Module | Former top-level skill | Primary path |
|--------|------------------------|--------------|
| **generate-engine** | `grok-imagine-generate-engine` | `references/modules/generate-engine/` |
| **overlay-engine** | `grok-imagine-overlay-engine` | `references/modules/overlay-engine/` |

## Triggers

Routed via **skill-orchestrator** phrase map + this feeder + natural language:

| Phrases (examples) | Module |
|--------------------|--------|
| pure generate, generate engine, from-scratch | generate-engine |
| overlay engine, edit image engine, reference edit | overlay-engine |
| dual engine test, harness, test (with image) | active module’s `prompt_harness.md` |
| image + no parameters | active module’s `prompt_default_six.md` |

## Protocols (miner pattern)

Each module SKILL.md is a **router only**. Full steps live in:

```text
references/modules/<engine>/references/dual-engine-test/protocols/
```

| File | Role |
|------|------|
| `prompt_default_six.md` | No-param default: 6 outputs |
| `prompt_harness.md` | Test harness entry + menu loop |
| `prompt_option_A.md` … `E.md` | Menu options |
| `prompt_m2_split.md` / `prompt_m3_merge.md` | Merge modes |
| `prompt_display_rules.md` | One code block, short alt, bold titles |
| `prompt_scoring.md` | Mandatory scores |
| `help.md` | Map for humans |
| `ENGINE.md` | Generate vs overlay scope |

**Rule:** Do not implement menu letters from prose in SKILL.md alone — open the protocol file.

## Relation to packs / presets / Echo

1. Echo (or user) supplies DNA brief + optional style hint.
2. `scripts/engine_hook.py` / `pipeline_activate.py` may add pack/preset terms.
3. Module protocols own **default six, harness, scoring, display**.
4. DNA locks (ears, height, gem) remain non-negotiable above style packs.

## Integration docs

- `generate-engine/INTEGRATION_GUIDE.md` — style_chain / functional bridge
- Root **QUICKSTART.md** §9 — dual-engine quick path
- Root **SKILL.md** — Modules + dual-engine pointer section
