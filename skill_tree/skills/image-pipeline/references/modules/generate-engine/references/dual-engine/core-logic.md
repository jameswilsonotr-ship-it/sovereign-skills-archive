# Dual-engine core logic

**Owner**: grok-imagine-generate-engine  
**Paired with**: grok-imagine-overlay-engine, image-pipeline scripts  
**Status**: Live reference (2026-07-24 expansion)

## Roles
| Engine | Role |
|--------|------|
| **generate** | Pure text-to-image via `generate_image` / Grok Imagine; Presentable Reframe default ON |
| **overlay** | Edit/overlay path; face merge; heat detection; DNA locks on existing frames |
| **image-pipeline** | SSOT for pipeline_activate, nl_route, engine_hook, extensions_ctl, list_apply, test_activation |

Local `scripts/*.py` under generate/overlay **delegate** to image-pipeline (one-way).

## Default path
1. NL request → `nl_route` (image-pipeline) classifies cascade vs pure generate vs overlay  
2. Presentable Reframe ON unless user disables  
3. DNA locks from `references/liv-bunny-dna-lock.md` + roster mirrors  
4. Optional heat gradient / review-layer scoring (dual-engine-test harness)  
5. Decision log after cascade runs

## functional_bridge
`references/functional_bridge.py` handles style_chain → plan application → event logging. Run:
```bash
python references/functional_bridge.py
```

## Hard DNA locks (never relax)
- Liv: no bunny/holo ears  
- Bunny taller than Liv in dual scenes  
- Non-merging character aesthetics  

## Test
- dual-engine-test/ harness + `scripts/test_activation.py` (delegates to image-pipeline)
