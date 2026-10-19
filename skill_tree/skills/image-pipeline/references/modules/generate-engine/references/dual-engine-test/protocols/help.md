# Help — Imagine Engine Protocols
**Read this file** when the user asks for help, menu, or how the engine works.

## Router pattern
SKILL.md is only the router. Every trigger loads a protocol under `references/dual-engine-test/protocols/`.

| Trigger | Protocol file |
|---------|----------------|
| image in, no parameters | `prompt_default_six.md` (parameterized — see `scripts/default_six.py`) |
| `characters: [shauna]` / single entity six | `prompt_default_six.md` mode `single_entity` |
| `test` / `harness` / `dual engine test` | `prompt_harness.md` |
| **A** / formulation / DNA pair | `prompt_option_A.md` |
| **B** / CSP | `prompt_option_B.md` |
| **C** / heat gradient | `prompt_option_C.md` |
| **D** / angle expansion | `prompt_option_D.md` |
| **E** / minimal | `prompt_option_E.md` |
| **M2** / split face | `prompt_m2_split.md` |
| **M3** / full merge | `prompt_m3_merge.md` |
| scoring questions | `prompt_scoring.md` |
| display / double prompt issues | `prompt_display_rules.md` |

Always also respect `prompt_display_rules.md` and `prompt_scoring.md` when emitting images.
